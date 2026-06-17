from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AppUser
from .forms import AppUserCreationForm, AppUserChangeForm
from django.contrib.auth import logout as auth_logout
from .forms import LoginForm 
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.backends import BaseBackend

def logout(request):    
    auth_logout(request)
    
    return redirect('accounts:login')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/login.html',context)
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = AppUserBackend().authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:user_list')
            else:
                messages.error(request,'Email o password incorrecto.')
                return render(request, 'accounts/login.html', {'form': form})
        else:
            return render(request, 'accounts/login.html', {'form': form})


class AppUserBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None
        try:
            user = AppUser.objects.get(email=email)
        except AppUser.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            user = AppUser.objects.get(id=user_id)
        except AppUser.DoesNotExist:
            return None
        return user


class UserListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'usuarios': AppUser.objects.all().order_by('-id'),
            'titulo': 'Lista de Usuarios'
        }
        return render(request, 'accounts/index.html', context)


class UserCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': AppUserCreationForm(),
            'titulo': 'Registrar Nuevo Usuario'
        }
        return render(request, 'accounts/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = AppUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:user_list')
        
        context = {'form': form, 'titulo': 'Registrar Nuevo Usuario'}
        return render(request, 'accounts/registration.html', context)


class UserUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        usuario = get_object_or_404(AppUser, pk=pk)
        context = {
            'form': AppUserChangeForm(instance=usuario),
            'titulo': f'Editar Usuario: {usuario.username}'
        }
        return render(request, 'accounts/edit.html', context)

    def post(self, request, pk, *args, **kwargs):
        usuario = get_object_or_404(AppUser, pk=pk)
        form = AppUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('accounts:user_list')
        
        context = {'form': form, 'titulo': f'Editar Usuario: {usuario.username}'}
        return render(request, 'accounts/edit.html', context)


class UserDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        usuario = get_object_or_404(AppUser, pk=pk)
        usuario.delete()
        return redirect('accounts:user_list')
    

class UserShowView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        usuario_instancia = get_object_or_404(AppUser, pk=pk)
        context = {
            'user': usuario_instancia,
            'titulo_pagina': f"Perfil de {usuario_instancia.username} - Gestión"
        }
        return render(request, 'accounts/show.html', context)