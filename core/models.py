from datetime import timezone, timedelta, date

from django.db import models
from django.contrib.auth.models import User


class ClientDetail(models.Model):
    GENDER_CHOICES = [
        ('M', 'Чоловіча'),
        ('F', 'Жіноча'),
    ]

    GOAL_CHOICES = [
        ('lose_weight', 'Схуднення'),
        ('gain_muscle', 'Набір м\'язової маси'),
        ('fitness', 'Підтримка форми'),
        ('strength', 'Збільшення сили'),
        ('endurance', 'Витривалість'),
        ('rehabilitation', 'Реабілітація'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_detail')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата народження')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='Стать')
    height = models.PositiveIntegerField(null=True, blank=True, verbose_name='Зріст (см)')
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Вага (кг)')
    fitness_goal = models.CharField(max_length=20, choices=GOAL_CHOICES, blank=True, verbose_name='Фітнес ціль')
    experience_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Початківець'),
            ('intermediate', 'Середній'),
            ('advanced', 'Просунутий'),
        ],
        default='beginner',
        verbose_name='Рівень підготовки'
    )
    medical_conditions = models.TextField(blank=True, verbose_name='Медичні обмеження')
    emergency_contact = models.CharField(max_length=100, blank=True, verbose_name='Контакт для екстреного зв\'язку')
    emergency_phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон екстреного контакту')
    newsletter_subscription = models.BooleanField(default=True, verbose_name='Підписка на новини')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Client Detail'
        verbose_name_plural = 'Clients Details'

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} - Профіль'

    @property
    def age(self):
        if self.birth_date:
            from datetime import date
            today = date.today()
            return today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

    @property
    def bmi(self):
        if self.height and self.weight:
            height_m = self.height / 100
            return round(float(self.weight) / (height_m * height_m), 1)
        return None


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    specialization = models.CharField(max_length=100, verbose_name='Specialization')
    experience_years = models.PositiveIntegerField(verbose_name='Years of Experience')
    certifications = models.TextField(verbose_name='Certifications', help_text='List certifications separated by comma')
    bio = models.TextField(verbose_name='Biography', blank=True)
    photo = models.ImageField(upload_to='trainers/', blank=True, null=True, verbose_name='Photo')
    is_active = models.BooleanField(default=True, verbose_name='Active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Trainer'
        verbose_name_plural = 'Trainers'

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} - {self.specialization}'

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

    def get_certifications_list(self):
        return [cert.strip() for cert in self.certifications.split(',') if cert.strip()]


class WorkoutType(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(verbose_name='Description')
    color_class = models.CharField(max_length=50, verbose_name='CSS Color Class')
    icon = models.CharField(max_length=50, verbose_name='Font Awesome Icon')
    is_active = models.BooleanField(default=True, verbose_name='Active')

    class Meta:
        verbose_name = 'Workout Type'
        verbose_name_plural = 'Workout Types'

    def __str__(self):
        return self.name


class WorkoutSchedule(models.Model):
    WEEKDAYS = [
        (0, 'Понеділок'),
        (1, 'Вівторок'),
        (2, 'Середа'),
        (3, 'Четвер'),
        (4, 'П\'ятниця'),
        (5, 'Субота'),
        (6, 'Неділя'),
    ]

    name = models.CharField(max_length=100, verbose_name='Class Name')
    workout_type = models.ForeignKey(WorkoutType, on_delete=models.CASCADE, verbose_name='Workout Type')
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, verbose_name='Trainer')
    weekday = models.IntegerField(choices=WEEKDAYS, verbose_name='Weekday')
    start_time = models.TimeField(verbose_name='Start Time')
    end_time = models.TimeField(verbose_name='End Time')
    max_participants = models.PositiveIntegerField(verbose_name='Max Participants')
    description = models.TextField(blank=True, verbose_name='Description')
    is_active = models.BooleanField(default=True, verbose_name='Active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Workout Schedule'
        verbose_name_plural = 'Workout Schedules'
        ordering = ['weekday', 'start_time']

    def __str__(self):
        return f'{self.name} - {self.get_weekday_display()} {self.start_time}'

    @property
    def duration_minutes(self):
        start = timezone.datetime.combine(date.today(), self.start_time)
        end = timezone.datetime.combine(date.today(), self.end_time)
        return int((end - start).total_seconds() / 60)

    @property
    def time_slot(self):
        return f"{self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}"

    def get_current_participants_count(self):
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        target_date = start_of_week + timedelta(days=self.weekday)

        return WorkoutBooking.objects.filter(
            schedule=self,
            date=target_date,
            status='confirmed'
        ).count()

    @property
    def available_spots(self):
        return self.max_participants - self.get_current_participants_count()

    @property
    def is_full(self):
        return self.available_spots <= 0


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50, verbose_name='Plan Name')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Price')
    duration_days = models.PositiveIntegerField(verbose_name='Duration (days)')
    features = models.TextField(
        verbose_name='Features',
        help_text='List features separated by new line'
    )
    excluded_features = models.TextField(
        blank=True,
        verbose_name='Excluded Features',
        help_text='List excluded features separated by new line'
    )
    personal_training_sessions = models.PositiveIntegerField(
        default=0,
        verbose_name='Personal Training Sessions'
    )
    is_popular = models.BooleanField(default=False, verbose_name='Popular')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    color = models.CharField(max_length=20, default='gray', verbose_name='Theme Color')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'
        ordering = ['price']

    def __str__(self):
        return f'{self.name} - ₴{self.price}'

    def get_features_list(self):
        return [feature.strip() for feature in self.features.split('\n') if feature.strip()]

    def get_excluded_features_list(self):
        return [feature.strip() for feature in self.excluded_features.split('\n') if feature.strip()]

    @property
    def period_display(self):
        if self.duration_days == 30:
            return 'місяць'
        elif self.duration_days == 90:
            return '3 місяці'
        elif self.duration_days == 365:
            return 'рік'
        else:
            return f'{self.duration_days} днів'


