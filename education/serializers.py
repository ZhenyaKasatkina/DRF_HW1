from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from education.models import Course, Lesson, Subscription
from education.validators import validate_url


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.URLField(validators=[validate_url], read_only=True)

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = SerializerMethodField()
    subscription = SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)
    url = serializers.URLField(validators=[validate_url], read_only=True)

    def get_count_lessons(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_subscription(self, course):
        if Subscription.objects.filter(is_active=True, course=course):
            return f"На {course.name} Вы подписаны"
        else:
            return f"На {course.name} Вы не подписаны"

    class Meta:
        model = Course
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = "__all__"
