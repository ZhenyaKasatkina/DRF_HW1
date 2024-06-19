from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from education.models import Course, Lesson, Subscription
from education.paginators import Pagination
from education.permissions import IsModerator, IsOwner
from education.serializers import (CourseSerializer, LessonSerializer,
                                   SubscriptionSerializer)
from education.tasks import send_email_about_course_updates


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = Pagination

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (
                IsAuthenticated,
                ~IsModerator,
            )
        elif self.action == "destroy":
            self.permission_classes = (IsOwner | ~IsModerator,)
        elif self.action in ["update", "partial_update", "retrieve", "list"]:
            self.permission_classes = (IsModerator | IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_queryset(self, *args, **kwargs):
        if self.request.user.groups.filter(name="moderator").exists():
            print(self)
            return Course.objects.all()
        else:
            if not self.request.user.is_anonymous:
                return Course.objects.filter(owner=self.request.user)
            return None


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = Pagination
    permission_classes = (IsModerator | IsOwner,)

    def get_queryset(self, *args, **kwargs):
        if self.request.user.groups.filter(name="moderator").exists():
            return Lesson.objects.all()
        else:
            if not self.request.user.is_anonymous:
                return Lesson.objects.filter(owner=self.request.user)
            return None


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsModerator | IsOwner,)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        ~IsModerator,
    )

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsModerator | IsOwner,)


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (~IsModerator | IsOwner,)


class LessonAPIView(APIView):
    """Обновление урока по запросу Пользователя"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def post(self, *args, **kwargs):
        today = timezone.now()
        user = self.request.user
        lesson_id = self.request.data["lesson"]
        # получаем объект курса из базы
        lesson_item = get_object_or_404(Lesson, pk=lesson_id)
        # print(lesson_item)

        # получаем объект курска, в который включен текущий урок у текущего пользователя
        course_item = Course.objects.filter(owner=user, lesson=lesson_id).first()
        # print(course_item)
        # получаем объекты подписок по текущему пользователю и курсу
        subs_item = Subscription.objects.filter(owner=user, course=course_item.pk)

        # Если последнее обновление у пользователя на этот курс и урок было менее 4 часов - то сообщаем
        # что обновление урока можно запросить только через 4 часа после последнего обновления
        if (
            subs_item.exists()
            and (today - course_item.last_update).seconds > 14400
            # or (today - lesson_item.last_update).seconds > 14400
        ):
            item = send_email_about_course_updates.delay(
                user.email, lesson_item.pk, "Lesson"
            )
            # print(item.ready())
            message = f"Обновление на урок {lesson_item.name} отправлено Вам на электронную почту"

        elif (
            subs_item.exists()
            and (today - course_item.last_update).seconds < 14400
            # or (today - lesson_item.last_update).seconds < 14400
        ):
            message = "С последнего обновления прошло менее 4-х часов"

        # Возвращаем ответ в API
        return Response({"message": message})


class SubscriptionAPIView(APIView):
    """Подключение подписки на обновление курса"""

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data["course"]
        # получаем объект курса из базы
        course_item = get_object_or_404(Course, pk=course_id)

        # получаем объекты подписок по текущему пользователю и курсу
        subs_item = Subscription.objects.filter(owner=user, course=course_id)
        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(course=course_item, owner=user, is_active=True)
            message = "подписка добавлена"
            # print((user.email, course_item.name))
            item = send_email_about_course_updates.delay(
                user.email, course_item.pk, "Course"
            )
            print(item.ready())

        # Возвращаем ответ в API
        return Response({"message": message})
