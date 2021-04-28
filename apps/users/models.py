from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    date_joined = None

    name = models.TextField()
    email = models.EmailField(unique=True)
    is_guest = models.BooleanField(default=True)
    join_date = models.DateTimeField(default=timezone.now)
    registration_date = models.DateTimeField(null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
