from django.urls import path
from . import views

urlpatterns = [
    # Было: path('stats/', views.stats_view, name='stats')
    path('', views.stats_view, name='stats'), 
    
    # Было: path('stats/charts/', views.stats_charts_view, name='stats_charts')
    path('charts/', views.stats_charts_view, name='stats_charts'), 
]