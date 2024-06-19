from datetime import datetime

import pytz
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings
from users.models import Payment, User
from users.permissions import IsRealUser
from users.serializers import (PaymentSerializer, UserOtherSerializer,
                               UserSerializer)
from users.services import (create_stripe_price, create_stripe_product,
                            create_stripe_session, get_stripe_session_result)


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
    filterset_fields = (
        "course",
        "lesson",
    )
    search_fields = ("way",)
    ordering_fields = ("date",)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_anonymous:
            queryset = queryset.filter(user=self.request.user)
            return queryset
        return None


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        zone = pytz.timezone(settings.TIME_ZONE)
        new_payment = serializer.save(user=self.request.user, date=datetime.now(zone))

        # print(new_payment.course.name)
        # print(new_payment.lesson)
        if new_payment.course:
            new_payment.price = new_payment.course.price
            name_product = create_stripe_product(new_payment.course.name)
            price = create_stripe_price(new_payment.course.price, name_product)
        if new_payment.lesson:
            new_payment.price = new_payment.lesson.price
            name_product = create_stripe_product(new_payment.lesson.name)
            price = create_stripe_price(new_payment.lesson.price, name_product)
        session_id, payment_link = create_stripe_session(price)
        new_payment.session_id = session_id
        new_payment.link = payment_link
        new_payment.save()


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentAPIView(APIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def post(self, *args, **kwargs):
        """Получаем инфо по оплате имеющегося в базе платежа по "session_id" """
        # user = self.request.user
        # print(self.request.data["session_id"])
        session_id = self.request.data["session_id"]
        # получаем объект платежа из базы
        payment_item = get_object_or_404(Payment, session_id=session_id)
        # получаем информацию об оплате
        is_paid = get_stripe_session_result(session_id)["payment_status"]
        # print(is_paid)

        # Если оплата произведена - сохраняем ее и выводим сообщение об этом
        if is_paid == "paid":
            payment_item.is_paid = True
            payment_item.save()
            message = "Оплачено"
        # Если нет - то выводим сообщение об этом
        else:
            message = "Не оплачено"
        # Возвращаем ответ в API
        return Response({"message": message})
