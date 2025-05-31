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
            'past_workouts': [],      # Минулі тренування
            'total_workouts': 0,      # Загальна кількість
            'this_month_workouts': 0, # За цей місяць
        })
        return context

