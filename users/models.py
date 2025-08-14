from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    """
    Кастомный менеджер для модели User, где email является уникальным
    идентификатором вместо username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным email и паролем.
        """
        if not email:
            raise ValueError("The Email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создает и сохраняет суперпользователя с указанным email и паролем.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class UserRoles(models.TextChoices):
    """
    Класс для создания вариантов перечисляемых строк поля role.
    """
    USER = "user", "User"
    ADMIN = "admin", "Admin"


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="Email адрес", unique=True)
    first_name = models.CharField(verbose_name="Имя", max_length=150)
    last_name = models.CharField(verbose_name="Фамилия", max_length=150)
    phone = models.CharField(verbose_name="Номер телефона", max_length=20)
    role = models.CharField(
        verbose_name="Роль",
        max_length=20,
        choices=UserRoles.choices,
        default=UserRoles.USER
    )
    image = models.ImageField(
        verbose_name="Аватар",
        upload_to="users/avatars/",
        null=True,
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email