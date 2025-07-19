import eventlet
import smtplib
from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponse, BadHeaderError
from config.settings import EMAIL_HOST_USER
from edu_materials.models import Course
from .models import Subscription, User


@shared_task
def send_course_update(course_id):
    """Отправляет сообщение об обновлении материалов курса тем, кто подписан на этот курс."""

    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course_id)
    recipient_list = [subscription.owner.email for subscription in subscriptions]

    try:
        send_mail(
            subject='В курсе произошли изменения',
            message=f'В курсе "{course.name}" произошли изменения',
            from_email=EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=True
        )
    except smtplib.SMTPException:
        raise smtplib.SMTPException


@shared_task
def blocking_users():
    """Блокирует пользователей, которые бездействуют более 30 дней."""

    users = User.objects.filter(is_active=True)
    today = timezone.now()
    was_blocked = [] # будем собирать сюда email заблокированных
    for user in users:
        if user.last_login:
            if today - user.last_login > timedelta(days=30):
                was_blocked.append(user.email)
                user.is_active = False
                user.save()
        return was_blocked

    if was_blocked:
        recipient_list = [user.email for user in User.objects.filter(groups__name="Администратор")]
        try:
            send_mail(
                subject='Блокировка неактивных пользователей',
                message=f"Пользователи: {', '.join(was_blocked)} заблокированы.",
                from_email=EMAIL_HOST_USER,
                recipient_list=recipient_list,
                fail_silently=True
            )
        except BadHeaderError:
            return HttpResponse('Обнаружена ошибка')
        except smtplib.SMTPException:
            raise smtplib.SMTPException
        print(f"Пользователи:{', '.join(was_blocked)} заблокированы.")


@shared_task
def test_add():
    print("hello")
