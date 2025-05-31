from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView


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
            return redirect('core:login')
        context = {
            'form': form,
        }
        return render(request=request, template_name='core/register.html', context=context)
