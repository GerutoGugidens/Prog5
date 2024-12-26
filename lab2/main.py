import requests

from secret import api_key
import json
from urllib import request
from getweatherdata import get_raw_weather_data

def format_data(weather_data: dict):
    print(f'Город: {weather_data["name"]}')
    print(f'Страна: {weather_data["sys"]["country"]}')
    print(f'Долгота: {weather_data["coord"]["lon"]}')
    print(f'Широта: {weather_data["coord"]["lat"]}')
    time_zone = weather_data['timezone']
    utc_offset = time_zone / 3600
    print(f'Временная зона: UTC{utc_offset:+.0f}')
    print(f'Ощущается как: {round(weather_data["main"]["feels_like"], 2)}°C')

if __name__ == '__main__':
    format_data(get_raw_weather_data('Moscow', api_key))
    print("\n\n")
    format_data(get_raw_weather_data('Saint Petersburg', api_key))
    print("\n\n")
    format_data(get_raw_weather_data('Chicago', api_key))
    print("\n\n")
    format_data(get_raw_weather_data('Daci', api_key))
