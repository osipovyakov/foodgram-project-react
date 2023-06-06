from api.serializers import SubscribeRecipeSerializer
from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from rest_framework import generics, status
from rest_framework.response import Response


class CreateDestroyMixin(generics.CreateAPIView, generics.DestroyAPIView):
    http_method = ['post', 'delete']

    def create(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        if self.get_queryset().filter(
            recipe=recipe, user=self.request.user
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.model.objects.create(recipe=recipe, user=self.request.user)
        serializer = SubscribeRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        if not self.get_queryset().filter(
            recipe=recipe, user=self.request.user
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        is_favorited = self.get_queryset().filter(recipe=recipe,
                                                  user=self.request.user)
        is_favorited.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
