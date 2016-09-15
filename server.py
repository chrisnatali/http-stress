from aiohttp import web
import json

async def handle(request):
    print(request.headers)
    print(await request.content.read())
    print(request.content_type)
    return web.Response(
        body=json.dumps({'result': 'OK'}).encode('utf-8'),
        content_type='application/json')

def init_function(argv):
    app = web.Application()
    app.router.add_route('GET', '/jobs', handle)
    app.router.add_route('GET', '/status', handle)
    app.router.add_route('POST', '/jobs', handle)
    return app
