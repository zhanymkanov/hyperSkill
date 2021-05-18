import datetime
import logging

import pytz
from clickhouse_driver.errors import ServerException
from config.celery import app as celery_app
from celery.utils.log import get_task_logger

from django.db.models import QuerySet

from apps.clickhouse import Clickhouse
from apps.events.models import Events


logger = get_task_logger(__name__)
logging.basicConfig(level=logging.DEBUG)

STEPIK_FOUNDED_DATETIME = datetime.datetime(2013, 9, 1, tzinfo=pytz.UTC)


@celery_app.task(
    autoretry_for=(ServerException,),
    max_retries=10,
    retry_backoff=True,
    retry_backoff_max=700,
    retry_jitter=False
)
def load_to_ch():
    """Load consolidated events data from postgres to clickhouse every 5 minutes."""

    clickhouse = Clickhouse()
    last_parsed: datetime.datetime = clickhouse.get_latest_event_time()[0][0]
    last_parsed: str = last_parsed.strftime("%Y-%m-%d %H:%M:%S.%f")

    logger.info(f"Started data collection starting from {last_parsed}")

    events: QuerySet = Events.objects.select_related("user")  # join tables
    insert_values = events.filter(time__gt=last_parsed).values_list(  # as tuples
        "time",
        "user_id",
        "user__join_date",
        "user__registration_date",
        "user__name",
        "user__email",
        "user__is_guest",
        "target_id",
        "action_id",
    ).iterator(chunk_size=100_000)
    clickhouse.insert_data(val for val in insert_values)

    logger.info(f"Successfully loaded data to CH")
