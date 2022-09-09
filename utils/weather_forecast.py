import math
from datetime import datetime
from threading import Thread
from typing import Dict, List, Union
from slugify import slugify
import requests


class CityWeather:
    url: str = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&units=metric&lang=pt_br'
    key: str = '33144145c7a985b35257ce805cc01845'

    def __init__(self, city: str) -> None:
        self.city: str = city.replace('-', ' ').capitalize()
        self.city_name: str = ''
        self.weathers: List[Dict] = []
        self.slug: str = ''

    def connect_api(self) -> bool:
        try:
            response_weather = requests.get(self.url.format(self.city, self.key)).json()
            

            if response_weather['cod'] != '200':
                return False
            
            self._add_weather_in_list(response_weather)
            self.city_name = response_weather['city']['name']
            self.slug = slugify(self.city_name)
            
            print(f'entrei na: {self.city} {datetime.now()}')
            return True
        except requests.exceptions.ConnectionError:
            return False
        except Exception as e:
            print(e)
            return False
    
    def _add_weather_in_list(self, dict_weathers: Dict) -> None:
        for weather_forecast in dict_weathers['list']:
            self.weathers.append(
                {
                'temp': math.floor(weather_forecast['main']['temp']),
                'feels_like': math.floor(weather_forecast['main']['feels_like']),
                'humidity': weather_forecast['main']['humidity'],
                'description': weather_forecast['weather'][0]['description'],
                'icon': weather_forecast['weather'][0]['icon'],
                'date': self.config_date_brazilian(weather_forecast['dt_txt']),
                'hour': self.config_hour_brazilian(weather_forecast['dt_txt']),
                }
            )

    @staticmethod
    def config_date_brazilian(date: str) -> str:
        date_converted = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return datetime.strftime(date_converted, '%d/%m/%Y')
    
    @staticmethod
    def config_hour_brazilian(date: str) -> str:
        hour_converted = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return datetime.strftime(hour_converted, '%H:%M')
    

class CityWeatherFactory:
    @staticmethod
    def get_city(name: str) -> Union[CityWeather, None]:
        city = CityWeather(name)
        return city


class CityThread(Thread):
    def __init__(self, city: CityWeather) -> None:
        self.city = city
        super().__init__()

    def run(self) -> None:
        self.city.connect_api()