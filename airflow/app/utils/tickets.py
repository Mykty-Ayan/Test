import asyncio
import typing as tp

from app import dto
from app.utils import provider
from app.context import AppContext


async def get_tickets(context: AppContext) -> tp.Optional[tp.List[dto.Ticket]]:
    provider_urls = [context.secrets.get('provider_a'), context.secrets.get('provider_b')]
    futures = [
        provider.ProviderClient.get_tickets(url)
        for url in provider_urls
    ]

    result = await asyncio.gather(*futures)

    return result


