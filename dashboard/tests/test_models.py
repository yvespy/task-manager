from django.utils import timezone

from django.test import TestCase

from dashboard.models import Position, Worker, TaskType, Task


class ModelsTest(TestCase):
    def test_position_str(self):
        position = Position.objects.create(name="test")
        self.assertEqual(str(position), position.name)

    def test_worker_str(self):
        position = Position.objects.create(name="Manager")
        worker = Worker.objects.create_user(username="johndoe", password="password123", position=position)
        self.assertEqual(str(worker), worker.username)

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="Bug")
        self.assertEqual(str(task_type), task_type.name)

    def test_task_str_and_default_priority(self):
        task_type = TaskType.objects.create(name="New feature")
        task = Task.objects.create(name="Create task page", task_type=task_type)
        self.assertEqual(str(task), "Create task page (Medium)")

    def test_task_priority_choices(self):
        task_type = TaskType.objects.create(name="New feature")
        task = Task.objects.create(name="Create task page", task_type=task_type, priority=Task.Priority.HIGH)
        self.assertEqual(task.priority, "High")

    def test_task_many_assignees(self):
        position = Position.objects.create(name="QA")
        worker1 = Worker.objects.create_user(username="johndoe", password="password321", position=position)
        worker2 = Worker.objects.create_user(username="janedoe", password="password123", position=position)
        task_type = TaskType.objects.create(name="New feature")
        task = Task.objects.create(name="Create task page", task_type=task_type)
        task.assignees.set([worker1, worker2])
        self.assertEqual(task.assignees.count(), 2)
        self.assertIn(worker1, task.assignees.all())
        self.assertIn(worker2, task.assignees.all())

    def test_task_deadline_and_completion(self):
        task_type = TaskType.objects.create(name="Refactoring")
        deadline = timezone.now() + timezone.timedelta(days=3)
        task = Task.objects.create(
            name="Refactoring login page",
            task_type=task_type,
            deadline=deadline,
            is_completed=True
        )
        self.assertEqual(task.is_completed, True)
        self.assertEqual(task.deadline.date(), deadline.date())

