from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Product


# Create your views here.
def dashboard(request):
    return render(request, 'manageStores/dansboard.html')


# ----------------------------------- Product -------------------------------------
def create_product(request):
    return HttpResponse('hello')