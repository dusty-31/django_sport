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
