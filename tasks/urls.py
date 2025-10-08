from django.urls import path
from .api_views import TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView
from . import views
from .views import (
    TaskListView, TaskDetailView, TaskCreateView,
    TaskUpdateView, TaskDeleteView
)

from django.urls import path
from .views import (
    TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    BugReportListView, BugReportDetailView, BugReportCreateView, BugReportUpdateView, BugReportDeleteView,
    NoteListView, NoteDetailView, NoteCreateView, NoteUpdateView, NoteDeleteView,
)

urlpatterns = [
    path("", views.home,name="home"),
    # --------------------
    # 🔹 Task URLs
    # --------------------
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),

    # --------------------
    # 🔹 BugReport URLs
    # --------------------
    path("bugs/", BugReportListView.as_view(), name="bug-list"),
    path("bugs/create/", BugReportCreateView.as_view(), name="bug-create"),
    path("bugs/<int:pk>/", BugReportDetailView.as_view(), name="bug-detail"),
    path("bugs/<int:pk>/update/", BugReportUpdateView.as_view(), name="bug-update"),
    path("bugs/<int:pk>/delete/", BugReportDeleteView.as_view(), name="bug-delete"),

    # --------------------
    # 🔹 Note URLs
    # --------------------
    path("notes/", NoteListView.as_view(), name="note-list"),
    path("notes/create/", NoteCreateView.as_view(), name="note-create"),
    path("notes/<int:pk>/", NoteDetailView.as_view(), name="note-detail"),
    path("notes/<int:pk>/update/", NoteUpdateView.as_view(), name="note-update"),
    path("notes/<int:pk>/delete/", NoteDeleteView.as_view(), name="note-delete"),

    # --------------------
    # 🔹 Search
    # --------------------
    path("search/",  views.search_view , name="search"),
]
