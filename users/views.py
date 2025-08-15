from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import (
    OpenApiResponse, extend_schema, inline_serializer
)
from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.permissions import IsOwner
from users.serializers import (
    PasswordResetConfirmSerializer, PasswordResetSerializer, UserSerializer
)

User = get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    """
    Регистрация пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class PasswordResetView(generics.GenericAPIView):
    """
    Запрос на отправку ссылки для сброса пароля на указанный Email.
    """

    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        request=PasswordResetSerializer,
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="PasswordResetSuccessResponse",
                    fields={
                        "detail": serializers.CharField(
                            default="Password reset e-mail has been sent."
                        )
                    },
                )
            )
        },
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = force_str(urlsafe_base64_encode(force_bytes(user.pk)))

            reset_url = settings.PASSWORD_RESET_CONFIRM_URL.format(
                uid=uid, token=token
            )

            subject = "Password Reset Requested"
            message = f"Link to reset your password: {reset_url}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

        return Response(
            {"detail": "Password reset e-mail has been sent."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    Запрос на подтверждение сброса и установки нового пароля.
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        request=PasswordResetConfirmSerializer,
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="PasswordResetConfirmView",
                    fields={
                        "detail": serializers.CharField(
                            default="Password has been reset successfully."
                        )
                    },
                )
            )
        },
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(
                urlsafe_base64_decode(serializer.validated_data["uid"])
            )
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(
            user, serializer.validated_data["token"]
        ):
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                {"detail": "Password has been reset successfully."}
            )

        RefreshToken.for_user(user).blacklist()

        return Response(
            {"detail": "Invalid token or uid."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserListAPIView(generics.ListAPIView):
    """
    Запрос на вывод списка пользователей.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    Запрос на вывод детальной информации по пользователю.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser | IsOwner)
    lookup_field = "pk"


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    Запрос на обновление пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser | IsOwner)
    lookup_field = "pk"

    def perform_update(self, serializer):
        if "password" in serializer.validated_data:
            user = serializer.save()
            user.set_password(serializer.validated_data["password"])
            user.save()
        else:
            serializer.save()


class UserDestroyAPIView(generics.DestroyAPIView):
    """
    Запрос на удаление пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    lookup_field = "pk"
