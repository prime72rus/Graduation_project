from django.urls import path

from ads.apps import AdsConfig
from ads.views import (
    AdCreateAPIView, AdDestroyAPIView, AdListAPIView, AdRetrieveAPIView,
    AdUpdateAPIView, ReviewCreateAPIView, ReviewDestroyAPIView,
    ReviewListAPIView, ReviewRetrieveAPIView, ReviewUpdateAPIView
)

app_name = AdsConfig.name

urlpatterns = [
    path("ads/", AdListAPIView.as_view(), name="ads_list"),
    path(
        "ads/retrieve/<int:pk>/",
        AdRetrieveAPIView.as_view(),
        name="ad_retrieve",
    ),
    path("ads/create/", AdCreateAPIView.as_view(), name="ad_create"),
    path("ads/update/<int:pk>/", AdUpdateAPIView.as_view(), name="ad_update"),
    path(
        "ads/destroy/<int:pk>/", AdDestroyAPIView.as_view(), name="ad_destroy"
    ),
    path("reviews/", ReviewListAPIView.as_view(), name="reviews_list"),
    path(
        "reviews/retrieve/<int:pk>/",
        ReviewRetrieveAPIView.as_view(),
        name="review_retrieve",
    ),
    path(
        "reviews/create/", ReviewCreateAPIView.as_view(), name="review_create"
    ),
    path(
        "reviews/update/<int:pk>/",
        ReviewUpdateAPIView.as_view(),
        name="review_update",
    ),
    path(
        "reviews/destroy/<int:pk>/",
        ReviewDestroyAPIView.as_view(),
        name="review_destroy",
    ),
]
