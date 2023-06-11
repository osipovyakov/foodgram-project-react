from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import CustomUserView
from api.views import IngredientsViewSet, TagViewSet, RecipeViewSet

router = DefaultRouter()
router.register(r'users', CustomUserView)
router.register(r'ingredients', IngredientsViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
