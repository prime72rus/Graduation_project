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
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "user")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создает и сохраняет суперпользователя с указанным email и паролем.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
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
    """
    Кастомная модель пользователя
    """

    id: models.AutoField

    username = None
    email = models.EmailField(
        verbose_name="Email адрес",
        unique=True,
        help_text="Укажите свой Email адрес",
    )
    first_name = models.CharField(
        verbose_name="Имя", max_length=150, help_text="Укажите имя"
    )
    last_name = models.CharField(
        verbose_name="Фамилия", max_length=150, help_text="Укажите фамилию"
    )
    phone = models.CharField(
        verbose_name="Номер телефона",
        max_length=20,
        blank=True,
        null=True,
        help_text="Укажите номер телефона",
    )
    role = models.CharField(
        verbose_name="Роль",
        max_length=20,
        choices=UserRoles.choices,
        default=UserRoles.USER,
        help_text="Укажите роль",
    )
    image = models.ImageField(
        verbose_name="Аватар",
        upload_to="media/users/avatars/",
        null=True,
        blank=True,
        help_text="Выберите аватарку",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
