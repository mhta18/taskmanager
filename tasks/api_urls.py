from django.urls import path
from .api_views import (
    TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView,
    BugReportListCreateAPIView, BugReportRetrieveUpdateDestroyAPIView,
    NoteListCreateAPIView, NoteRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    # --------------------
    # 🔹 Task API
    # --------------------
    path("tasks/", TaskListCreateAPIView.as_view(), name="api-task-list"),
    path("tasks/<int:pk>/", TaskRetrieveUpdateDestroyAPIView.as_view(), name="api-task-detail"),

    # --------------------
    # 🔹 BugReport API
    # --------------------
    path("bugs/", BugReportListCreateAPIView.as_view(), name="api-bug-list"),
    path("bugs/<int:pk>/", BugReportRetrieveUpdateDestroyAPIView.as_view(), name="api-bug-detail"),

    # --------------------
    # 🔹 Note API
    # --------------------
    path("notes/", NoteListCreateAPIView.as_view(), name="api-note-list"),
    path("notes/<int:pk>/", NoteRetrieveUpdateDestroyAPIView.as_view(), name="api-note-detail"),
]
