from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import logging
from .forms import ProfileUpdateForm, TCConsentForm, CustomSignUpForm
from .models import UserProfile


from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # This sets the session cookie automatically
            return redirect('profile')  # or wherever you want to redirect after login
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'users/templates/registration/login.html')


@login_required
def delete_account(request):
    user = request.user
    logout(request)  # Logs the user out
    user.delete()  # Deletes the user account
    messages.success(request, "Your account has been deleted successfully.")
    return redirect('landing')  # Redirect after deletion

def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Save GDPR consent
            UserProfile.objects.create(user=user, tc_consent=form.cleaned_data['tc_consent'])
            login(request, user)  # Log the user in after signup
            return redirect('home')  # Redirect to the landing page or another page
    else:
        form = CustomSignUpForm()
    return render(request, 'users/signup_new.html', {'form': form})


def home(request):
    return render(request, 'users/sustainhome.html')

def landing(request):
    return render(request, 'users/landing.html')


def terms_and_conditions(request):
    return render(request, 'users/tc.html')

def privacy_policy(request):
    return render(request, 'users/privacy_policy.html')

logger = logging.getLogger(__name__)


'''def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        new_email = request.POST.get('email')

        logger.info(f"User {user.username} changed email to {new_email}")  # Logs changes

        user.email = new_email
        user.save()

        return redirect('profile')  # This should trigger a redirect

    return render(request, 'users/profile.html', {'user': user})'''


@login_required
def profile_view(request):
    """Handles profile updates including GDPR consent."""
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=user)
        tc_form = TCConsentForm(request.POST, instance=user_profile)

        if profile_form.is_valid() and tc_form.is_valid():
            profile_form.save()
            tc_form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')
    else:
        profile_form = ProfileUpdateForm(instance=user)
        tc_form = TCConsentForm(instance=user_profile)

    return render(request, 'users/profile.html', {
        'profile_form': profile_form,
        'tc_form': tc_form
    })

@login_required
def user_data_view(request):
    """GDPR-compliant view to show and export user data."""
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    user_data = {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "date_joined": user.date_joined,
        "last_login": user.last_login,
        "tc_consent": user_profile.tc_consent,
    }

    # Export data as JSON
    if request.GET.get("export") == "json":
        return JsonResponse(user_data, safe=False)

    return render(request, "users/user_data.html", {"user_data": user_data})