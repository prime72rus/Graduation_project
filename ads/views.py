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
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdFilter


class AdRetrieveAPIView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated, IsAdminUser | IsOwner)
    lookup_field = "pk"


class AdCreateAPIView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated,)


class AdUpdateAPIView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated, IsAdminUser | IsOwner)
    lookup_field = "pk"


class AdDestroyAPIView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated, IsAdminUser | IsOwner)
    lookup_field = "pk"


class ReviewListAPIView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)


class ReviewRetrieveAPIView(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    lookup_field = "pk"


class ReviewCreateAPIView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)


class ReviewUpdateAPIView(UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated, IsAdminUser | IsOwner)
    lookup_field = "pk"


class ReviewDestroyAPIView(DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated, IsAdminUser | IsOwner)
    lookup_field = "pk"
