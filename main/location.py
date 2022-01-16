import requests

def get_location():
    api_url = 'https://ipapi.co/json'
    res = requests.get(api_url)
    data = res.json()

    loc = {
        'lat': data['latitude'],
        'lon': data['longitude']
    }

    return loc