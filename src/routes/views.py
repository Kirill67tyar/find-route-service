from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.messages.views import messages

from trains.models import Train
from cities.models import City
from routes.utils import get_routes
from routes.forms import RouteForm, RouteModelForm


def home_view(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form, })


def find_routes_view(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            try:
                context = get_routes(request, form)
            except ValueError as err:
                messages.error(request, err)
                return render(request, 'routes/home.html', {'form': form})
            return render(request, 'routes/home.html', context)
        return render(request, 'routes/home.html', {'form': form})
    else:
        # form = RouteForm()
        # return render(request, 'routes/home.html', {'form': form, })
        messages.error(request, 'Ошибка ввода')
        return redirect(reverse('home'))


def add_routes_view(request):
    if request.method == 'POST':
        data = request.POST
        context = {}
        if data:
            from_city = int(data['from_city'])
            to_city = int(data['to_city'])
            total_time = int(data['total_time'])
            trains = data['trains'].split(',')
            trains_ids = [int(t) for t in trains if t.isdigit()]
            qs = Train.objects.filter(pk__in=trains_ids).select_related(
                'from_city', 'to_city')
            cities = City.objects.filter(
                pk__in=[from_city, to_city, ]).in_bulk()
            form = RouteModelForm(
                initial={
                    'from_city': cities[from_city],
                    'to_city': cities[to_city],
                    'travel_times': total_time,
                    'trains': qs,
                }
            )
            context['form'] = form
        return render(request, 'routes/create.html', context=context)
    else:
        messages.error(request, 'Не будь таким хитрожопым')
        return redirect('/')

