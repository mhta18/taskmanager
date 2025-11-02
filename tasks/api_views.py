from rest_framework import generics, permissions
from django.db.models import Q
from .models import Task, BugReport, Note
from .serializers import TaskSerializer, BugReportSerializer, NoteSerializer
from .permissions import IsOwnerOrReadOnly
import logging

logger = logging.getLogger('project')

class BaseItemListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = self.model.objects.all()
        query = self.request.GET.get("q") 
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)
        logger.info(f"User '{self.request.user}' created a new {self.model.__name__} titled '{instance.title}'")

        
class BaseItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"User '{request.user}' viewed details of {self.model.__name__} titled '{instance.title}'")
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(f"User '{self.request.user}' updated {self.model.__name__} titled '{instance.title}'")

    def perform_destroy(self, instance):
        logger.info(f"User '{self.request.user}' deleted {self.model.__name__} titled '{instance.title}'")
        super().perform_destroy(instance)




class TaskListCreateAPIView(BaseItemListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    model = Task

class TaskRetrieveUpdateDestroyAPIView(BaseItemRetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    model = Task

class BugReportListCreateAPIView(BaseItemListCreateAPIView):
    queryset = BugReport.objects.all()
    serializer_class = BugReportSerializer
    model = BugReport


class BugReportRetrieveUpdateDestroyAPIView(BaseItemRetrieveUpdateDestroyAPIView):
    queryset = BugReport.objects.all()
    serializer_class = BugReportSerializer
    model = BugReport

class NoteListCreateAPIView(BaseItemListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    model = Note


class NoteRetrieveUpdateDestroyAPIView(BaseItemRetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    model = Note



