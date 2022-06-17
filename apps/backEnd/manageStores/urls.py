from django.urls import path,include
from . import views

app_name = 'manageStores'

# ------------------------ category ----------------------
category = [
    path('listing/',        views.category_listing, name='category_listing'),
    path('create/',         views.category_create,  name='category_create'),
    path('update/<int:pk>/',views.category_update,  name='category_update'),
]

urlpatterns = [
    # -------------------- dashboard ---------------------
    path('dashboard/', views.dashboard, name='dashboard'),
    # -------------------- category ----------------------
    path('category/', include(category)),

    path('product/create/', views.create_product, name='create_product'),


]
