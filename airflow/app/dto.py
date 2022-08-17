import dataclasses
import datetime
import typing as tp


@dataclasses.dataclass
class Departure:
    at: datetime.datetime
    airport: str


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


@dataclasses.dataclass
class Flight:
    duration: int
    segments: tp.List[Segment] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Pricing:
    total: float
    base: float
    taxes: float
    currency: str


@dataclasses.dataclass
class Ticket:
    refundable: bool
    validating_airline: str
    pricing: Pricing
    flights: tp.List[Flight] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Currency:
    fullname: str
    title: str
    description: float
    quantity: int
    to_date: datetime.datetime

    @classmethod
    def from_xml(cls, fullname: str, title: str, description: float, quantity: int, to_date: datetime.datetime):
        return cls(fullname=fullname, title=title, description=description, quantity=quantity, to_date=to_date)
