from django.db import models


class Ad(models.Model):
    """
    Модель объявления
    """

    title = models.CharField(
        verbose_name="Название товара",
        max_length=255,
        help_text="Укажите название товара"
    )
    price = models.PositiveIntegerField(
        verbose_name="Цена товара",
        default=0,
        help_text="Укажите цену товара"
    )
    description = models.TextField(
        verbose_name="Описание товара",
        help_text="Укажите описание товара"
    )
    author = models.ForeignKey(
        "users.User",
        verbose_name="Пользователь который создал объявление",
        on_delete=models.CASCADE,
        related_name="ads",
        help_text="Укажите пользователя создавшего объявление"
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания объявления",
        auto_now_add=True,
        help_text="Укажите дату создания объявления"
    )

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Модель отзыва
    """

    text = models.TextField(
        verbose_name="Отзыв на товар",
        help_text="Укажите текст отзыва"
    )
    author = models.ForeignKey(
        "users.User",
        verbose_name="Автор отзыва",
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="Укажите автора отзыва"
    )
    ad = models.ForeignKey(
        "ads.Ad",
        verbose_name="Объявление, под которым оставлен отзыв",
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="Укажите объявление, под которым оставлен отзыв"
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания отзыва",
        auto_now_add=True,
        help_text="Укажите дату создания отзыва"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return f'Отзыв от {self.author} к объявлению "{self.ad.title}"'
