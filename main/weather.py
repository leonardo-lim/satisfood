import requests
from decouple import config
from main.location import get_location, geocoding

def check_rain(address, ip_address):
    # Check whether the user input address or not
    if address:
        loc = geocoding(address)
    else:
        loc = get_location(ip_address)

    # Get user location
    lat = loc['lat']
    lon = loc['lon']

    api_key = config('WEATHER_API_KEY')
    api_url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=hourly,minutely&units=metric&appid={api_key}'

    # Request and get weather data
    res = requests.get(api_url)
    data = res.json()

    # Get weather condition
    weather_condition = data['current']['weather'][0]['main']

    # Check whether the weather condition is raining or not
    is_rain = weather_condition == 'Thunderstorm' or weather_condition == 'Drizzle' or weather_condition == 'Rain'

    return is_rain