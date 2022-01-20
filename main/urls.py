from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('authenticate', views.authenticate, name='authenticate'),
    path('register', views.register, name='register'),
    path('create_user', views.create_user, name='create_user'),
    path('logout', views.logout, name='logout'),
    path('result', views.result, name='result')
]