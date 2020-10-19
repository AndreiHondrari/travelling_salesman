import uuid

from django.contrib.auth import get_user_model
from django.db import models

from jobs import constants

User = get_user_model()


class Job(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    status = models.CharField(
        max_length=20,
        choices=constants.JobStatus.choices,
        default=constants.JobStatus.PENDING
    )
    locations = models.JSONField()
    num_vehicles = models.IntegerField(default=1)
    starting_location = models.IntegerField(default=0)
    full_result = models.JSONField(blank=True, default="")
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.uuid}"
