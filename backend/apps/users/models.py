from django.contrib.auth.models import AbstractUser
from django.db import models

from ..tasks.utils import generate_id


class BotUser(AbstractUser):
    id = models.CharField(
        max_length=16, primary_key=True, default=generate_id, editable=False
    )
    telegram_id = models.CharField(max_length=16, unique=True, blank=False)

    def __str__(self):
        return self.telegram_id
