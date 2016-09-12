import asyncio
import aiohttp

class HttpStress():
    
    POST = "POST"
    GET = "GET"

    def __init__(self, http_tests):
        self.http_tests = http_tests
        self.client = aiohttp.ClientSession()
    
    async def run_tests(self):
        for url, method, data_params, headers, test in self.http_tests:
            if method == HttpStress.GET:
                await self.do_get(url, data_params, headers, test)
            elif method == HttpStress.POST:
                await self.do_post(url, data_params, headers, test)

    async def do_post(self, url, post_data, headers, test_response):
        pass

    async def do_get(self, url, params, headers, test_response):
        async with self.client.get(url, params=params, headers=headers) as response:
            test_response(await response.json())

    def __del__(self):
        self.client.close()


def test_mr_status(response):
    print(response)

if __name__ == '__main__':

    stress = HttpStress(
        http_tests=[
            ('http://modelrunner.io/status', 
             'GET', 
             None, 
             {'Accept': 'application/json'},
             test_mr_status)])

    
    asyncio.get_event_loop().run_until_complete(stress.run_tests())
