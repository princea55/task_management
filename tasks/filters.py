# tasks/filters.py

import django_filters

from .models import Task


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['status', 'priority', 'due_date', 'assigned_to']
