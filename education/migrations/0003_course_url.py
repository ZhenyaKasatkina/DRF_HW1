# Generated by Django 5.0.6 on 2024-06-12 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("education", "0002_course_owner_lesson_owner"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="url",
            field=models.URLField(
                blank=True, null=True, verbose_name="ссылка на материал"
            ),
        ),
    ]
