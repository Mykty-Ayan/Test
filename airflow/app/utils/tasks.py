import asyncio
import uuid
import threading

from app import context
from app.utils import tickets


async def generate_search(ctx: context.AppContext) -> str:
    search_id = str(uuid.uuid4())
    context.db.tickets.insert_one({
        'search_id': search_id,
        'status': 'PENDING',
    })
    threading.Thread(target=run_background, name="fetch_tickets", args=(ctx, search_id,), daemon=True).start()
    return search_id


def run_background(ctx: context.AppContext, search_id: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tickets_list = loop.run_until_complete(tickets.get_tickets(ctx))
    ctx.db.tickets.update_one(
        {
            'search_id': search_id
        },
        {'$set': {
            'items': tickets_list,
            'status': 'COMPLETED'
        }})