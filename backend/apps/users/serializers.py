from rest_framework import serializers
from .models import BotUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ["id", "telegram_id"]
        read_only_fields = ["id"]
