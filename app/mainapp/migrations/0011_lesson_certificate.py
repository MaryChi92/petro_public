# Generated by Django 4.2.5 on 2024-02-19 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_studentcourse_lessons_starts_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='certificate',
            field=models.ImageField(blank=True, null=True, upload_to='lessons_certificates/', verbose_name='Сертификат'),
        ),
    ]