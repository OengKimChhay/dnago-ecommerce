import os

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django import forms

# Custom import
from .form import (
    RegistrationForm,
    LoginForm,
    UpdateForm,
    ChangePassForm
)
from django.contrib.auth import authenticate, login, logout, get_user_model


# --------------create user------------------
def auth_register(request):
    try:
        breadcrumbs = (
            {'User': ''},
            {'Listing': 'user:auth_listing'},
            {'Create': ''},
        )
        if request.method == 'POST':
            form = RegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'User has been registered.')
                return redirect("user:auth_register")
        else:
            form = RegistrationForm()
        return render(request, 'backEnd/user/create.html', {'form': form, 'breadcrumbs': breadcrumbs})
    except Exception as e:
        messages.error(request, e)
        return redirect("user:auth_listing")


# -------------- listing user -----------------
def auth_listing(request):
    try:
        breadcrumbs = (
            {'User': ''},
            {'Listing': 'user:auth_listing'},
        )
        user_model = get_user_model()
        users = user_model.objects.all()

        search = request.GET.get('search')
        role = request.GET.get('role')
        if search is not None:
            users = users.filter(Q(fullname__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search))
        elif role is not None:
            if role == 'admin':
                users = users.filter(is_admin=1)
            if role == 'customer':
                users = users.filter(is_customer=1)
            if role == 'staff':
                users = users.filter(is_staff=1)
            if role == 'active':
                users = users.filter(is_active=1)
        else:
            search = ''
        return render(request, 'backEnd/user/listing.html', {'users': users, 'search':search, 'breadcrumbs':breadcrumbs})
    except Exception as e:
        messages.error(request, e)
        return redirect("user:auth_listing")


# -------------- view detail user -------------
def auth_view(request, pk):
    try:
        user_model = get_user_model()
        user = user_model.objects.get(id=pk)
        breadcrumbs = (
            {'User': ''},
            {'Listing': 'user:auth_listing'},
            {'View': ''},
            { user.fullname : ''}
        )
        return render(request, 'backEnd/user/view.html', {'user': user, 'breadcrumbs':breadcrumbs})
    except Exception as e:
        messages.error(request, e)
        return redirect("user:auth_listing")


# -------------- update user ----------------
def auth_update(request, pk):
    try:
        user_model = get_user_model()
        user = user_model.objects.get(id=pk)
        breadcrumbs = (
            {'User': ''},
            {'Listing': 'user:auth_listing'},
            {'Update': ''},
            { user.fullname : ''}
        )
        form = UpdateForm(request.POST or None, request.FILES or None, instance=user)

        if user is not None:
            if request.method == 'POST':
                if form.is_valid():
                    old_password = form.cleaned_data["password"]
                    
                    # ----check old password -----
                    if not user.check_password(old_password):
                        messages.error(request, 'Old Password not match.')
                    else:
                        # ----remove old pic------
                        if len(request.FILES) != 0:
                            old_profile = user.profile.path
                            if os.path.exists(old_profile):
                                os.remove(old_profile)
                        form.save()
                        messages.success(request, 'User has been updated.')

            return render(request, 'backEnd/user/update.html', {'form': form, 'old_user': user, 'breadcrumbs':breadcrumbs})
        else:
            messages.error(request, 'Cant find this number.')
            return redirect('user:auth_listing')
    except Exception as e:
        messages.error(request, e)
        return redirect("user:auth_listing")


# --------------- change password ----------
def auth_change_password(request, pk):
    try:
        user_model = get_user_model()
        user = user_model.objects.get(id=pk)
        breadcrumbs = (
            {'User': ''},
            {'Listing': 'user:auth_listing'},
            {'Update': ''},
            { user.fullname : ''}
        )
        form = ChangePassForm(request.POST , instance=user)

        if user is not None:
            if request.method == 'POST':
                if form.is_valid():
                    old_password = form.cleaned_data["password"]
                    
                    # ----check old password -----
                    if not user.check_password(old_password):
                        messages.error(request, 'Old Password not match.')
                    else:
                        form.save()
                        messages.success(request, 'Paasword has been updated.')

            return render(request, 'backEnd/user/change_password.html', {'form': form, 'old_user': user, 'breadcrumbs':breadcrumbs})
        else:
            messages.error(request, 'Cant find this number.')
            return redirect('user:auth_listing')

    except Exception as e:
        messages.error(request, e)
        return redirect("user:auth_listing")


# -------------- delete user ---------------
def auth_delete(request, pk):
    user_model = get_user_model()
    user = user_model.objects.get(id=pk)
    if user is not None:
        old_profile = user.profile.path
        if os.path.exists(old_profile):
            os.remove(old_profile)
        user.delete()
        messages.success(request, f'{user.fullname} has been deleted.')
    return redirect("user:auth_listing")


# -------------- login user -----------------
def auth_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                user = authenticate(email=email, password=password)
                if user is not None:
                    if user.is_admin:
                            login(request, user)
                            return redirect('manageStores:dashboard')
                    else:
                        messages.error(request, 'Sorry your account does\'nt have any permissions to access. Your\'re not Admin')
                else:
                    messages.error(request, mark_safe('Invalid username or password. <br/> <small style="font-size:12px;">Note: Your account can be Inactive.</small>'))
            except Exception as e:
                            messages.error(request, 'There is something wrong with your account. please try again.')   
    else:
        form = LoginForm()
    return render(request, 'backEnd/user/login.html', {'form': form})


# ------------- logout user ----------------
def auth_logout(request):
    logout(request)
    return redirect("user:auth_login")
