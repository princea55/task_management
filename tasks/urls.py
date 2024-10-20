# tasks/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, TaskViewSetV2

router = DefaultRouter()
router.register('tasks', TaskViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v2/tasks/', TaskViewSetV2.as_view({'get': 'list'})),
]
