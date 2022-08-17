import asyncio
import threading

import uuid

from aiohttp import web

from app import context
from app.utils import tasks


async def handle(request: web.Request, ctx: context.AppContext) -> web.Response:
    search_id = tasks.generate_search_id(ctx)
    return web.json_response({'search_id': search_id})
