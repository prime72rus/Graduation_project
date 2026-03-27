from rest_framework import serializers

from ads.models import Ad, Review


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = [
            "id",
            "title",
            "price",
            "description",
            "author",
            "created_at",
        ]
        read_only_fields = ("author",)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "text", "author", "ad", "created_at"]
        read_only_fields = ("author",)
