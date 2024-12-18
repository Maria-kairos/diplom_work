from django.urls import path
from center_app.views import *
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('', index, name='index'),
    path('services/', services, name='services'),
    path('doctors/', doctors, name='doctors'),
    path('contacts/', contacts, name='contacts'),
    path('register/', sign_up, name='register'),
    path('zapis/', appointment_view, name='zapis'),
]