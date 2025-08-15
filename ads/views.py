from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from ads.filters import AdFilter
from ads.models import Ad, Review
from ads.pagination import AdPagination
from ads.serializers import AdSerializer, ReviewSerializer
from users.permissions import IsOwner


class AdListAPIView(ListAPIView):
    """
    Запрос на получение списка объявлений.
    """

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdFilter


class AdRetrieveAPIView(RetrieveAPIView):
    """
    Запрос на вывод детальной информации об объявлении.
    """

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated, IsAdminUser | IsOwner)
    lookup_field = "pk"


class AdCreateAPIView(CreateAPIView):
    """
    Запрос на создание объявления.
    """

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated,)


class AdUpdateAPIView(UpdateAPIView):
    """
    Запрос на обновление объявления.
    """

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated, IsAdminUser | IsOwner)
    lookup_field = "pk"


class AdDestroyAPIView(DestroyAPIView):
    """
    Запрос на удаление объявления.
    """

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated, IsAdminUser | IsOwner)
    lookup_field = "pk"


class ReviewListAPIView(ListAPIView):
    """
    Запрос списка отзывов.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)


class ReviewRetrieveAPIView(RetrieveAPIView):
    """
    Запрос на вывод детальной информации об отзыве.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    lookup_field = "pk"


class ReviewCreateAPIView(CreateAPIView):
    """
    Запрос на создание отзыва.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)


class ReviewUpdateAPIView(UpdateAPIView):
    """
    Запрос на обновление отзыва.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated, IsAdminUser | IsOwner)
    lookup_field = "pk"


class ReviewDestroyAPIView(DestroyAPIView):
    """
    Запрос на удаление отзыва.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated, IsAdminUser | IsOwner)
    lookup_field = "pk"
