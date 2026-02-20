from django.contrib import admin

from .models import Tag, Task


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "due_date", "completed")
    list_filter = ("tags", "due_date", "completed")
