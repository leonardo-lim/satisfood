from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from datetime import date
from main.main import *

def index(request):
    try:
        request.session['is_authenticated']
        request.session['name']
    except:
        request.session['is_authenticated'] = False
        request.session['name'] = ''

    return render(request, 'main/layouts/base.html', { 'layout': 'index', 'year': date.today().year, 'is_authenticated': request.session['is_authenticated'], 'name': request.session['name'] })

def login(request):
    try:
        request.session['is_authenticated']
        request.session['name']
    except:
        request.session['is_authenticated'] = False
        request.session['name'] = ''

    if request.session['is_authenticated']:
        return redirect('/')
    else:
        return render(request, 'main/layouts/base.html', { 'layout': 'login', 'year': date.today().year, 'is_authenticated': request.session['is_authenticated'], 'name': request.session['name'] })

def authenticate(request):
    try:
        request.session['is_authenticated']
        request.session['name']
    except:
        request.session['is_authenticated'] = False
        request.session['name'] = ''

    user = {}
    user['username'] = request.POST['username']
    user['password'] = request.POST['password']

    # Check whether all the fields are filled or not
    if not user['username'] or not user['password']:
        error_message = 'Please fill in all the fields'
        return render(request, 'main/layouts/base.html', { 'layout': 'login', 'year': date.today().year, 'is_authenticated': request.session['is_authenticated'], 'name': request.session['name'], 'user': user, 'error_message': error_message })
    else:
        registered_users = User.objects.all()
        exist = False

        # Check whether the username exists in database or not
        for registered_user in registered_users:
            if registered_user.username == user['username']:
                name = registered_user.name
                hashed_password = registered_user.password
                exist = True
                break

        if not exist:
            error_message = 'Username does not exist'
            return render(request, 'main/layouts/base.html', { 'layout': 'login', 'year': date.today().year, 'is_authenticated': request.session['is_authenticated'], 'name': request.session['name'], 'user': user, 'error_message': error_message })
        else:
            # Check whether the password matches or not
            if not check_password(user['password'], hashed_password):
                error_message = 'Password is incorrect'
                return render(request, 'main/layouts/base.html', { 'layout': 'login', 'year': date.today().year, 'is_authenticated': request.session['is_authenticated'], 'name': request.session['name'], 'user': user, 'error_message': error_message })
            else:
                request.session['is_authenticated'] = True
                request.session['username'] = user['username']
                request.session['name'] = name
                return redirect('/')

def register(request):
    try:
        request.session['is_authenticated']
        request.session['name']
    except:
        request.session['is_authenticated'] = False
        request.session['name'] = ''

    if request.session['is_authenticated']:
        return redirect('/')
    else:
        return render(request, 'main/layouts/base.html', { 'layout': 'register', 'year': date.today().year, 'is_authenticated': request.session['is_authenticated'], 'name': request.session['name'] })

def create_user(request:HttpRequest):
    try:
        request.session['is_authenticated']
        request.session['name']
    except:
        request.session['is_authenticated'] = False
        request.session['name'] = ''

    user = {}
    user['name'] = request.POST['name']
    user['username'] = request.POST['username']
    user['password'] = request.POST['password']
    user['confirm_password'] = request.POST['confirm_password']

    # Check whether all the fields are filled or not
    if not user['name'] or not user['username'] or not user['password'] or not user['confirm_password']:
        error_message = 'Please fill in all the fields'
        return render(request, 'main/layouts/base.html', { 'layout': 'register', 'year': date.today().year, 'is_authenticated': request.session['is_authenticated'], 'name': request.session['name'], 'user': user, 'error_message': error_message })
    else:
        invalid = False

        # Check whether the username format is valid or not
        for i in range(0, len(user['username'])):
            if (user['username'][i] >= 'a' and user['username'][i] <= 'z') or (user['username'][i] >= '0' and user['username'][i] <= '9') or user['username'][i] == '.' or user['username'][i] == '-' or user['username'][i] == '_':
                continue
            else:
                invalid = True
                break

        if invalid:
            error_message = 'Invalid username format'
            return render(request, 'main/layouts/base.html', { 'layout': 'register', 'year': date.today().year, 'is_authenticated': request.session['is_authenticated'], 'name': request.session['name'], 'user': user, 'error_message': error_message })

        # Check whether the password and confirm password match or not
        if user['password'] != user['confirm_password']:
            error_message = 'Password does not match'
            return render(request, 'main/layouts/base.html', { 'layout': 'register', 'year': date.today().year, 'is_authenticated': request.session['is_authenticated'], 'name': request.session['name'], 'user': user, 'error_message': error_message })
        else:
            registered_users = User.objects.all()
            exist = False

            # Check whether the username already exists in database or not
            for registered_user in registered_users:
                if registered_user.username == user['username']:
                    exist = True
                    break

            if exist:
                error_message = 'Username already exists'
                return render(request, 'main/layouts/base.html', { 'layout': 'register', 'year': date.today().year, 'is_authenticated': request.session['is_authenticated'], 'name': request.session['name'], 'user': user, 'error_message': error_message })
            else:
                new_user = User.objects.create()
                new_user.name = user['name']
                new_user.username = user['username']
                new_user.password = make_password(user['password'])
                new_user.save()
                messages.success(request, 'Registration successful. You can login now')
                return redirect('/login')

