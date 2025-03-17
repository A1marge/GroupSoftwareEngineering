from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='game2_index'),
    path('check-in/', views.check_in, name='game2_check_in'),
    path('mark-square/', views.mark_square, name='game2_mark_square'),
]