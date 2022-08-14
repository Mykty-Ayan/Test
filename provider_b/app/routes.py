from aiohttp import web

from app.api.v1 import search


def setup_routes(app: web.Application) -> None:
    app.router.add_post(
        '/v1/search/',
        search.handle,
    )
