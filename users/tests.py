from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from education.models import Course, Lesson
from users.models import Payment, User


class UsersTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="new_email@list.ru", password="123q")
        self.course = Course.objects.create(name="программирование", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="тестирование", course=self.course, owner=self.user
        )
        self.payment = Payment.objects.create(
            user=self.user,
            date="2024-06-02T00:00:00+03:00",
            course=self.course,
            price="12000.01",
            way="перевод",
        )
        self.client.force_authenticate(user=self.user)

    def test_login(self):
        """Проверка login"""

        url = reverse("users:login")
        data = {"email": "em@list.ru", "password": "1q"}
        self.user = User.objects.create(
            email=data.get("email"), password=make_password(data.get("password"))
        )
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {"email": "123asd", "password": "12qwe"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve(self):
        """Проверка детализации"""

        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), self.user.email)

        url = reverse("users:user-detail", args=(101,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(data.get("email"), None)

    def test_create(self):
        """Проверка создания пользователя"""

        url = reverse("users:user-list")
        data = {"email": "create@list.ru", "password": "qwe"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

        data = {"email": "create@list.ru"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.all().count(), 2)

    def test_update(self):
        """Проверка изменения пользователя"""

        url = reverse("users:user-detail", args=(self.user.pk,))
        data = {"email": "create@list.ru", "password": ""}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"password": ["This field may not be blank."]}
        )

    def test_delete(self):
        """Проверка удаления пользователя"""

        url = reverse("users:user-detail", args=(not self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(User.objects.all().count(), 1)

        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)

    def test_list(self):
        """Проверка списка пользователей"""

        url = reverse("users:user-list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {"id": self.user.pk, "email": self.user.email, "phone": None, "town": None}
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_list_payment(self):
        """Проверка списка платежей"""

        url = reverse("users:payment_list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.payment.pk,
                "date": self.payment.date,
                "price": self.payment.price,
                "way": self.payment.way,
                "user": self.user.pk,
                "course": self.course.pk,
                "lesson": None,
                "is_paid": self.payment.is_paid,
                "link": self.payment.link,
                "session_id": self.payment.session_id,
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
