from django import forms
from django.forms import DateTimeInput
from .models import Appointment


class AppointmentForm(forms.ModelForm):
	class Meta:
		model = Appointment
		fields = [
			'guest_name', 'guest_email', 'guest_phone', 
			'description', 'price', 'payment_method', 
			'appointment_date', 'appointment_time'
		]
		widgets = {
			'guest_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Tu nombre completo'}),
			'guest_email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'tu@email.com'}),
			'guest_phone': forms.TextInput(attrs={'class': 'input', 'placeholder': '+56 9 1234 5678'}),
			'description': forms.Textarea(attrs={'class': 'input', 'rows': 4, 'placeholder': 'Ej: Corte fade, acabado fácil'}),
			'price': forms.NumberInput(attrs={'class': 'input', 'placeholder': '15000'}),
			'payment_method': forms.Select(attrs={'class': 'input'}),
			'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'input'}),
			'appointment_time': forms.TimeInput(attrs={'type': 'time', 'class': 'input'}),
		}


class AppointmentCreateForm(AppointmentForm):
	pass


class AppointmentUpdateForm(AppointmentForm):
	pass



class AppointmentSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input text-center text-lg font-bold uppercase tracking-wider',
            'placeholder': 'EJ: BC-8492 Ó 8681234567'
        })
    )