from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import ClientDetail


@receiver(post_save, sender=User)
def create_client_detail(sender, instance, created, **kwargs):
    if created:
        ClientDetail.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_client_detail(sender, instance, **kwargs):
    if hasattr(instance, 'client_detail'):
        instance.client_detail.save()
