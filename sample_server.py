"""
Sample Server used to test http_stress against

Modify endpoints and handlers as needed

Example:
    $ python -m aiohttp.web -H localhost -P 9000 server:init

See [aiohttp docs](http://aiohttp.readthedocs.io/en/stable/web.html)
"""

from aiohttp import web
import json

async def handle(request):
    print(request.headers)
    print(await request.content.read())
    print(request.content_type)
    return web.Response(
        body=json.dumps({'result': 'OK'}).encode('utf-8'),
        content_type='application/json')

def init(argv):
    app = web.Application()
    app.router.add_route('GET', '/jobs', handle)
    app.router.add_route('GET', '/status', handle)
    app.router.add_route('POST', '/jobs', handle)
    return appfrom aiohttp import web
