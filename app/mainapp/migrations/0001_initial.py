# Generated by Django 4.2.5 on 2023-12-13 13:46

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150, verbose_name='Польза')),
                ('image', models.ImageField(blank=True, null=True, upload_to='benefit_img/', verbose_name='Изображение')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удален')),
            ],
            options={
                'verbose_name': 'Польза',
                'verbose_name_plural': 'Польза',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150, verbose_name='Название курса')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True, verbose_name='URL')),
                ('category', models.CharField(choices=[('ART', 'ИСКУССТВО'), ('DESIGN', 'ДИЗАЙН'), ('SOFT_SKILLS', 'SOFT SKILLS')], max_length=11, verbose_name='Категория курса')),
                ('note', models.CharField(blank=True, max_length=200, verbose_name='Цель курса')),
                ('description', models.TextField(blank=True, verbose_name='Описание курса')),
                ('price', models.IntegerField(verbose_name='Стоимость курса')),
                ('image', models.ImageField(blank=True, null=True, upload_to='сourses_images', verbose_name='Изображение')),
                ('duration', models.CharField(blank=True, max_length=25, verbose_name='Продолжительность курса')),
                ('age_group', models.CharField(blank=True, max_length=25, verbose_name='Возрастная группа')),
                ('tools', models.TextField(blank=True, verbose_name='Необходимые материалы и инструменты для курса')),
                ('filling', models.TextField(blank=True, verbose_name='Наполнение курса')),
                ('question_lessons_features', models.TextField(verbose_name='Как проходят занятия на курсе?')),
                ('question_access_duration', models.TextField(verbose_name='На сколько по времени доступен курс?')),
                ('question_homework', models.TextField(verbose_name='Что насчет домашнего задания?')),
                ('question_joining_telegram_chat', models.TextField(verbose_name='Что я получу, вступив в телеграм-канал курса?')),
                ('question_paid_no_access', models.TextField(verbose_name='Я оплатил и не получил доступ к курсу')),
                ('telegram_channel_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на тг-канал')),
                ('on_sale', models.BooleanField(default=False, verbose_name='В продаже')),
                ('is_popular', models.BooleanField(default=False, verbose_name='Популярный')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удален')),
                ('benefits', models.ManyToManyField(related_name='courses', to='mainapp.benefit', verbose_name='Польза курса')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150, verbose_name='Название урока')),
                ('number', models.IntegerField(verbose_name='Номер урока')),
                ('type', models.CharField(choices=[('Online lesson', 'Онлайн-урок'), ('Video lesson', 'Видеоурок')], max_length=13, verbose_name='Тип урока')),
                ('lesson_goal', models.TextField(blank=True, verbose_name='Цель урока')),
                ('new_skill', models.TextField(blank=True, verbose_name='Чему научится ребенок')),
                ('materials', models.TextField(blank=True, verbose_name='Что нужно для урока')),
                ('image', models.ImageField(blank=True, null=True, upload_to='lessons_img/', verbose_name='Изображение')),
                ('description', models.TextField(blank=True, verbose_name='Описание урока')),
                ('video_file', models.FileField(blank=True, null=True, upload_to='lessons_videos/', verbose_name='Видео в записи')),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='lessons_files/', verbose_name='Дополнительный файл')),
                ('link', models.CharField(blank=True, max_length=150, verbose_name='Ссылка на онлайн-урок')),
                ('lesson_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата онлайн-урока')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удален')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='mainapp.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
                'ordering': ['course', 'number'],
            },
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=150, verbose_name='Имя ментора')),
                ('last_name', models.CharField(max_length=150, verbose_name='Фамилия ментора')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='mentor', verbose_name='Фото ментора')),
                ('status', models.CharField(max_length=255, verbose_name='Статус')),
                ('quote', models.TextField(verbose_name='Высказывание')),
                ('experience', models.TextField(verbose_name='Образование и Опыт')),
                ('credo', models.TextField(verbose_name='Кредо и Сильные стороны')),
                ('approach', models.TextField(verbose_name='Подход в обучении')),
            ],
            options={
                'verbose_name': 'Ментор',
                'verbose_name_plural': 'Менторы',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Preparation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=50, verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Уровень подготовки',
                'verbose_name_plural': 'Уровни подготовки',
            },
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=50, unique=True, verbose_name='Промокод')),
                ('discount', models.IntegerField(verbose_name='Скидка в %')),
                ('for_students', models.BooleanField(verbose_name='Для зарегистрированных пользователей')),
                ('for_subscribers', models.BooleanField(verbose_name='Для подписчиков на новости')),
                ('for_user', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Промокод для конкретного юзера (указать email)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('expiration_date', models.DateTimeField(verbose_name='Действует до')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удален')),
            ],
            options={
                'verbose_name': 'Промокод',
                'verbose_name_plural': 'Промокоды',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator], verbose_name='Адрес электронной почты')),
            ],
            options={
                'verbose_name': 'Подписчик на новостную рассылку',
                'verbose_name_plural': 'Подписчики на новостную рассылку',
                'ordering': ['first_name', 'email'],
            },
        ),
        migrations.CreateModel(
            name='Talent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Талант')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='talent_img/', verbose_name='Изображение')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удален')),
            ],
            options={
                'verbose_name': 'Талант',
                'verbose_name_plural': 'Таланты',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='StudentsWork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('image', models.ImageField(blank=True, null=True, upload_to='students_best_pics_files/', verbose_name='Изображение')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='studentworks', to=settings.AUTH_USER_MODEL, verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'Работа студента',
                'verbose_name_plural': 'Работы студентов',
            },
        ),
        migrations.CreateModel(
            name='StudentsHomework',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('image1', models.ImageField(blank=True, null=True, upload_to='homework_files/', verbose_name='Изображение')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='homework_files/', verbose_name='Изображение')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='homework_files/', verbose_name='Изображение')),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='homework_files/', verbose_name='Дополнительный файл')),
                ('comment_student', models.TextField(blank=True, verbose_name='Комментарий студента')),
                ('comment_mentor', models.TextField(blank=True, verbose_name='Комментарий ментора')),
                ('lesson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='studenthomework', to='mainapp.lesson', verbose_name='Урок')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studenthomework', to=settings.AUTH_USER_MODEL, verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'Домашнее задание студента',
                'verbose_name_plural': 'Домашние задания студентов',
            },
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('lesson_number', models.IntegerField(default=1, verbose_name='Номер доступного урока')),
                ('note', models.TextField(blank=True, verbose_name='Примечания по студенту на этом курсе')),
                ('order_number', models.CharField(max_length=8, unique=True, verbose_name='Номер заказа')),
                ('purchase_price', models.IntegerField(blank=True, null=True, verbose_name='Цена покупки')),
                ('bank', models.CharField(blank=True, max_length=150, verbose_name='Банк')),
                ('order_id_alfa', models.CharField(verbose_name='id заказа в системе банка')),
                ('paid', models.BooleanField(default=False, verbose_name='Оплачен')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удален')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='mainapp.course', verbose_name='Курс')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL, verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'Курс студента',
                'verbose_name_plural': 'Курс студента',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='course',
            name='mentors',
            field=models.ManyToManyField(related_name='courses', to='mainapp.mentor', verbose_name='Менторы'),
        ),
        migrations.AddField(
            model_name='course',
            name='preparation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='mainapp.preparation', verbose_name='Уровень подготовки'),
        ),
        migrations.AddField(
            model_name='course',
            name='talents',
            field=models.ManyToManyField(related_name='courses', to='mainapp.talent', verbose_name='Навыки, которые дает курс'),
        ),
    ]