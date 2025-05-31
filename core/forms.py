from django import forms
from django.contrib.auth.models import User
from .models import ClientDetail


class UserProfileForm(forms.ModelForm):
    """Форма для редагування основної інформації користувача"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all',
                'placeholder': 'Ваше ім\'я'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all',
                'placeholder': 'Ваше прізвище'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all',
                'placeholder': 'example@powerzone.ua'
            }),
        }
        labels = {
            'first_name': 'Ім\'я',
            'last_name': 'Прізвище',
            'email': 'Email',
        }


class ClientDetailForm(forms.ModelForm):
    """Форма для редагування додаткової інформації клієнта"""

    class Meta:
        model = ClientDetail
        fields = [
            'phone', 'birth_date', 'gender', 'height', 'weight',
            'fitness_goal', 'experience_level', 'medical_conditions',
            'emergency_contact', 'emergency_phone', 'newsletter_subscription'
        ]
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all',
                'placeholder': '+380 (66) 123-45-67'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all',
                'placeholder': '175'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all',
                'placeholder': '70.5',
                'step': '0.1'
            }),
            'fitness_goal': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all'
            }),
            'experience_level': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all'
            }),
            'medical_conditions': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all',
                'rows': 3,
                'placeholder': 'Опишіть медичні обмеження або залиште порожнім'
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all',
                'placeholder': 'ПІБ контактної особи'
            }),
            'emergency_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all',
                'placeholder': '+380 (66) 123-45-67'
            }),
            'newsletter_subscription': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-primary bg-gray-50 border-gray-300 rounded focus:ring-primary focus:ring-2'
            }),
        }