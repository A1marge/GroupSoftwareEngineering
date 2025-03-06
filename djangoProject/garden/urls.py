from .views import garden_view
from django.urls import path

urlpatterns = [
    path('', garden_view, name='garden'),
]