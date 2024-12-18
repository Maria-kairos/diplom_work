from django.contrib import admin
from .models import Piple
from .models import Service

admin.site.register(Service)

@admin.register(Piple)
class Admin_Piple(admin.ModelAdmin):
    list_display = ('username', 'password', 'repeat_password', 'age', 'number')
    search_fields = ('username',)
    list_filter = ('password', 'repeat_password', 'age', 'number')
    fields = [('username', 'password', 'repeat_password', 'age', 'number')]
# Register your models here.
