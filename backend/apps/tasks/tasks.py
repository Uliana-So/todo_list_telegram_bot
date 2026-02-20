from celery import shared_task
from django.utils import timezone
from .models import Task


@shared_task
def send_due_notification(task_id):
    try:
        task = Task.objects.get(id=task_id)

        if task.completed:
            return

        print(f"Задача '{task.title}' просрочена!")

    except Task.DoesNotExist:
        pass
