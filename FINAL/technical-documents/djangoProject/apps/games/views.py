from django.shortcuts import render
from django.http import JsonResponse
from ..bingo.views import markSquare
from ..users.models import UserProfile
from django.http import JsonResponse
import json

# Game 1 : QUIZ
def quiz_view(request):
    # Set of questions for the quiz
    questions = [
        {"text": "When does the University aim to be net zero?", "answer": "2030"},
        {"text": "What system does the University use to integrate sustainability (acronym)?", "answer": "EMS"},
        {"text": "What kind of emergency did the University declare in 2019?", "answer": "Climate"},
        {"text": "What is the name of Exeter's sustainability goal for the long-term?", "answer": "Strategy2030"},
        {"text": "Which Exeter campus leads sustainability?", "answer": "Penryn"},
        {"text": "How many UN Sustainability Development Goals are there?", "answer": "17"},
        {"text": "What is Exeter Univerisities biodiversity action plan called?", "answer": "Nature"},

    ]
    if request.method == 'POST':
        correct_answers = 0
        total_questions = len(questions)

        # Checks the users correct answers
        for i, question in enumerate(questions):
            user_answer = request.POST.get(f'question_{i}')
            if user_answer and user_answer.strip().lower() == question["answer"].lower():
                correct_answers += 1

        # If the user got all questions right, mark the square as done.
        if(correct_answers == total_questions):
            markSquare("1", UserProfile.objects.get(user=request.user))

        # renders the results
        return render(request, 'games/quiz_result.html', {
            'correct_answers': correct_answers,
            'total_questions': total_questions,
        })

    # renders the quiz questions
    return render(request, 'games/quiz.html', {'questions': questions})


# Game 2 : RECYCLE SORT
def recycle_sort(request):
    return render(request, 'games/recycle_sort.html')

# Game 3 : ECO RUNNER
def eco_runner(request):
    return render(request, 'games/eco_runner.html')

# Game 4 : ECO MATCH
def eco_memory(request):
    return render(request, 'games/eco_memory.html')

#game 5 : GPS 1
def gps_game(request):
    return render(request, 'games/gps_game.html')

#game 6 : GPS 2
def gps_game2(request):
    return render(request, 'games/gps_game2.html')

# Game 7 : GPS 3
def gps_game3(request):
    return render(request, 'games/gps_game3.html')

# Game 8 : GPS 4
def gps_game4(request):
    return render(request, 'games/gps_game4.html')

# Game 9 : GPS 5
def gps_game5(request):
    return render(request, 'games/gps_game5.html')

# Game 10 : Youtube Video 1
def video1(request):
    markSquare("10", UserProfile.objects.get(user=request.user))
    return render(request, 'games/video1.html')

# Game 11 : Youtube Video
def video2(request):
    markSquare("11", UserProfile.objects.get(user=request.user))
    return render(request, 'games/video2.html')

# Game 12 : Article1
def article1(request):
    markSquare("12", UserProfile.objects.get(user=request.user))
    return render(request, 'games/article1.html')

# Game 13 : Article2
def article2(request):
    markSquare("13", UserProfile.objects.get(user=request.user))
    return render(request, 'games/article2.html')

# Game 14 : Article3
def article3(request):
    markSquare("14", UserProfile.objects.get(user=request.user))
    return render(request, 'games/article3.html')

# Game 15 : Article4
def article4(request):
    markSquare("15", UserProfile.objects.get(user=request.user))
    return render(request, 'games/article4.html')

# Game 16 : Article5
def article5(request):
    markSquare("16", UserProfile.objects.get(user=request.user))
    return render(request, 'games/article5.html')


#@login_required
def mark_square_ajax(request):
    """
    Marks a bingo square based on the challenge name provided in the request.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Get JSON data from the request
            challenge_name = data.get("challenge", None)  # Extract challenge name

            if not challenge_name:
                return JsonResponse({"status": "error", "message": "Missing challenge name."}, status=400)

            user_profile = UserProfile.objects.get(user=request.user)
            markSquare(challenge_name, user_profile)  # Pass dynamic challenge name
            return JsonResponse({"status": "success", "message": f"Square '{challenge_name}' marked as done!"})
        
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data."}, status=400)
        except UserProfile.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User profile not found."}, status=404)
    
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)
