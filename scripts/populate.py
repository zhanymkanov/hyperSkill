import os  # noqa

import django  # noqa

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # noqa
django.setup()  # noqa

import random
import logging
from time import sleep
from typing import List

from django.utils import timezone

from apps.events.models import Events
from apps.steps.models import Steps
from apps.users.models import User

from . import utils

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def populate_steps(num_steps: int = 10000) -> List[Steps]:
    return Steps.objects.bulk_create(Steps() for _ in range(num_steps))


def populate_users(num_users: int = 10000) -> List[User]:
    bulk_users = []
    for _ in range(num_users):
        user = _create_random_user()

        bulk_users.append(user)

    return User.objects.bulk_create(bulk_users)


def populate_events(
    *, users: List[User] = None, steps: List[Steps] = None, now: bool = False
):
    users = users or User.objects.all()
    steps = steps or Steps.objects.all()

    num_see = min(User.objects.count(), 10_000)
    num_submit = num_see // 2
    num_solve = num_submit // 2

    see_events = _create_events_list(steps, users, action=Events.Actions.SEE, now=now)
    submit_events = _create_events_list(
        steps, users[:num_submit], action=Events.Actions.SUBMIT, now=now
    )
    solve_events = _create_events_list(
        steps, users[:num_solve], action=Events.Actions.SOLVE, now=now
    )

    Events.objects.bulk_create(
        see_events + submit_events + solve_events
    )


def _create_random_user():
    random_name = utils.random_text()

    user = User(
        name=random_name,
        email=f"{random_name}@mail.com",
        join_date=utils.random_date(),
    )

    if utils.random_registered():
        user.registration_date = utils.random_registration_date(user.join_date)
        user.is_guest = False

    return user


def _create_events_list(steps, users, *, action, now):
    return [
        Events(
            user=user,
            time=timezone.now() if now else utils.random_datetime(),
            action_id=action,
            target=random.choice(steps)
        ) for user in users
    ]


if __name__ == '__main__':
    logger.info("Started the population script")
    steps = populate_steps()
    logger.info("Populated steps data")
    users = populate_users()
    logger.info("Populated users data")
    populate_events(users=users, steps=steps)
    logger.info("Populated events data")

    while 1:
        logger.info("Started the population script")
        steps = populate_steps()
        logger.info("Populated steps data")
        users = populate_users()
        logger.info("Populated users data")
        populate_events(users=users, steps=steps, now=True)
        logger.info("Populated events data")
        sleep(2)
