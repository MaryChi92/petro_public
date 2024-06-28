from pathlib import Path

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from time import time
from uuid import uuid4
from phonenumber_field.modelfields import PhoneNumberField

from mainapp.models import Course, Lesson


class StudentUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, first_name, email, phone_number, password=None):
        """
        Creates and saves a User with the given first_name, email, phone_number and password.
        """
        if not email:
            raise ValueError('Необходимо задать адрес электронной почты')

        user = self.model(
            first_name=first_name,
            email=self.normalize_email(email),
            phone_number=phone_number
        )
        user.set_password(password)
        user.is_active = False
        user.activation_key_expires += timedelta(days=2)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, email, phone_number, password=None):
        """
        Creates and saves a SuperUser with the given first_name, email, phone_number and password.
        """
        user = self.create_user(
            first_name=first_name,
            email=email,
            phone_number=phone_number,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


def users_avatars_path(instance, filename):
    num = int(time() * 1000)
    suffix = Path(filename).suffix
    return f"avatars/{num}{suffix}"


class StudentUser(AbstractUser):
    id = models.UUIDField(default=uuid4, primary_key=True)
    username = None
    first_name = models.CharField(verbose_name="Имя", max_length=30, blank=False)
    email = models.EmailField(verbose_name="Адрес электронной почты", unique=True, blank=False,
                              validators=[EmailValidator])
    phone_number = PhoneNumberField(verbose_name="Номер телефона", max_length=12, unique=True, blank=False)
    age = models.IntegerField(verbose_name="Возраст", blank=True, null=True)
    bio = models.TextField(verbose_name="Биография", blank=True)
    photo = models.ImageField(verbose_name="Фото", blank=True, null=True, upload_to=users_avatars_path)
    courses = models.ManyToManyField(Course, verbose_name="Курсы", blank=True, related_name="students")
    free_lessons = models.ManyToManyField(Lesson, verbose_name="Бесплатные уроки", blank=True, related_name="students")
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    deleted = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=now)

    objects = StudentUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone_number']

    def __str__(self):
        return f'{self.first_name} {self.email}'

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

    @staticmethod
    def get_student(email):
        return StudentUser.objects.filter(email=email).first()

    def get_students_free_lessons(self):
        return self.free_lessons
