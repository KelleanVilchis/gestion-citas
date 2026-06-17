from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import random
import string
from apps.accounts import models
from .models import Appointment
from .forms import AppointmentSearchForm, AppointmentCreateForm, AppointmentUpdateForm
from django.db.models import Q  # 🌟 IMPORTA LA Q CORRECTAMENTE AQUÍ

class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'titulo_pagina': 'Home - Barber & Studio'
        }
        return render(request, 'appointment/home.html', context)
	

class AppointmentListView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		context = {
			'appointments': Appointment.objects.all().order_by('-id'),
			'titulo': 'Lista de Citas'
		}
		return render(request, 'appointment/index.html', context)


def generate_unique_appointment_code():
    length = 5  
    while True:
        random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        code = f"BR-{random_code}" 
        
        if not Appointment.objects.filter(code_appointment=code).exists():
            return code

class AppointmentCreateView(View): 
    def get(self, request, *args, **kwargs):
        initial_data = {
            'appointment_date': request.GET.get('date'),
            'appointment_time': request.GET.get('time')
        }
        context = {
            'form': AppointmentCreateForm(initial=initial_data),
            'titulo': 'Crear Nueva Cita'
        }
        return render(request, 'appointment/create.html', context) 
    def post(self, request, *args, **kwargs):
        form = AppointmentCreateForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.code_appointment = generate_unique_appointment_code()
            
            if request.user.is_authenticated:
                appointment.customer = request.user
            
            appointment.save()
            
            return redirect('appointments:home') 
        context = {'form': form, 'titulo': 'Crear Nueva Cita'}
        return render(request, 'appointment/create.html', context)


class AppointmentUpdateView(LoginRequiredMixin, View):
	def get(self, request, pk, *args, **kwargs):
		appointment = get_object_or_404(Appointment, pk=pk)
		context = {
			'form': AppointmentUpdateForm(instance=appointment),
			'titulo': f'Editar Cita: {appointment.customer.username}'
		}
		return render(request, 'appointment/edit.html', context)

	def post(self, request, pk, *args, **kwargs):
		appointment = get_object_or_404(Appointment, pk=pk)
		form = AppointmentUpdateForm(request.POST, instance=appointment)
		if form.is_valid():
			form.save()
			return redirect('appointments:appointment_list')

		context = {'form': form, 'titulo': f'Editar Cita: {appointment.customer.username}'}
		return render(request, 'appointment/edit.html', context)


class AppointmentDeleteView(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		appointment = get_object_or_404(Appointment, pk=pk)
		appointment.delete()
		return redirect('appointments:appointment_list')


class AppointmentShowView(LoginRequiredMixin, View):
	def get(self, request, pk, *args, **kwargs):
		appointment = get_object_or_404(Appointment, pk=pk)
		context = {
			'appointment': appointment,
			'titulo_pagina': f"Cita de {appointment.customer.username}" 
		}
		return render(request, 'appointment/show.html', context)


class CheckAppointmentView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': AppointmentSearchForm(),
            'titulo_pagina': 'Lookup Appointment - Barber & Studio'
        }
        return render(request, 'appointment/check.html', context)



class SearchAppointmentAJAXView(View):
    def post(self, request, *args, **kwargs):
        query = request.POST.get('search_query', '').strip()
        appointment = None
        print(f"Received search query: '{query}'") 
        if query:
            appointment = Appointment.objects.filter(
                Q(code_appointment__iexact=query) | 
                Q(guest_phone=query)
            ).first()

        context = {
            'appointment': appointment,
            'query': query
        }
        return render(request, 'appointment/partials/search_results.html', context)
	


