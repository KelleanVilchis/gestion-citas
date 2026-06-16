from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Appointment
from .forms import AppointmentCreateForm, AppointmentUpdateForm


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


class AppointmentCreateView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		context = {
			'form': AppointmentCreateForm(),
			'titulo': 'Crear Nueva Cita'
		}
		return render(request, 'appointment/create.html', context)

	def post(self, request, *args, **kwargs):
		form = AppointmentCreateForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('appointments:appointment_list')

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
