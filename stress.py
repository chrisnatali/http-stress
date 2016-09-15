import asyncio
import requests
import functools
import copy
import argparse
import json

class HttpStress():
    
    def __init__(self, http_tests, event_loop):
        self.http_tests = http_tests
        self.event_loop = event_loop
    
    def async_tests(self):
        """
        returns a list of coroutines to be run async by event loop
        """
        coroutines = []
        for timestep, url, method, data in self.http_tests:
            coroutine = self.make_request(timestep, url, method, data)
            coroutines.append(coroutine)

        return coroutines

    async def make_request(self, timestep, url, method, data):
        await asyncio.sleep(timestep)
        arg_dict = copy.deepcopy(data)
        # read data from any files 
        if 'files' in arg_dict:
            file_dict = dict()
            for attr_name, file_name in arg_dict['files'].items():
                with open(file_name, 'rb') as fh:
                    file_dict[attr_name] = (file_name, fh.read())

            arg_dict['files'] = file_dict
        partial = functools.partial(requests.request, method, url, **arg_dict)
        response = await self.event_loop.run_in_executor(None, partial)
        print(','.join([str(timestep), url, method, response.text]))

def convert_record(tup):
    try:
        result = (int(tup[0]), str(tup[1]), str(tup[2]), json.loads(tup[3]))
    except Exception as e:
        raise Exception("Bad test tuple: {}, error {}".format(tup, e))
    return result
       
if __name__ == '__main__':

    # read tests from file 
    http_tests = []
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--tests_file",
        help="csv file of timestep,url,method,config_json for each request")
     
    args = parser.parse_args()
    for line in open(args.tests_file, 'r'):
        raw_record = tuple([field.strip() for field in line.split(',', 3)])
        test_record = convert_record(raw_record)
        http_tests.append(test_record)

    loop = asyncio.get_event_loop()
    stress = HttpStress(http_tests=http_tests, event_loop=loop)
    asyncio.get_event_loop().run_until_complete(asyncio.wait(stress.async_tests()))
