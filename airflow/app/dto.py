from __future__ import annotations

import dataclasses
import datetime
import typing as tp


@dataclasses.dataclass
class Departure:
    at: datetime.datetime
    airport: str

    @classmethod
    def from_dict(cls, at: datetime.datetime, airport: str) -> Departure:
        return cls(at=at, airport=airport)


@dataclasses.dataclass
class Arrival(Departure):
    pass


@dataclasses.dataclass
class Segment:
    operating_airline: str
    marketing_airline: str
    flight_number: str
    equipment: tp.Optional[str]
    departure: Departure
    arrival: Arrival
    baggage: str

    @classmethod
    def from_dict(cls, operating_airline: str,
                  marketing_airline: str,
                  flight_number: str,
                  departure: Departure,
                  arrival: Arrival,
                  baggage: str,
                  equipment=None) -> Segment:
        return cls(operating_airline=operating_airline,
                   marketing_airline=marketing_airline,
                   flight_number=flight_number,
                   departure=departure,
                   arrival=arrival,
                   baggage=baggage,
                   equipment=equipment)


@dataclasses.dataclass
class Flight:
    duration: int
    segments: tp.List[Segment] = dataclasses.field(default_factory=list)

    @classmethod
    def from_dict(cls, duration: int, segments: tp.List[Segment]) -> Flight:
        return cls(duration=duration, segments=segments)


@dataclasses.dataclass
class Pricing:
    total: float
    base: float
    taxes: float
    currency: str

    @classmethod
    def from_dict(cls, total: float, base: float, taxes: float, currency: str) -> Pricing:
        return cls(total=total, base=base, taxes=taxes, currency=currency)


@dataclasses.dataclass
class Ticket:
    refundable: bool
    validating_airline: str
    pricing: Pricing
    flights: tp.List[Flight] = dataclasses.field(default_factory=list)

    @classmethod
    def from_dict(cls, refundable: bool,
                  validating_airline: str,
                  pricing: Pricing,
                  flights: tp.List[Flight]) -> Ticket:
        return cls(refundable=refundable,
                   validating_airline=validating_airline,
                   pricing=pricing,
                   flights=flights)


@dataclasses.dataclass
class Currency:
    fullname: str
    title: str
    description: float
    quantity: int
    to_date: datetime.datetime

    @classmethod
    def from_xml(cls,
                 fullname: str,
                 title: str,
                 description: float,
                 quantity: int,
                 to_date: datetime.datetime) -> Currency:
        return cls(fullname=fullname,
                   title=title,
                   description=description,
                   quantity=quantity,
                   to_date=to_date)


@dataclasses.dataclass
class SearchResult:
    search_id: str
    status: str
    items: tp.List[Ticket] = dataclasses.field(default_factory=list)

    @classmethod
    def from_dict(cls, search_id: str, status: str, items: tp.List[Ticket]) -> SearchResult:
        return cls(search_id=search_id,
                   status=status,
                   items=items)
