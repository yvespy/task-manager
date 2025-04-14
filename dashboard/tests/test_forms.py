from django.test import TestCase
from dashboard.forms import SignUpForm, TaskForm
from dashboard.models import Position, Worker, Task, TaskType
from django.utils import timezone
from datetime import timedelta


class SignUpFormTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")

    def test_signup_form_valid(self):
        form_data = {
            "username": "testuser",
            "first_name": "test_name",
            "last_name": "test_last_name",
            "email": "test@mail.com",
            "position": self.position.id,
            "password": "testpassword",
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

        worker = form.save()
        self.assertTrue(worker.check_password("testpassword"))
        self.assertEqual(worker.position, self.position)

    def test_signup_form_missing_required_field(self):
        form_data = {
            "username": "testuser",
            "first_name": "",
            "last_name": "test_last_name",
            "email": "test@mail.com",
            "position": self.position.id,
            "password": "testpassword",
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)


class TaskFormTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Bug")
        self.worker = Worker.objects.create_user(
            username="testuser",
            password="testpassword",
        )

    def test_task_form_valid(self):
        deadline = timezone.now() + timezone.timedelta(days=1)
        form_data = {
            "name": "Fix bug",
            "description": "Fix the issue",
            "deadline": deadline.strftime("%Y-%m-%dT%H:%M"),
            "priority": Task.Priority.MEDIUM,
            "task_type": self.task_type.id,
            "assignee": [self.worker.id],
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_invalid_missing_name(self):
        deadline = timezone.now() + timedelta(days=1)
        form_data = {
            "name": "",
            "description": "No task name",
            "deadline": deadline.strftime("%Y-%m-%dT%H:%M"),
            "priority": Task.Priority.MEDIUM,
            "task_type": self.task_type.id,
            "assignees": [self.worker.id],
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
