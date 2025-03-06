from django.shortcuts import render

# Create your views here.
def garden_view(request):
    return render(request, 'garden.html')