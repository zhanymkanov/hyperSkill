import datetime
import logging

import pytz
from config.celery import app as celery_app

from django.db.models import QuerySet

from apps.clickhouse import Clickhouse
from apps.events.models import Events


logger = logging.getLogger("ch_worker")
logging.basicConfig(level=logging.DEBUG)

STEPIK_FOUNDED_DATETIME = datetime.datetime(2013, 9, 1, tzinfo=pytz.UTC)


@celery_app.task
def ch_every_min():
    last_parsed = STEPIK_FOUNDED_DATETIME
    logger.info(f"Started data collection starting from {last_parsed}")

    events: QuerySet = Events.objects.select_related("user")
    insert_values = events.filter(time__gt=last_parsed).values_list(
        "time",
        "user_id",
        "user__join_date",
        "user__registration_date",
        "user__name",
        "user__email",
        "user__is_guest",
        "target_id",
        "action_id",
    )
    logger.info(f"Values to insert: {insert_values.count()}")

    clickhouse = Clickhouse()
    clickhouse.insert_data(val for val in insert_values)
    logger.info(f"Successfully loaded data to CH")

