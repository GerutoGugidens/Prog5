import os
from secret import api_key


def get_raw_weather_data(city, key):
    import requests
    import json
    if type(city) is not str:
        raise ValueError('параметр city не является строкой')
    if not key:
        raise ValueError('ключ для отправки запросов к API не задан')

    query = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={key}&lang=RU"
    try:
        r = requests.get(query)
    except requests.RequestException as e:
        print(f'Ошибка отправки или получения ответа от API openweathermap.org  ')
    else:
        if r.status_code == 200:
            data = r.text
            # return data
            return json.loads(data)
        if r.status_code == 404:
            print(f'В параметрах запроса (вероятно, в параметре город - ошибка. Ответ 404')