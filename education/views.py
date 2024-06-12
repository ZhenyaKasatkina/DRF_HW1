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
            return Course.objects.filter(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = Pagination
    permission_classes = (IsModerator | IsOwner,)

    def get_queryset(self, *args, **kwargs):
        if self.request.user.groups.filter(name="moderator").exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


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


class SubscriptionAPIView(APIView):
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
        # Возвращаем ответ в API
        return Response({"message": message})
