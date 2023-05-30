from django.urls import include, path
from djoser.views import TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import (CustomTokenCreateView, CustomUserView, FollowViewSet,
                    ListSubscriberViewSet)

router = DefaultRouter()

router.register(r'', CustomUserView, basename='users')

urlpatterns = [

    path('me/', CustomUserView.as_view({'get': 'me'})),
    path('<int:pk>/', CustomUserView.as_view({'get': 'retrieve'})),
    path('subscriptions/', ListSubscriberViewSet.as_view({'get': 'list'})),
    path('<int:pk>/subscribe/', FollowViewSet.as_view()),
    path('token/login/', CustomTokenCreateView.as_view()),
    path('token/logout/', TokenDestroyView.as_view()),
    path('', include(router.urls)),

]
