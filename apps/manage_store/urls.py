from django.urls import path, include
from . import views

app_name = 'manage_store'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    # -------------------- Product url----------------------

    path('product/create/', views.create_product, name='create_product'),
]

