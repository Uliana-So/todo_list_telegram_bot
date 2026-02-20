from rest_framework import viewsets
from .models import BotUser
from .serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Только чтение пользователей через API.
    """

    queryset = BotUser.objects.all()
    serializer_class = UserSerializer
