from datetime import datetime, date, timedelta, time as dtime

from django.forms import HiddenInput
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import random
import string
from apps.accounts import models
from .models import Appointment, StatusAppointment, BarberSchedule
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
            guest_phone = form.cleaned_data.get('guest_phone')
            guest_email = form.cleaned_data.get('guest_email')  
            if not request.user.is_authenticated:
                duplicate_appointment = Appointment.objects.filter(
                    Q(guest_phone=guest_phone) | Q(guest_email=guest_email),
                    status=StatusAppointment.SCHEDULED
                ).exists()
                if duplicate_appointment:
                    form.add_error('guest_phone', 'Usted ya cuenta con una cita programada activa en nuestro sistema.')
                    context = {'form': form, 'titulo': 'Crear Nueva Cita'}
                    return render(request, 'appointment/create.html', context)
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
	


class BookAppointmentView(View):
    SLOT_DURATION = timedelta(hours=1, minutes=30)
    DEFAULT_START_TIME = dtime(hour=9, minute=0)
    DEFAULT_END_TIME = dtime(hour=19, minute=0)

    def _get_selected_day(self, value, fallback):
        selected = parse_date(value) if value else None
        return selected if selected and selected >= fallback else fallback

    def _get_schedule_hours(self, day_date):
        try:
            schedule = BarberSchedule.objects.get(day_of_week=day_date.weekday(), is_active=True)
            return schedule.start_time, schedule.end_time
        except BarberSchedule.DoesNotExist:
            return self.DEFAULT_START_TIME, self.DEFAULT_END_TIME

    def _is_slot_available(self, day_date, slot_time, appointments):
        slot_start = datetime.combine(day_date, slot_time)
        slot_end = slot_start + self.SLOT_DURATION
        for appointment in appointments:
            if appointment.appointment_date != day_date or not appointment.appointment_time:
                continue
            appointment_start = datetime.combine(day_date, appointment.appointment_time)
            appointment_end = appointment_start + self.SLOT_DURATION
            if slot_start < appointment_end and appointment_start < slot_end:
                return False
        return True

    def _get_available_slots_for_day(self, day_date, appointments):
        start_time, end_time = self._get_schedule_hours(day_date)
        slots = []
        current = datetime.combine(day_date, start_time)
        end_dt = datetime.combine(day_date, end_time)

        while current + self.SLOT_DURATION <= end_dt:
            slot_time = current.time()
            slots.append({
                'label': slot_time.strftime('%H:%M'),
                'time': slot_time,
                'available': self._is_slot_available(day_date, slot_time, appointments),
            })
            current += self.SLOT_DURATION

        return slots

    def _build_week_days(self, today, appointments, selected_day):
        week_days = []
        for offset in range(7):
            day = today + timedelta(days=offset)
            slots = self._get_available_slots_for_day(day, appointments)
            week_days.append({
                'date': day,
                'weekday': day.strftime('%a'),
                'day': day.day,
                'available_slots': sum(1 for slot in slots if slot['available']),
                'selected': day == selected_day,
            })
        return week_days

    def _prepare_book_form(self, form):
        form.fields['appointment_date'].widget = HiddenInput()
        form.fields['appointment_time'].widget = HiddenInput()
        form.fields['appointment_date'].required = True
        form.fields['appointment_time'].required = True

    def get(self, request, *args, **kwargs):
        today = date.today()
        selected_day = self._get_selected_day(request.GET.get('day'), today)
        end_date = today + timedelta(days=6)
        appointments = Appointment.objects.filter(
            appointment_date__range=(today, end_date),
            status=StatusAppointment.SCHEDULED,
        )

        # Detectar si es una petición AJAX para cambiar de día
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            slots = self._get_available_slots_for_day(selected_day, appointments)
            context = {
                'selected_slots': slots,
                'selected_day': selected_day,
            }
            # Devolvemos solo el fragmento de los slots y las etiquetas mutables
            return render(request, 'appointment/partials/slots_render.html', context)

        # Código original para la carga inicial de la página completo
        form = AppointmentCreateForm(initial={
            'appointment_date': selected_day,
            'appointment_time': request.GET.get('time', ''),
        })
        self._prepare_book_form(form)

        context = {
            'titulo_pagina': 'Book Appointment - Barber & Studio',
            'titulo': 'Reserva tu cita',
            'week_days': self._build_week_days(today, appointments, selected_day),
            'selected_day': selected_day,
            'selected_slot_time': request.GET.get('time', ''),
            'selected_slots': self._get_available_slots_for_day(selected_day, appointments),
            'today': today,
            'form': form,
        }
        return render(request, 'appointment/book.html', context)

    def post(self, request, *args, **kwargs):
        today = date.today()
        selected_day = self._get_selected_day(request.POST.get('appointment_date'), today)
        end_date = today + timedelta(days=6)
        appointments = Appointment.objects.filter(
            appointment_date__range=(today, end_date),
            status=StatusAppointment.SCHEDULED,
        )

        form = AppointmentCreateForm(request.POST)
        self._prepare_book_form(form)

        if form.is_valid():
            appointment_date = form.cleaned_data.get('appointment_date')
            appointment_time = form.cleaned_data.get('appointment_time')

            if not appointment_date or not appointment_time:
                form.add_error(None, 'Selecciona un día y una hora antes de continuar.')
            elif not self._is_slot_available(appointment_date, appointment_time, appointments):
                form.add_error(None, 'El horario seleccionado ya no está disponible. Elige otro.')
            else:
                appointment = form.save(commit=False)
                appointment.code_appointment = generate_unique_appointment_code()
                if request.user.is_authenticated:
                    appointment.customer = request.user
                appointment.save()
                return redirect('appointments:home')

        context = {
            'titulo_pagina': 'Book Appointment - Barber & Studio',
            'titulo': 'Reserva tu cita',
            'week_days': self._build_week_days(today, appointments, selected_day),
            'selected_day': selected_day,
            'selected_slot_time': request.POST.get('appointment_time', ''),
            'selected_slots': self._get_available_slots_for_day(selected_day, appointments),
            'today': today,
            'form': form,
        }
        return render(request, 'appointment/book.html', context)
