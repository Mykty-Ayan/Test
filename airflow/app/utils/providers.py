import abc
import datetime

import typing as tp

import aiohttp

from lxml import etree

from airflow.app import dto


class BaseProviderClient(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    async def get_tickets(base_url: str):
        raise NotImplementedError


class ProviderClient(BaseProviderClient):

    @staticmethod
    async def get_tickets(base_url: str):
        async with aiohttp.ClientSession(base_url, trust_env=True) as session:
            async with session.post(
                    '/v1/search/'
            ) as response:
                if response.status != 200:
                    return None

                data = await response.json()

                return data


class CurrencyProvider:
    @staticmethod
    async def _get_currencies(base_url: str, to_date: datetime.datetime) -> tp.Optional[bytes]:
        async with aiohttp.ClientSession(base_url) as session:
            async with session.get(
                    f'/rss/get_rates.cfm?fdate={to_date.strftime("%d.%m.%Y")}'
            ) as response:
                if response.status != 200:
                    return None

                data = await response.read()
                return data

    async def get_currencies(self, base_url: str, to_date: datetime.datetime) -> tp.Optional[list[dto.Currency]]:
        response = await self._get_currencies(base_url, to_date)
        if response is None:
            return None
        tree = etree.fromstring(response)
        currency_list = list()
        for item in tree.xpath('//item'):
            currency: dto.Currency = dto.Currency.from_xml(
                fullname=item.xpath('fullname/text()')[0],
                title=item.xpath('title/text()')[0],
                description=float(item.xpath('description/text()')[0]),
                quantity=int(item.xpath('quant/text()')[0]),
                to_date=datetime.datetime.strptime(tree.xpath('date/text()')[0], '%d.%m.%Y')
            )
            currency_list.append(currency)
        return currency_list
