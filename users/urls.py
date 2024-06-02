from django.urls import path

from users.apps import UsersConfig
from users.views import ProfileUpdateAPIView, ProfileCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('create/', ProfileCreateAPIView.as_view(), name='profile_create'),
    path('update/<int:pk>/', ProfileUpdateAPIView.as_view(), name='profile_update'),
]
