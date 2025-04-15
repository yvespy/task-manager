from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from dashboard.models import TaskType, Task


class PublicDashboardViewTests(TestCase):
    def test_login_required(self):
        url = reverse("worker-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateDashboardViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = "testuser",
            password = "testpassword",
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="Bug")

    def test_retrieve_task_list(self):
        url = reverse("task-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "dashboard/tasks_list.html")

    def test_dashboard_view(self):
        url = reverse("dashboard")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "pages/dashboard/dashboard.html")
        self.assertIn("tasks_list", res.context)
        self.assertIn("completed_tasks", res.context)

    def test_create_task(self):
        url = reverse("task-add")
        res = self.client.post(url, {
            "name": "Test Task",
            "description": "Test description",
            "deadline": "2025-05-01",
            "priority": "High",
            "task_type": self.task_type.id,
        })

        self.assertEqual(res.status_code, 302)

    def test_complete_task(self):
        task = Task.objects.create(name="Test Task", is_completed=False)
        task.assignees.add(self.user)

        url = reverse("task-complete", args=[task.id])
        res = self.client.post(url)

        task.refresh_from_db()
        self.assertTrue(task.is_completed)
        self.assertRedirects(res, reverse("dashboard"))

    def test_worker_detail_view(self):
        worker = get_user_model().objects.create_user(
            username = "user_test",
            password = "testpassword",
        )

        self.client.force_login(worker)

        url = reverse("worker-detail", args=[worker.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, worker.username)

    def test_task_delete_by_assignee(self):
        task = Task.objects.create(name="Delete Task", is_completed=False)
        task.assignees.add(self.user)

        url = reverse("task-delete", args=[task.id])
        res = self.client.post(url)

        self.assertRedirects(res, reverse("dashboard"))
        self.assertFalse(Task.objects.filter(id=task.id).exists())
