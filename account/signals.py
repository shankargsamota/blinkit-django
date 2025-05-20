# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.core.mail import send_mail
from vendor.models import Vendor

@receiver(post_save, sender=User)
def create_vendor_for_vendor_users(sender, instance, created, **kwargs):
    if created: 
        #send mail
        send_mail(
            subject='Your order has been placed!',
            message=f'Hi {instance.first_name},\n\nYour account for #{instance.email} has been created successfully!',
            from_email='samota.shankar.2803@gmail.com',
            recipient_list=[instance.email],
            fail_silently=False,
        )
    
        if instance.is_vendor:
            full_name = f"{instance.first_name} {instance.last_name}".strip()

            Vendor.objects.update_or_create(
                user=instance, 
                defaults={"name": full_name, "address": instance.location}
            )

