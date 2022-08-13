import asyncio
import argparse

from aiohttp import web

from app import routes


async def create_app():
    app = web.Application()

    routes.setup_routes(app)

    return app


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0')
    parser.add_argument('--port', type=str, default=8889)

    return parser.parse_args()


def main():
    args = parse_args()

    app = asyncio.get_event_loop().run_until_complete(create_app())

    web.run_app(app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
