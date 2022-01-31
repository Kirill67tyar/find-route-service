from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy
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
                return render(request, 'routes/home.html', {'form': form, })
            return render(request, 'routes/home.html', context)
        return render(request, 'routes/home.html', {'form': form, })
    else:
        # form = RouteForm()
        # return render(request, 'routes/home.html', {'form': form, })
        messages.error(request, 'Ошибка ввода')
        return redirect(reverse('home'))


def add_routes_view(request):
    if request.method == 'POST':
        data = request.POST
        print('%' * 20, data, sep='\n', end='\n' * 5)
        context = {}
        if data:
            # проблема этого обработчика (add_routes_view) в том,
            # что он два раза посылает post запрос,
            # сначала от формы со страницы home.html, а потом от формы со страницы create.html
            # print('*'*20,data,sep='\n',end='\n'*5)
            # print(data.get('total_time', 'what?'),end='\n'*5)
            from_city = int(data['from_city'])
            to_city = int(data['to_city'])
            total_time = int(data['total_time'])
            trains = data['trains'].split(',')
            print('@' * 20, trains, sep='\n', end='\n' * 5)
            trains_ids = [int(t) for t in trains if t.isdigit()]
            print('+' * 20, trains_ids, sep='\n', end='\n' * 5)
            qs = Train.objects.filter(pk__in=trains_ids).select_related(
                'from_city', 'to_city')
            print('^' * 20, qs, sep='\n', end='\n' * 5)
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
            # context['action'] = reverse_lazy('save_route')
        return render(request, 'routes/create.html', context=context)
    else:
        messages.error(request, 'Не будь таким хитрожопым')
        return redirect('/')
