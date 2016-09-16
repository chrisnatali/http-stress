# -*- coding: utf-8 -*-
import asyncio
import requests
import functools
import copy
import argparse
import json

class HttpStress():
    """ 
    Encapsulate an HttpStress simulation

    Allows for multiple simultaneous requests

    Attributes:
        http_requests:  http request tuples of form
            timestep, url, method, config

        event_loop: an asyncio event loop

    Examples:
        The following demonstrates how to use HttpStress

        >>> requests = [
            (1, 'http://test.io/endpoint1', 'GET', {}),
            (3, 'http://test.io/endpoint2', 'POST', {"files": {"file": "file.txt"}}),
            (1, 'http://test.io/endpoint3', 'GET', {"headers": {"Accept": "application/json"}})
            ]

        >>> loop = asyncio.get_event_loop()
        >>> stress = HttpStress(http_requests=requests, event_loop=loop)
        >>> asyncio.get_event_loop().run_until_complete(asyncio.wait(stress.tests_as_coroutines()))
        1,http://test.io/endpoint1,'GET',<html_response>
        1,http://test.io/endpoint3,'GET',{"json": "GET response"}
        3,http://test.io/endpoint2,'POST',POST response

    """
    
    def __init__(self, http_requests, event_loop):
        self.http_requests = http_requests
        self.event_loop = event_loop
    
    def requests_as_coroutines(self):
        """
        returns the requests as a list of coroutines to be run via
        asyncio event loop
        """
        coroutines = []
        for timestep, url, method, data in self.http_requests:
            coroutine = self.make_request(timestep, url, method, data)
            coroutines.append(coroutine)

        return coroutines

    async def make_request(self, timestep, url, method, data):
        """
        coroutine that will make a request at the specified timestep and
        print the response
        """
        await asyncio.sleep(timestep)
        arg_dict = copy.deepcopy(data)
        # put data from any files into the arg_dict
        if 'files' in arg_dict:
            file_dict = dict()
            for attr_name, file_name in arg_dict['files'].items():
                with open(file_name, 'rb') as fh:
                    file_dict[attr_name] = (file_name, fh.read())

            arg_dict['files'] = file_dict
        partial = functools.partial(requests.request, method, url, **arg_dict)
        response = await self.event_loop.run_in_executor(None, partial)
        print(','.join([str(timestep), url, method, response.text]))
    
    @staticmethod
    def convert_record(tup):
        """
        converts a requests tuple to form we expect and returns it OR
        raises Exception
        """
        try:
            result = (int(tup[0]), str(tup[1]), str(tup[2]), json.loads(tup[3]))
        except Exception as e:
            raise Exception("Bad test tuple: {}, error {}".format(tup, e))
        return result
           
if __name__ == '__main__':

    # read tests from file 
    http_requests = []
    parser = argparse.ArgumentParser(
        description=
    '''
    Simulate running a set of http requests as a way to 
    stress test http service(s)

    A stress simulation is defined by a csv of request records

    A request record is defined as <timestep>,<url>,<method>,<configuration> 

    <timestep>:  seconds from start of simulation
    <url>:  url to send request
    <method>:  http method for request
    <configuration>:  json configuration defining request parameters and headers
    
    Example input csv:

    3,http://localhost:8080/jobs,GET,{"headers": {"Accept": "application/json"}}
    0,http://localhost:8080/status,GET,{"headers": {"Accept": "application/json"}}
    1,http://localhost:8080/jobs,POST,{"files": {"zip_file": "sleep_count_8.zip"}, "data": {"model": "test", "job_name": "sleep_8_1"}, "headers": {"Accept": "application/json"}}

    ''',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "requests_file",
        help="csv file of timestep,url,method,config_json for each request")
     
    args = parser.parse_args()
    for line in open(args.requests_file, 'r'):
        raw_record = tuple([field.strip() for field in line.split(',', 3)])
        request_record = HttpStress.convert_record(raw_record)
        http_requests.append(request_record)

    loop = asyncio.get_event_loop()
    stress = HttpStress(http_requests=http_requests, event_loop=loop)
    asyncio.get_event_loop().run_until_complete(asyncio.wait(stress.requests_as_coroutines()))
