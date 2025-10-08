from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from tasks.models import Task, BugReport, Note

class ViewTestCase(TestCase):
    def setUp(self):

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

        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_task_list_view(self):
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertIn('tasks', response.context)
        self.assertEqual(len(response.context['tasks']), 1)

    def test_task_detail_view(self):
        response = self.client.get(reverse('task-detail', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        self.assertEqual(response.context['task'], self.task)

    def test_task_create_view_post_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        

        task_data = {
            'title': 'New Task',
            'description': 'New Task Description',
            'status': 'in_progress',
            'priority': 'high',
            "assigned_to": self.user.id,
        }
        response = self.client.post(reverse('task-create'), task_data)
        

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('task-list'))
        

        self.assertEqual(Task.objects.count(), 2)
        new_task = Task.objects.get(title='New Task')
        self.assertEqual(new_task.owner, self.user)

    def test_task_create_view_unauthenticated(self):
        response = self.client.get(reverse('task-create'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_task_update_view_post_owner(self):
        
        self.client.login(username='testuser', password='testpass123')
        
        
        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
            "status": "done",
            "priority": "high",
            "assigned_to": self.user.id,
        }
        response = self.client.post(reverse('task-update', kwargs={'pk': self.task.pk}), update_data)
        

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('task-list'))
        

        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Title')
        self.assertEqual(self.task.status, 'done')

    def test_task_update_view_non_owner(self):
        self.client.login(username='otheruser', password='testpass123')
        
        response = self.client.get(reverse('task-update', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 403)

    def test_task_delete_view_owner(self):
        self.client.login(username='testuser', password='testpass123')
        

        response = self.client.get(reverse('task-delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_confirm_delete.html')

        response = self.client.post(reverse('task-delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Task.objects.count(), 0)   

    def test_bug_report_list_view(self):
        response = self.client.get(reverse('bug-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bugs/bug_list.html')
        self.assertIn('bugs', response.context)

    def test_bug_report_detail_view(self):
        response = self.client.get(reverse('bug-detail', kwargs={'pk': self.bug.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bugs/bug_detail.html')

    def test_note_list_view(self):
        response = self.client.get(reverse('note-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_list.html')
        self.assertIn('notes', response.context)

    def test_note_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        
        note_data = {
            'title': 'New Note',
            'description': 'New Note Content',
            'note_type': 'meeting',
            'is_pinned': True
        }
        response = self.client.post(reverse('note-create'), note_data)
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Note.objects.count(), 2)  
        new_note = Note.objects.get(title='New Note')
        self.assertEqual(new_note.owner, self.user)
        self.assertTrue(new_note.is_pinned)

