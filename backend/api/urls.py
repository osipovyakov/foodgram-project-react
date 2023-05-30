from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DownloadShoppingList, FavoriteViewSet, IngredientsViewSet,
                    RecipeViewSet, ShoppingListViewSet, TagViewSet)

router = DefaultRouter()

router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [

    path('recipes/download_shopping_cart/', DownloadShoppingList.as_view()),
    path('recipes/<int:pk>/favorite/', FavoriteViewSet.as_view()),
    path('recipes/<int:pk>/shopping_cart/', ShoppingListViewSet.as_view()),
    path('users/', include('users.urls')),
    path('auth/', include('users.urls')),
    path('', include(router.urls)),
]
