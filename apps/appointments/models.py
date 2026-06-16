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


class Appointment(models.Model):
    code_appointment = models.CharField(max_length=8, unique=True, null=True, blank=True)
    customer = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    status = models.CharField(max_length=20, choices=StatusAppointment.choices, default=StatusAppointment.SCHEDULED)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.username + ' - ' + self.description[:20]