from django.db import models


class JobStatus(models.TextChoices):
    PENDING = "pending"
    TIME_OUT = "timeout"
    FAILED = "failed"
    SUCCESSFUL = "successful"
