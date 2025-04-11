from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from dashboard.models import Position, TaskType, Task


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testpassword",
        )
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(name="DevOps")
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="passwordtest",
            position=self.position,
        )

    def test_worker_position_listed(self):
        url = reverse("admin:dashboard_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)

    def test_worker_detail_position_listed(self):
        url = reverse("admin:dashboard_worker_change", args=[self.worker.id])
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)

    def test_task_list_display_fields(self):
        task_type = TaskType.objects.create(name="Bug")
        task = Task.objects.create(
            name="Fix login issue",
            description="Error 500 on login page",
            deadline="2025-04-30T15:00:00Z",
            priority=Task.Priority.HIGH,
            task_type=task_type,
        )
        url = reverse("admin:dashboard_task_changelist")
        res = self.client.get(url)
        self.assertContains(res, task.name)
        self.assertContains(res, task.description)
        self.assertContains(res, task.task_type.name)