from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.messages.views import messages

from routes.forms import RouteForm
from routes.utils import get_routes


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
