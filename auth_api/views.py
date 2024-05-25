from argparse import Action

from core import settings as django_settings
from django.contrib.auth import get_user_model, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.serializers import ValidationError

from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from djoser.views import UserViewSet
from djoser.conf import settings as djoser_settings

from .serializers import UserLoginSerializer

User = get_user_model()

tokenSetCookieArguments = {
    "max_age": django_settings.TOKEN_COOKIE_MAX_AGE,
    "secure": django_settings.TOKEN_COOKIE_SECURE,
    "httponly": django_settings.TOKEN_COOKIE_HTTPONLY,
    "samesite": django_settings.TOKEN_COOKIE_SAMESITE,
}


# Custom Djoser UserViewSet
class CustomUserAPIViewSet(UserViewSet):

    @method_decorator(csrf_protect, name="dispatch")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        if djoser_settings.SEND_ACTIVATION_EMAIL:
            return super().activation(request, *args, **kwargs)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["post"], detail=False)
    def resend_activation(self, request, *args, **kwargs):
        if djoser_settings.SEND_ACTIVATION_EMAIL:
            return super().resend_activation(request, *args, **kwargs)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["post"], detail=False, url_path=f"set_{User.USERNAME_FIELD}")
    def set_username(self, request, *args, **kwargs):
        if djoser_settings.SET_USERNAME:
            return super().set_username(request, *args, **kwargs)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["post"], detail=False, url_path=f"reset_{User.USERNAME_FIELD}")
    def reset_username(self, request, *args, **kwargs):
        if djoser_settings.SET_USERNAME:
            return super().reset_username(request, *args, **kwargs)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["post"], detail=False, url_path=f"reset_{User.USERNAME_FIELD}_confirm")
    def reset_username_confirm(self, request, *args, **kwargs):
        if djoser_settings.SET_USERNAME:
            return super().reset_username_confirm(request, *args, **kwargs)
        return Response(status=status.HTTP_404_NOT_FOUND)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GetCSRFTokenAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomLoginAndTokenObtainPairAPIView(TokenObtainPairView):
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie, name="dispatch")
    def post(self, request: Request, *args, **kwargs) -> Response:
        userLoginSerializer = UserLoginSerializer(data=request.data)
        serializer = self.get_serializer(data=request.data)

        if userLoginSerializer.is_valid(raise_exception=True):
            try:
                user = userLoginSerializer.validated_data
                login(request, user)
            except (ValueError, TypeError) as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        if serializer.validated_data:
            data = {"user": user.slug}
            response = Response(data, status=status.HTTP_200_OK)

            response.set_cookie(
                key="user",
                value=user.slug,
                max_age=django_settings.TOKEN_COOKIE_MAX_AGE,
                secure=django_settings.TOKEN_COOKIE_SECURE,
                httponly=False,
                samesite=django_settings.TOKEN_COOKIE_SAMESITE,
            )

            response.set_cookie(
                key="access",
                value=serializer.validated_data["access"],
                **tokenSetCookieArguments,
            )

            response.set_cookie(
                key="refresh",
                value=serializer.validated_data["refresh"],
                **tokenSetCookieArguments,
            )

            return response

        return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshAPIView(TokenRefreshView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        if serializer.validated_data:
            response = Response(status=status.HTTP_200_OK)

            response.set_cookie(
                key="access",
                value=serializer.validated_data["access"],
                **tokenSetCookieArguments,
            )

            return response

        return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("user")
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response


"""DJANGO basic authentication
class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format = None):
        userRegisterSerializer = UserRegisterSerializer(data = request.data)
        if userRegisterSerializer.is_valid():
            newUser = userRegisterSerializer.save()
            if newUser:
                data = {"message": f'Created new user {newUser.username}'}
                return Response(data, status=status.HTTP_201_CREATED)
        return Response(userRegisterSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format = None):
        userLoginSerializer = UserLoginSerializer(data = request.data)
        if userLoginSerializer.is_valid():
            authenticatedUser = userLoginSerializer.get_authenticated_user_cache()
            login(request, authenticatedUser)
            data = {"message": f'Logged in as {authenticatedUser.username}'}
            return Response(data, status=status.HTTP_200_OK)
        return Response(userLoginSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutAPIView(APIView):
    permission_classes = [AllowAny, IsAuthenticated]
    
    def post(self, request, format = None):
        logout(request)
        data = {"message": "Logged out"}
        return Response(data, status=status.HTTP_200_OK)
"""
