from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from education.models import Course, Lesson


@shared_task
def send_email_about_course_updates(email, pk, model):
    """Направляет письмо об обновлении курса/урока"""

    today = timezone.now()
    if model == "Lesson":
        item = Lesson.objects.filter(pk=pk).first()
        item_name = "урок"
    if model == "Course":
        item = Course.objects.filter(pk=pk).first()
        item_name = "курс"
    print(item_name, item.name, item.url)
    send_mail(
        subject=f"Обновление {item_name}а '{item.name}'",
        message=f"Привет! Обновленный {item_name} '{item.name}' можно посмотреть по ссылке: {item.url}",
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

    item.last_update = today
    item.save()
