from django.db import models
from django.contrib.auth.models import User


class Guest(models.Model):
    session_key = models.CharField(max_length=40, unique=True, null=True, blank=True,
                                   verbose_name="Ключ сессии")
    first_visit = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Время первого визита")
    last_action = models.DateTimeField(auto_now=True,
                                       verbose_name="Время последнего действия")

# Модель для Авторизованного пользователя для дальнейшей разработки
class AuthorizedUser(models.Model):
    # Связь "один к одному"
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)


    class Meta:
        verbose_name = "Авторизованный Пользователь"
        verbose_name_plural = "Авторизованные Пользователи"

    def __str__(self):
        return self.user.username


# Модель для Администратора для дальнейшей разработки
class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Дополнительные поля для администратора
    role = models.CharField(max_length=100, default='Менеджер')

    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"

    def __str__(self):
        return f"Администратор: {self.user.username}"


# Модель для Заявки/Плана
class RoomPlan(models.Model):
    client = models.ForeignKey(AuthorizedUser, on_delete=models.CASCADE, related_name='room_plans')
    title = models.CharField(max_length=255)
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    # plan_file = models.FileField(upload_to='room_plans/')

    STATUS_CHOICES = [
        ('NEW', 'Новая'),
        ('IN_PROGRESS', 'В работе'),
        ('COMPLETED', 'Завершена'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')

    class Meta:
        verbose_name = "План Помещения"
        verbose_name_plural = "Планы Помещений"

    def __str__(self):
        return f"План {self.title} от {self.client.user.username}"
