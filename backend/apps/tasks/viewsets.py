from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


from .models import Tag, Task
from .serializers import TaskSerializer, TagSerializer
from ..users.models import BotUser


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        telegram_id = self.request.headers.get("X-Telegram-ID")
        return Task.objects.filter(owner__telegram_id=telegram_id)

    def perform_create(self, serializer):
        telegram_id = self.request.headers.get("X-Telegram-ID")

        bot_user, _ = BotUser.objects.get_or_create(telegram_id=telegram_id)

        serializer.save(owner=bot_user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
