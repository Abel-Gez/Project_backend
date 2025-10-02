from rest_framework import serializers
from .models import StaffUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# Staff Serializer for general purposes
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffUser
        fields = ['id', 'username', 'email', 'role']


# Serializer for creating new staff users
class StaffCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = StaffUser
        fields = ['username', 'email', 'role', 'password']

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = StaffUser.objects.create_user(**validated_data, password=password)
        return user


# Login Serializer (for username/password validation)
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        if not user.is_active:
            raise serializers.ValidationError("User account is inactive")
        data['user'] = user
        return data


# Custom JWT serializer to include username and role in the response
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add extra responses to the payload
        data['username'] = self.user.username
        data['role'] = self.user.role
        return data
