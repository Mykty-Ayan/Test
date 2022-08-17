import asyncio
import uuid
import threading

from app import context
from app import storage
from app import dto
from app.utils import tickets


async def generate_search_id(ctx: context.AppContext) -> str:
    search_id = str(uuid.uuid4())
    database = storage.MongoStorage(ctx)
    database.create_task_with_search_id(search_id=search_id)
    threading.Thread(target=run_background,
                     name="fetch_tickets",
                     args=(database, search_id,),
                     daemon=True).start()
    return search_id


def run_background(database: storage.MongoStorage, ctx: context.AppContext, search_id: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tickets_list = loop.run_until_complete(tickets.get_tickets(ctx))
    database.update_task_with_search_id(
        search_id,
        tickets=tickets_list
    )
