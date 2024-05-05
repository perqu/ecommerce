from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from utils.validators import password_validator, last_name_validator, first_name_validator, username_validator
from .models import User

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'username']

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'email':{'required': True},
            'username':{'required': True},
            'password':{'required': True, 'write_only': True}
        }

    def create(self, validated_data):
            password = validated_data.pop('password')
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            return user

    def validate_first_name(self, value):
        first_name_validator(value)
        return value

    def validate_last_name(self, value):
        last_name_validator(value)
        return value

    def validate_username(self, value):
        username_validator(value)
        return value

    def validate_password(self, value):
        password_validator(value)
        return value
        
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

    def validate_first_name(self, value):
        first_name_validator(value)
        return value

    def validate_last_name(self, value):
        last_name_validator(value)
        return value

    def validate_username(self, value):
        username_validator(value)
        return value

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

    def validate_new_password(self, value):
        password_validator(value)
        return value

    def save(self):
        new_password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(new_password)
        user.save()
        return user
    