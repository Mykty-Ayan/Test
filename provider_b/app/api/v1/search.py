import asyncio

from aiohttp import web

from app.utils import parsers


async def handle(request: web.Request) -> web.Response:
    data = parsers.JsonParser.parse('response_b.json')
    await asyncio.sleep(60)
    return web.json_response(data)
