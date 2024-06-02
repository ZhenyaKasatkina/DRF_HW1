from django.contrib.auth.models import AbstractUser
from django.db import models

from education.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Пользователь"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    phone = models.CharField(max_length=35, verbose_name="телефон", **NULLABLE)
    town = models.CharField(max_length=100, verbose_name="город", **NULLABLE)
    avatar = models.ImageField(
        upload_to="users/avatars/", verbose_name="аватарка", **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        # Строковое отображение объекта
        return f"{self.email}"

    class Meta:
        verbose_name = "пользователь"  # Настройка для наименования одного объекта
        verbose_name_plural = (
            "пользователи"  # Настройка для наименования набора объектов
        )


class Payment(models.Model):
    """Платеж"""

    user = models.ForeignKey(
        User,
        related_name="payment",
        on_delete=models.CASCADE,
        verbose_name="пользователь",
    )
    date = models.DateField(verbose_name="Дата оплаты")
    course = models.ForeignKey(
        Course,
        related_name="payment",
        on_delete=models.CASCADE,
        verbose_name="оплаченный курс",
        **NULLABLE,
    )
    lesson = models.ForeignKey(
        Lesson,
        related_name="payment",
        on_delete=models.CASCADE,
        verbose_name="оплаченный урок",
        **NULLABLE,
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="сумма оплаты"
    )
    CASH = "наличные"
    TRANSFER = "перевод"
    WAY = {
        CASH: "наличные",
        TRANSFER: "перевод",
    }
    way = models.CharField(
        choices=WAY, max_length=15, verbose_name="Способ оплаты", default=CASH
    )

    def __str__(self):
        # Строковое отображение объекта
        return (
            f"{[self.course if self.course else self.lesson]}: сумма платежа {self.price}, дата {self.date}, "
            f"плательщик {self.user}, способ оплаты {self.way}"
        )

    class Meta:
        verbose_name = "платеж"  # Настройка для наименования одного объекта
        verbose_name_plural = "платежи"  # Настройка для наименования набора объектов
