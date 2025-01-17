"""
URL configuration for django_conf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from mainapp import views as main_views
from authapp import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.index, name='index'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('register/', auth_views.register_view, name='register'),
    path('reset-password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('password-reset/done/', auth_views.password_reset_done_view, name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.StudentPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.password_reset_complete_view, name='password_reset_complete'),

    path('subscribe/', main_views.subscribe_view),
    path('courses/<str:slug>/', main_views.view_course, name='course'),
    path('courses-all/', main_views.view_courses_all, name='courses_all'),
    path('buy-course/<str:slug>/', main_views.user_buy_course_view, name='buy_course'),
    path('apply-promo/<str:slug>/', main_views.apply_promo, name='apply_promo'),
    path('payment-success/', main_views.payment_success_view, name='payment_success'),
    path('payment-fail/', main_views.payment_fail_view, name='payment_fail'),
    path('free-lessons/', main_views.get_all_free_lessons_view, name='free_lessons'),
    path('add-free-lesson/<str:lesson_id>/', main_views.user_add_free_lesson_view, name='add_free_lesson'),

    path('self-page/', main_views.view_self_page, name='self-page'),
    path('self-page-info/', main_views.view_self_page_info, name='self-page-info'),
    path('self-page-settings/', auth_views.ChangePasswordView.as_view(), name='self-page-settings'),
    path('password-change-done/', auth_views.password_change_done_view, name='password_change_done'),
    path('self-account/', main_views.view_self_account, name='self-account'),
    path('self-account/course/<str:slug>/', main_views.view_self_account_course, name='self-account-course'),
    path('self-account/free-lesson/<str:lesson_id>/', main_views.view_self_account_free_lesson, name='self-account-free-lesson'),
    path('self-account/lesson/<str:slug>/<int:number>/<int:hw>/', main_views.view_self_account_course_lesson, name='self-account-lesson'),
    path('self-account/lesson_zero/<str:slug>/', main_views.view_self_account_course_lesson_zero, name='self-account-lesson-zero'),
    path('self-account/lesson_delete_img/<str:slug>/<int:number>/<str:path>/<str:name>/', main_views.view_delete_homework_files, name='self-account-lesson-delete-img'),
    # path('courses/', include('mainapp.urls', namespace='courses')),
    path('authapp/', include('authapp.urls', namespace='authapp')),
    path('filter-courses/', main_views.filter_courses, name='filter_courses'),

    path('documents/<str:name>/', main_views.get_document, name='documents'),

    path("cookies_consent/", include("cookie_consent.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
