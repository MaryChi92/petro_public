# Generated by Django 4.2.5 on 2024-02-21 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_alter_lesson_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='type',
            field=models.CharField(choices=[('Онлайн-урок', 'Онлайн-урок'), ('Видеоурок', 'Видеоурок')], max_length=13, verbose_name='Тип урока'),
        ),
    ]
