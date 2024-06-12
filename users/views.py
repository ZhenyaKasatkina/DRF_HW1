from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.permissions import IsRealUser
from users.serializers import (PaymentSerializer, UserOtherSerializer,
                               UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)
        if self.action in ["destroy", "update", "partial_update"]:
            self.permission_classes = (IsRealUser,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return UserSerializer
        if self.action == "list":
            return UserOtherSerializer
        if self.action == "retrieve":
            if self.get_object() == self.request.user:
                return UserSerializer
            else:
                return UserOtherSerializer
        if self.action in ["update", "partial_update"]:
            if self.get_object() == self.request.user:
                return UserSerializer


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_fields = ("course", "lesson",)
    search_fields = ("way",)
    ordering_fields = ("date",)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user)
        return queryset
