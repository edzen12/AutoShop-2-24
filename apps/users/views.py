from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy

from apps.users.forms import RegisterForm, LoginForm, ProfileForm
from apps.cart.utils import merge_cart


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'auth/register.html', {'form':form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'auth/register.html', {'form':form})
    

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'auth/login.html', {'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                merge_cart(request, user)
                return redirect('home')

        return render(request, 'auth/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'auth/profile.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'auth/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user