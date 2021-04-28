from django.db import models
from django.utils import timezone

from apps.steps.models import Steps


class Events(models.Model):
    class Actions(models.TextChoices):
        SEE = 0, "SEEN"
        SUBMIT = 1, "SUBMITTED"
        SOLVE = 2, "SOLVED"

    time = models.DateTimeField(default=timezone.now)
    action_id = models.TextField(choices=Actions.choices)
    target_id = models.ForeignKey(Steps, null=True, on_delete=models.SET_NULL)
