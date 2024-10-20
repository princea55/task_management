# tasks/views.py
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import throttle_classes
from rest_framework.permissions import BasePermission
from rest_framework.throttling import UserRateThrottle

from .filters import TaskFilter
from .models import Task
from .serializers import TaskSerializer


class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'manager']


class IsAssignedUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assigned_to == request.user


@throttle_classes([UserRateThrottle])
@extend_schema(tags=['Tasks'])
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsAssignedUser()]
        elif self.action in ['create', 'destroy']:
            return [IsAdminOrManager()]
        return super().get_permissions()


@extend_schema(tags=['Tasks V2'])
class TaskViewSetV2(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
