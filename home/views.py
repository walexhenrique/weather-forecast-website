import random


from django.shortcuts import render
from utils.weather_forecast import CityThread, CityWeatherFactory

capitals = ['Rio branco', 'Maceio', 'Macapá', 'Manaus', 'Fortaleza', 'Brasilia',
                'Vitória', 'Goiânia', 'São Luís', 'Cuiabá', 'Campo Grande', 'Belo Horizonte',
                'Belém', 'João Pessoa', 'Curitiba', 'Recife', 'Teresina', 'Rio de Janeiro', 
                'Natal', 'Porto Alegre', 'Boa Vista', 'Florianópolis', 'São Paulo', 'Aracaju',
                'Palmas'
    ]
# Create your views here.
def index(request):
    
    capitals_random = random.sample(capitals, 6)
    cities = [CityWeatherFactory.get_city(capital) for capital in capitals_random]
    
    cities_thread = [CityThread(city) for city in cities]

    for city_t in cities_thread:
        city_t.start()
    
    for city_t in cities_thread:
        city_t.join()


    return render(request, 'home/index.html', {
        'cities': cities,
        'title': 'Home',
    }
    )
