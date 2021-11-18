from django.urls import path

from cities.views import *

app_name = 'cities'

urlpatterns = [
    path('', home_view, name='home'),
    path('<int:pk>/', home_view, name='city'),
]