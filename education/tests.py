from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from education.models import Course, Lesson, Subscription
from users.models import User


class EducationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="new_email@list.ru")
        self.course = Course.objects.create(name="программирование", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="тестирование", course=self.course, owner=self.user
        )
        self.sub = Subscription.objects.create(
            is_active=True, owner=self.user, course=self.course
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Проверка детализации"""

        url = reverse("education:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(data)
        self.assertEqual(data.get("name"), self.lesson.name)

        url = reverse("education:lesson_retrieve", args=(101,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_lesson_create(self):
        """Проверка создания урока"""

        url = reverse("education:lesson_create")

        data = {"name": "python", "course": 55}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.all().count(), 1)

        data = {"name": "python", "course": self.course.pk, "owner": not self.user}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.all().count(), 1)

        data = {"name": "python", "course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Проверка изменения урока"""

        url = reverse("education:lesson_update", args=(self.lesson.pk,))
        data = {"price": 1000.002, "course": self.course.pk}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.lesson.price, None)

        data = {"name": "jw", "course": self.course.pk}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), data["name"])

    def test_lesson_delete(self):
        """Проверка удаления урока"""

        url = reverse("education:lesson_delete", args=(101,))
        response = self.client.delete(url)
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Lesson.objects.all().count(), 1)

        url = reverse("education:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Проверка списка уроков"""

        url = reverse("education:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video": None,
                    "name": self.lesson.name,
                    "preview": None,
                    "description": None,
                    "course": self.course.pk,
                    "price": None,
                    "owner": self.user.pk,
                }
            ],
        }
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_change_sub_activity(self):
        """Изменение активности подписок пользователя"""

        url = reverse("education:sub")
        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "подписка удалена"})

        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "подписка добавлена"})

        data = {"course": 101}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(), {"detail": "No Course matches the given query."}
        )

    def test_course_retrieve(self):
        """Проверка детализации курса"""

        url = reverse("education:course-detail", args=(self.course.pk,))
        # print(url)
        response = self.client.get(url)
        data = response.json()
        # print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(data)
        self.assertEqual(data.get("name"), self.course.name)

        url = reverse("education:course-detail", args=(101,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(data, {"detail": "No Course matches the given query."})

    def test_course_create(self):
        """Проверка создания курса"""

        url = reverse("education:course-list")
        # print(url)
        data = {}
        response = self.client.post(url, data)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Course.objects.all().count(), 1)

        data = {"name": "иностранных языков"}
        response = self.client.post(url, data)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_update(self):
        """Проверка изменения курса"""

        url = reverse("education:course-detail", args=(self.course.pk,))
        data = {"name": "иностранных языков"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), data["name"])

        data = {"url": "my@list.ru"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(None, self.course.url)

    def test_delete(self):
        """Проверка удаления курса"""

        url = reverse("education:course-detail", args=(None,))
        response = self.client.delete(url)
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Course.objects.all().count(), 1)

        url = reverse("education:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_list(self):
        """Проверка списка курсов"""

        url = reverse("education:course-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "count_lessons": Lesson.objects.filter(
                        course=self.course.pk
                    ).count(),
                    "subscription": "На программирование Вы подписаны",
                    "lesson": [
                        {
                            "id": self.lesson.pk,
                            "video": None,
                            "name": self.lesson.name,
                            "preview": None,
                            "description": None,
                            "course": self.course.pk,
                            "owner": self.course.owner.pk,
                            "price": None,
                        },
                    ],
                    "url": None,
                    "name": self.course.name,
                    "preview": None,
                    "description": None,
                    "owner": self.course.owner.pk,
                    "price": None,
                },
            ],
        }
        # print(data)
        # print(result)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
