import os

from django.db.models import Q
from django_conf import settings
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST

import json
import requests

import mainapp.models as mainapp_models
import authapp.models as authapp_models
from authapp import views as authapp_views
from mainapp.course_unisender_template_id import course_template_id


def index(request):
    #  Курсы за исключением первого, первые три
    courses = mainapp_models.Course.objects.exclude(Q(slug='first-course') | Q(deleted=True))[:3]
    for course in courses:
        course.description = course.description.split('\n')

    # courses.description.str.split('\n')
    # descriptions = courses.description.split('\n')
    # Первый курс выбирается по слагу first-course
    first_course = get_object_or_404(mainapp_models.Course, slug='first-course')
    descriptions_first = first_course.description.split('\n')

    context = {'courses': courses,
               # 'descriptions': descriptions,
               'first_course': first_course,
               'descriptions_first': descriptions_first,
               }
    return render(request, 'mainapp/index.html', context)


def subscribe_view(request):
    first_name = request.POST.get("name")
    email = request.POST.get("email")

    if not all(
        [
            first_name,
            email,
        ]
    ):
        messages.error(request, message='Почта или имя в форме подписки на новости заполнены с ошибкой, или не заполнены'
                                        'вовсе')
        return redirect(request.META.get('HTTP_REFERER'))

    subscriber = mainapp_models.Subscriber.objects.filter(email=email).first()
    if not subscriber:
        subscriber = mainapp_models.Subscriber.objects.create(first_name=first_name, email=email)
        return send_mail_to_subscribe_user(subscriber, request)
    elif subscriber.email == email:
        messages.error(request, message='Вы уже подписаны на новости нашей школы')

    return redirect(request.META.get('HTTP_REFERER'))


def send_mail_to_subscribe_user(user, request):
    unisender_template = {"template_id": "17a8cb5c-9029-11ee-ae52-6aed3ee1a8cd"}
    unisender_template_json = json.dumps(unisender_template)

    email = EmailMessage(
        subject="Приветствуем в сообществе онлайн-школы 'Петроглиф'",
        to=[user.email],
        headers={'X-UNISENDER-GO': unisender_template_json},
    )
    email.send()
    print(email)

    messages.info(request, f'Первое письмо с сюрпризом уже на вашей почте - бежим проверять!')
    return redirect('index')


def view_course(request, slug):
    ''' Страница вывода конкретного курса '''
    current_number = 1
    current_user = request.user

    course = get_object_or_404(mainapp_models.Course, slug=slug)
    descriptions = course.description.split('\n')

    if current_user.is_authenticated:
        # Необходимо установить current_number для текущего пользователя на этот курс (default 1)
        studentCourse = mainapp_models.StudentCourse.objects.filter(Q(user=current_user) & Q(course=course)).first()
        if studentCourse:
            current_number = studentCourse.lesson_number

    lessons = mainapp_models.Lesson.objects.filter(course=course)
    for lesson in lessons:
        lesson.material = lesson.materials.split('\n')
        # print(' /// context_course : ', lesson.material)
    # print('image: ', image)
    # for i in range(1,6):
    #     print(i)
    # print(' /// context_course : ', descriptions, ' |o|||o| ', course.filling.split('\n'))
    mentor = get_mentor_course(request, slug)

    context = {'course': course,
               'descriptions': descriptions,
               'course_tools': course.tools.split('\n'),
               'course_filling': course.filling.split('\n'),
               'lessons': lessons,
               'mentor': mentor,
               'current_number': current_number,
               }
    # print(' /// context_course : ', lesson.material)
    return render(request, 'mainapp/course.html', context)


def view_courses_all(request):
    #  Курсы за исключением первого, все
    courses = mainapp_models.Course.objects.exclude(Q(slug='first-course') | Q(deleted=True))
    for course in courses:
        course.description = course.description.split('\n')

    # Первый курс выбирается по слагу first-course
    # first_course = get_object_or_404(mainapp_models.Course, slug='first-course')
    # descriptions_first = first_course.description.split('\n')

    # Первый курс также необходимо приобретать!
    first_course = mainapp_models.Course.objects.filter(slug='first-course')
    descriptions_first = None
    if first_course:
        first_course = first_course[0]
        descriptions_first = first_course.description.split('\n')

    context = {'courses': courses,
               'first_course': first_course,
               'descriptions_first': descriptions_first,
               }
    return render(request, 'mainapp/courses_all.html', context)


