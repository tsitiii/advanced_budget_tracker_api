from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.utils import timezone
import uuid

class PasswordResetCode(models.Model):
    user = models.ForeignKey('auth_feature.User', on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)

    def __str__(self):
        return f"{self.user.email} - {self.code}"


class User(AbstractUser):
    full_name = models.CharField(max_length=100,db_index=True)
    email  = models.EmailField(unique=True)
    
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.full_name
