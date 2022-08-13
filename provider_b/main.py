import asyncio
import argparse

from aiohttp import web

from app import routes
from app.context import AppContext


async def create_app(args):
    app = web.Application()

    ctx = AppContext(secrets_dir=args.secrets_dir)

    app.on_startup.append(ctx.on_startup)
    app.on_shutdown.append(ctx.on_shutdown)

    routes.setup_routes(app, ctx)

    return app


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0')
    parser.add_argument('--port', type=str, default=8888)
    parser.add_argument('--secrets-dir', type=str, required=True)

    return parser.parse_args()


def main():
    args = parse_args()

    app = asyncio.get_event_loop().run_until_complete(create_app(args))

    web.run_app(app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
