import django_filters
from recipes.models import Recipe


class TagFilterSet(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )

    class Meta:
        model = Recipe
        fields = ('tags',)
