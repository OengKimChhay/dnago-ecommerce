from django.http import HttpResponse
from django.shortcuts import render
from .form import UserForm


# Create your views here.
def auth_register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        try:
            if form.is_valid():
                return HttpResponse('sd')
        except Exception as e:
            return HttpResponse(e)
    else:
        form = UserForm()
    return render(request, 'manage_store/user/create.html', {'form': form})
