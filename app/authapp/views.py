from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView


from random import random
from hashlib import sha1
import json
from requests.exceptions import HTTPError

from authapp.models import StudentUser
from authapp.forms import ChangePasswordForm
from django_conf import settings


User = get_user_model()


def login_view(request):
    # получаем из данных запроса POST отправленные через форму данные
    email = request.POST.get("email")
    password = request.POST.get("password")
    user = authenticate(request, email=email, password=password)
    if user is not None:
        if user.is_active:
            try:
                login(request, user)
                return redirect('self-account')
            except HTTPError as e:
                print('haaaaaaaaaaaaaaaa')
                print(e)
                return redirect('index')
        else:
            messages.error(request, 'Ваш аккаунт неактивен')
    else:
        messages.error(request, 'Вы неверно указали почту или пароль')
        # return HttpResponse(f"<h2>Email: {email}  Password: {password}</h2>")
        return redirect(request.META.get('HTTP_REFERER'))


def logout_view(request):
    logout(request)
    if 'self-page' in request.META.get('HTTP_REFERER') or 'self-account' in request.META.get('HTTP_REFERER'):
        return redirect('index')
    return redirect(request.META.get('HTTP_REFERER'))


def register_view(request):
    first_name = request.POST.get("name")
    email = request.POST.get("email")
    phone_number = request.POST.get("phone")
    password = request.POST.get("password")

    if not all(
        [
            first_name,
            email,
            phone_number,
            password
        ]
    ):
        messages.error(request, message='Форма регистрации заполнена некорректно')
        return redirect(request.META.get('HTTP_REFERER'))

    student = StudentUser.objects.filter(Q(email=email) | Q(phone_number=phone_number)).first()
    if not student:
        user = StudentUser.objects.create_user(first_name, email, phone_number, password)
        activation_link = create_activation_link(user)
        return send_mail_to_activate_user(user, activation_link, request)
    elif student.email == email:
        messages.error(request, message=f'Пользователь с таким email: {email} уже существует')
    elif student.phone_number == phone_number:
        messages.error(request, message=f'Пользователь с таким номером телефона: {phone_number} уже существует')

    return redirect(request.META.get('HTTP_REFERER'))


def create_activation_link(user):
    salt = sha1(str(random()).encode('utf-8')).hexdigest()[:6]
    user.activation_key = sha1((user.email + salt).encode('utf-8')).hexdigest()
    user.save()

    activation_link = reverse_lazy('authapp:confirm_email', kwargs={'email': user.email,
                                                                    'activation_key': user.activation_key})
    return activation_link


def send_mail_to_activate_user(user, activation_link, request):
    unisender_template = {"template_id": "c78b69b8-9028-11ee-b48b-62f7586ed56e",
                          "global_substitutions": {"URL": f"{settings.DOMAIN_NAME}{activation_link}"}}
    unisender_template_json = json.dumps(unisender_template)
    # Ссылка действительна до {user.activation_key_expires}',

    email = EmailMessage(
        subject="Подтверждение адреса электронной почты на сайте Петроглиф",
        to=[user.email],
        headers={'X-UNISENDER-GO': unisender_template_json},
    )
    email.send()

    messages.info(request, f'На ваш адрес электронной почты было отправлено письмо с подтверждением.\n'
                           f'Пожалуйста, проверьте свою электронную почту и нажмите на ссылку подтверждения, чтобы завершить регистрацию.\n'
                           f'Если письмо не пришло, проверьте папку спам.')
    return redirect(request.META.get('HTTP_REFERER'))


class UserConfirmEmailView(View):
    @staticmethod
    def get(request, email, activation_key):
        user = StudentUser.objects.filter(email=email).first()

        if user is not None and user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            login(request, user, backend='authapp.auth.EmailAuthBackend')
            messages.success(request, 'Ваш адрес электронной почты успешно подтвержден. Спасибо за регистрацию!')
            return redirect('self-account')
        else:
            messages.error(request, 'Ссылка для подтверждения по электронной почте недействительна или срок ее действия'
                                    'истек. Пожалуйста, зарегистрируйтесь снова. Либо попробуйте войти в личный кабинет.')
            return redirect('index')


class ChangePasswordView(PasswordChangeView):
    template_name = "mainapp/self_page.html"


def password_change_done_view(request):
    messages.info(request, message='Ваш пароль был успешно изменен.')
    return redirect('self-page-settings')


def password_reset_done_view(request):
    messages.info(request, message='На вашу почту отправлено письмо с инструкцией по  восстановлению  пароля! На всякий случай, проверьте спам.')
    return redirect(request.META.get('HTTP_REFERER'))


def password_reset_complete_view(request):
    messages.info(request, message='Ваш пароль был сохранен. Теперь вы можете войти.')
    return redirect('index')


class StudentPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "mainapp/reset_password.html"


def csrf_failure(request, reason=""):
    """Default view for CSRF failures."""
    return render(
        request,
        "mainapp/403_csrf.html",
        {"reason": reason},
        status=403,
    )
