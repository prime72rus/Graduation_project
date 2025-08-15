from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from users.apps import UsersConfig
from users.views import (
    PasswordResetConfirmView, PasswordResetView, UserCreateAPIView,
    UserDestroyAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView
)

app_name = UsersConfig.name

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserCreateAPIView.as_view(), name="user_register"),
    path(
        "reset_password/", PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "reset_password_confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("", UserListAPIView.as_view(), name="users_list"),
    path(
        "retrieve/<int:pk>/",
        UserRetrieveAPIView.as_view(),
        name="user_retrieve",
    ),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="user_update"),
    path(
        "destroy/<int:pk>/", UserDestroyAPIView.as_view(), name="user_destroy"
    )
]
