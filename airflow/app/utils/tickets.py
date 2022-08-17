import typing as tp

from app import dto
from app.utils import providers
from app.context import AppContext


async def get_tickets(context: AppContext) -> tp.Optional[tp.List[dto.Ticket]]:
    provider_urls = [context.secrets.get('provider_a'), context.secrets.get('provider_b')]
    result = list()
    for url in provider_urls:
        response = await providers.ProviderClient.get_tickets(url)
        if response is None:
            continue
        result.extend(response)
        
    if not result:
        return None
        
    for i in range(len(result)):
        result[i] = dto.Ticket.from_dict(
                refundable=result[i]['refundable'],
                validating_airline=result[i]['validating_airline'],
                pricing=dto.Pricing.from_dict(
                    total=float(result[i]['pricing']['total']),
                    base=float(result[i]['pricing']['base']),
                    taxes=float(result[i]['pricing']['taxes']),
                    currency=result[i]['pricing']['currency'],
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
                ) for flight in result[i]['flights']],
            )
    return result
