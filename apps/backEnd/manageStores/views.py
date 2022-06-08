from django.shortcuts import render
from django.http import HttpResponse

# Custom import
from .models import Category, Product
from .form import (
    CategoryForm
)

# ----------------------------------- Category -------------------------------------
def category_listing(request):
    category = Category.objects.all()
    return render(request, 'backEnd/category/listing.html', {'category': category})

def category_create(request):
    form = CategoryForm()
    return render(request, 'backEnd/category/create.html', {'form': form})

# ----------------------------------- Dashhboard -----------------------------------
def dashboard(request):
    return render(request, 'backEnd/dansboard.html')


# ----------------------------------- Product --------------------------------------
def create_product(request):
    return HttpResponse('hello')
