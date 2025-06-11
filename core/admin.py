from django.contrib import admin

from .models import (
    Trainer,
    WorkoutType,
    WorkoutSchedule,
    SubscriptionPlan,
    UserSubscription,
    WorkoutBooking,
    WorkoutSession,
    PaymentHistory
)


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkoutType)
class WorkoutTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkoutSchedule)
class WorkoutScheduleAdmin(admin.ModelAdmin):
    pass


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkoutBooking)
class WorkoutBookingAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    pass
