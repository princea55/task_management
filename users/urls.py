# users/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import SignupView, LoginView, UserViewSet, ChangePasswordView

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change/password/', ChangePasswordView.as_view(), name='change_password'),
    path('api/v1/', include(router.urls)),
    # User-related endpoints

]
