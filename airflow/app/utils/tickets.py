import asyncio
import threading
import typing as tp

from app import dto
from app.utils import provider
from app.context import AppContext


async def get_tickets(context: AppContext) -> tp.Optional[tp.List[dto.Ticket]]:
    provider_urls = [context.secrets.get('provider_a'), context.secrets.get('provider_b')]
    result = list()
    for url in provider_urls:
        response = await provider.ProviderClient.get_tickets(url)
        if response is None:
            continue
        result.extend(response)
    return result
