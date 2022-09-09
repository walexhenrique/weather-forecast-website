from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, redirect, render
from django.core.validators import validate_email
from slugify import slugify


# Create your views here.
def login(request):
    if request.method != 'POST':

        # User logged don't can login again
        if request.user.is_authenticated:
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

    if request.method != 'POST':
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')

        return render(request, 'accounts/register.html', {'title': 'Crie a sua conta'})
    
    username = request.POST.get('username')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password_1 = request.POST.get('password_1')
    password_2 = request.POST.get('password_2')

    if not username or not first_name or not last_name or not email or not password_1 or not password_2:
        return render(request, 'accounts/register.html', {'title':'Crie a sua conta'})

    try:
        validate_email(email)
    except:
        return render(request, 'accounts/register.html', {'title':'Crie a sua conta'})

    if len(username) < 5:
        return render(request, 'accounts/register.html', {'title':'Crie a sua conta'})
    
    if User.objects.filter(username=username).exists():
        return render(request, 'accounts/register.html', {'title':'Crie a sua conta'})
    
    if User.objects.filter(email=email).exists():
        return render(request, 'accounts/register.html', {'title':'Crie a sua conta'})
    
    if len(password_1) < 5 or len(password_2) < 5:
        return render(request, 'accounts/register.html', {'title':'Crie a sua conta'})
    
    if password_1 != password_2:
        return render(request, 'accounts/register.html', {'title':'Crie a sua conta'})

    new_user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password_1)
    new_user.save()
    return redirect('accounts:login')

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
