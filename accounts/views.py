from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, redirect, render


# Create your views here.
def login(request):
    if request.method != 'POST':

        # User logged don't can login again
        if not auth.get_user(request):
            return redirect('accounts:dashboard')

        return render(request, 'accounts/login.html', {'title' : 'Login'})
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = auth.authenticate(request, username=username, password=password)
    if not user:
        return render(request, 'accounts/login.html', {'title' : 'Login'})
    
    auth.login(request, user)

    return redirect('accounts:dashboard')

def register(request):
    return HttpResponse('TEMPORARIO')

def dashboard(request):
    return HttpResponse('Dashboard')

def about_city(request):
    return HttpResponse('TEMPORARIO')
