from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

from .serializers import (
    UserSerializer,
    MyTokenObtainPairSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

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
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

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

        return Response(
            {"detail": "Invalid token or uid."},
            status=status.HTTP_400_BAD_REQUEST,
        )
