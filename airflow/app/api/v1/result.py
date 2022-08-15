from aiohttp import web

from app import context


async def handle(request: web.Request, ctx: context.AppContext) -> web.Response:
    search_id = request.match_info.get('search_id')
    currency = request.match_info.get('currency')
    
    return web.json_response({'hello': 'world'})
