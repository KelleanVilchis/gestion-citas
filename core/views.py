from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.models import AppUser


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'titulo_pagina': 'Panel de Control - Inicio',
            'total_usuarios': AppUser.objects.count(),
            'usuarios': AppUser.objects.all(),
        }
        return render(request, 'base.html', context)