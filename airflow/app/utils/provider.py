import abc

import aiohttp


class BaseProviderClient(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    async def get_tickets(base_url: str):
        raise NotImplementedError


class ProviderClient(BaseProviderClient):

    @staticmethod
    async def get_tickets(base_url: str):
        async with aiohttp.ClientSession(base_url) as session:
            async with session.post(
                    '/v1/search/'
            ) as response:
                if response.status != 200:
                    return None

                data = await response.json()
                print(data)
                return data
