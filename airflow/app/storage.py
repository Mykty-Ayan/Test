import abc
import typing as tp

from app import dto
from app import context


class Storage(abc.ABC):

    @abc.abstractmethod
    def get_by_search_id(self, search_id: str) -> dto.SearchResult:
        raise NotImplementedError

    @abc.abstractmethod
    def create_task_with_search_id(self, search_id: str):
        raise NotImplementedError

    @abc.abstractmethod
    def update_task_with_search_id(self, search_id: str, tickets: dto.Ticket, status: str = 'COMPLETED'):
        raise NotImplementedError

    @abc.abstractmethod
    def insert_currencies(self, currencies: tp.List[dto.Currency]):
        raise NotImplementedError

    @abc.abstractmethod
    def get_currency(self, currency_title: str) -> dto.Currency:
        raise NotImplementedError


class MongoStorage(Storage):

    def __init__(self, ctx: context.AppContext):
        self.context = ctx

    def get_by_search_id(self, search_id: str) -> tp.Optional[dto.SearchResult]:
        result = self.context.db.tickets.find_one({'search_id': search_id}, {'_id': 0})
        if not result:
            return None

        return dto.SearchResult.from_dict(
            search_id=result['search_id'],
            status=result['status'],
            items=[dto.Ticket.from_dict(
                refundable=item['refundable'],
                validating_airline=item['validating_airline'],
                pricing=dto.Pricing.from_dict(
                    total=float(item['pricing']['total']),
                    base=float(item['pricing']['base']),
                    taxes=float(item['pricing']['taxes']),
                    currency=item['pricing']['currency'],
                ),
                flights=[dto.Flight(
                    duration=flight['duration'],
                    segments=[dto.Segment.from_dict(
                        operating_airline=flight['segments'][0]['operating_airline'],
                        marketing_airline=flight['segments'][0]['marketing_airline'],
                        flight_number=flight['segments'][0]['flight_number'],
                        equipment=flight['segments'][0]['equipment'],
                        departure=dto.Departure.from_dict(
                            at=flight['segments'][0]['dep']['at'],
                            airport=flight['segments'][0]['dep']['airport']
                        ),
                        arrival=dto.Arrival.from_dict(
                            at=flight['segments'][0]['arr']['at'],
                            airport=flight['segments'][0]['arr']['airport']
                        ),
                        baggage=flight['segments'][0]['baggage']
                    )]
                ) for flight in item['flights']]
            ) for item in result['items']]
        )

    def create_task_with_search_id(self, search_id: str):
        self.context.db.tickets.insert_one({
            'search_id': search_id,
            'status': 'PENDING'

        })

    def update_task_with_search_id(self, search_id, tickets: tp.List[dto.Ticket], status: str = 'COMPLETED'):
        self.context.db.tickets.update_one(
            {
                'search_id': search_id
            },
            {'$set': {
                'items': [ticket.asdict() for ticket in tickets],
                'status': 'COMPLETED'
            }})

    def insert_currencies(self, currencies: tp.List[dto.Currency]):
        self.context.db.currencies.insert_many(
            [currency.asdict() for currency in currencies]
        )

    def get_currency(self, currency_title: str) -> tp.Optional[dto.Currency]:
        return self.context.db.currencies.find_one({
            'title': currency_title
        })
