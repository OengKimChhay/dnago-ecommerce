from django.urls import path, include
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.auth_register, name='auth_register'),
]

