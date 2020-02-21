from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name = 'main-home'),
    path('cpu/', views.cpu, name = 'cpu-home')
]
