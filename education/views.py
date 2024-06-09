from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from education.models import Course, Lesson
from education.permissions import IsModerator, IsOwner
from education.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (
                IsAuthenticated,
                ~IsModerator,
            )
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                IsOwner,
                ~IsModerator,
            )
        elif self.action in ["update", "partial_update", "retrieve", "list"]:
            self.permission_classes = (
                IsAuthenticated,
                IsModerator | IsOwner,
            )
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
    # queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )

    def get_queryset(self, *args, **kwargs):
        if self.request.user.groups.filter(name="moderator").exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    # queryset = Lesson.objects.all()
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
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        ~IsModerator,
        IsOwner,
    )
