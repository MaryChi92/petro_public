# Generated by Django 4.2.5 on 2023-12-19 10:35

import authapp.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authapp", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentuser",
            name="photo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=authapp.models.users_avatars_path,
                verbose_name="Фото",
            ),
        ),
    ]
