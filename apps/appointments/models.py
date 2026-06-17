from django.db import models
from apps.accounts.models import AppUser

class StatusAppointment(models.TextChoices):
    SCHEDULED = 'scheduled', 'Scheduled'
    COMPLETED = 'completed', 'Completed'
    CANCELED = 'canceled', 'Canceled'


class PaymentMethod(models.TextChoices):
    CASH = 'cash', 'Cash'
    TRANSFER = 'transfer', 'Transfer'
    CREDIT_CARD = 'credit_card', 'Credit Card'
    DEBIT_CARD = 'debit_card', 'Debit Card'


# 📅 NUEVO: Define el horario de apertura y cierre de la barbería por cada día de la semana
class BarberSchedule(models.Model):
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    day_of_week = models.IntegerField(choices=DAY_CHOICES, unique=True)
    start_time = models.TimeField(help_text="Hora de apertura (ej: 09:00)")
    end_time = models.TimeField(help_text="Hora de cierre (ej: 19:00)")
    is_active = models.BooleanField(default=True, help_text="¿Se trabaja este día?")

    def __str__(self):
        return f"{self.get_day_of_week_display()}: {self.start_time} - {self.end_time}"


class Appointment(models.Model):
    code_appointment = models.CharField(max_length=8, unique=True, null=True, blank=True)

    customer = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True)

    guest_name = models.CharField(max_length=100, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)
    guest_phone = models.CharField(max_length=20, null=True, blank=True)

    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    status = models.CharField(max_length=20, choices=StatusAppointment.choices, default=StatusAppointment.SCHEDULED)

    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointments'
        ordering = ['appointment_date', 'appointment_time']

    def __str__(self):
        identificador = self.customer.username if self.customer else f"Guest: {self.guest_name}"
        return f"{identificador} - {self.appointment_date} @ {self.appointment_time}"