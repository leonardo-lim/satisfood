import requests
import urllib
from decouple import config

def get_location():
    api_url = 'https://ipapi.co/json'

    # Request and get location data
    res = requests.get(api_url)
    data = res.json()

    # Store result in Python Dictionary
    loc = {
        'lat': data['latitude'],
        'lon': data['longitude']
    }

    return loc

def geocoding(address):
    # Encode address to URL
    address_url = urllib.parse.quote(address)

    api_key = config('GEO_API_KEY')
    api_url = f'https://api.geoapify.com/v1/geocode/search?text={address_url}&apiKey={api_key}'

    # Request and get location data
    res = requests.get(api_url)
    data = res.json()

    # Store result in Python Dictionary
    loc = {
        'lat': data['features'][0]['properties']['lat'],
        'lon': data['features'][0]['properties']['lon']
    }

    return loc