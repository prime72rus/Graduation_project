import django_filters

from ads.models import Ad


class AdFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr="icontains", label="Поиск по названию"
    )

    class Meta:
        model = Ad
        fields = ["title"]
