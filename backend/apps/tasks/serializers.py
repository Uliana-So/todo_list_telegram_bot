from rest_framework import serializers
from .models import Task, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("owner",)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["tags"] = [tag.name for tag in instance.tags.all()]
        return rep

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        task = Task.objects.create(**validated_data)

        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            task.tags.add(tag)

        return task

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_data is not None:
            instance.tags.clear()
            for tag_name in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)

        return instance