def get_all_free_lessons_view(request):
    free_lessons = mainapp_models.Lesson.get_all_free_lessons()
    # desc = free_lessons.description.split('\n')

    context = {'free_lessons': free_lessons}
    return render(request, 'mainapp/free_lessons_all.html', context)


def user_add_free_lesson_view(request, lesson_id):
    current_user = request.user
    lesson = mainapp_models.Lesson.objects.filter(id=lesson_id).first()
    if current_user.is_authenticated:
        current_user.free_lessons.add(lesson)
        current_user.save()
        return redirect(f'self-account-free-lesson', lesson_id=lesson_id)
    else:
        messages.error(request, message='Чтобы просмотреть урок, необходимо авторизоваться')
        return redirect('free_lessons')


def get_mentor_course(request, slug):
    course = get_object_or_404(mainapp_models.Course, slug=slug)
    mentor = mainapp_models.Mentor.objects.filter(courses=course).first()
    return mentor


def view_self_page(request):
    current_user = request.user
    if current_user.is_authenticated:
        context = {'user': current_user,  }
        return render(request, 'mainapp/self_page.html', context)
    else:
        messages.error(request, 'Для входа в личный кабинет Вам необходимо авторизоваться')
        return redirect('index')


def view_self_page_info(request):
    current_user = request.user
    first_name = request.POST.get("name")
    age = request.POST.get("age")
    photo = request.FILES.get("photo")
    bio = request.POST.get("about")
    if first_name:
        current_user.first_name = first_name
    if age:
        current_user.age = age
    if bio:
        current_user.bio = bio
    if photo:
        if current_user.photo and os.path.exists(current_user.photo.path):
            os.remove(current_user.photo.path)
        current_user.photo = photo

    current_user.save()
    return redirect('self-page')


def view_self_account(request):
    current_user = request.user
    if current_user.is_authenticated:
        active_and_completed_courses_quantity = mainapp_models.StudentCourse.get_number_of_active_and_completed_courses(
            current_user)
        student_free_lessons = current_user.get_students_free_lessons()

        student_courses = mainapp_models.StudentCourse.objects.filter(user=current_user)

        context = {'student_courses': student_courses,
                   'active_courses_number': active_and_completed_courses_quantity[0],
                   'completed_courses_number': active_and_completed_courses_quantity[1],
                   'student_free_lessons': student_free_lessons,
                   }
        return render(request, 'mainapp/user_page.html', context)
    else:
        messages.error(request, 'Для входа в личный кабинет Вам необходимо авторизоваться')
        return redirect('index')


def user_buy_course_view(request, slug):
    current_user = request.user
    course = get_object_or_404(mainapp_models.Course, slug=slug)
    price_after_promo = request.POST.get('price')
    price = int(price_after_promo) if price_after_promo else course.price
    promocode = request.POST.get('promocode')

    if current_user.is_authenticated and current_user not in course.students.all() and course:
        # В таблице StudentCourse необходимо сделать соответствующую запись
        student_course = mainapp_models.StudentCourse.objects.filter(Q(user=current_user) & Q(course=course)).first()
        if not student_course:
            student_course = mainapp_models.StudentCourse()
            student_course.user = current_user
            student_course.course = course
            student_course.promocode = promocode
            student_course.save()
        if course.lessons_starts_on:
            student_course.lessons_starts_on = course.lessons_starts_on
            student_course.save()
        student_course.create_order_number()

        order_number = student_course.order_number

        if price == 0:
            get_course_for_free(request, student_course, current_user, course)
            return redirect('self-account')
        else:
            token = settings.ALFA_TOKEN
            amount = price * 100
            return_url = "https://petrocreative.ru/payment-success/"
            fail_url = "https://petrocreative.ru/payment-fail/"
            description = f'Курс "{course.title}"'
            email = current_user.email
            response = requests.get(f"https://payment.alfabank.ru/payment/rest/register.do?token={token}"
                                    f"&orderNumber={order_number}&amount={amount}&returnUrl={return_url}&failUrl={fail_url}"
                                    f"&description={description}&email={email}")
            try:
                order_id_alfa = response.json()["orderId"]
                print(order_id_alfa)
                student_course.order_id_alfa = order_id_alfa
                student_course.save()
                return redirect(response.json()["formUrl"])
            except:
                messages.error(request, message="Что-то пошло не так: попробуйте обновить страницу и попробовать снова."
                                                " Если ошибка повторяется, напишите нам на почту: help@petrocreative.ru")
                return redirect('course', slug=course.slug)
    else:
        messages.error(request, message="Для покупки курса вам необходимо авторизоваться, либо вы уже записаны на этот курс")
        return redirect('course', slug=course.slug)


