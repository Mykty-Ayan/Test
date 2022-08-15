import asyncio
import typing as tp

import pymongo

from apscheduler.schedulers import asyncio as async_scheduler
from apscheduler.jobstores import mongodb

from pymongo import database

from app.utils import secrets


class AppContext:
    def __init__(self, *, secrets_dir: str):
        self.secrets: secrets.SecretsReader = secrets.SecretsReader(secrets_dir)
        self.client: pymongo.MongoClient = pymongo.MongoClient(self.secrets.get('mongodb'))
        self.db: tp.Optional[database.Database] = None

    async def on_startup(self, app=None):

        self.db = self.client.get_database('aviata')

    async def on_shutdown(self, app=None):
        self.client.close()