class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активний'),
        ('expired', 'Закінчився'),
        ('suspended', 'Призупинено'),
        ('cancelled', 'Скасовано'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, verbose_name='Plan')
    start_date = models.DateField(verbose_name='Start Date')
    end_date = models.DateField(verbose_name='End Date')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Status')
    auto_renew = models.BooleanField(default=False, verbose_name='Auto Renew')
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Payment Amount')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Subscription'
        verbose_name_plural = 'User Subscriptions'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.plan.name} ({self.status})'

    @property
    def days_left(self):
        if self.status == 'active' and self.end_date >= date.today():
            return (self.end_date - date.today()).days
        return 0

    @property
    def is_active(self):
        return self.status == 'active' and self.end_date >= date.today()

    def save(self, *args, **kwargs):
        if not self.end_date and self.start_date:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)


class WorkoutBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('confirmed', 'Підтверджено'),
        ('cancelled', 'Скасовано'),
        ('completed', 'Завершено'),
        ('no_show', 'Не з\'явився'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    schedule = models.ForeignKey(WorkoutSchedule, on_delete=models.CASCADE, verbose_name='Schedule')
    date = models.DateField(verbose_name='Workout Date')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed', verbose_name='Status')
    notes = models.TextField(blank=True, verbose_name='Notes')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Workout Booking'
        verbose_name_plural = 'Workout Bookings'
        unique_together = ['user', 'schedule', 'date']
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.schedule.name} - {self.date}'

    @property
    def is_upcoming(self):
        workout_datetime = timezone.datetime.combine(
            self.date,
            self.schedule.start_time
        )
        return workout_datetime > timezone.now()

    @property
    def is_past(self):
        workout_datetime = timezone.datetime.combine(
            self.date,
            self.schedule.end_time
        )
        return workout_datetime < timezone.now()


class WorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    booking = models.OneToOneField(
        WorkoutBooking,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Workout Booking'
    )
    workout_type = models.ForeignKey(WorkoutType, on_delete=models.CASCADE, verbose_name='Workout Type')
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, verbose_name='Trainer')
    date = models.DateField(verbose_name='Workout Date')
    duration_minutes = models.PositiveIntegerField(verbose_name='Duration (minutes)')

    # General metrics
    calories_burned = models.PositiveIntegerField(null=True, blank=True, verbose_name='Calories Burned')
    heart_rate_avg = models.PositiveIntegerField(null=True, blank=True, verbose_name='Average Heart Rate')
    heart_rate_max = models.PositiveIntegerField(null=True, blank=True, verbose_name='Max Heart Rate')

    # Strength metrics
    exercises_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Exercise Data',
        help_text='JSON with exercise information, sets, reps, weight'
    )

    notes = models.TextField(blank=True, verbose_name='Trainer Notes')
    user_notes = models.TextField(blank=True, verbose_name='User Notes')
    rating = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Workout Rating (1-5)'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Workout Session'
        verbose_name_plural = 'Workout Sessions'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.workout_type.name} - {self.date}'


class PaymentHistory(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('completed', 'Завершено'),
        ('failed', 'Неуспішно'),
        ('refunded', 'Повернено'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('card', 'Картка'),
        ('cash', 'Готівка'),
        ('bank_transfer', 'Банківський переказ'),
        ('online', 'Онлайн платіж'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    subscription = models.ForeignKey(
        UserSubscription,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Subscription'
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Amount')
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='Payment Method'
    )
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name='Payment Status'
    )
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name='Transaction ID')
    description = models.CharField(max_length=200, verbose_name='Payment Description')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payment History'
        verbose_name_plural = 'Payment History'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - ₴{self.amount} - {self.get_status_display()}'

    @property
    def plan_name(self):
        return self.subscription.plan.name if self.subscription else 'Інше'
