from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Клиент'),
        ('admin', 'Администратор'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='client')
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.username