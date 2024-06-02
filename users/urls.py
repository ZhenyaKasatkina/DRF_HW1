from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import (  # ProfileUpdateAPIView, ProfileCreateAPIView, ProfileRetrieveAPIView,
    PaymentListAPIView, UserViewSet)

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
] + router.urls
