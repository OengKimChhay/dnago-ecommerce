from django.urls import path, include

from . import views

app_name = 'user'

urlpatterns = [
    path('login/',          views.auth_login,       name='auth_login'),
    path('logout/',         views.auth_logout,      name='auth_logout'),
    path('register/',       views.auth_register,    name='auth_register'),
    path('listing/',        views.auth_listing,     name='auth_listing'),
    path('view/<int:pk>/',  views.auth_view,        name='auth_view'),
    path('update/<int:pk>/',views.auth_update,      name='auth_update'),
    path('delete/<int:pk>/',views.auth_delete,      name='auth_delete'),
]