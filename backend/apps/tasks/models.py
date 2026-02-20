from django.db import models

from apps.users.models import BotUser
from .utils import generate_id


class Tag(models.Model):
    id = models.CharField(
        max_length=8, primary_key=True, default=generate_id, editable=False
    )
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.CharField(
        primary_key=True, max_length=16, default=generate_id, editable=False
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
