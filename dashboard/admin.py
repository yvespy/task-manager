from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from dashboard.models import Worker, Position, TaskType, Task


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", )
    fieldsets = UserAdmin.fieldsets + (
        (
            "Personal information", {"fields": ("position",)}
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Personal information",
            {
                "fields": ("first_name", "last_name", "position",)
            }
        ),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "deadline",
        "priority",
        "task_type",
        "is_completed",
    ]
    list_filter = [
        "name",
        "is_completed",
        "priority",
        "task_type",
    ]


admin.site.register(Position)
admin.site.register(TaskType)
