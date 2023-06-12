from distutils.util import strtobool

import django_filters
from recipes.models import Favorite, Ingredient, Recipe


class IngredientFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilterSet(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    is_favorited = django_filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return Recipe.objects.none()
        new_queryset = Favorite.objects.filter(
            user=self.request.user).values_list('recipe_id')
        if not strtobool(value):
            return queryset.difference(new_queryset)
        return queryset.filter(id__in=new_queryset)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(shopping_cart__user=user)
        return queryset
