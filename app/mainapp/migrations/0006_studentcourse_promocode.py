# Generated by Django 4.2.5 on 2023-12-19 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_lesson_video_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcourse',
            name='promocode',
            field=models.CharField(blank=True, max_length=50, verbose_name='Примененный промокод'),
        ),
    ]