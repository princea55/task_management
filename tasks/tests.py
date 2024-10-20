from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Task, Comment
from tasks.serializers import CommentSerializer, TaskSerializer

User = get_user_model()


class TaskViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password123', role='user')
        self.manager = User.objects.create_user(username='manager', password='password123', role='manager')
        self.admin = User.objects.create_user(username='admin', password='password123', role='admin')
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            status='pending',
            priority='medium',
            due_date=date.today(),
            assigned_to=self.user,
            created_by=self.manager
        )

    def test_get_tasks(self):
        """Test that tasks can be retrieved."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Task')

    def test_create_task(self):
        """Test that a task is created successfully."""
        self.client.force_authenticate(user=self.admin)
        data = {
            'title': 'New Task',
            'description': 'This is a new task',
            'status': 'pending',
            'priority': 'high',
            'due_date': date.today(),
            'assigned_to': self.user.id,
            'created_by': self.admin.id
        }
        response = self.client.post(reverse('task-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Task')

    def test_update_task_permission(self):
        """Test that only the assigned user can update the task."""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Task',
        }
        response = self.client.patch(reverse('task-detail', args=[self.task.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Task')

    def test_non_assigned_user_cannot_update(self):
        """Test that users who are not assigned cannot update the task."""
        another_user = User.objects.create_user(username='another_user', password='password123', role='user')
        self.client.force_authenticate(user=another_user)
        data = {'title': 'Illegal Update'}
        response = self.client.patch(reverse('task-detail', args=[self.task.id]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_tasks(self):
        """Test filtering tasks by priority."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('task-list'), {'priority': 'medium'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['priority'], 'medium')


class TaskSerializerTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', role='user')
        self.admin_user = User.objects.create_user(username='admin', password='password123', role='admin')
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            status='pending',
            priority='medium',
            due_date=date.today(),
            assigned_to=self.user,
            created_by=self.user
        )

    def test_task_serializer(self):
        """Test the Task serializer data."""
        serializer = TaskSerializer(instance=self.task)
        data = serializer.data
        self.assertEqual(data['title'], 'Test Task')
        self.assertEqual(data['status'], 'pending')

    def test_task_assignment_to_admin(self):
        """Ensure the task cannot be assigned to admin users."""
        data = {
            'title': 'Invalid Task',
            'description': 'Test task',
            'status': 'pending',
            'priority': 'high',
            'due_date': date.today(),
            'assigned_to': self.admin_user.id,
            'created_by': self.admin_user.id,
        }

        serializer = TaskSerializer(data=data, context={'request': self.client.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(serializer.errors['non_field_errors'][0], "Tasks cannot be assigned to Admin users.")


class CommentSerializerTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', role='user')
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            status='pending',
            priority='medium',
            due_date=date.today(),
            assigned_to=self.user,
            created_by=self.user
        )
        self.comment = Comment.objects.create(
            task=self.task, user=self.user, comment='Test comment'
        )

    def test_comment_serializer(self):
        """Test the Comment serializer data."""
        serializer = CommentSerializer(instance=self.comment)
        data = serializer.data
        self.assertEqual(data['comment'], 'Test comment')
