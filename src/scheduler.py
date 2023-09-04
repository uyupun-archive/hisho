from typing import Callable, Any

from apscheduler.job import Job
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.base import BaseTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.base import JobLookupError

from . import remind


class Scheduler:
    def __init__(self, url="sqlite:///database.sqlite") -> None:
        jobstores = {
            "default": SQLAlchemyJobStore(url=url)
        }
        self._scheduler = BackgroundScheduler(jobstores=jobstores)
        self._set_default_jobs()
        self._scheduler.start()

    def _set_default_jobs(self) -> None:
        self._scheduler.add_job(
            remind.remind_mtg_candidate_date,
            trigger=CronTrigger(day="15", hour="9", minute="0"),
            id="mtg_candidate_reminder",
            replace_existing=True,
        )

    def get_jobs(self) -> list[Job]:
        return self._scheduler.get_jobs()

    def remove_job(self, id: str) -> bool:
        try:
            self._scheduler.remove_job(id)
            return True
        except JobLookupError:
            return False

    def add_job(self, func: Callable[..., Any], trigger: BaseTrigger, id: str, replace_existing: bool=False):
        self._scheduler.add_job(func, trigger=trigger, id=id, replace_existing=replace_existing)
