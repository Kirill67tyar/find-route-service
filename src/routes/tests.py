from datetime import datetime

from django.test import TestCase

from cities.models import City
from trains.models import Train


class AllTestsCase(TestCase):

    def setUp(self) -> None:
        self.city_A = City.objects.create(name='A')
        self.city_B = City.objects.create(name='B')
        self.city_C = City.objects.create(name='C')
        self.city_D = City.objects.create(name='D')
        self.city_E = City.objects.create(name='E')
        data = [
            {
                'name': 't1',
                'from_city': self.city_A,
                'to_city': self.city_B,
                'travel_time': 9,
                'departure_time': datetime.now(),
                'arrival_time': datetime.now(),
            },
            {
                'name': 't2',
                'from_city': self.city_B,
                'to_city': self.city_D,
                'travel_time': 8,
                'departure_time': datetime.now(),
                'arrival_time': datetime.now(),
            },
            {
                'name': 't3',
                'from_city': self.city_A,
                'to_city': self.city_C,
                'travel_time': 7,
                'departure_time': datetime.now(),
                'arrival_time': datetime.now(),
            },
            {
                'name': 't4',
                'from_city': self.city_C,
                'to_city': self.city_B,
                'travel_time': 6,
                'departure_time': datetime.now(),
                'arrival_time': datetime.now(),
            },
            {
                'name': 't5',
                'from_city': self.city_B,
                'to_city': self.city_E,
                'travel_time': 5,
                'departure_time': datetime.now(),
                'arrival_time': datetime.now(),
            },
            {
                'name': 't6',
                'from_city': self.city_B,
                'to_city': self.city_A,
                'travel_time': 10,
                'departure_time': datetime.now(),
                'arrival_time': datetime.now(),
            },
            {
                'name': 't7',
                'from_city': self.city_A,
                'to_city': self.city_C,
                'travel_time': 11,
                'departure_time': datetime.now(),
                'arrival_time': datetime.now(),
            },
            {
                'name': 't8',
                'from_city': self.city_E,
                'to_city': self.city_D,
                'travel_time': 4,
                'departure_time': datetime.now(),
                'arrival_time': datetime.now(),
            },
            {
                'name': 't9',
                'from_city': self.city_D,
                'to_city': self.city_E,
                'travel_time': 3,
                'departure_time': datetime.now(),
                'arrival_time': datetime.now(),
            },
        ]
        cities_lst = list(map(lambda value: Train(**value), data))
        Train.objects.bulk_create(cities_lst)
