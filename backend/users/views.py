from api.serializers import (CustomTokenCreateSerializer, CustomUserSerializer,
                             SubscribeUserSerializer)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import TokenCreateView, UserViewSet
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow

User = get_user_model()


class CustomTokenCreateView(TokenCreateView):
    serializer_class = CustomTokenCreateSerializer


class CustomUserView(UserViewSet):
    serializer_class = CustomUserSerializer
    http_method = ['get', 'post', ]

    def get_queryset(self):
        return User.objects.all()

    @action(detail=False, methods=('get',))
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class ListSubscriberViewSet(UserViewSet):
    serializer_class = SubscribeUserSerializer
    http_method = ['get', ]

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)


class FollowViewSet(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = SubscribeUserSerializer
    queryset = Follow.objects.all()
    http_method = ['post', 'delete', ]

    def create(self, request, *args, **kwargs):
        follower = get_object_or_404(
            User, id=self.kwargs.get('pk'))
        user = self.request.user
        if user == follower:
            return Response(
                {'Нельзя подписаться на себя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Follow.objects.filter(follower=follower, user=user).exists():
            return Response(
                {'Нельзя подписаться второй раз!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        follow = Follow.objects.create(follower=follower, user=user)
        serializer = self.get_serializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        follower = get_object_or_404(User, id=self.kwargs.get('pk'))
        follow = Follow.objects.filter(
            follower=follower, user=self.request.user)
        if follow.exists():
            follow.delete()
            return Response(
                {'Вы отписались от пользователя!'},
                status=status.HTTP_204_NO_CONTENT)
        else:
            return None
