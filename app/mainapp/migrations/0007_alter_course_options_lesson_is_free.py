# Generated by Django 4.2.5 on 2024-02-05 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_studentcourse_promocode'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['-on_sale', 'title'], 'verbose_name': 'Курс', 'verbose_name_plural': 'Курсы'},
        ),
        migrations.AddField(
            model_name='lesson',
            name='is_free',
            field=models.BooleanField(default=False, verbose_name='Бесплатный'),
        ),
    ]