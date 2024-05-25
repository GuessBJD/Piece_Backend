from django.contrib.auth import get_user_model
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import *

app_name = "auth_api"

router = DefaultRouter()
router.register("users", CustomUserAPIViewSet)

User = get_user_model()

urlpatterns = router.urls

urlpatterns += [
    path("csrf/", GetCSRFTokenAPIView.as_view(), name="csrf-token"),
    path("login/", CustomLoginAndTokenObtainPairAPIView.as_view(), name="login"),
    path("token/refresh/", CustomTokenRefreshAPIView.as_view(), name="token-refresh"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]