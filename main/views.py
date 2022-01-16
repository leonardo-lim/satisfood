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

    return render(response, 'main/layouts/base.html', { 'restaurants': result, 'layout': 'result', 'year': date.today().year })