def logout(request):
    try:
        request.session['is_authenticated']
        request.session['name']
    except:
        request.session['is_authenticated'] = False
        request.session['name'] = ''

    if request.session['is_authenticated']:
        request.session['is_authenticated'] = False
        request.session['username'] = ''
        request.session['name'] = ''
        messages.success(request, 'You have been logged out')

    return redirect('/login')

def option(request):
    try:
        request.session['is_authenticated']
        request.session['name']
    except:
        request.session['is_authenticated'] = False
        request.session['name'] = ''

    if not request.session['is_authenticated']:
        return redirect('/login')
    else:
        return render(request, 'main/layouts/base.html', { 'layout': 'option', 'year': date.today().year, 'is_authenticated': request.session['is_authenticated'], 'name': request.session['name'] })

def address(request):
    try:
        request.session['is_authenticated']
        request.session['name']
    except:
        request.session['is_authenticated'] = False
        request.session['name'] = ''

    if not request.session['is_authenticated']:
        return redirect('/login')
    else:
        return render(request, 'main/layouts/base.html', { 'layout': 'address', 'year': date.today().year, 'is_authenticated': request.session['is_authenticated'], 'name': request.session['name'] })

def result(request:HttpRequest):
    try:
        request.session['is_authenticated']
        request.session['name']
    except:
        request.session['is_authenticated'] = False
        request.session['name'] = ''

    if not request.session['is_authenticated']:
        return redirect('/login')
    else:
        try:
            address = request.POST['address']
            use_ip_location = False
        except:
            address = ''
            use_ip_location = True

        # Check whether the field is filled or not
        if not use_ip_location and not address:
            error_message = 'Please fill in the field'
            return render(request, 'main/layouts/base.html', { 'layout': 'address', 'year': date.today().year, 'is_authenticated': request.session['is_authenticated'], 'name': request.session['name'], 'error_message': error_message })
        else:
            ip_address = request.headers['X-Forwarded-For']
            registered_users = User.objects.all()

            # Find logged in user in database
            for registered_user in registered_users:
                if registered_user.username == request.session['username']:
                    prev_restaurant_type = registered_user.prev_restaurant
                    break

            # Check whether the user is new or not
            if prev_restaurant_type:
                prev_restaurant = {
                    'name': '',
                    'type': prev_restaurant_type,
                    'location': '',
                    'phone': '',
                    'rating': 0,
                    'review': 0,
                    'image': ''
                }

                result = recommend_restaurants(prev_restaurant, address, ip_address)
            else:
                result = show_restaurants(address, ip_address)

            # Check whether the weather condition is raining or not
            if result['is_rain']:
                is_rain = True
                rain_food_restaurants = result['rain_food_restaurants']
                non_rain_food_restaurants = result['non_rain_food_restaurants']

                return render(request, 'main/layouts/base.html', { 'rain_food_restaurants': rain_food_restaurants, 'non_rain_food_restaurants': non_rain_food_restaurants, 'is_rain': is_rain, 'layout': 'result', 'year': date.today().year, 'is_authenticated': request.session['is_authenticated'], 'name': request.session['name'] })
            else:
                is_rain = False
                restaurants = result['restaurants']

                return render(request, 'main/layouts/base.html', { 'restaurants': restaurants, 'is_rain': is_rain, 'layout': 'result', 'year': date.today().year, 'is_authenticated': request.session['is_authenticated'], 'name': request.session['name'] })

def mark(request:HttpRequest):
    try:
        request.session['is_authenticated']
        request.session['name']
    except:
        request.session['is_authenticated'] = False
        request.session['name'] = ''

    restaurant_type = request.POST['restaurant_type']
    registered_users = User.objects.all()

    # Find logged in user in database
    for registered_user in registered_users:
        if registered_user.username == request.session['username']:
            registered_user.prev_restaurant = restaurant_type
            registered_user.save()
            break

    return render(request, 'main/layouts/base.html', { 'layout': 'marked', 'year': date.today().year, 'is_authenticated': request.session['is_authenticated'], 'name': request.session['name'] })