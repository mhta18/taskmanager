from rest_framework import generics, permissions
from django.db.models import Q
from .models import Task, BugReport, Note
from .serializers import TaskSerializer, BugReportSerializer, NoteSerializer
from .permissions import IsOwnerOrReadOnly


# --------------------
# 🔹 Base View
# --------------------
class BaseItemListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = self.model.objects.all()
        query = self.request.GET.get("q")  # ?q=search
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BaseItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class TaskListCreateAPIView(BaseItemListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    model = Task


class TaskRetrieveUpdateDestroyAPIView(BaseItemRetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskListCreateAPIView(BaseItemListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    model = Task


class TaskRetrieveUpdateDestroyAPIView(BaseItemRetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class BugReportListCreateAPIView(BaseItemListCreateAPIView):
    queryset = BugReport.objects.all()
    serializer_class = BugReportSerializer
    model = BugReport


class BugReportRetrieveUpdateDestroyAPIView(BaseItemRetrieveUpdateDestroyAPIView):
    queryset = BugReport.objects.all()
    serializer_class = BugReportSerializer

class NoteListCreateAPIView(BaseItemListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    model = Note


class NoteRetrieveUpdateDestroyAPIView(BaseItemRetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer



