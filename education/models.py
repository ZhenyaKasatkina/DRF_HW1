from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    """Курс"""

    name = models.CharField(max_length=150, verbose_name="Название")
    preview = models.ImageField(upload_to="preview/", verbose_name="превью", **NULLABLE)
    description = models.TextField(verbose_name="описание", **NULLABLE)

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
    video = models.URLField(verbose_name="ссылка на видео", **NULLABLE)
    course = models.ForeignKey(
        Course, related_name="lesson", on_delete=models.CASCADE, verbose_name="курс"
    )

    def __str__(self):
        # Строковое отображение объекта
        return f"Урок: {self.name}."

    class Meta:
        verbose_name = "урок"  # Настройка для наименования одного объекта
        verbose_name_plural = "уроки"  # Настройка для наименования набора объектов
