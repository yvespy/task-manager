from django.urls import path

from dashboard import views
from dashboard.views import index, WorkerListView, WorkerDetailView, TaskCreateView, \
    TaskDetailView, TaskCompleteView, TaskUpdateView, DashboardView, TaskDeleteView, TaskListView

urlpatterns = [
    path("", index, name="index"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>", WorkerDetailView.as_view(), name="worker-detail"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("sign_up/", views.sign_up_view, name="sign_up"),
    path("tasks/add/", TaskCreateView.as_view(), name="task-add"),
    path("dashboard/<int:pk>/complete/", TaskCompleteView.as_view(), name="task-complete"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task"),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("dashboard/tasks_list", TaskListView.as_view(), name="task-list"),
]
