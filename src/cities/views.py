from django.shortcuts import render

from cities.models import City
from cities.utils import get_object_or_null, get_view_at_console1 as cons

__all__ = (
    'home_view',
)


def home_view(request, pk=None):
    if pk:
        city = get_object_or_null(City, pk=pk)
        context = {'object': city, }
        return render(request, 'cities/detail.html', context=context)

    cities = City.objects.values()
    cities2 = City.objects.all()
    context = {'objects_list': cities, }

    # # in console
    # # ---------------------------
    # cons(cities)
    # cons(cities2)
    # # ---------------------------

    return render(request, 'cities/home.html', context=context)