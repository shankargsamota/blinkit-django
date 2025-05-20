from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from account.models import User


@shared_task
def send_email_task(subject, message, recipient_list):
    print("[TASK STARTED] Sending email...")
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='samota.shankar.2803@gmail.com',
            recipient_list=recipient_list,
            fail_silently=False,
        )
        print("[TASK COMPLETED] Email sent.")
    except Exception as e:
        print(f"[TASK ERROR] Failed to send email: {e}")


@shared_task
def process_user_details():
    today = now().date()
    users = User.objects.all()
    for user in users:
        print(user)