def get_course_for_free(request, student_course, current_user, course):
    student_course.purchase_price = 0
    student_course.paid = True
    student_course.save()

    course.students.add(current_user)
    course.save()

    messages.success(request, message=f'Поздравляем! Вы записаны на курс {course.title}. '
                                      f'На почте вас ждёт приветственное  письмо!')

    send_mail_course_greetings(current_user, course)


def payment_success_view(request):
    order_id_alfa = request.GET.get('orderId')
    # В таблице StudentCourse необходимо сделать соответствующую запись
    student_course = mainapp_models.StudentCourse.objects.filter(order_id_alfa=order_id_alfa).first()
    student_course.paid = True
    student_course.save()

    current_user = request.user
    course = mainapp_models.Course.objects.filter(title=student_course.course.title).first()
    course.students.add(current_user)
    course.save()

    token = settings.ALFA_TOKEN
    response = requests.get(f"https://payment.alfabank.ru/payment/rest/getOrderStatusExtended.do?token={token}"
                            f"&orderId={order_id_alfa}")
    if response.json()["amount"] and response.json()["bankInfo"]["bankName"]:
        student_course.purchase_price = int(response.json().get("amount")) / 100
        student_course.bank = response.json().get("bankInfo").get("bankName")
        student_course.save()

    messages.success(request, message=f'Поздравляем! Вы записаны на курс {course.title}.'
                                      f'На почте вас ждёт приветственное  письмо!')

    send_mail_course_greetings(current_user, course)
    return redirect('self-account')


def send_mail_course_greetings(user, course):
    course_unisender_template_id = course_template_id.get(course.slug)
    unisender_template = {"template_id": course_unisender_template_id}
    unisender_template_json = json.dumps(unisender_template)

    email = EmailMessage(
        subject=f"Добро пожаловать на курс “{course.title}”",
        to=[user.email],
        headers={'X-UNISENDER-GO': unisender_template_json},
    )
    email.send()


def payment_fail_view(request):
    order_id_alfa = request.GET.get('orderId')
    student_course = mainapp_models.StudentCourse.objects.filter(order_id_alfa=order_id_alfa).first()
    course = student_course.course

    alfa_username = settings.ALFA_USERNAME
    alfa_password = settings.ALFA_PASSWORD
    response = requests.get(f"https://payment.alfabank.ru/payment/rest/getOrderStatusExtended.do?userName={alfa_username}"
                            f"&password={alfa_password}&orderId={order_id_alfa}")

    if response.json()["actionCodeDescription"]:
        if response.json()["actionCodeDescription"] in ("2028", "2025", "2024", "2023"):
            error_message = "Ошибка проведения платежа. Напишите на почту: help@petrocreaive.ru или в наш" \
                            "телеграмм- чат: @petroglifcreative"
        else:
            error_message = response.json()["actionCodeDescription"]
    else:
        error_message = "Ошибка проведения платежа. Попробуйте позднее."
    messages.error(request, message=error_message)
    return redirect('course', slug=course.slug)


