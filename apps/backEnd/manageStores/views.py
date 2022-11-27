from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
import time

# Custom import
from .models import Category, Product
from .form import (
    CategoryForm
)


# ----------------------------------- Category -------------------------------------
def category_listing(request):
    try:
        breadcrumbs = (
            {'Category': ''},
            {'Listing': 'manageStores:category_listing'}
        )

        categories = Category.objects.all()
        search = request.GET.get('search')
        if search is not None:
            categories = categories.filter(Q(name__icontains=search) | Q(slug__icontains=search))
        else:
            search = ''
        return render(request, 'backEnd/category/listing.html', {
            'categories': categories,
            'search': search,
            'breadcrumbs': breadcrumbs
        })
    except Exception as e:
        messages.error(request, e)
        return redirect("manageStores:category_listing")


def category_create(request):
    try:
        breadcrumbs = (
            {'Category': ''},
            {'Listing': 'manageStores:category_listing'},
            {'Create': ''}
        )

        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Category has been created.')
                return redirect("manageStores:category_create")
        else:
            form = CategoryForm()
        return render(request, 'backEnd/category/create.html', {'form': form,'breadcrumbs': breadcrumbs})
    except Exception as e:
        messages.error(request, e)
        return redirect("manageStores:category_listing")


def category_update(request,pk):
    try:
        category = Category.objects.get(id=pk)
        breadcrumbs = (
            {'Category': ''},
            {'Listing': 'manageStores:category_listing'},
            {'Update': ''},
            { category.name: ''}
        )

        form = CategoryForm(request.POST or None, instance=category)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Category has been updated.')
        return render(request, 'backEnd/category/update.html', {'form': form, 'breadcrumbs': breadcrumbs})
    except Exception as e:
        messages.error(request, e)
        return redirect("manageStores:category_listing")


def category_view(request,slug):
    try:
        category = Category.objects.filter(slug=slug).first()
        breadcrumbs = (
            {'Category': ''},
            {'Listing': 'manageStores:category_listing'},
            {'View': ''},
            {category.name: ''}
        )
        if category:
            return render(request, 'backEnd/category/view.html', {'category': category, 'breadcrumbs':breadcrumbs})
    except Exception as e:
        messages.error(request, e)
        return redirect("manageStores:category_listing")


def category_delete(request,pk):
    try:
        category = Category.objects.get(id=pk)
        if category is not None:
            category.delete()
            messages.success(request, f'Category {category.name} has been deleted.')
        return redirect("manageStores:category_listing")
    except Exception as e:
        messages.error(request, e)
        return redirect("manageStores:category_listing")


# ----------------------------------- Dashhboard -----------------------------------
def dashboard(request):
    return render(request, 'backEnd/dansboard.html')


# ----------------------------------- Product --------------------------------------
def create_product(request):
    return HttpResponse('hello')
