from api.serializers import (CustomTokenCreateSerializer, CustomUserSerializer,
                             SubscribeUserSerializer)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import TokenCreateView, UserViewSet
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow

User = get_user_model()


class CustomTokenCreateView(TokenCreateView):
    serializer_class = CustomTokenCreateSerializer


class CustomUserView(UserViewSet):
    quyryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        if request.method == 'POST':
            serializer = SubscribeUserSerializer(
                author, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = get_object_or_404(
                Follow, user=user, author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeUserSerializer(
            pages, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
