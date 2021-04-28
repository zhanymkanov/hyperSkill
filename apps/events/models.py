from django.db import models
from django.utils import timezone

from apps.steps.models import Steps
from apps.users.models import User


class Events(models.Model):
    class Actions(models.IntegerChoices):
        SEE = 0
        SUBMIT = 1
        SOLVE = 2

    time = models.DateTimeField(default=timezone.now)
    action_id = models.IntegerField(choices=Actions.choices)
    target = models.ForeignKey(Steps, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
