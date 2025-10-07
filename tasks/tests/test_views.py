from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from tasks.models import Task, BugReport, Note

class ViewTestCase(TestCase):
    def setUp(self):
        """Set up test data that will be used in multiple tests"""
        # Create users
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        
        # Create test objects
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Task Description',
            owner=self.user,
            status='todo',
            priority='medium'
        )
        
        self.bug = BugReport.objects.create(
            title='Test Bug',
            description='Test Bug Description',
            owner=self.user,
            severity='high',
            status='reported'
        )
        
        self.note = Note.objects.create(
            title='Test Note',
            description='Test Note Content',
            owner=self.user,
            note_type='general',
            is_pinned=False
        )
        
        # Create client
        self.client = Client()

    def test_home_view(self):
        """Test that home page loads correctly"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_task_list_view(self):
        """Test task list view"""
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertIn('tasks', response.context)
        self.assertEqual(len(response.context['tasks']), 1)

    def test_task_detail_view(self):
        """Test task detail view"""
        response = self.client.get(reverse('task-detail', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        self.assertEqual(response.context['task'], self.task)

    def test_task_create_view_post_authenticated(self):
        """Test that authenticated users can create tasks via POST"""
        self.client.login(username='testuser', password='testpass123')
        
        # Test POST request with valid data - should redirect (302)
        task_data = {
            'title': 'New Task',
            'description': 'New Task Description',
            'status': 'in_progress',
            'priority': 'high',
            "assigned_to": self.user.id,
        }
        response = self.client.post(reverse('task-create'), task_data)
        
        # Should redirect to task list on success (302)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('task-list'))
        
        # Check that task was created
        self.assertEqual(Task.objects.count(), 2)
        new_task = Task.objects.get(title='New Task')
        self.assertEqual(new_task.owner, self.user)

    def test_task_create_view_unauthenticated(self):
        """Test that unauthenticated users are redirected to login"""
        response = self.client.get(reverse('task-create'))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_task_update_view_post_owner(self):
        """Test that task owner can update their task via POST"""
        self.client.login(username='testuser', password='testpass123')
        
        # Test POST request with update data - should redirect (302)
        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
            "status": "done",
            "priority": "high",
            "assigned_to": self.user.id,
        }
        response = self.client.post(reverse('task-update', kwargs={'pk': self.task.pk}), update_data)
        
        # Should redirect to task list (302)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('task-list'))
        
        # Refresh task from database and check updates
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Title')
        self.assertEqual(self.task.status, 'done')

    def test_task_update_view_non_owner(self):
        """Test that non-owners cannot update tasks"""
        self.client.login(username='otheruser', password='testpass123')
        
        response = self.client.get(reverse('task-update', kwargs={'pk': self.task.pk}))
        # Should return 403 Forbidden due to UserPassesTestMixin
        self.assertEqual(response.status_code, 403)

    def test_task_delete_view_owner(self):
        """Test that task owner can delete their task"""
        self.client.login(username='testuser', password='testpass123')
        
        # Test GET request (confirm delete page)
        response = self.client.get(reverse('task-delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_confirm_delete.html')
        
        # Test POST request (actual deletion)
        response = self.client.post(reverse('task-delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect to task list
        self.assertEqual(Task.objects.count(), 0)   # Task should be deleted

    def test_bug_report_list_view(self):
        """Test bug report list view"""
        response = self.client.get(reverse('bug-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bugs/bug_list.html')
        self.assertIn('bugs', response.context)

    def test_bug_report_detail_view(self):
        """Test bug report detail view"""
        response = self.client.get(reverse('bug-detail', kwargs={'pk': self.bug.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bugs/bug_detail.html')

    def test_note_list_view(self):
        """Test note list view"""
        response = self.client.get(reverse('note-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_list.html')
        self.assertIn('notes', response.context)

    def test_note_create_view(self):
        """Test note creation by authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        
        note_data = {
            'title': 'New Note',
            'description': 'New Note Content',
            'note_type': 'meeting',
            'is_pinned': True
        }
        response = self.client.post(reverse('note-create'), note_data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(Note.objects.count(), 2)   # Original + new one
        
        new_note = Note.objects.get(title='New Note')
        self.assertEqual(new_note.owner, self.user)
        self.assertTrue(new_note.is_pinned)

class ModelTestCase(TestCase):
    """Basic model tests to ensure models work correctly"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='modeluser',
            password='testpass123'
        )
    
    def test_task_creation(self):
        task = Task.objects.create(
            title='Model Test Task',
            description='Test Description',
            owner=self.user
        )
        self.assertEqual(str(task), 'Model Test Task (todo)')
        self.assertEqual(task.owner, self.user)
        self.assertEqual(task.status, 'todo')  # Default value
    
    def test_bug_report_creation(self):
        bug = BugReport.objects.create(
            title='Model Test Bug',
            description='Bug Description',
            owner=self.user
        )
        self.assertEqual(str(bug), 'Bug: Model Test Bug (medium)')
        self.assertEqual(bug.severity, 'medium')  # Default value
    
    def test_note_creation(self):
        note = Note.objects.create(
            title='Model Test Note',
            description='Note Content',
            owner=self.user,
            is_pinned=True
        )
        self.assertEqual(str(note), 'Note: Model Test Note (general)')
        self.assertTrue(note.is_pinned)