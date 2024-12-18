from django.contrib.auth.backends import BaseBackend
from .models import Piple

class PipleBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Piple.objects.get(username=username)
            if user.password == password:
                return user
        except Piple.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Piple.objects.get(pk=user_id)
        except Piple.DoesNotExist:
            return None