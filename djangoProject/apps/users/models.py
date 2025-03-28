from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tc_consent = models.BooleanField(default=False)
    consent_date = models.DateTimeField(auto_now_add=True)
    friends = models.ManyToManyField("self", symmetrical=False, blank=True)
    bingo_board = models.JSONField(default=list)

    # Stats 
    total_crates_opened = models.PositiveIntegerField(default=0)
    total_garden_plants = models.PositiveIntegerField(default=0)
    most_used_garden_crop = models.CharField(max_length=50, blank=True)

    # 🎰 Casino stats
    total_casino_games_played = models.PositiveIntegerField(default=0)
    total_casino_wagered = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_casino_green_bets = models.PositiveIntegerField(default=0)
    total_casino_green_fund_donated = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_casino_wins = models.PositiveIntegerField(default=0)

    # 🧪 Crafting stats
    total_items_crafted = models.PositiveIntegerField(default=0)
    rare_items_crafted = models.PositiveIntegerField(default=0)
    most_crafted_item = models.CharField(max_length=100, blank=True)

    # ⚔️ Climate duels stats
    climate_duels_played = models.PositiveIntegerField(default=0)
    climate_duels_won = models.PositiveIntegerField(default=0)
    climate_duel_eco_score = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    def add_friend(self, friend):
        """Add a friend (if not already friends)."""
        if friend not in self.friends.all():
            self.friends.add(friend)
            friend.friends.add(self)
            return True
        return False

    def has_sent_request(self, to_user):
        """Check if a friend request has already been sent."""
        return FriendRequest.objects.filter(from_user=self, to_user=to_user).exists()

    def has_received_request(self, from_user):
        """Check if there is a pending friend request from this user."""
        return FriendRequest.objects.filter(from_user=from_user, to_user=self).exists()

    def remove_friend(self, friend):
        """Removes a friend."""
        if friend in self.friends.all():
            self.friends.remove(friend)
            friend.friends.remove(self)
            return True
        return False

    # Existing currency
    currency_balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    # New currency (farm-generated)
    farm_currency = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    total_experience = models.IntegerField(default=0)
    experience_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    # Methods for regular currency (unchanged)
    def add_currency(self, amount, description="Credit added", is_farm_currency=False):
        """Add currency, with optional farm currency support."""
        from django.db import transaction
        amount = Decimal(amount)
        
        with transaction.atomic():
            if is_farm_currency:
                self.farm_currency += amount
                self.save()
                FarmCurrencyTransaction.objects.create(
                    profile=self,
                    transaction_type='credit',
                    amount=amount,
                    description=description
                )
            else:
                self.currency_balance += amount
                self.save()
                CurrencyTransaction.objects.create(
                    profile=self,
                    transaction_type='credit',
                    amount=amount,
                    description=description
                )

    def deduct_currency(self, amount, description="Debit applied"):
        """Deduct currency but prevent negative values."""
        from django.db import transaction
        amount = Decimal(amount)

        if amount <= 0:  # Prevent invalid deductions
            return False  

        with transaction.atomic():
            if self.currency_balance >= amount:
                self.currency_balance -= amount
                self.save()
                CurrencyTransaction.objects.create(
                    profile=self,
                    transaction_type='debit',
                    amount=amount,
                    description=description
                )
                return True
            return False

    # Methods for new farm currency
    def add_farm_currency(self, amount, description="FarmCoin added"):
        """Add the new farm currency to the user's balance."""
        from django.db import transaction
        amount = Decimal(amount)
        with transaction.atomic():
            self.farm_currency += amount
            self.save()
            FarmCurrencyTransaction.objects.create(
                profile=self,
                transaction_type='credit',
                amount=amount,
                description=description
            )

    def deduct_farm_currency(self, amount, description="FarmCoin spent"):
        """Deduct the farm currency for purchases."""
        from django.db import transaction
        amount = Decimal(amount)
        with transaction.atomic():
            if self.farm_currency >= amount:
                self.farm_currency -= amount
                self.save()
                FarmCurrencyTransaction.objects.create(
                    profile=self,
                    transaction_type='debit',
                    amount=amount,
                    description=description
                )
                return True
            return False

    def get_required_xp(self, level):
        # For level 1, the requirement is 100 XP; for higher levels, an exponential formula.
        return int(100 * (1.5 ** (level - 1)))
    
    def add_experience(self, amount):
        if amount < 0:
            return  # Optionally handle negative values
        self.total_experience += amount
        
        level = 1
        xp_remaining = self.total_experience
        while xp_remaining >= self.get_required_xp(level):
            required = self.get_required_xp(level)
            if xp_remaining < required:
                break
            xp_remaining -= required
            level += 1
        
        self.level = level
        self.experience_points = xp_remaining
        self.save()
    

    def check_achievements(self):
        from django.utils.timezone import now
        from .achievements import ACHIEVEMENT_CONDITIONS
        awarded = False
        for achievement in Achievement.objects.all():
            condition = ACHIEVEMENT_CONDITIONS.get(achievement.name)
            if condition and condition(self):
                if not self.user_achievements.filter(achievement=achievement).exists():
                    self.achievements.add(achievement, through_defaults={'date_awarded': now()})
                    awarded = True
                    print(f"Awarded achievement: {achievement.name} to user: {self.user.username}")
        if not awarded:
            print("No new achievements awarded for user:", self.user.username)

    def calculate_green_impact(self):
        # Sum over each investment: sustainability_rating * shares
        total = Decimal('0.00')
        for investment in self.user.investments.all():
            total += investment.company.sustainability_rating * investment.shares
        return total

    def get_stats(self):
        return {
            "username": self.user.username,
            "currency_balance": self.currency_balance,
            "farm_currency": self.farm_currency,
            "level": self.level,
            "experience_points": self.experience_points,
            "total_experience": self.total_experience,
            "green_impact": self.calculate_green_impact(),
            "achievements": list(self.achievements.select_related("achievement").all()),
            "friends": self.friends.all()
        }

class CurrencyTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
         ('credit', 'Credit'),
         ('debit', 'Debit'),
    )
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f"{self.profile.user.username} {self.transaction_type} {self.amount} on {self.created_at}"

class FarmCurrencyTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="farm_transactions")
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.user.username} {self.transaction_type} {self.amount} on {self.created_at}"
    
class Achievement(models.Model):
    """Defines a list of achievements users can earn."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    xp_reward = models.IntegerField(default=0)  # XP gained when unlocking
    coin_reward = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))  # Coins gained
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    """Tracks which users have earned which achievements."""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="achievements")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_awarded = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')  # Prevent duplicate achievements

    def __str__(self):
        return f"{self.user.user.username} earned {self.achievement.name} on {self.date_awarded}"

@classmethod
def get_top_users(cls, limit=10):
    """Returns the top users by level and XP."""
    return cls.objects.order_by('-level', '-experience_points')[:limit]

class FriendRequest(models.Model):
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sent_requests")
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="received_requests")
    timestamp = models.DateTimeField(auto_now_add=True)

    def accept(self):
        """Accept a friend request."""
        self.to_user.add_friend(self.from_user)
        self.delete()

    def decline(self):
        """Decline a friend request."""
        self.delete()