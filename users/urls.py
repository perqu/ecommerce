from django.urls import path
from .views import UserDetailView, UserListView, LoginAPIView, AccountView, ChangePasswordView

urlpatterns = [
    path('/login', LoginAPIView.as_view(), name='login'),
    path('', UserListView.as_view(), name='user-list'),
    path('/<uuid:uuid>', UserDetailView.as_view(), name='user-detail'),
    path('/me', AccountView.as_view(), name='user-me'),
    path('/me/change-password', ChangePasswordView.as_view(), name='change-password'),
]
