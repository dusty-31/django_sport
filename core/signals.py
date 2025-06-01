from datetime import date

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from core.models import ClientDetail, UserSubscription, WorkoutBooking, WorkoutSession


@receiver(post_save, sender=User)
def create_client_detail(sender, instance, created, **kwargs):
    if created:
        ClientDetail.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_client_detail(sender, instance, **kwargs):
    if hasattr(instance, 'client_detail'):
        instance.client_detail.save()


@receiver(pre_save, sender=UserSubscription)
def update_subscription_status(sender, instance, **kwargs):
    """Автоматично оновлює статус абонемента при збереженні"""
    if instance.end_date < date.today() and instance.status == 'active':
        instance.status = 'expired'


@receiver(post_save, sender=WorkoutBooking)
def create_workout_session_on_completion(sender, instance, **kwargs):
    """Створює сесію тренування після завершення запису"""
    if instance.status == 'completed' and not hasattr(instance, 'workoutsession'):
        WorkoutSession.objects.create(
            user=instance.user,
            booking=instance,
            workout_type=instance.schedule.workout_type,
            trainer=instance.schedule.trainer,
            date=instance.date,
            duration_minutes=instance.schedule.duration_minutes
        )
