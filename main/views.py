from django.shortcuts import render
from datetime import date

def index(response):
    return render(response, 'main/layouts/base.html', { 'layout': 'index', 'year': date.today().year })