from django.views.decorators.csrf import csrf_exempt
# @require_POST
@csrf_exempt
def apply_promo(request, slug):
    message_error = 'Вы ввели неверный промокод, либо срок действия промокода истек'

    promocode_text = request.POST.get("promocode")
    promocode = mainapp_models.PromoCode.objects.filter(text__iexact=promocode_text).first()
    course = get_object_or_404(mainapp_models.Course, slug=slug)
    current_user = request.user

    if promocode and not promocode.is_promocode_expired():
        if promocode.for_students and authapp_models.StudentUser.objects.filter(email=current_user.email).first():
            fp = course.get_final_price(promocode.discount)
            return JsonResponse({'final_price': fp})
        elif promocode.for_subscribers and mainapp_models.Subscriber.objects.filter(email=current_user.email).first():
            fp = course.get_final_price(promocode.discount)
            return JsonResponse({'final_price': fp})
        elif mainapp_models.PromoCode.is_promocode_for_user:
            fp = course.get_final_price(promocode.discount)
            return JsonResponse({'final_price': fp})
        else:
            return JsonResponse({'final_price': 'the same', 'message_error': message_error})
    else:
        return JsonResponse({'final_price': 'the same', 'message_error': message_error})


def view_self_account_course(request, slug):
    current_user = request.user
    if current_user.is_authenticated:
        course = current_user.courses.filter(slug=slug).first()
        if course:
            student_course = mainapp_models.StudentCourse.objects.filter(Q(user=current_user) & Q(course=course)).first()
            lessons = course.lessons.all().order_by('number')

            context = {'user': current_user,
                       'studentCourse': student_course,
                       'lessons': lessons,
                       'course': course,
                       }

            return render(request, 'mainapp/user_course.html', context)

        else:
            messages.error(request, 'У Вас нет такого курса!')
            return redirect('index')

    messages.error(request, 'Для данных действий необходимо авторизоваться')
    return redirect('index')


def view_self_account_free_lesson(request, lesson_id):
    current_user = request.user
    if current_user.is_authenticated:
        free_lesson = current_user.free_lessons.filter(id=lesson_id).first()

        if free_lesson:
            free_lesson_desc = free_lesson.description.split('\n')

            context = {
                "free_lesson": free_lesson,
                "free_lesson_desc": free_lesson_desc,
            }
            return render(request, 'mainapp/account_lesson_free.html', context)
        else:
            messages.error(request, 'У Вас нет такого урока! Выберите урок здесь')
            return redirect('free-lessons')
    else:
        messages.error(request, 'Для данных действий необходимо авторизоваться')
        return redirect('index')


def view_self_account_course_lesson(request, slug, number, hw):
    current_user = request.user
    if current_user.is_authenticated:
        course = current_user.courses.filter(slug=slug).first()

        if course:
            student_course = mainapp_models.StudentCourse.objects.filter(Q(user=current_user) & Q(course=course)).first()

            lesson = course.lessons.filter(number=number).first()
            lesson_desc = lesson.description.split('\n')
            lesson_desc_hw = lesson.description_homework.split('\n')
            lesson_count = course.lessons.count()

            btn_l = ''
            btn_r = ''
            if number == 1:
                if hw == 0:
                    btn_l = f'/self-account/lesson_zero/{slug}/'
                    btn_r = f'/self-account/lesson/{slug}/{number}/1/'
                else:
                    btn_l = f'/self-account/lesson/{slug}/{number}/0/'
                    btn_r = f'/self-account/lesson/{slug}/{number + 1}/0/'
            if number > 1 and number < lesson_count:
                if hw == 0:
                    btn_l = f'/self-account/lesson/{slug}/{number - 1}/1/'
                    btn_r = f'/self-account/lesson/{slug}/{number}/1/'
                else:
                    btn_l = f'/self-account/lesson/{slug}/{number}/0/'
                    btn_r = f'/self-account/lesson/{slug}/{number + 1}/0/'
            if number == lesson_count:
                if hw == 0:
                    btn_l = f'/self-account/lesson/{slug}/{number - 1}/1/'
                    btn_r = f'/self-account/lesson/{slug}/{number}/1/'
                else:
                    btn_l = f'/self-account/lesson/{slug}/{number}/0/'

            if request.method == 'POST':
                student_homework = save_homework_files(request, lesson, current_user)
            else:
                student_homework = mainapp_models.StudentsHomework.objects.filter(Q(lesson=lesson) & Q(student=current_user)).first()

            context = {'user': current_user,
                       'studentCourse': student_course,
                       'lesson': lesson,
                       'course': course,
                       'hw': hw,
                       'lesson_desc': lesson_desc,
                       'lesson_desc_hw': lesson_desc_hw,
                       'student_homework': student_homework,
                       'btn_l': btn_l,
                       'btn_r': btn_r,
                       }

            if student_course.lesson_number == number:
                student_course.lesson_number = number + 1
                student_course.save()
                if course.lessons.count() < student_course.lesson_number:
                    student_course.is_completed = True
                    student_course.save()

            return render(request, 'mainapp/user_lesson.html', context)

        else:
            messages.error(request, 'У Вас нет такого курса!')
            return redirect('index')

    messages.error(request, 'Для данных действий необходимо авторизоваться')
    return redirect('index')


