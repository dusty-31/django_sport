from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
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
