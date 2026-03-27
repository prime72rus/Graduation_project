from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ads.models import Ad, Review
from users.models import User


class AdTestCase(APITestCase):
    """
    Тестирование модели Ad.
    """

    def setUp(self):
        """
        Подготовка тестовых данных.
        """
        self.client = APIClient()

        self.admin = User.objects.create_user(
            email="admin@email.com",
            first_name="Test",
            last_name="Test",
            password="password",
            role="admin",
        )
        self.user = User.objects.create_user(
            email="user@email.com",
            first_name="Test",
            last_name="Test",
            password="password",
        )
        self.not_author = User.objects.create_user(
            email="not_author@email.com",
            first_name="Test",
            last_name="Test",
            password="password",
        )
        self.ad = Ad.objects.create(
            title="Test", price=1000, description="Test", author=self.user
        )

    def test_ad_create(self):
        """
        Тест: создание объявления.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("ads_reviews:ad_create")
        data = {
            "title": "Test_create",
            "price": 5000,
            "description": "Test_create",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ad.objects.count(), 2)
        self.assertEqual(Ad.objects.last().author, self.user)

    def test_ad_create_price_equal_to_zero(self):
        """
        Тест: создание объявления с отрицательной ценой.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("ads_reviews:ad_create")
        data = {
            "title": "Test_create",
            "price": -5000,
            "description": "Test_create",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Ad.objects.count(), 1)
        self.assertEqual(
            response.data["price"][0],
            "Ensure this value is greater than or equal to 0.",
        )

    def test_ads_list_authorized(self):
        """
        Тест: вывод списка объявлений авторизованным пользователем.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("ads_reviews:ads_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Test")

    def test_ads_list_not_authorized(self):
        """
        Тест: вывод списка объявлений не авторизованным пользователем.
        """
        url = reverse("ads_reviews:ads_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Test")

    def test_ad_retrieve_authorized(self):
        """
        Тест: детальный вывод объявления авторизованным пользователем.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("ads_reviews:ad_retrieve", args=[self.ad.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test")

    def test_ad_retrieve_not_authorized(self):
        """
        Тест: детальный вывод объявления не авторизованным пользователем.
        """
        url = reverse("ads_reviews:ad_retrieve", args=[self.ad.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ad_update(self):
        """
        Тест: обновление объявления автором.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("ads_reviews:ad_update", args=[self.ad.id])
        data = {"price": 10000}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.price, 10000)

    def test_ad_destroy_by_admin(self):
        """
        Тест: удаление объявления администратором.
        """
        self.client.force_authenticate(user=self.admin)
        url = reverse("ads_reviews:ad_destroy", args=[self.ad.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ad.objects.filter(id=self.ad.id).exists())

    def test_ad_destroy_by_author(self):
        """
        Тест: удаление объявления автором.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("ads_reviews:ad_destroy", args=[self.ad.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ad.objects.filter(id=self.ad.id).exists())

    def test_ad_destroy_by_not_author(self):
        """
        Тест: удаление объявления не автором.
        """
        self.client.force_authenticate(user=self.not_author)
        url = reverse("ads_reviews:ad_destroy", args=[self.ad.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ad_string_representation(self):
        """Тест: строковое представление объявления"""
        self.assertEqual(str(self.ad), "Test")


class ReviewTestCase(APITestCase):
    """
    Тестирование модели Review
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
        self.ad = Ad.objects.create(
            title="Test Ad", price=1000, description="Test", author=self.user
        )
        self.review = Review.objects.create(
            text="Good!", author=self.user, ad=self.ad
        )

    def test_create_review(self):
        """
        Тест: авторизованный пользователь может создать отзыв.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("ads_reviews:review_create")
        data = {"text": "Great product!", "ad": self.ad.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        self.assertEqual(Review.objects.last().author, self.user)

    def test_list_reviews(self):
        """
        Тест: любой авторизованный может посмотреть список отзывов.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("ads_reviews:reviews_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_review_by_admin(self):
        """
        Тест: админ может посмотреть детали отзыва.
        """
        self.client.force_authenticate(user=self.admin)
        url = reverse("ads_reviews:review_retrieve", args=[self.review.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], "Good!")

    def test_retrieve_review_forbidden_for_regular_user(self):
        """
        Тест: обычный пользователь не может посмотреть детали отзыва.
        """
        self.client.force_authenticate(user=self.other_user)
        url = reverse("ads_reviews:review_retrieve", args=[self.review.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_review_by_author(self):
        """
        Тест: автор может редактировать свой отзыв.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("ads_reviews:review_update", args=[self.review.id])
        data = {"text": "Updated text"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.text, "Updated text")

    def test_update_review_by_admin(self):
        """
        Тест: админ может редактировать любой отзыв.
        """
        self.client.force_authenticate(user=self.admin)
        url = reverse("ads_reviews:review_update", args=[self.review.id])
        data = {"text": "Admin edited"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_review_forbidden_for_other_user(self):
        """
        Тест: другой пользователь не может редактировать чужой отзыв.
        """
        self.client.force_authenticate(user=self.other_user)
        url = reverse("ads_reviews:review_update", args=[self.review.id])
        data = {"text": "Hacked!"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review_by_author(self):
        """Тест: автор может удалить свой отзыв"""
        self.client.force_authenticate(user=self.user)
        url = reverse("ads_reviews:review_destroy", args=[self.review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_delete_review_by_admin(self):
        """
        Тест: админ может удалить любой отзыв.
        """
        self.client.force_authenticate(user=self.admin)
        url = reverse("ads_reviews:review_destroy", args=[self.review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_review_forbidden_for_other_user(self):
        """
        Тест: другой пользователь не может удалить чужой отзыв.
        """
        self.client.force_authenticate(user=self.other_user)
        url = reverse("ads_reviews:review_destroy", args=[self.review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_string_representation(self):
        """
        Тест: строковое представление отзыва.
        """
        self.assertEqual(
            str(self.review),
            'Отзыв от user@example.com к объявлению "Test Ad"',
        )
