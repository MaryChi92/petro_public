# Generated by Django 4.2.5 on 2023-12-18 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_lesson_description_homework'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video_file',
            field=models.URLField(blank=True, null=True, verbose_name='Видео в записи'),
        ),
    ]
