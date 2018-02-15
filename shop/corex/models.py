from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserPreferences(models.Model):
    user = models.OneToOneField(User, related_name="preferences", blank=True, null=True, on_delete=models.CASCADE)
    sessionid = models.CharField(max_length= 64, blank=True, null=True)
    currency = models.CharField(max_length=3)
