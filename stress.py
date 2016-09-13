import asyncio
import aiohttp
import time

class HttpStress():
    
    POST = "POST"
    GET = "GET"

    def __init__(self, http_tests):
        self.http_tests = http_tests
        self.client = aiohttp.ClientSession()
    
    def async_tests(self):
        """
        returns a list of futures to be run async by event loop
        """
        futures = []
        for timestep, url, method, kwargs in self.http_tests:
            futures.append(self.make_request(timestep, url, method, kwargs))

        return futures

    async def make_request(self, timestep, url, method, kwargs):
        print("timestep {} method {} url {}".format(timestep, method, url))
        await asyncio.sleep(timestep)
        async with self.client.request(method, url, **kwargs) as response:
            print(await response.text())
       
    def __del__(self):
        self.client.close()

if __name__ == '__main__':

    stress = HttpStress(
        http_tests=[
            (3, 'http://modelrunner.io/jobs', 'GET', {'headers': {'Accept': 'application/json'}}),
            (0, 'http://modelrunner.io/status', 'GET', {'headers': {'Accept': 'application/json'}}),
            ])
    
    asyncio.get_event_loop().run_until_complete(asyncio.wait(stress.async_tests()))
