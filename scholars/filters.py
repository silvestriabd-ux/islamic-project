import django_filters
from django.db.models import Q
from .models import Scholar


class ScholarFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_q", label="Search")
    madhhab = django_filters.CharFilter(lookup_expr="iexact")
    birth_place = django_filters.CharFilter(lookup_expr="icontains")

    birth_year_min = django_filters.NumberFilter(
        field_name="birth_year", lookup_expr="gte", label="Born after")
    birth_year_max = django_filters.NumberFilter(
        field_name="birth_year", lookup_expr="lte", label="Born before")
    death_year_min = django_filters.NumberFilter(
        field_name="death_year", lookup_expr="gte", label="Died after")
    death_year_max = django_filters.NumberFilter(
        field_name="death_year", lookup_expr="lte", label="Died before")

    class Meta:
        model = Scholar
        fields = [
            "madhhab",
            "birth_place",
        ]

    def filter_q(self, queryset, name, value):
        value = (value or "").strip()
        if not value:
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(short_bio__icontains=value)
            | Q(biography__icontains=value)
            | Q(teachers__icontains=value)
            | Q(students__icontains=value)
            | Q(famous_books__icontains=value)
        )
