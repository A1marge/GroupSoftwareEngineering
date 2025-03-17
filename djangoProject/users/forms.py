from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile


class SignUpForm(UserCreationForm):
    tc_consent = forms.BooleanField(
        required=True,
        label="I agree to the processing of my personal data in accordance with the GDPR.",
        help_text="You must agree to our terms to create an account."
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'tc_consent')


class ProfileUpdateForm(forms.ModelForm):
    """Form to update username and email."""
    class Meta:
        model = User
        fields = ['username', 'email']

class TCConsentForm(forms.ModelForm):
    """Form to handle T&Cs consent."""
    class Meta:
        model = UserProfile
        fields = ['tc_consent']



class CustomSignUpForm(UserCreationForm):
    tc_consent = forms.BooleanField(
        required=True,
        label="I agree to the processing of my personal data in accordance with the T&Cs.",
        help_text="You must agree to our terms to create an account."
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'tc_consent')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Passwords do not match")
            if len(password1) < 8:
                raise ValidationError("Password must be at least 8 characters long")
            if not any(char.isdigit() for char in password1):
                raise ValidationError("Password must contain at least one digit")
            if not any(char.isalpha() for char in password1):
                raise ValidationError("Password must contain at least one letter")
            
            

        return password2