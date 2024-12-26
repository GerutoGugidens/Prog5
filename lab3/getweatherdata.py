def get_weather_data(city, key):
    import requests
    import json
    query = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={key}&lang=RU"
    r = requests.get(query)
    data = r.text
    result_json = json.loads(data)
    result_json = {
        'name': result_json['name'],
        'country': result_json['sys']['country'],
        'coord': result_json['coord'],
        'humidity': result_json['main']['humidity'],
        'feels_like': result_json['main']['feels_like'],
        'pressure': result_json['main']['pressure'],
        'speed_wind': result_json['wind']['speed']
    }
    return result_json
