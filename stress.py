import asyncio
import requests
import functools
import copy

class HttpStress():
    
    def __init__(self, http_tests, event_loop):
        self.http_tests = http_tests
        self.event_loop = event_loop
    
    def async_tests(self):
        """
        returns a list of futures to be run async by event loop
        """
        futures = []
        for timestep, url, method, data in self.http_tests:
            coroutine = self.make_request(timestep, url, method, data)
            futures.append(coroutine)

        return futures

    async def make_request(self, timestep, url, method, data):
        print("timestep {} method {} url {}".format(timestep, method, url))
        await asyncio.sleep(timestep)
        arg_dict = copy.deepcopy(data)
        # read data from any files 
        if 'files' in arg_dict:
            file_dict = {attr_name: open(file_name, 'rb').read() for 
                         attr_name, file_name in arg_dict['files'].items()}
            arg_dict['files'] = file_dict
        partial = functools.partial(requests.request, method, url, **arg_dict)
        response = await self.event_loop.run_in_executor(None, partial)
        print(timestep, url, method, response)
       
if __name__ == '__main__':

    loop = asyncio.get_event_loop()

    stress = HttpStress(
        http_tests=[
            (3, 'http://localhost:9000/jobs', 'GET', {'headers': {'Accept': 'application/json'}}),
            (0, 'http://localhost:9000/status', 'GET', {'headers': {'Accept': 'application/json'}}),
            (1, 'http://localhost:9000/jobs', 'POST', {'files': {'zip_file': 'sleep_count_8.zip'}, 'data': {'model': 'test', 'job_name': 'sleep_8_1'}, 'headers': {'Accept': 'application/json'}}),
            ],
        event_loop=loop)
    
    asyncio.get_event_loop().run_until_complete(asyncio.wait(stress.async_tests()))
