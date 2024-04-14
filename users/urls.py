from django.urls import path
from .views import UserDetailView, UserListView, LoginAPIView, ChangePasswordAPIView

urlpatterns = [
    path('/login', LoginAPIView.as_view(), name='login'),
    path('', UserListView.as_view(), name='user-list'),
    path('/<uuid:uuid>', UserDetailView.as_view(), name='user-detail'),
    path('/change-password', ChangePasswordAPIView.as_view(), name='change-password'),
]
