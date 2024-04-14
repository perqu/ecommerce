from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import check_password

class UserGetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'username', 'email']
        read_only_fields = ['uuid']

class UserPostSerializer(serializers.Serializer):
    username = serializers.CharField(default='')
    password = serializers.CharField(default='')
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False, default='')
    last_name = serializers.CharField(required=False, default='')

class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'username', 'email', 'first_name', 'last_name', 'email_verified', 'profile']
        read_only_fields = ['uuid']

class UserPatchSerializer(serializers.ModelSerializer):
    username = serializers.CharField(default='')
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False, default='')
    last_name = serializers.CharField(required=False, default='')
    email_verified = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['uuid', 'username', 'email', 'first_name', 'last_name', 'email_verified', 'profile']
        read_only_fields = ['uuid']

class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError("Old password is incorrect")
        return value

    def save(self):
        new_password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(new_password)
        user.save()
        return user