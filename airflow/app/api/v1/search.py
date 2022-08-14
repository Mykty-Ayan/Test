import asyncio

import uuid

from aiohttp import web

from app import context
from app.utils import tickets


async def handle(request: web.Request, ctx: context.AppContext) -> web.Response:
    search_id = str(uuid.uuid4())

    all_tickets = await tickets.get_tickets(ctx)


    return web.json_response({'search_id': search_id})
