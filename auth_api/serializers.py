from django.forms import ValidationError
from django.contrib.auth import get_user_model, authenticate, password_validation

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

UserModel = get_user_model()
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def _user_authenticator(self, email, password):
        if email and password:
            authenticated_user_cache = authenticate(email=email, password=password)
            if authenticated_user_cache is None:
                raise serializers.ValidationError("Invalid credentials")
            self._confirm_user_active(authenticated_user_cache)
        return authenticated_user_cache
    
    def _confirm_user_active(self, user):
        if not user.is_active:
            raise serializers.ValidationError("User is not active")
    
    def validate(self, data):
        user = self._user_authenticator(data['email'], data['password'])
        return user

"""
class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    userCreationForm = None

    def validate(self, data):
        self.userCreationForm = CustomUserCreationForm(data)
        if not self.userCreationForm.is_valid():
            raise serializers.ValidationError(self.userCreationForm.errors)
        return data
    
    def create(self, validated_data):
        user = self.userCreationForm.save()
        return user

class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def _email_unique_validator(self, email):
        if email and UserModel.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Email already exists")
    
    def _passwords_match_validator(self, password1, password2):
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError("Passwords do not match")
    
    def _password_strength_validator(self, password, instance=None):
        if password:
            try:
                password_validation.validate_password(password, instance)
            except ValidationError as error:
                raise serializers.ValidationError(error)

    def validate_email(self, value):
        self._email_unique_validator(value)
        return value
    
    def validate(self, data):
        self._passwords_match_validator(data['password1'], data['password2'])
        self._password_strength_validator(data['password1'], UserModel(email=data['email']))
        return data
    
    def create(self, validated_data):
        createdUser = UserModel(email=validated_data["email"])
        createdUser.set_password(validated_data["password1"])
        createdUser.save()
        return createdUser
"""