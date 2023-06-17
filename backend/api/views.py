import io

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Tag)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientFilterSet, RecipeFilterSet
from .paginations import LimitPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    IngredientSerializer, RecipeCreateUpdateSerializer, RecipeSerializer,
    TagSerializer, FavoriteSerializer, ShoppingCartSerializer, RecipeWithoutRequestSerializer)

User = get_user_model()


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilterSet
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateUpdateSerializer

    def action_post_delete(self, pk, serializer_class):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        object = serializer_class.Meta.model.objects.filter(
            user=user, recipe=recipe
        )

        if self.request.method == 'POST':
            serializer = serializer_class(
                data={'user': user.id, 'recipe': pk},
                context={'request': self.request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if object.exists():
                object.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'error': 'Этого рецепта нет в списке'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST', 'DELETE'], detail=True)
    def favorite(self, request, pk):
        return self.action_post_delete(pk, FavoriteSerializer)

    @action(methods=['POST', 'DELETE'], detail=True)
    def shopping_cart(self, request, pk):
        return self.action_post_delete(pk, ShoppingCartSerializer)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart_recipe__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        buffer = io.BytesIO()
        shopping_list_fin = canvas.Canvas(buffer)
        pdfmetrics.registerFont(TTFont('TimesNewRoman', 'TimesNewRoman.ttf'))
        shopping_list_fin.setFont('TimesNewRoman', 14)
        shopping_list_fin.drawString(
            100, 750, f'{user.get_full_name()}, вот Ваш Cписок покупок:')
        y = 700

        for ingredient in ingredients:
            string = (
                f'- {ingredient["ingredient__name"]} '
                f'({ingredient["ingredient__measurement_unit"]})'
                f' - {ingredient["amount"]}')
            shopping_list_fin.drawString(100, y, string)
            y -= 30
        shopping_list_fin.showPage()
        shopping_list_fin.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,
                            filename='shopping_list.pdf')
