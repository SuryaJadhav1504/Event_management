# events/authentication.py
from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend
from django.db.models import Q

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(email=email))  # We are using email to look up the user
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
