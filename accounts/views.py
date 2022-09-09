from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.shortcuts import HttpResponse, redirect, render
from slugify import slugify
from utils import weather_forecast
from .models import City


# Create your views here.
def login(request):
    if request.method != 'POST':
        
        # User logged don't can login again
        if request.user.is_authenticated:
            messages.add_message(request, messages.INFO, 'Você já está logado')
            return redirect('accounts:dashboard')

        return render(request, 'accounts/login.html', {'title' : 'Login'})
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = auth.authenticate(request, username=username, password=password)
    if not user:
        messages.add_message(request, messages.ERROR, 'username e senha inválidos')
        return render(request, 'accounts/login.html', {'title' : 'Login'})
    
    auth.login(request, user)

    return redirect('accounts:dashboard')

def logout(request):
    messages.add_message(request, messages.SUCCESS, 'Deslogado com sucesso')
    auth.logout(request)
    return redirect('home:index')

def register(request):

    if request.method != 'POST':
        if request.user.is_authenticated:
            messages.add_message(request, messages.INFO, 'Você já está logado')
            return redirect('accounts:dashboard')

        return render(request, 'accounts/register.html', {'title': 'Crie a sua conta'})
    
    username = request.POST.get('username')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password_1 = request.POST.get('password_1')
    password_2 = request.POST.get('password_2')

    if not username or not first_name or not last_name or not email or not password_1 or not password_2:
        messages.add_message(request, messages.ERROR, 'Todos os campos são obrigatórios')
        return render(request, 'accounts/register.html', {'title':'Crie a sua conta'})

    try:
        validate_email(email)
    except:
        messages.add_message(request, messages.ERROR, 'Email inválido')
        return render(request, 'accounts/register.html', {'title':'Crie a sua conta'})

    if len(username) < 5:
        messages.add_message(request, messages.ERROR, 'Nome de usuário precisa ter mais de 5 caracteres')
        return render(request, 'accounts/register.html', {'title':'Crie a sua conta'})
    
    if User.objects.filter(username=username).exists():
        messages.add_message(request, messages.ERROR, 'Username já existente no sistema')
        return render(request, 'accounts/register.html', {'title':'Crie a sua conta'})
    
    if User.objects.filter(email=email).exists():
        messages.add_message(request, messages.ERROR, 'Email já existente no sistema')
        return render(request, 'accounts/register.html', {'title':'Crie a sua conta'})
    
    if len(password_1) < 5 or len(password_2) < 5:
        messages.add_message(request, messages.ERROR, 'O tamanho mínimo da senha é 5 caracteres')
        return render(request, 'accounts/register.html', {'title':'Crie a sua conta'})
    
    if password_1 != password_2:
        messages.add_message(request, messages.ERROR, 'As senhas não correspondem entre si')
        return render(request, 'accounts/register.html', {'title':'Crie a sua conta'})

    new_user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password_1)
    new_user.save()
    messages.add_message(request, messages.SUCCESS, 'Conta criada com sucesso')
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

@login_required(login_url='accounts:login')
def about_city(request, city):

    if request.method == 'POST':
        user = auth.get_user(request)
        city_in_bd = user.cities.filter(slug=city).exists()

        if not city_in_bd:
            messages.add_message(request, messages.SUCCESS, 'Cidade adicionada a sua dashboard')
            
            city_api = weather_forecast.CityWeather(city)
            
            if city_api.connect_api():
                new_city = City.objects.create(name=city_api.city_name, slug=slugify(city_api.city_name), profile=user)
                new_city.save()
        else:
            messages.add_message(request, messages.SUCCESS, 'Cidade removida da sua dashboard')

            City.objects.filter(slug=city).delete()

    user = auth.get_user(request)
    city_in_bd = user.cities.filter(slug=city).exists()
    
    # tem a cidade no banco do usuario
    if city_in_bd:
        city = user.cities.filter(slug=city).first().name
    
    city_api = weather_forecast.CityWeather(city)
    if not city_api.connect_api():
        messages.add_message(request, messages.ERROR, 'Cidade não encontrada')

        return redirect('accounts:dashboard')
        
    return render(request, 'accounts/about.html', {
        'city': city_api, 
        'title': f'Previsão do tempo de {city_api.city}',
        'city_added': city_in_bd,
        })
