import datetime
import random
import string

import pytz


IS_REGISTERED_CHANCE = 0.4
STEPIK_FOUNDED_DATE = datetime.date(2013, 9, 1)
STEPIK_FOUNDED_DATETIME = datetime.datetime(2013, 9, 1, tzinfo=pytz.UTC)
MAX_RANDOM_REG_DAYS = 365 * 7


def random_text(length: int = 16) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


def random_registered():
    return random.random() <= IS_REGISTERED_CHANCE  # if less, than user is registered


def random_date():
    random_days = random.randint(1, MAX_RANDOM_REG_DAYS)
    return STEPIK_FOUNDED_DATE + datetime.timedelta(days=random_days)


def random_datetime():
    random_days = random.randint(1, MAX_RANDOM_REG_DAYS)
    return STEPIK_FOUNDED_DATETIME + datetime.timedelta(days=random_days)


def random_registration_date(join_date: datetime.date):
    random_days = random.randint(1, 90)
    return join_date + datetime.timedelta(days=random_days)
