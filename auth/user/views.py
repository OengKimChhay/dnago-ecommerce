from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .form import UserForm
from django.contrib.auth import authenticate, login, logout, get_user_model


# Create your views here.
def auth_register(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'User has been registered.')
                return redirect("user:auth_register")
        except Exception as e:
            return HttpResponse(e)
    else:
        form = UserForm()
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
        if role == 'verify':
            users = users.filter(is_verified=1)
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
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User has been updated.')
            return redirect("user:auth_register")
    return render(request, 'manage_store/user/create.html', {'form': form})


def auth_delete(request, pk):
    user_model = get_user_model()
    user = user_model.objects.get(id=pk)
    if user:
        user.delete()
        messages.success(request, f'{user.fullname} has been deleted.')
    return redirect("user:auth_listing")


def auth_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_admin:  # check if user is_admin
                login(request, user)
                return redirect('manage_store:dashboard')
            else:
                messages.error(request, 'Sorry this user is admin')
        else:
            messages.error(request, 'Invalid user name or password')
    return render(request, 'manage_store/user/login.html')
