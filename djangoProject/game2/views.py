from django.shortcuts import render
from django.http import JsonResponse
from users.models import UserProfile
from django.contrib.auth.decorators import login_required
import json

def index(request):
    return render(request, 'game2/templates/index.html')

def check_in(request):
    return render(request, 'game2/templates/index.html')


@login_required
def mark_square(request):
    data = json.loads(request.body)
    challenge = int(data.get("challenge"))
    
    # Get user profile
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Get completed games from database
    completed = user_profile.completed_games if user_profile.completed_games else []
    
    # Add new challenge if not already completed
    if challenge not in completed:
        completed.append(challenge)
        user_profile.completed_games = completed
        user_profile.save()
        
    # Also update session for immediate feedback
    request.session["completed_challenges"] = completed
    
    return JsonResponse({"success": True})