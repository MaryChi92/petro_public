# Generated by Django 4.2.5 on 2024-02-07 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_studentcourse_is_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcourse',
            name='lessons_starts_on',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата старта потока'),
        ),
    ]