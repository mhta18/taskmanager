from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Task, BugReport, Note
from django.db.models import Q
import logging


logger = logging.getLogger('project')



def home(request):
    return render(request, "base.html")


class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"


class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description", "status", "priority", "assigned_to"]
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ["title", "description", "status", "priority", "assigned_to"]
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task-list")

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.owner


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task-list")

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.owner


class BugReportListView(ListView):
    model = BugReport
    template_name = "bugs/bug_list.html"
    context_object_name = "bugs"


class BugReportDetailView(DetailView):
    model = BugReport
    template_name = "bugs/bug_detail.html"


class BugReportCreateView(LoginRequiredMixin, CreateView):
    model = BugReport
    fields = ["title", "description", "severity", "status", "expected_result"]
    template_name = "bugs/bug_form.html"
    success_url = reverse_lazy("bug-list")

    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class BugReportUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BugReport
    fields = ["title", "description", "severity", "status", "expected_result"]
    template_name = "bugs/bug_form.html"
    success_url = reverse_lazy("bug-list")

    def test_func(self):
        bug = self.get_object()
        return self.request.user == bug.owner


class BugReportDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BugReport
    template_name = "bugs/bug_confirm_delete.html"
    success_url = reverse_lazy("bug-list")

    def test_func(self):
        bug = self.get_object()
        return self.request.user == bug.owner



class NoteListView(ListView):
    model = Note
    template_name = "notes/note_list.html"
    context_object_name = "notes"


class NoteDetailView(DetailView):
    model = Note
    template_name = "notes/note_detail.html"


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ["title", "description", "note_type", "is_pinned", "tags"]
    template_name = "notes/note_form.html"
    success_url = reverse_lazy("note-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        logger.info(f"Note '{form.instance.title}' created by {self.request.user.username}")
        return response
    
class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    fields = ["title", "description", "note_type", "is_pinned", "tags"]
    template_name = "notes/note_form.html"
    success_url = reverse_lazy("note-list")

    def test_func(self):
        note = self.get_object()
        return self.request.user == note.owner


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    template_name = "notes/note_confirm_delete.html"
    success_url = reverse_lazy("note-list")

    def test_func(self):
        note = self.get_object()
        return self.request.user == note.owner

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