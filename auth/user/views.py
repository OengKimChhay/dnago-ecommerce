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
    search = request.GET.get('search')
    if search is not None:
        users = user_model.objects.filter(Q(fullname__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search))
    else:
        users = user_model.objects.all()
    return render(request, 'manage_store/user/listing.html', {'users': users})


def auth_view(request, pk):
    user_model = get_user_model()
    user = user_model.objects.get(id=pk)
    return HttpResponse(user)