def view_self_account_course_lesson_zero(request, slug):
    current_user = request.user
    if current_user.is_authenticated:
        course = current_user.courses.filter(slug=slug).first()

        if course:
            student_course = mainapp_models.StudentCourse.objects.filter(Q(user=current_user) & Q(course=course)).first()
            student_course = student_course

            course_desc = course.description.split('\n')

            context = {'user': current_user,
                       'studentCourse': student_course,
                       'course': course,
                       'course_desc': course_desc,
                       }

            return render(request, 'mainapp/user_lesson_zero.html', context)

        else:
            messages.error(request, 'У Вас нет такого курса!')
            return redirect('index')

    messages.error(request, 'Для данных действий необходимо авторизоваться')
    return redirect('index')


def save_homework_files(request, lesson, current_user):
    image1 = request.FILES.get("image1")
    image2 = request.FILES.get("image2")
    image3 = request.FILES.get("image3")
    pdf_file = request.FILES.get("pdf_file")
    comment_student = request.POST.get("comment_student")

    student_homework = mainapp_models.StudentsHomework.objects.filter(Q(lesson=lesson) | Q(student=current_user)).first()

    if not student_homework:
        student_homework = mainapp_models.StudentsHomework.objects.create(lesson=lesson, student=current_user,
                                                                          image1=image1, image2=image2, image3=image3,
                                                                          pdf_file=pdf_file,
                                                                          comment_student=comment_student)
    else:
        if image1 != None:
            student_homework.image1 = image1
        if image2 != None:
            student_homework.image2 = image2
        if image3 != None:
            student_homework.image3 = image3
        if pdf_file != None:
            student_homework.pdf_file = pdf_file
        student_homework.comment_student = comment_student
        student_homework.save()

    return student_homework


def view_delete_homework_files(request, slug, number, path, name):
    current_user = request.user
    if current_user.is_authenticated:
        course = current_user.courses.filter(slug=slug).first()
        if course:
            lesson = course.lessons.filter(number=number)
            student_homework = mainapp_models.StudentsHomework.objects.filter(Q(lesson=lesson) | Q(student=current_user)).first()
            fname = path + '/' + name

            if student_homework.image1 == fname:
                student_homework.image1.delete()
                student_homework.save()
            if student_homework.image2 == fname:
                student_homework.image2.delete()
                student_homework.save()
            if student_homework.image3 == fname:
                student_homework.image3.delete()
                student_homework.save()
            if student_homework.pdf_file == fname:
                student_homework.pdf_file.delete()
                student_homework.save()

            return redirect('self-account-lesson', slug=slug, number=number, hw=1)

        else:
            messages.error(request, 'У Вас нет такого курса!')
            return redirect('index')

    messages.error(request, 'Для данных действий необходимо авторизоваться')
    return redirect('index')


def filter_courses(request):
    key = request.GET['key']
    try:
        #Ищем сразу ключ в объектах Уровня подготовки
        preparation = mainapp_models.Preparation.objects.get(value=key)
        courses = mainapp_models.Course.objects.filter(preparation_id=preparation.id)
    except mainapp_models.Preparation.DoesNotExist:
        # Если не находим ищем в объектах курса по полю age_group
        courses = mainapp_models.Course.objects.filter(age_group=key)

    for course in courses:
        course.description = course.description.split('\n')
    context = {'courses': courses,
               'key': key}
    return render(request, 'mainapp/courses_filter.html', context)


def get_document(request, name):
    context = {
        'doc_name': f'{name}.pdf',
    }
    return render(request, 'mainapp/document.html', context)
