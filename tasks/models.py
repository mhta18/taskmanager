from django.db import models 
from django.contrib.auth.models import User


class BaseItem(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 


class Task(BaseItem):  
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'In Review'),
        ('done', 'Done'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')

    class Meta:
        unique_together = ('owner', 'title')

    def __str__(self):
        return f"{self.title} ({self.status})"


class BugReport(BaseItem): 
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('reopened', 'Reopened'),
    ]

    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    expected_result = models.TextField(blank=True)

    class Meta:
        unique_together = ('owner', 'title')

    def __str__(self):
        return f"Bug: {self.title} ({self.severity})"


class Note(BaseItem): 
    NOTE_TYPES = [
        ('general', 'General'),
        ('meeting', 'Meeting'),
        ('research', 'Research'),
        ('idea', 'Idea'),
        ('personal', 'Personal'),
    ]
    
    note_type = models.CharField(max_length=20, choices=NOTE_TYPES, default='general')
    is_pinned = models.BooleanField(default=False)
    tags = models.CharField(max_length=100, blank=True)
    
    class Meta:
        unique_together = ('owner', 'title')

    def __str__(self):
        return f"Note: {self.title} ({self.note_type})"
