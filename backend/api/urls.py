from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import IngredientsViewSet, RecipeViewSet, TagViewSet

router = DefaultRouter()

router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [

    path('users/', include('users.urls')),
    path('auth/', include('users.urls')),
    path('', include(router.urls)),
]
