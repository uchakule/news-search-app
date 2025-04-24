from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.search_news, name='search_news'),
    path('history/', views.history, name='search_history'),
    path('refresh/<str:keyword>/', views.refresh_news, name='refresh_news'),
]