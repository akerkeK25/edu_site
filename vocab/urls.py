from django.urls import path
from . import views

app_name = 'vocab'

urlpatterns = [
    path('', views.deck_list, name='deck_list'),
    path('card/add/', views.card_create, name='card_create'),
    path('csv/upload/', views.upload_csv, name='upload_csv'),
    path('study/<int:deck_id>/', views.study, name='study'),
    path('study/<int:deck_id>/check/', views.check_answer, name='check_answer'),
]
