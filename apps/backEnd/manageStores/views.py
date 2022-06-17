from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages

# Custom import
from .models import Category, Product
from .form import (
    CategoryForm
)


# ----------------------------------- Category -------------------------------------
def category_listing(request):
    search = request.GET.get('search')
    categories = Category.objects.all()
    if search is not None:
        categories = categories.filter(Q(name__icontains=search) | Q(slug__icontains=search))
    return render(request, 'backEnd/category/listing.html', {'categories': categories, 'search': search})


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category has been created.')
            return redirect("manageStores:category_create")
    else:
        form = CategoryForm()
    return render(request, 'backEnd/category/create.html', {'form': form})


def category_update(request,pk):
    try:
        category = Category.objects.get(id=pk)
        form = CategoryForm(request.POST or None, instance=category)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Category has been updated.')
        return render(request, 'backEnd/category/update.html', {'form': form})
    except Exception as e:
        messages.error(request, e)
        return redirect("manageStores:category_listing")

# ----------------------------------- Dashhboard -----------------------------------
def dashboard(request):
    return render(request, 'backEnd/dansboard.html')


# ----------------------------------- Product --------------------------------------
def create_product(request):
    return HttpResponse('hello')
