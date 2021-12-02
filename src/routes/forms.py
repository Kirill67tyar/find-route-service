from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import (
    Form, ModelForm, TextInput, Select, SelectMultiple,
    DateTimeInput, NumberInput, ModelChoiceField, ModelMultipleChoiceField,
)

from cities.models import City

cities = City.objects.all()


class RouteForm(Form):
    from_city = ModelChoiceField(
        queryset=cities, label=_('Из города'), widget=Select(
            attrs={'class': ' form-control js-example-basic-single', }
        )
    )
    to_city = ModelChoiceField(
        queryset=cities, label=_('В город'), widget=Select(
            attrs={'class': 'form-control js-example-basic-single', }
        )
    )
    cities = ModelMultipleChoiceField(
        queryset=cities, label=_('Через какие города'), required=False,
        widget=SelectMultiple(
            attrs={'class': 'form-control js-example-basic-multiple', }
        )
    )
    traveling_time = forms.IntegerField(
        label=_('Ожидаемое время поездки'), widget=NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'время в пути', }
        ),
    )
