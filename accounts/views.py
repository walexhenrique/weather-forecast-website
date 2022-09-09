from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, redirect, render
from slugify import slugify


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

def logout(request):
    auth.logout(request)
    return redirect('home:index')

def register(request):
    return HttpResponse('TEMPORARIO')

@login_required(login_url='accounts:login')
def dashboard(request):
    
    if request.method == 'POST':
        city = request.POST.get('search')
        city_slugify = slugify(city)
        return redirect('accounts:about_city', city=city_slugify)
    
    user = auth.get_user(request)
    cities = user.cities.all()

    return render(request, 'accounts/dashboard.html', 
    {
        'title': f'Dashboard | {user.first_name}',
        'cities': cities
    })

def about_city(request, city):
    return HttpResponse(f'TEMPORARIO {city}')
