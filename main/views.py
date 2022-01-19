from django.shortcuts import render
from datetime import date
from main.main import *

def index(response):
    return render(response, 'main/layouts/base.html', { 'layout': 'index', 'year': date.today().year })

def result(response):
    prev_restaurant = {}

    # Check whether the user is new or not
    if prev_restaurant:
        result = recommend_restaurants(prev_restaurant)
    else:
        result = show_restaurants()

    # Check whether the weather condition is raining or not
    if result['is_rain']:
        is_rain = True
        rain_food_restaurants = result['rain_food_restaurants']
        non_rain_food_restaurants = result['non_rain_food_restaurants']

        return render(response, 'main/layouts/base.html', { 'rain_food_restaurants': rain_food_restaurants, 'non_rain_food_restaurants': non_rain_food_restaurants, 'is_rain': is_rain, 'layout': 'result', 'year': date.today().year })
    else:
        is_rain = False
        restaurants = result['restaurants']

        return render(response, 'main/layouts/base.html', { 'restaurants': restaurants, 'is_rain': is_rain, 'layout': 'result', 'year': date.today().year })