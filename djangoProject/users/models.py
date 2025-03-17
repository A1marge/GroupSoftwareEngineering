from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tc_consent = models.BooleanField(default=False)
    consent_date = models.DateTimeField(auto_now_add=True)
    completed_games = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"