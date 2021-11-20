from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (DetailView, CreateView, UpdateView, DeleteView, )

from cities.models import City
from cities.forms import CityModelForm, CityForm
from cities.utils import get_object_or_null, get_view_at_console1 as cons

__all__ = (
    'home_view', 'CityDetailView', 'CityCreatelView', 'CityUpdateView', 'CityDeleteView'
)


def home_view(request):
    cities = City.objects.values()
    cities2 = City.objects.all()

    context = {'objects_list': cities, }

    # # in console
    # # ---------------------------
    # cons(cities)
    # cons(cities2)
    # # ---------------------------

    return render(request, 'cities/home.html', context=context)


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'

    def get(self, request, *args, **kwargs):
        cons(self.queryset)
        return super().get(request, *args, **kwargs)


class CityCreatelView(CreateView):
    # model = City
    form_class = CityModelForm
    template_name = 'cities/create.html'
    # success_url = reverse_lazy('cities:home')


class CityUpdateView(UpdateView):
    model = City
    form_class = CityModelForm
    template_name = 'cities/update.html'


class CityDeleteView(DeleteView):
    model = City
    success_url = reverse_lazy('cities:home')
    # template_name = 'cities/delete.html'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
