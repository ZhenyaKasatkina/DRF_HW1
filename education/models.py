from django.db import models

from config.settings import AUTH_USER_MODEL

User = AUTH_USER_MODEL

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    """Курс"""

    name = models.CharField(max_length=150, verbose_name="Название")
    preview = models.ImageField(upload_to="preview/", verbose_name="превью", **NULLABLE)
    description = models.TextField(verbose_name="описание", **NULLABLE)
    url = models.URLField(verbose_name="ссылка на материал", **NULLABLE)
    owner = models.ForeignKey(
        User,
        related_name="course",
        verbose_name="владелец",
        on_delete=models.SET_NULL,
        **NULLABLE,
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="стоимость курса", **NULLABLE
    )
    last_update = models.DateTimeField(
        verbose_name="Дата последнего обновления", **NULLABLE
    )

    def __str__(self):
        # Строковое отображение объекта
        return f"Курс: {self.name}."

    class Meta:
        verbose_name = "курс"  # Настройка для наименования одного объекта
        verbose_name_plural = "курсы"  # Настройка для наименования набора объектов


class Lesson(models.Model):
    """Урок"""

    name = models.CharField(max_length=150, verbose_name="Название")
    preview = models.ImageField(upload_to="preview/", verbose_name="превью", **NULLABLE)
    description = models.TextField(verbose_name="описание", **NULLABLE)
    url = models.URLField(verbose_name="ссылка на видео", **NULLABLE)
    course = models.ForeignKey(
        Course, related_name="lesson", on_delete=models.CASCADE, verbose_name="курс"
    )
    owner = models.ForeignKey(
        User,
        related_name="lesson",
        verbose_name="владелец",
        on_delete=models.SET_NULL,
        **NULLABLE,
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="стоимость урока", **NULLABLE
    )
    last_update = models.DateTimeField(
        verbose_name="Дата последнего обновления", **NULLABLE
    )

    def __str__(self):
        # Строковое отображение объекта
        return f"Урок: {self.name}."

    class Meta:
        verbose_name = "урок"  # Настройка для наименования одного объекта
        verbose_name_plural = "уроки"  # Настройка для наименования набора объектов


class Subscription(models.Model):
    """Подписка"""

    is_active = models.BooleanField(verbose_name="наличие подписки")
    course = models.ForeignKey(
        Course,
        related_name="subscription",
        on_delete=models.CASCADE,
        verbose_name="курс",
    )
    owner = models.ForeignKey(
        User,
        related_name="subscription",
        verbose_name="владелец",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        # Строковое отображение объекта
        return f"Подписка на {self.pk}."

    class Meta:
        verbose_name = "подписка"  # Настройка для наименования одного объекта
        verbose_name_plural = "подписки"  # Настройка для наименования набора объектов
