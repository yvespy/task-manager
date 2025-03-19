from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from dashboard.models import Worker, Task


def index(request: HttpRequest) -> HttpResponse:
    num_employees = Worker.objects.all().count()
    num_tasks = Task.objects.all().count()

    context = {
        "num_employees": num_employees,
        "num_tasks": num_tasks,
    }

    return render(request, "dashboard/index.html", context=context)


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "workers_list"
    paginate_by = 10


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    context_object_name = "worker_detail"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "tasks_list"


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    context_object_name = "task_detail"