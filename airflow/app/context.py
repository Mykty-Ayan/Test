import datetime
import typing as tp

import pymongo

from apscheduler.schedulers import asyncio as async_scheduler
from apscheduler import job
from apscheduler.triggers import cron

from pymongo import database

from app.utils import secrets
from app.utils import providers


class AppContext:
    def __init__(self, *, secrets_dir: str):
        self.secrets: secrets.SecretsReader = secrets.SecretsReader(secrets_dir)
        self.client: pymongo.MongoClient = pymongo.MongoClient(self.secrets.get('mongodb'))
        self.db: tp.Optional[database.Database] = None
        self.scheduler: async_scheduler.AsyncIOScheduler = self.create_scheduler()

    async def on_startup(self, app=None):
        self.add_currency_jobs()
        self.scheduler.start()
        self.db = self.client.get_database('aviata')

    async def on_shutdown(self, app=None):
        self.client.close()
        self.scheduler.shutdown()

    @staticmethod
    def create_scheduler() -> async_scheduler.AsyncIOScheduler:
        return async_scheduler.AsyncIOScheduler({
            'apscheduler.jobstores.mongo': {
                'type': 'mongodb'
            },
            'apscheduler.timezone': 'Asia/Almaty'
        })

    def add_currency_jobs(self):
        currency_job: tp.Optional[job.Job] = self.scheduler.get_job('currency', jobstore='mongodb')
        if currency_job is not None:
            return

        today = datetime.datetime.today()
        currency_trigger = cron.CronTrigger(
            year='*',
            month='*',
            day_of_week='*',
            day='*',
            hour=12,
            minute=0,
            second='*'
        )
        self.scheduler.add_job(
            providers.CurrencyProvider.get_currencies,
            args=(
                self.secrets.get('national_bank'),
                today,
            ),
            id='currency',
            name='currency',    
            trigger=currency_trigger,
            jobstore='mongodb',
            next_run_time=today + datetime.timedelta(seconds=10)
        )
