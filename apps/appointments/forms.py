from django import forms
from django.forms import DateTimeInput
from .models import Appointment


class AppointmentForm(forms.ModelForm):
	class Meta:
		model = Appointment
		fields = ['customer', 'description', 'price', 'payment_method', 'status', 'date']
		widgets = {
			'description': forms.Textarea(attrs={'rows': 3}),
			'date': DateTimeInput(attrs={'type': 'datetime-local'}),
		}


class AppointmentCreateForm(AppointmentForm):
	pass


class AppointmentUpdateForm(AppointmentForm):
	pass
