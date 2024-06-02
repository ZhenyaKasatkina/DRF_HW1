# Generated by Django 5.0.6 on 2024-05-28 15:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150, verbose_name="Название")),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="preview/",
                        verbose_name="превью",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="описание"),
                ),
            ],
            options={
                "verbose_name": "курс",
                "verbose_name_plural": "курсы",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150, verbose_name="Название")),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="preview/",
                        verbose_name="превью",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="описание"),
                ),
                (
                    "video",
                    models.URLField(
                        blank=True, null=True, verbose_name="ссылка на видео"
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lesson",
                        to="education.course",
                        verbose_name="курс",
                    ),
                ),
            ],
            options={
                "verbose_name": "урок",
                "verbose_name_plural": "уроки",
            },
        ),
    ]