from django.contrib.auth.models import AbstractUser
from django.db import models

class UserType(models.TextChoices):
    ADMIN = 'ADM','Administrador'
    CLIENTE = 'CLI','Cliente'


class AppUser(AbstractUser):
    user_type = models.CharField(max_length=3, choices=UserType.choices, default=UserType.CLIENTE)
    pass  