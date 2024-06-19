from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_user_activity():
    """Деактивация Пользователя, если он не входил более 30 дней"""

    today = timezone.now()
    print(f"сегодня: {today}")
    users = User.objects.all()
    for user in users:
        print(f" пользователь: {user.email}, {user.last_login}")
        if user.last_login is None or (today - user.last_login).days > 30:
            user.is_active = False
            user.save()
            print(f" неактивный {user.email}")
