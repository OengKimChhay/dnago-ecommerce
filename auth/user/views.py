import os

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
# Custom import
from .form import (
    RegistrationForm,
    LoginForm,
    UpdateForm
)
from django.contrib.auth import authenticate, login, logout, get_user_model


# Create your views here.
def auth_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'User has been registered.')
            return redirect("user:auth_register")
    else:
        form = RegistrationForm()
    return render(request, 'manage_store/user/create.html', {'form': form})


def auth_listing(request):
    user_model = get_user_model()
    users = user_model.objects.all()

    search = request.GET.get('search')
    role = request.GET.get('role')
    if search is not None:
        users = users.filter(Q(fullname__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search))
    if role is not None:
        if role == 'admin':
            users = users.filter(is_admin=1)
        if role == 'customer':
            users = users.filter(is_customer=1)
        if role == 'staff':
            users = users.filter(is_staff=1)
        if role == 'active':
            users = users.filter(is_active=1)
    else:
        users = user_model.objects.all()
    return render(request, 'manage_store/user/listing.html', {'users': users})


def auth_view(request, pk):
    user_model = get_user_model()
    user = user_model.objects.get(id=pk)
    return render(request, 'manage_store/user/view.html', {'user': user})


def auth_update(request, pk):
    user_model = get_user_model()
    user = user_model.objects.get(id=pk)
    form = UpdateForm(request.POST or None, request.FILES or None, instance=user)
    if user is not None:
        if request.method == 'POST':
            try:
                if form.is_valid():
                    # ----remove old pic------
                    if len(request.FILES) != 0:
                        old_profile = user.profile.path
                        if os.path.exists(old_profile):
                            os.remove(old_profile)
                    form.save()
                    messages.success(request, 'User has been updated.')
                    return render(request, 'manage_store/user/update.html', {'form': form, 'old_profile': user})
            except Exception as e:
                messages.error(request, e)
                return render(request, 'manage_store/user/update.html', {'form': form, 'old_profile': user})

        return render(request, 'manage_store/user/update.html', {'form': form, 'old_profile': user})
    else:
        messages.error(request, 'Cant find this number.')
        return redirect('user:auth_listing')


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


def auth_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            checkUser = get_user_model().objects.get(email=email)
            if checkUser.is_active:
                user = authenticate(email=email, password=password)
                if user is not None:
                    if user.is_active:  # check if user is_admin
                        if user.is_admin:
                            login(request, user)
                            return redirect('manage_store:dashboard')
                        else:
                            messages.error(request, 'Sorry this user is not admin')
                    else:
                        messages.error(request, 'Sorry this user is not Inactivate')
                else:
                    messages.error(request, 'Invalid user name or password')
            else:
                messages.error(request, 'Sorry this user is  Inactivate')
    else:
        form = LoginForm()
    return render(request, 'manage_store/user/login.html', {'form': form})


def auth_logout(request):
    logout(request)
    return redirect("user:auth_login")
