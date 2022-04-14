"""travel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from routes.views import *

urlpatterns = [
    path('adminka_/', admin.site.urls),  # http://127.0.0.1:8000/adminka_/
    path('cities/', include('cities.urls', namespace='cities')),
    path('trains/', include('trains.urls', namespace='trains')),
    path('accounts/', include('accounts.urls', namespace='accounts')),

    # --- patterns for routes ---
    path('', home_view, name='home'),
    path('find-route/', find_route_view, name='find-route'),
    path('add-route/', add_route_view, name='add-route'),
    path('save-route/', save_route_view, name='save-route'),
    path('list/', RouteListView.as_view(), name='list'),
    path('detail/<int:pk>/', RouteDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', RouteDeleteView.as_view(), name='delete'),
]

# 11.98
# (пересмотреть 53 урок, хорошо показан механизм деббагинга на pycharm)
# (пересмотреть 55 урок, очень полезный)
# (24 урок для настройки шаблонных тегов)
# (33 урок для того как настроить runserver прямо из pycharm)
# (11.77 обзор хостингов и серверов, ngrok или туннелирование)

# find-route-service

# https://find-route-service.herokuapp.com/

"""
T-34
Владивосток - Кыив (10)

T-35
Кыив - Сочи (15)
"""


"""
Данные для сервера ubuntu

filename - gunicorn_config.py
command = '/home/kirill/scrap/venv/bin/gunicorn'
pythonpath = '/home/kirill/scrap/src'
bind = '127.0.0.1:8005'
workers = 3
user = 'kirill'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=scraping_service.settings'


filename - start_gunicorn.sh
#!/bin/bash
source /home/kirill/scrap/venv/bin/activate
exec gunicorn -c "/home/kirill/scrap/src/gunicorn_config.py" scraping_service.wsgi

proxy_pass http://127.0.0.1:8005;
proxy_set_header X-Forvarded-Host $server_name;
proxy_set_header X-Real-IP $remote_addr;
add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
add_header Acces-Control-Allow-Origin *;



[program:gunicorn]
command=/home/kirill/scrap/bin/start_gunicorn.sh
user=kirill
process_name=%(program_name)s
numproc=1
autostart=1
autorestart=1
redirect_stderr=true

"""