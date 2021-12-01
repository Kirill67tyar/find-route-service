from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, )

from cities.models import City
from cities.forms import CityModelForm, CityForm
from cities.utils import get_object_or_null, get_view_at_console1 as cons

__all__ = (
    'home_view', 'CityDetailView', 'CityCreatelView',
    'CityUpdateView', 'CityDeleteView', 'CityListView',
)


def home_view(request):
    # cities = City.objects.values()
    cities = City.objects.all()
    paginator = Paginator(object_list=cities, per_page=5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'objects_list': cities,
        'page_obj': page_obj,
    }

    # # in console
    # # ---------------------------
    # cons(cities)
    # cons(cities2)
    # # ---------------------------

    return render(request, 'cities/home.html', context=context)


class CityListView(ListView):
    model = City
    paginate_by = 5
    template_name = 'cities/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['my_form'] = CityModelForm()
        return context



class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'

    def get(self, request, *args, **kwargs):
        cons(self.queryset)
        return super().get(request, *args, **kwargs)


class CityCreatelView(SuccessMessageMixin, CreateView):
    # model = City
    form_class = CityModelForm
    template_name = 'cities/create.html'
    success_message = 'Город успешно создан'
    # success_url = reverse_lazy('cities:home')


class CityUpdateView(SuccessMessageMixin, UpdateView):
    model = City
    form_class = CityModelForm
    template_name = 'cities/update.html'
    success_message = 'Город успешно отредактирован'


class CityDeleteView(DeleteView):
    model = City
    success_url = reverse_lazy('cities:home')

    # template_name = 'cities/delete.html'

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Город успешно удалён')
        return self.post(request, *args, **kwargs)
