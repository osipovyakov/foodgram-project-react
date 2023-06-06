import io

import django_filters
from django.contrib.auth import get_user_model
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Tag)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import generics, mixins, pagination, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import TagFilterSet
from .mixins import CreateDestroyMixin
from .serializers import (IngredientSerializer, RecipeCreateUpdateSerializer,
                          RecipeSerializer, SubscribeRecipeSerializer,
                          TagSerializer)

User = get_user_model()


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_metod = ['get']


class IngredientsViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    pagination_class = None
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method = ['get']

    def search_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        name = self.request.query_params.get('name', None)

        if name is not None:
            return queryset.filter(name__istartswith=name)
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    http_method = ['get', 'post', 'patch', 'delete']
    filter_back = (DjangoFilterBackend,)
    filter_class = TagFilterSet

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateUpdateSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        is_favorited = self.request.query_params.get('is_favorited')
        in_shopping_cart = self.request.query_params.get('in_shopping_cart')
        author = self.request.query_params.get('author')
        if author is not None:
            queryset = queryset.filter(author=author)
        if is_favorited:
            queryset = queryset.filter(recipe_favorite__user=self.request.user)
        elif in_shopping_cart:
            self.pagination_class = pagination.LimitOffsetPagination
            return queryset.filter(recipe_shoppinglist__user=self.request.user)
        return queryset


class FavoriteViewSet(CreateDestroyMixin):
    model = Favorite
    queryset = Favorite.objects.all()


class ShoppingListViewSet(CreateDestroyMixin):
    model = ShoppingList
    queryset = ShoppingList.objects.all()


class DownloadShoppingList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    http_method = ['get']

    def get(self, request, *args, **kwargs):
        recipes = Recipe.objects.filter(
            recipe_shoppinglist__user=self.request.user)
        ingredients_list = []
        for recipe in recipes:
            ingredients = RecipeIngredient.objects.filter(recipe=recipe)
            ingredients_list += ingredients
        ingredient = []
        for item in ingredients_list:
            name = Ingredient.objects.get(name=item.ingredient.name)
            amount = item.amount
            if name in ingredient:
                ingredient[ingredient.index(name) + 1] += amount
            else:
                ingredient += (name, amount)

        buffer = io.BytesIO()
        shopping_list_fin = canvas.Canvas(buffer)
        pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
        shopping_list_fin.setFont('Vera', 14)
        shopping_list_fin.drawString(
            100, 750, 'Вот Ваш Cписок покупок:')
        y = 700
        for index in range(0, len(ingredient), 3):
            string = (
                f' *  {ingredient[index]} — {str(ingredient[index+1])}')
            shopping_list_fin.drawString(100, y, string)
            y -= 30
        shopping_list_fin.showPage()
        shopping_list_fin.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,
                            filename='shopping_list.pdf')
