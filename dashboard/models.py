from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True
    )


class TaskType(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "Urgent"
        HIGH = "High"
        MEDIUM = "Medium"
        LOW = "Low"

    name = models.CharField(max_length=250)
    description = models.TextField(max_length=500, blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.SET_NULL,
        null=True
    )
    assignees = models.ManyToManyField(
        Worker,
        related_name="task_assigned",
        blank=True
    )

    class Meta:
        ordering = ["-priority"]

    def __str__(self) -> str:
        return f"{self.name} ({self.priority})"
