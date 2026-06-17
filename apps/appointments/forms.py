from django import forms
from django.forms import DateTimeInput
from .models import Appointment


class AppointmentForm(forms.ModelForm):
	class Meta:
		model = Appointment
	# 🌟 Reemplaza 'date' por los dos campos nuevos aquí:
		fields = [
			'guest_name', 'guest_email', 'guest_phone', 
			'description', 'price', 'payment_method', 
			'appointment_date', 'appointment_time'
		]
		widgets = {
			'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'input'}),
			'appointment_time': forms.TimeInput(attrs={'type': 'time', 'class': 'input'}),
			'description': forms.Textarea(attrs={'class': 'input', 'rows': 3}),
			# ... tus otros widgets ...
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