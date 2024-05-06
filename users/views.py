from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from django.shortcuts import get_object_or_404

from utils.permissions import HasGroupPermission
from utils.throttle import LoginThrottle
from utils.paginators import SmallResultsSetPagination
from .models import User
from .serializers import AuthSerializer, UserListSerializer, UserDetailSerializer, UserCreateSerializer, UserEditSerializer, ChangePasswordSerializer
from utils.scheme import KnoxTokenScheme

class LoginAPIView(KnoxLoginView):
    """
    A view to handle user authentication and token generation.
    """
    throttle_classes = [LoginThrottle]
    serializer_class = AuthSerializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """
        Authenticate user and generate a token.

        Required parameters in the request:
        - username: The username of the user (string).
        - password: The password of the user (string).
        """
        serializer = AuthTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPIView, self).post(request, format=None)

class UserListCreateView(APIView):
    """
    A view to list all users or create a new user.
    """
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']
    pagination_class = SmallResultsSetPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(name="page_size", type=OpenApiTypes.INT, description='Page Size for pagination.', required=False),
            OpenApiParameter(name="page", type=OpenApiTypes.INT, description='Page number for pagination.', required=False),
        ],
    )
    def get(self, request):
        """
        Get a list of paginated users.

        Example:
        http://localhost:8000/users?page=2&page_size=20
        """
        users = User.objects.all().order_by('username')

        paginator = self.pagination_class()
        paginated_users = paginator.paginate_queryset(users, request)

        serializer = UserListSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(request=UserCreateSerializer)
    def post(self, request):
        """
        Create a new user.

        Required parameters in the request:
        - username: The username of the user (string).
        - email: The email of the user (string).
        - password: The password of the user (string).

        Optional parameters:
        - first_name: The first name of the user (string).
        - last_name: The last name of the user (string).
        - is_superuser: Indicates if the user is a superuser (boolean).
        - is_staff: Indicates if the user is staff (boolean).
        - is_active: Indicates if the user is active (boolean).
        - email_verified: Indicates if the email of the user is verified (boolean).
        - last_login: The date and time of the last login (string, format: "YYYY-MM-DDThh:mm:ss.sssZ").
        - date_joined: The date and time when the user joined (string, format: "YYYY-MM-DDThh:mm:ss.sssZ").
        - profile: The profile information of the user (string, UUID format).
        - groups: The groups to which the user belongs (list of integers).
        - user_permissions: The permissions of the user (list of integers).
        """
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    """
    A view to retrieve, update or delete an user instance.
    """
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']

    def get(self, request, uuid):
        """
        Retrieve details of an user by UUID.

        Required parameter in the URL:
        - uuid: The UUID of the user to retrieve (string).
        """
        user = get_object_or_404(User, uuid=uuid)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=UserEditSerializer)
    def patch(self, request, uuid):
        """
        Edit user.

        Possible parameters in the request:
        - username: The username of the user (string).
        - email: The email of the user (string).
        - first_name: The first name of the user (string).
        - last_name: The last name of the user (string).
        - is_superuser: Indicates if the user is a superuser (boolean).
        - is_staff: Indicates if the user is staff (boolean).
        - is_active: Indicates if the user is active (boolean).
        - email_verified: Indicates if the email of the user is verified (boolean).
        - last_login: The date and time of the last login (string, format: "YYYY-MM-DDThh:mm:ss.sssZ").
        - date_joined: The date and time when the user joined (string, format: "YYYY-MM-DDThh:mm:ss.sssZ").
        - profile: The profile information of the user (string, UUID format).
        - groups: The groups to which the user belongs (list of integers).
        - user_permissions: The permissions of the user (list of integers).
        """
        user = get_object_or_404(User, uuid=uuid)
        serializer = UserEditSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        """
        Delete an user by UUID.

        Required parameter in the URL:
        - uuid: The UUID of the user to delete (string).
        """
        user = get_object_or_404(User, uuid=uuid)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserAccountView(APIView):
    """
    A view to display user data.
    """

    def get(self, request):
        """
        Retrieve details of your account.
        """
        user = get_object_or_404(User, uuid=request.user.uuid)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ChangePasswordView(APIView):
    """
    A view to handle changing user password.
    """
    @extend_schema(
        request=ChangePasswordSerializer,
    )
    def post(self, request):
        """
        Change user password.

        Required parameters in the request:
        - old_password: The old password of the user (string).
        - new_password: The new password of the user (string).
        """
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
