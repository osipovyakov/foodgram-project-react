import django_filters
from django.contrib.auth import get_user_model
from recipes.models import Ingredient, Recipe, Tag

User = get_user_model()


class IngredientFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilterSet(django_filters.FilterSet):
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = django_filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)

    def filter_is_favorited(self, queryset, name, value):
        queryset = queryset.filter(favorite_recipe__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        queryset.filter(shopping_cart_recipe__user=self.request.user)
        return queryset
