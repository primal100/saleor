from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model

User = get_user_model()

class UserPreferences(models.Model):
    user = models.OneToOneField(User, related_name="preferences", blank=True, null=True, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, related_name="preferences", blank=True, null=True, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3)
