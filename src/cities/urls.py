from django.urls import path

from cities.views import home

app_name = 'cities'

urlpatterns = [
    path('home/', home, name='home'),
]