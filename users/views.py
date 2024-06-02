from rest_framework import generics

from users.models import User
from users.serializers import UserSerializer


class ProfileCreateAPIView(generics.CreateAPIView):
    """
    Создание пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ProfileUpdateAPIView(generics.UpdateAPIView):
    """
    Редактирование профиля пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
