from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    # -------------------- Product url----------------------

    path('product/create/', views.create_product, name='create_product'),
]

