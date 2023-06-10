from django.urls import include, path

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
