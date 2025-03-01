from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tc_consent = models.BooleanField(default=False)
    consent_date = models.DateTimeField(auto_now_add=True)
    leafcoins = models.PositiveIntegerField(default=0)
    #two_factor_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile - {self.leafcoins} Leafcoins"
    
class LeafcoinTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    reason = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} Leafcoin for {self.reason} on {self.date}"