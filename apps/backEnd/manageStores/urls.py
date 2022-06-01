from django.urls import path
from . import views

app_name = 'manageStores'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('product/create/', views.create_product, name='create_product'),
]
