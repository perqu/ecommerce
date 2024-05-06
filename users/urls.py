from django.urls import path
from .views import LoginAPIView, UserListCreateView, UserDetailView, UserAccountView, ChangePasswordView

urlpatterns = [
    path('/login', LoginAPIView.as_view(), name='login'),
    path('', UserListCreateView.as_view(), name='user-list'),
    path('/<uuid:uuid>', UserDetailView.as_view(), name='user-detail'),
    path('/me', UserAccountView.as_view(), name='user-me'),
    path('/me/change-password', ChangePasswordView.as_view(), name='change-password'),
]
