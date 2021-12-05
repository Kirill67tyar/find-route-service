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
from routes.views import home_view, find_routes_view, add_routes_view

urlpatterns = [
    path('adminka_/', admin.site.urls),  # http://127.0.0.1:8000/adminka_/
    path('cities/', include('cities.urls', namespace='cities')),
    path('trains/', include('trains.urls', namespace='trains')),
    path('', home_view, name='home'),
    path('find-routes/', find_routes_view, name='find-routes'),
    path('add-routes/', add_routes_view, name='add-routes'),
]

# 10.67
# (пересмотреть 55 урок, очень полезный)


"""
T-34
Владивосток - Кыив (10)

T-35
Кыив - Сочи (15)
"""