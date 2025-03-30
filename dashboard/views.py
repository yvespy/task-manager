from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import TemplateView

from dashboard.forms import SignUpForm, TaskForm
from dashboard.models import Worker, Task, TaskType


def index(request: HttpRequest) -> HttpResponse:
    num_employees = Worker.objects.all().count()
    num_tasks = Task.objects.all().count()
    num_completed = Task.objects.filter(is_completed=True).count()

    context = {
        "num_employees": num_employees,
        "num_tasks": num_tasks,
        "num_completed": num_completed,
    }

    return render(request, "dashboard/index.html", context=context)


class ActiveTaskView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "includes/active_task.html"
    context_object_name = "tasks_list"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Task.objects.filter(is_completed=False)
        return Task.objects.filter(assignees=user, is_completed=False)


class CompletedTaskView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "includes/completed_task.html"
    context_object_name = "completed_tasks"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Task.objects.filter(is_completed=True)
        return Task.objects.filter(assignees=user, is_completed=True)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "pages/dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["workers"] = Worker.objects.filter(is_superuser=False)

        if user.is_superuser:
            tasks_list = Task.objects.filter(is_completed=False)
            completed_tasks = Task.objects.filter(is_completed=True)
        else:
            tasks_list = Task.objects.filter(assignees=user, is_completed=False)
            completed_tasks = Task.objects.filter(assignees=user, is_completed=True)

        task_paginator = Paginator(tasks_list, 5)
        completed_task_paginator = Paginator(completed_tasks, 5)

        task_page_number = self.request.GET.get('task_page')
        completed_page_number = self.request.GET.get('completed_page')

        context["tasks_list"] = task_paginator.get_page(task_page_number)
        context["completed_tasks"] = completed_task_paginator.get_page(completed_page_number)

        return context


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "workers_list"
    template_name = "dashboard/worker_list.html"
    paginate_by = 10


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    context_object_name = "worker_detail"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "dashboard/tasks_list.html"
    context_object_name = "list_of_tasks"
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.all().prefetch_related("assignees")
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "dashboard/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "dashboard/create_task.html"
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = Worker.objects.all()
        return context

    def form_valid(self, form):
        task = form.save(commit=False)
        task.save()
        task.assignees.add(self.request.user)
        return super().form_valid(form)


class TaskCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = True
        task.save()
        return redirect("dashboard")

    def get_success_url(self):
        return reverse_lazy("dashboard")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("dashboard")
    template_name = "dashboard/task_confirm_delete.html"
    context_object_name = "task"

    def get_object(self, queryset=None):
        task = get_object_or_404(Task, pk=self.kwargs["pk"])
        return task


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = ["name", "description", "deadline", "priority", "task_type"]
    template_name = "dashboard/task_update.html"
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_types"] = TaskType.objects.all()
        if self.request.user.is_superuser:
            context["assignees"] = Worker.objects.all()
        else:
            context["assignees"] = self.object.assignees.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        if 'assignees' in self.request.POST:
            assignees_ids = self.request.POST.getlist('assignees')
            self.object.assignees.set(assignees_ids)

        return response


def sign_up_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = SignUpForm()
    return render(request, "registration/sign-up.html", {"form": form})
