from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.users.models import UserProfile


class SignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')  # Ensure this matches your `urls.py`

    def test_signup_GET(self):
        """Test that the signup page loads correctly"""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup_new.html')

    def test_signup_POST_valid(self):
        """Test signing up with valid data"""
        response = self.client.post(self.signup_url, {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
            'tc_consent': True  # Assuming this field is in SignUpForm
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())  # User created
        self.assertTrue(UserProfile.objects.filter(user__username='testuser').exists())  # UserProfile created

    def test_signup_POST_invalid(self):
        """Test signup with invalid data"""
        response = self.client.post(self.signup_url, {
            'username': 'short',
            'email': 'invalid-email',
            'password1': 'pass',
            'password2': 'mismatch',
            'gdpr_consent': False
        })
        self.assertEqual(response.status_code, 200)  # Should stay on same page
        self.assertFalse(get_user_model().objects.filter(username='short').exists())  # No user created


class DeleteAccountViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_delete_account(self):
        """Test that the user can delete their account"""
        response = self.client.post(reverse('delete_account'))  # Ensure URL name is correct
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(get_user_model().objects.filter(username='testuser').exists())  # User deleted

class EditProfileViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='old@example.com', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_edit_profile_GET(self):
        """Test rendering the profile page"""
        # Send GET request to the profile page
        response = self.client.get(reverse('profile'))

        # Ensure the response is a success (200)
        self.assertEqual(response.status_code, 200)

        # Ensure the user context is passed correctly to the template
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.email)

class StaticViewsTest(TestCase):
    def test_landing_page(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/landing.html')

    def test_privacy_policy_page(self):
        response = self.client.get(reverse('privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/privacy_policy.html')

