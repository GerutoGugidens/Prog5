import requests
import matplotlib.pyplot as plt
import datetime
from secret import api_key
def get_forecast_weather_data(lat, lon, key):
    """Получение прогнозных данных о погоде через OpenWeather API."""
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': key,
        'units': 'metric',
        'lang': 'RU'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при запросе данных: {response.status_code}")
        return None

def process_forecast_data(forecast_data):
    """Извлечение температур и времени из прогнозных данных."""
    temps = []
    times = []
    if 'list' in forecast_data:
        for entry in forecast_data['list']:
            temps.append(entry['main']['temp'])
            times.append(datetime.datetime.fromtimestamp(entry['dt']))
    return temps, times

def plot_weather_data(temps, times):
    """Построение scatterplot и boxplot."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    axes[0].scatter(times, temps, alpha=0.6, color='blue')
    axes[0].set_title("Температура за прогнозный период (scatterplot)")
    axes[0].set_xlabel("Время")
    axes[0].set_ylabel("Температура, °C")
    axes[0].grid()

    axes[1].boxplot(temps, vert=False, patch_artist=True, boxprops={'facecolor': 'lightblue'})
    axes[1].set_title("Распределение температуры (boxplot)")
    axes[1].set_xlabel("Температура, °C")

    plt.tight_layout()
    plt.show()

# Основной блок выполнения
if __name__ == "__main__":
    global api_key
    city = "Москва"

    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={api_key}"
    geocode_response = requests.get(geocode_url)
    if geocode_response.status_code == 200:
        city_data = geocode_response.json()
        if city_data:
            lat = city_data[0]['lat']
            lon = city_data[0]['lon']

            forecast_data = get_forecast_weather_data(lat, lon, api_key)
            if forecast_data:
                temps, times = process_forecast_data(forecast_data)
                plot_weather_data(temps, times)
        else:
            print("Не удалось найти координаты города.")
    else:
        print(f"Ошибка при запросе координат города: {geocode_response.status_code}")