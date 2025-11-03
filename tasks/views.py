from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Task, BugReport, Note
from django.db.models import Q
import logging


logger = logging.getLogger('project')



def home(request):
    logger.info(f"User '{request.user}' visited the home page")
    return render(request, "base.html")


class BaseOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.owner


class BaseListView(ListView):

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")

        if query:
            logger.info(f"User '{self.request.user}' searched for '{query}' in {self.model.__name__}")
            queryset = queryset.filter(title__icontains=query)
        else:
            logger.info(f"User '{self.request.user}' viewed list of {self.model.__name__}s")

        return queryset


class BaseCreateView(LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        logger.info(f"User '{self.request.user}' created {self.model.__name__} titled '{form.instance.title}'")
        return response


class BaseUpdateView(BaseOwnerMixin, UpdateView):

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"User '{self.request.user}' updated {self.model.__name__} titled '{form.instance.title}'")
        return response


class BaseDeleteView(BaseOwnerMixin, DeleteView):

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"User '{request.user}' deleted {self.model.__name__} titled '{instance.title}'")
        return super().delete(request, *args, **kwargs)


class BaseDetailView(DetailView):

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"User '{request.user}' viewed details of {self.model.__name__} titled '{instance.title}'")
        return super().get(request, *args, **kwargs)



class TaskListView(BaseListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"


class TaskDetailView(BaseDetailView):
    model = Task
    template_name = "tasks/task_detail.html"


class TaskCreateView(BaseCreateView):
    model = Task
    fields = ["title", "description", "status", "priority", "assigned_to"]
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task-list")




class TaskUpdateView(BaseUpdateView):
    model = Task
    fields = ["title", "description", "status", "priority", "assigned_to"]
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task-list")


class TaskDeleteView(BaseDeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task-list")



class BugReportListView(BaseListView):
    model = BugReport
    template_name = "bugs/bug_list.html"
    context_object_name = "bugs"


class BugReportDetailView(BaseDetailView):
    model = BugReport
    template_name = "bugs/bug_detail.html"


class BugReportCreateView(BaseCreateView):
    model = BugReport
    fields = ["title", "description", "severity", "status", "expected_result"]
    template_name = "bugs/bug_form.html"
    success_url = reverse_lazy("bug-list")


class BugReportUpdateView(BaseUpdateView):
    model = BugReport
    fields = ["title", "description", "severity", "status", "expected_result"]
    template_name = "bugs/bug_form.html"
    success_url = reverse_lazy("bug-list")


class BugReportDeleteView(BaseDeleteView):
    model = BugReport
    template_name = "bugs/bug_confirm_delete.html"
    success_url = reverse_lazy("bug-list")


class NoteListView(BaseListView):
    model = Note
    template_name = "notes/note_list.html"
    context_object_name = "notes"


class NoteDetailView(BaseDetailView):
    model = Note
    template_name = "notes/note_detail.html"


class NoteCreateView(BaseCreateView):
    model = Note
    fields = ["title", "description", "note_type", "is_pinned", "tags"]
    template_name = "notes/note_form.html"
    success_url = reverse_lazy("note-list")


class NoteUpdateView(BaseUpdateView):
    model = Note
    fields = ["title", "description", "note_type", "is_pinned", "tags"]
    template_name = "notes/note_form.html"
    success_url = reverse_lazy("note-list")


class NoteDeleteView(BaseDeleteView):
    model = Note
    template_name = "notes/note_confirm_delete.html"
    success_url = reverse_lazy("note-list")

def search_view(request):
    query = request.GET.get('q', '').strip()
    notes = tasks = bugs = []

    if query:
        notes = Note.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        tasks = Task.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        bugs = BugReport.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    context = {
        'query': query,
        'notes': notes,
        'tasks': tasks,
        'bugs': bugs,
    }

    logger.info(f"User '{request.user}' searched for '{query}'")
    return render(request, 'search_results.html', context)