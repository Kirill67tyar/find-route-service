from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, )

from trains.models import Train
from cities.utils import get_object_or_null, get_view_at_console1 as cons

__all__ = (
    'home_view', 'TrainListView',
    'TrainDetailView',
    # 'TrainCreatelView',
    # 'TrainUpdateView', 'TrainDeleteView',
)


def home_view(request):
    # trains = Train.objects.values()
    trains = Train.objects.all()
    paginator = Paginator(object_list=trains, per_page=5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'objects_list': trains,
        'page_obj': page_obj,
    }

    return render(request, 'trains/home.html', context=context)


class TrainListView(ListView):
    model = Train
    paginate_by = 5
    template_name = 'trains/home.html'



class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    template_name = 'trains/detail.html'

    def get(self, request, *args, **kwargs):
        cons(self.queryset)
        return super().get(request, *args, **kwargs)
#
#
# class TrainCreatelView(SuccessMessageMixin, CreateView):
#     # model = Train
#     form_class = TrainModelForm
#     template_name = 'trains/create.html'
#     success_message = 'Поезд успешно создан'
#     # success_url = reverse_lazy('trains:home')
#
#
# class TrainUpdateView(SuccessMessageMixin, UpdateView):
#     model = Train
#     form_class = TrainModelForm
#     template_name = 'trains/update.html'
#     success_message = 'Поезд успешно отредактирован'
#
#
# class TrainDeleteView(DeleteView):
#     model = Train
#     success_url = reverse_lazy('trains:home')
#
#     # template_name = 'trains/delete.html'
#
#     def get(self, request, *args, **kwargs):
#         messages.success(request, 'Поезд успешно удалён')
#         return self.post(request, *args, **kwargs)
