from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserTestCase(APITestCase):
    """
    Тестирование модели User.
    """

    def setUp(self):
        """
        Подготовка тестовых данных.
        """
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="user@example.com",
            first_name="User",
            last_name="Test",
            password="password123",
            role="user",
        )
        self.admin = User.objects.create_user(
            email="admin@example.com",
            first_name="Admin",
            last_name="Test",
            password="password123",
            role="admin",
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            first_name="Other",
            last_name="User",
            password="password123",
            role="user",
        )

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_user_registration(self):
        """
        Тест: регистрация нового пользователя.
        """
        url = reverse("users:user_register")
        data = {
            "email": "newuser@example.com",
            "password": "newpass123",
            "first_name": "New",
            "last_name": "User",
            "role": "user",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)  # user + admin + other + new
        new_user = User.objects.get(email="newuser@example.com")
        self.assertFalse(new_user.is_staff)

    def test_list_users_by_admin(self):
        """
        Тест: только админ может посмотреть список пользователей.
        """
        self.client.force_authenticate(user=self.admin)
        url = reverse("users:users_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_users_forbidden_for_regular_user(self):
        """
        Тест: обычный пользователь не может посмотреть список пользователей.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("users:users_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_own_user(self):
        """
        Тест: пользователь может посмотреть свои данные.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("users:user_retrieve", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_other_user_by_admin(self):
        """
        Тест: админ может посмотреть любого пользователя.
        """
        self.client.force_authenticate(user=self.admin)
        url = reverse("users:user_retrieve", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_other_user_forbidden(self):
        """
        Тест: пользователь не может посмотреть чужого пользователя.
        """
        self.client.force_authenticate(user=self.other_user)
        url = reverse("users:user_retrieve", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_own_user(self):
        """
        Тест: пользователь может обновить свои данные.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("users:user_update", args=[self.user.id])
        data = {"first_name": "Updated"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")

    def test_update_user_password(self):
        """
        Тест: обновление пароля через update.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("users:user_update", args=[self.user.id])
        data = {"password": "newstrongpass123"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newstrongpass123"))

    def test_delete_user_by_admin(self):
        """
        Тест: админ может удалить пользователя.
        """
        self.client.force_authenticate(user=self.admin)
        url = reverse("users:user_destroy", args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_delete_user_forbidden(self):
        """
        Тест: обычный пользователь не может удалить другого.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("users:user_destroy", args=[self.admin.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_password_reset_email_sent(self):
        """
        Тест: отправка письма для сброса пароля.
        """
        url = reverse("users:password_reset")
        data = {"email": self.user.email}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Password Reset Requested", mail.outbox[0].subject)

    def test_password_reset_email_not_found_silent(self):
        """
        Тест: email не существует — всё равно 200 (для безопасности).
        """
        url = reverse("users:password_reset")
        data = {"email": "unknown@example.com"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 0)

    def test_password_reset_confirm_valid(self):
        """
        Тест: сброс пароля по валидной ссылке.
        """
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))

        url = reverse("users:password_reset_confirm")
        data = {"uid": uid, "token": token, "new_password": "newpassword123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword123"))

    def test_password_reset_confirm_invalid_token(self):
        """
        Тест: невалидный токен.
        """
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        url = reverse("users:password_reset_confirm")
        data = {
            "uid": uid,
            "token": "invalid-token",
            "new_password": "newpass123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_confirm_invalid_uid(self):
        """
        Тест: невалидный uid.
        """
        token = default_token_generator.make_token(self.user)
        url = reverse("users:password_reset_confirm")
        data = {
            "uid": "invalid-uid",
            "token": token,
            "new_password": "newpass123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_string_representation(self):
        """
        Тест строкового представления привычки.
        """
        self.assertEqual(str(self.admin), "admin@example.com")


class UserManagerTestCase(TestCase):
    """
    Тестирование кастомного менеджера модели User.
    """

    def test_create_superuser(self):
        """
        Тест: создание суперпользователя с корректными правами.
        """
        email = "superuser@example.com"
        password = "superpass123"

        user = User.objects.create_superuser(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.role, "admin")
        self.assertTrue(user.is_active)

    def test_create_superuser_without_is_staff_raises_error(self):
        """
        Тест: ошибка, если is_staff=False.
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="superuser@example.com",
                password="superpass123",
                is_staff=False,
            )

    def test_create_superuser_without_is_superuser_raises_error(self):
        """
        Тест: ошибка, если is_superuser=False.
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="superuser@example.com",
                password="superpass123",
                is_superuser=False,
            )

    def test_create_superuser_sets_role_admin(self):
        """
        Тест: role автоматически устанавливается в 'admin'.
        """
        user = User.objects.create_superuser(
            email="superuser@example.com", password="superpass123"
        )
        self.assertEqual(user.role, "admin")

    def test_create_superuser_password_is_hashed(self):
        """
        Тест: пароль хешируется/
        """
        user = User.objects.create_superuser(
            email="superuser@example.com", password="superpass123"
        )
        self.assertTrue(user.password.startswith("pbkdf2_"))
        self.assertTrue(user.check_password("superpass123"))
