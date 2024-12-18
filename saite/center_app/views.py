from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegister
from .models import *
from django.core.paginator import Paginator
import os
from django.conf import settings
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth.models import User


def appointment_view(request):
    services = Service.objects.all()
    if request.method == 'POST':
        print(f"request.POST: {request.POST}")
        service_id = request.POST.get('service')
        appointment_time_str = request.POST.get('appointment_time')
        try:
            print(f"service_id: {service_id}")
            service = Service.objects.get(id=service_id)
            print(f"Service: {service}")
            print(f"User: {request.user}")
            if request.user.is_anonymous:
                print(f"User is anonymous")
            else:
                print(f"User id: {request.user.id}")
            appointment_time = datetime.fromisoformat(appointment_time_str)
            appointment_time = timezone.make_aware(appointment_time)
            if appointment_time <= timezone.now():
                return render(request, 'zapis.html', {'services': services, 'error': 'Выберите время в будущем'})
            if Appointment.objects.filter(appointment_time=appointment_time).exists():
                return render(request, 'zapis.html', {'services': services, 'error': 'На это время уже есть запись'})

            phone_number = None
            if hasattr(request.user, 'number'):
                phone_number = request.user.number
            try:
                user = Piple.objects.get(id = request.user.id)
                print(f"User: {user}")
            except Piple.DoesNotExist as e:
                print(f"Piple.DoesNotExist: {e}")
                return render(request, 'zapis.html', {'services': services, 'error': 'Пользователь не найден'})
            Appointment.objects.create(service=service, appointment_time=appointment_time, user=user, phone_number=phone_number)
            messages.success(request, 'Вы успешно записались на прием!')
            return redirect('zapis')
        except Service.DoesNotExist as e:
            print(f"Service.DoesNotExist: {e}")
            return render(request, 'zapis.html', {'services': services, 'error': 'Услуга не найдена'})
        except ValueError as e:
            print(f"ValueError: {e}")
            return render(request, 'zapis.html', {'services': services, 'error': 'Неправильный формат времени'})
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
            return render(request, 'zapis.html', {'services': services, 'error': 'Ошибка записи в базе данных'})
        except Exception as e:
            print(f"Exception: {e}")
            return render(request, 'zapis.html', {'services': services, 'error': 'Произошла ошибка'})
    return render(request, 'zapis.html', {'services': services})

def index(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html')

def doctors(request):
    return render(request, 'doctors.html')

def contacts(request):
    return render(request, 'contacts.html')

def register(request):
    return render(request, 'register.html')

def zapis(request):
    return render(request, 'zapis.html')

users = ['user1', 'user2', 'user3']

def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = request.POST.get('age')
        number = request.POST.get('number')
        try:
           user = Piple.objects.create(username=username, password=password, repeat_password = repeat_password, age = age, number = number, user_id = request.user.id)
           messages.success(request, 'Вы успешно зарегистрировались!')
           user = authenticate(request, username=username, password=password) # Правильное использование authenticate
           if user is not None:
                login(request, user) # Залогиниваем пользователя
                return redirect('zapis')
        except IntegrityError as e:
             print(f"IntegrityError: {e}")
             return render(request, 'register.html', {'error': 'Пользователь уже зарегистрирован'})
        except Exception as e:
            print(f"Exception: {e}")
            return render(request, 'register.html', {'error': 'Произошла ошибка регистрации'})
    return render(request, 'register.html')

def get_all_users():
    return Piple.objects.all().values_list('username', flat=True)

# Create your views here.
