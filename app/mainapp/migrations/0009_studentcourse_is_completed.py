# Generated by Django 4.2.5 on 2024-02-06 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_course_access_days_course_group_is_full_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcourse',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='Завершен'),
        ),
    ]