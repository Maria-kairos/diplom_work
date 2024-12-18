from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Piple(models.Model):
    username = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=150)
    repeat_password = models.CharField(max_length=150)
    age = models.IntegerField()
    number = models.CharField(max_length=20)
    user_id = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.username

    @property  # Добавили декоратор @property
    def is_authenticated(self):
        return True  # Указываем, что пользователь аутентифицирован

    @property  # Добавили декоратор @property
    def is_anonymous(self):
        return False  # Указываем, что пользователь не анонимный
class Service(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Appointment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    appointment_time = models.DateTimeField()
    user = models.ForeignKey(Piple, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.service.name} - {self.appointment_time} - {self.user} - {self.phone_number}"

class Cool(models.Model):
    name = models.CharField(max_length=150)

# Create your models here.
