from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError, transaction

from .models import (
    Company, Investment, MarketEvent, StockPriceHistory, Transaction,
    PortfolioSnapshot, Achievement, UserAchievement
)


class CompanyModelTests(TestCase):
    def test_str_returns_name(self):
        company = Company.objects.create(name="Test Company", current_stock_price=Decimal('100.00'))
        self.assertEqual(str(company), "Test Company")

    def test_price_low_since_set_when_price_below_threshold(self):
        company = Company.objects.create(name="Low Price Co", current_stock_price=Decimal('1.00'))
        self.assertIsNotNone(company.price_low_since)

    def test_price_low_since_reset_when_price_above_threshold(self):
        company = Company.objects.create(name="Low Price Co", current_stock_price=Decimal('1.00'))
        self.assertIsNotNone(company.price_low_since)
        company.current_stock_price = Decimal('100.00')
        company.save()
        self.assertIsNone(company.price_low_since)


class InvestmentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.company = Company.objects.create(name="Test Company", current_stock_price=Decimal('100.00'))

    def test_str_returns_expected_format(self):
        investment = Investment.objects.create(
            user=self.user,
            company=self.company,
            shares=10,
            purchase_price=Decimal('95.00')
        )
        expected_str = f"{self.user.username} - {self.company.name} (10 shares)"
        self.assertEqual(str(investment), expected_str)


class MarketEventModelTests(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test Company", current_stock_price=Decimal('100.00'))
        self.event = MarketEvent.objects.create(
            title="Test Event",
            description="Test Description",
            impact_factor=Decimal('1.00'),
            duration=60
        )
        self.event.companies_affected.add(self.company)

    def test_get_time_left_active(self):
        # Set event_date to 10 minutes ago, so there should be roughly 50 minutes left
        self.event.event_date = timezone.now() - timedelta(minutes=10)
        self.event.save()
        time_left = self.event.get_time_left()
        self.assertIn("minutes left", time_left)

    def test_get_time_left_expired(self):
        # Set event_date to 70 minutes ago, event should be expired
        self.event.event_date = timezone.now() - timedelta(minutes=70)
        self.event.save()
        self.assertEqual(self.event.get_time_left(), "Expired")

    def test_is_active(self):
        self.event.event_date = timezone.now() - timedelta(minutes=10)
        self.event.save()
        self.assertTrue(self.event.is_active())
        self.event.event_date = timezone.now() - timedelta(minutes=70)
        self.event.save()
        self.assertFalse(self.event.is_active())

    def test_end_timestamp(self):
        self.event.event_date = timezone.now()
        self.event.save()
        end_timestamp = self.event.end_timestamp
        expected = int(self.event.event_date.timestamp() + self.event.duration * 60)
        self.assertEqual(end_timestamp, expected)


class StockPriceHistoryModelTests(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test Company", current_stock_price=Decimal('100.00'))

    def test_str_returns_expected_format(self):
        price_history = StockPriceHistory.objects.create(
            company=self.company,
            price=Decimal('99.99')
        )
        expected_str = f"{self.company.name} at {price_history.date}: ${price_history.price}"
        self.assertEqual(str(price_history), expected_str)


class TransactionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.company = Company.objects.create(name="Test Company", current_stock_price=Decimal('100.00'))

    def test_str_returns_expected_format(self):
        transaction = Transaction.objects.create(
            user=self.user,
            company=self.company,
            transaction_type='buy',
            shares=5,
            price_per_share=Decimal('100.00'),
            total=Decimal('500.00')
        )
        expected_str = f"{self.user.username} buy 5 shares of {self.company.name} at {transaction.timestamp}"
        self.assertEqual(str(transaction), expected_str)


class PortfolioSnapshotModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_str_returns_expected_format(self):
        snapshot = PortfolioSnapshot.objects.create(
            user=self.user,
            total_value=Decimal('1000.00')
        )
        expected_str = f"{self.user.username} - ${snapshot.total_value} at {snapshot.timestamp}"
        self.assertEqual(str(snapshot), expected_str)


class AchievementModelTests(TestCase):
    def test_str_returns_name(self):
        achievement = Achievement.objects.create(
            name="Green Investor",
            description="Invest in sustainable companies",
            threshold=Decimal('1000.00')
        )
        self.assertEqual(str(achievement), "Green Investor")


class UserAchievementModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.achievement = Achievement.objects.create(
            name="Green Investor",
            description="Invest in sustainable companies",
            threshold=Decimal('1000.00')
        )

    def test_str_returns_expected_format(self):
        user_achievement = UserAchievement.objects.create(
            user=self.user, achievement=self.achievement
        )
        expected_str = f"{self.user.username} - {self.achievement.name}"
        self.assertEqual(str(user_achievement), expected_str)

    def test_unique_constraint(self):
        UserAchievement.objects.create(user=self.user, achievement=self.achievement)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                UserAchievement.objects.create(user=self.user, achievement=self.achievement)