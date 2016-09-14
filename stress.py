import asyncio
import aiohttp


async def fetch(session, wait, url, method, kwargs):
    print("timestep {} method {} url {}".format(wait, method, url))
    await asyncio.sleep(wait)
    async with session.get(url) as response:
        print(await response.text())


async def main(loop, tasks):
    async with aiohttp.ClientSession(loop=loop) as session:
        await asyncio.gather(*[fetch(session, *task) for task in tasks])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [
        (3, 'http://modelrunner.io/jobs', 'GET', {'headers': {'Accept': 'application/json'}}),
        (0, 'http://modelrunner.io/status', 'GET', {'headers': {'Accept': 'application/json'}}),
    ]
    loop.run_until_complete(main(loop, tasks))
