from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from core.forms import ClientDetailForm, UserProfileForm
from core.models import ClientDetail


class IndexView(TemplateView):
    template_name = 'core/index.html'


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        context = {
            'form': form,
        }
        return render(request=request, template_name='core/login.html', context=context)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('core:index')
        context = {
            'form': form,
        }
        return render(request=request, template_name='core/login.html', context=context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('core:index')


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        for field in form.fields.values():
            field.help_text = None
        context = {
            'form': form,
        }
        return render(request=request, template_name='core/register.html', context=context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        for field in form.fields.values():
            field.help_text = None
        if form.is_valid():
            form.save()
            messages.success(request, 'Реєстрація успішна! Ласкаво просимо до PowerZone!')
            return redirect('core:login')
        context = {
            'form': form,
        }
        return render(request=request, template_name='core/register.html', context=context)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'core/profile.html'
    login_url = reverse_lazy('core:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        if hasattr(user, 'client_detail'):
            context['client_detail'] = user.client_detail
        return context


class ProfileEditView(LoginRequiredMixin, View):
    template_name = 'core/profile_edit.html'
    login_url = reverse_lazy('core:login')

    def get_client_detail(self):
        client_detail, created = ClientDetail.objects.get_or_create(user=self.request.user)
        return client_detail

    def get(self, request):
        client_detail = self.get_client_detail()
        user_form = UserProfileForm(instance=request.user)
        detail_form = ClientDetailForm(instance=client_detail)

        context = {
            'user_form': user_form,
            'detail_form': detail_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        client_detail = self.get_client_detail()
        user_form = UserProfileForm(request.POST, instance=request.user)
        detail_form = ClientDetailForm(request.POST, instance=client_detail)

        if user_form.is_valid() and detail_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save()
                    detail = detail_form.save(commit=False)
                    detail.user = user
                    detail.save()

                    messages.success(request, 'Профіль успішно оновлено!')
                    return redirect('core:profile')
            except Exception as e:
                print(f"Error saving forms: {e}")
                messages.error(request, f'Помилка при збереженні: {e}')
        else:
            messages.error(request, 'Перевірте правильність введених даних')

        context = {
            'user_form': user_form,
            'detail_form': detail_form,
        }
        return render(request, self.template_name, context)


class MyWorkoutsView(LoginRequiredMixin, TemplateView):
    template_name = 'core/my_workouts.html'
    login_url = reverse_lazy('core:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Тут буде логіка для отримання тренувань користувача
        # Поки що додаємо тестові дані
        context.update({
            'user': self.request.user,
            # Після створення моделей тренувань тут будуть реальні дані
            'upcoming_workouts': [],  # Майбутні тренування
            'past_workouts': [],  # Минулі тренування
            'total_workouts': 10,  # Загальна кількість
            'this_month_workouts': 4,  # За цей місяць
        })
        return context


class MySubscriptionsView(LoginRequiredMixin, TemplateView):
    template_name = 'core/my_subscriptions.html'
    login_url = reverse_lazy('core:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Дані про доступні тарифні плани (з головної сторінки)
        subscription_plans = [
            {
                'name': 'Базовий',
                'price': 1200,
                'period': 'місяць',
                'features': [
                    'Доступ до тренажерного залу',
                    'Групові заняття',
                    'Консультація тренера',
                ],
                'excluded_features': [
                    'Персональні тренування',
                ],
                'is_popular': False,
                'color': 'gray'
            },
            {
                'name': 'Преміум',
                'price': 2000,
                'period': 'місяць',
                'features': [
                    'Доступ до тренажерного залу',
                    'Групові заняття',
                    '4 персональні тренування',
                    'Консультація дієтолога',
                ],
                'excluded_features': [],
                'is_popular': True,
                'color': 'primary'
            },
            {
                'name': 'VIP',
                'price': 3500,
                'period': 'місяць',
                'features': [
                    'Безлімітний доступ',
                    '8 персональних тренувань',
                    'Індивідуальна програма',
                    'Консультації фахівців',
                ],
                'excluded_features': [],
                'is_popular': False,
                'color': 'secondary'
            }
        ]

        context.update({
            'user': self.request.user,
            'subscription_plans': subscription_plans,
            # Тут буде логіка для отримання активних абонементів користувача
            'current_subscription': None,  # Поточний активний абонемент
            'subscription_history': [],  # Історія абонементів
            'days_left': 0,  # Днів залишилось
            'next_payment_date': None,  # Дата наступного платежу
        })
        return context


class ServicesView(TemplateView):
    template_name = 'core/services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = [
            {
                'id': 'personal-training',
                'title': 'Персональні тренування',
                'icon': 'fas fa-user-tie',
                'short_description': 'Індивідуальний підхід з досвідченими тренерами для максимального результату',
                'description': 'Персональні тренування - це найефективніший спосіб досягти ваших фітнес-цілей. Наші сертифіковані тренери розроблять індивідуальну програму тренувань, враховуючи ваш рівень підготовки, цілі та особливості організму.',
                'features': [
                    'Індивідуальна програма тренувань',
                    'Постійний контроль техніки виконання',
                    'Корекція програми відповідно до прогресу',
                    'Консультації з харчування',
                    'Мотивація та психологічна підтримка'
                ],
                'price_from': 500,
                'duration': '60 хвилин',
                'trainers': ['Іван Мельник', 'Анна Рибчак'],
                'image': 'services/personal-training.jpg',
                'color': 'primary'
            },
            {
                'id': 'strength-training',
                'title': 'Силові тренування',
                'icon': 'fas fa-dumbbell',
                'short_description': 'Професійне обладнання для нарощування м\'язової маси та сили',
                'description': 'Силові тренування спрямовані на розвиток м\'язової маси, сили та витривалості. Ми маємо повний арсенал професійного обладнання від провідних світових брендів.',
                'features': [
                    'Сучасне силове обладнання',
                    'Групові та індивідуальні заняття',
                    'Програми для початківців та професіоналів',
                    'Безпечні методики тренувань',
                    'Контроль прогресу'
                ],
                'price_from': 300,
                'duration': '90 хвилин',
                'trainers': ['Юрій Неонов', 'Макс Вірастюк'],
                'image': 'services/strength-training.jpg',
                'color': 'blue'
            },
            {
                'id': 'boxing',
                'title': 'Бокс і єдиноборства',
                'icon': 'fas fa-fist-raised',
                'short_description': 'Тренування з бойових мистецтв для самооборони та фізичної форми',
                'description': 'Заняття боксом та єдиноборствами допоможуть вам покращити координацію, швидкість реакції та загальну фізичну форму. Підходить як для початківців, так і для досвідчених спортсменів.',
                'features': [
                    'Вивчення базової техніки',
                    'Спаринг-тренування',
                    'Розвиток координації та спритності',
                    'Кардіо навантаження',
                    'Самооборона'
                ],
                'price_from': 350,
                'duration': '75 хвилин',
                'trainers': ['Макс Вірастюк'],
                'image': 'services/boxing.jpg',
                'color': 'red'
            },
            {
                'id': 'cardio',
                'title': 'Кардіо тренування',
                'icon': 'fas fa-heartbeat',
                'short_description': 'Ефективні кардіо-програми для схуднення та покращення витривалості',
                'description': 'Кардіо тренування допоможуть спалити зайві калорії, покращити роботу серцево-судинної системи та підвищити загальну витривалість організму.',
                'features': [
                    'Різноманітні кардіо-програми',
                    'HIIT тренування',
                    'Зумба та танцювальний фітнес',
                    'Велотренажери та бігові доріжки',
                    'Контроль пульсу'
                ],
                'price_from': 250,
                'duration': '45 хвилин',
                'trainers': ['Іван Мельник', 'Анна Рибчак'],
                'image': 'services/cardio.jpg',
                'color': 'green'
            },
            {
                'id': 'yoga',
                'title': 'Йога та стретчинг',
                'icon': 'fas fa-leaf',
                'short_description': 'Покращення гнучкості, рівноваги та внутрішньої гармонії',
                'description': 'Заняття йогою та стретчингом допоможуть покращити гнучкість, зняти напругу після силових тренувань та знайти внутрішню рівновагу.',
                'features': [
                    'Хатха та Віньяса йога',
                    'Ранкові та вечірні заняття',
                    'Медитативні практики',
                    'Покращення гнучкості',
                    'Зняття стресу'
                ],
                'price_from': 200,
                'duration': '60 хвилин',
                'trainers': ['Софія Дзень'],
                'image': 'services/yoga.jpg',
                'color': 'purple'
            },
            {
                'id': 'crossfit',
                'title': 'CrossFit',
                'icon': 'fas fa-fire',
                'short_description': 'Високоінтенсивні функціональні тренування для всіх груп м\'язів',
                'description': 'CrossFit поєднує в собі елементи важкої атлетики, гімнастики та кардіо. Це ідеальний вибір для тих, хто хоче комплексно розвивати своє тіло.',
                'features': [
                    'WOD (Workout of the Day)',
                    'Функціональні рухи',
                    'Командний дух',
                    'Масштабування для всіх рівнів',
                    'Постійна варіативність'
                ],
                'price_from': 400,
                'duration': '60 хвилин',
                'trainers': ['Анна Рибчак', 'Юрій Неонов'],
                'image': 'services/crossfit.jpg',
                'color': 'orange'
            }
        ]

        additional_services = [
            {
                'title': 'Консультація дієтолога',
                'description': 'Складання індивідуального плану харчування',
                'price': 800,
                'icon': 'fas fa-apple-alt'
            },
            {
                'title': 'Масаж',
                'description': 'Спортивний та релаксаційний масаж',
                'price': 600,
                'icon': 'fas fa-hand-paper'
            },
            {
                'title': 'Аналіз складу тіла',
                'description': 'Професійний аналіз на InBody',
                'price': 300,
                'icon': 'fas fa-chart-pie'
            }
        ]

        context.update({
            'services': services,
            'additional_services': additional_services,
        })
        return context


class FullScheduleView(TemplateView):
    template_name = 'core/full_schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Детальний розклад занять на тиждень
        schedule_data = {
            'monday': [
                {'time': '06:00-07:00', 'name': 'Кардіо Burn', 'trainer': 'Іван', 'capacity': '8/12', 'type': 'cardio'},
                {'time': '08:00-09:00', 'name': 'Силові для початківців', 'trainer': 'Юрій', 'capacity': '7/12', 'type': 'strength'},
                {'time': '12:00-13:00', 'name': 'Обідня енергія', 'trainer': 'Іван', 'capacity': '6/15', 'type': 'cardio'},
                {'time': '18:00-19:00', 'name': 'Evening CrossFit', 'trainer': 'Анна', 'capacity': '15/15', 'type': 'crossfit', 'full': True},
                {'time': '19:00-20:00', 'name': 'Вечірня Йога', 'trainer': 'Софія', 'capacity': '9/15', 'type': 'yoga'},
            ],
            'tuesday': [
                {'time': '06:00-07:00', 'name': 'Power Lifting', 'trainer': 'Юрій', 'capacity': '6/10', 'type': 'strength'},
                {'time': '08:00-09:00', 'name': 'CrossFit Basics', 'trainer': 'Анна', 'capacity': '9/15', 'type': 'crossfit'},
                {'time': '12:00-13:00', 'name': 'Йога Флоу', 'trainer': 'Софія', 'capacity': '10/15', 'type': 'yoga'},
                {'time': '18:00-19:00', 'name': 'Boxing Club', 'trainer': 'Макс', 'capacity': '10/12', 'type': 'boxing'},
                {'time': '19:00-20:00', 'name': 'Кардіо мікс', 'trainer': 'Іван', 'capacity': '13/18', 'type': 'cardio'},
            ],
            'wednesday': [
                {'time': '06:00-07:00', 'name': 'CrossFit WOD', 'trainer': 'Анна', 'capacity': '10/15', 'type': 'crossfit'},
                {'time': '08:00-09:00', 'name': 'Power Training', 'trainer': 'Юрій', 'capacity': '8/10', 'type': 'strength'},
                {'time': '12:00-13:00', 'name': 'Бойова підготовка', 'trainer': 'Макс', 'capacity': '8/12', 'type': 'boxing'},
                {'time': '18:00-19:00', 'name': 'CrossFit RX', 'trainer': 'Анна', 'capacity': '12/15', 'type': 'crossfit'},
                {'time': '19:00-20:00', 'name': 'Інь Йога', 'trainer': 'Софія', 'capacity': '7/12', 'type': 'yoga'},
            ],
            'thursday': [
                {'time': '06:00-07:00', 'name': 'HIIT Кардіо', 'trainer': 'Іван', 'capacity': '12/15', 'type': 'cardio'},
                {'time': '08:00-09:00', 'name': 'Functional Training', 'trainer': 'Анна', 'capacity': '11/15', 'type': 'crossfit'},
                {'time': '12:00-13:00', 'name': 'Обідня сила', 'trainer': 'Юрій', 'capacity': '5/10', 'type': 'strength'},
                {'time': '18:00-19:00', 'name': 'Спаринг тренування', 'trainer': 'Макс', 'capacity': '8/10', 'type': 'boxing'},
                {'time': '19:00-20:00', 'name': 'Табата', 'trainer': 'Іван', 'capacity': '14/18', 'type': 'cardio'},
            ],
            'friday': [
                {'time': '06:00-07:00', 'name': 'CrossFit', 'trainer': 'Анна', 'capacity': '8/15', 'type': 'crossfit'},
                {'time': '08:00-09:00', 'name': 'Zumba Fitness', 'trainer': 'Іван', 'capacity': '15/20', 'type': 'cardio'},
                {'time': '12:00-13:00', 'name': 'Dance Cardio', 'trainer': 'Іван', 'capacity': '12/20', 'type': 'cardio'},
                {'time': '18:00-19:00', 'name': 'Вечірня сила', 'trainer': 'Юрій', 'capacity': '10/10', 'type': 'strength', 'full': True},
                {'time': '19:00-20:00', 'name': 'Релакс Йога', 'trainer': 'Софія', 'capacity': '6/15', 'type': 'yoga'},
            ],
            'saturday': [
                {'time': '06:00-07:00', 'name': 'Ранкова Йога', 'trainer': 'Софія', 'capacity': '5/12', 'type': 'yoga'},
                {'time': '08:00-09:00', 'name': 'Бокс для початківців', 'trainer': 'Макс', 'capacity': '6/12', 'type': 'boxing'},
                {'time': '12:00-13:00', 'name': 'Saturday WOD', 'trainer': 'Анна', 'capacity': '7/15', 'type': 'crossfit'},
                {'time': '18:00-19:00', 'name': 'Weekend Burn', 'trainer': 'Іван', 'capacity': '11/15', 'type': 'cardio'},
                {'time': '19:00-20:00', 'name': 'Saturday Night', 'trainer': 'Анна', 'capacity': '8/12', 'type': 'crossfit'},
            ],
            'sunday': [
                {'time': '08:00-09:00', 'name': 'Хатха Йога', 'trainer': 'Софія', 'capacity': '8/15', 'type': 'yoga'},
            ]
        }

        # Типи тренувань з кольорами
        workout_types = {
            'cardio': {'name': 'Кардіо', 'color': 'bg-primary'},
            'strength': {'name': 'Силові', 'color': 'bg-blue-500'},
            'crossfit': {'name': 'Кросфіт', 'color': 'bg-green-500'},
            'boxing': {'name': 'Бокс', 'color': 'bg-red-500'},
            'yoga': {'name': 'Йога', 'color': 'bg-purple-500'},
        }

        # Тренери з повною інформацією
        trainers = {
            'Іван': {
                'full_name': 'Іван Мельник',
                'specialization': 'Кардіо тренер',
                'experience': '5 років',
                'certifications': ['ACSM', 'NASM-CPT']
            },
            'Юрій': {
                'full_name': 'Юрій Неонов',
                'specialization': 'Силовий тренер',
                'experience': '7 років',
                'certifications': ['NSCA-CSCS', 'StrongFirst']
            },
            'Анна': {
                'full_name': 'Анна Рибчак',
                'specialization': 'CrossFit тренер',
                'experience': '4 роки',
                'certifications': ['CrossFit Level 2', 'USAW']
            },
            'Макс': {
                'full_name': 'Макс Вірастюк',
                'specialization': 'Тренер з боксу',
                'experience': '8 років',
                'certifications': ['Майстер спорту з боксу']
            },
            'Софія': {
                'full_name': 'Софія Дзень',
                'specialization': 'Інструктор йоги',
                'experience': '6 років',
                'certifications': ['RYT-500', 'Yoga Alliance']
            },
        }

        # Часові слоти для відображення в таблиці
        time_slots = ['06:00-07:00', '08:00-09:00', '12:00-13:00', '18:00-19:00', '19:00-20:00']

        # Дні тижня
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        weekday_names = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П\'ятниця', 'Субота', 'Неділя']

        context.update({
            'schedule_data': schedule_data,
            'workout_types': workout_types,
            'trainers': trainers,
            'time_slots': time_slots,
            'weekdays': weekdays,
            'weekday_names': weekday_names,
        })
        return context


class SubscriptionsView(LoginRequiredMixin, TemplateView):
    template_name = 'core/subscriptions.html'
    login_url = reverse_lazy('core:login')

