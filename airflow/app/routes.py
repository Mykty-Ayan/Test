import typing as tp

from aiohttp import web

from provider_a.app.context import AppContext


def wrap_handler(handler, context: AppContext) -> tp.Callable:
    async def wrapper(request):
        return await handler(request, context)

    return wrapper


def setup_routes(app: web.Application, ctx: AppContext) -> None:
    app.router.add_post(
        '/v1/search',
        wrap_handler(
                # TODO
            ctx,
        ),
    )
    app.router.add_get(
        '/v1/result/{search_id}/{currency}',
        wrap_handler(
            # TODO
            ctx
        )
    )
