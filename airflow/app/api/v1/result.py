from aiohttp import web

from app import context


async def handle(request: web.Request, ctx: context.AppContext) -> web.Response:
    return web.json_response({'hello': 'world'})
