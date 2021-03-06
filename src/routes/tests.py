from datetime import datetime

from django.urls import reverse
from django.test import TestCase
from django.core.exceptions import ValidationError

from cities.models import City
from trains.models import Train
from cities import views as cities_views
from routes.utils import get_graph2, dfs_paths
from routes import forms as routes_forms, views as routes_views


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
            },
            {
                'name': 't2',
                'from_city': self.city_B,
                'to_city': self.city_D,
                'travel_time': 8,
            },
            {
                'name': 't3',
                'from_city': self.city_A,
                'to_city': self.city_C,
                'travel_time': 7,
            },
            {
                'name': 't4',
                'from_city': self.city_C,
                'to_city': self.city_B,
                'travel_time': 6,
            },
            {
                'name': 't5',
                'from_city': self.city_B,
                'to_city': self.city_E,
                'travel_time': 5,
            },
            {
                'name': 't6',
                'from_city': self.city_B,
                'to_city': self.city_A,
                'travel_time': 10,
            },
            {
                'name': 't7',
                'from_city': self.city_A,
                'to_city': self.city_C,
                'travel_time': 11,
            },
            {
                'name': 't8',
                'from_city': self.city_E,
                'to_city': self.city_D,
                'travel_time': 4,
            },
            {
                'name': 't9',
                'from_city': self.city_D,
                'to_city': self.city_E,
                'travel_time': 3,
            },
        ]
        cities_lst = list(map(lambda value: Train(**value), data))
        Train.objects.bulk_create(cities_lst)

    def test_model_city_duplicate(self):
        """???????????????????????? ?????????????????????????? ???????????? ?????? ???????????????? ?????????? ????????????"""
        city = City(name='A')

        with self.assertRaises(ValidationError):
            city.full_clean()
            # full_clean - Call clean_fields(), clean(), and validate_unique() on the model.
            #              Raise a ValidationError for any errors that occur.

    def test_model_train_duplicate(self):
        """???????????????????????? ?????????????????????????? ???????????? ?????? ???????????????? ?????????? ???????????? ?? ???????????????????? name"""
        train = Train(name='t9', from_city=self.city_D, to_city=self.city_E, travel_time=12131)

        with self.assertRaises(ValidationError):
            train.full_clean()

    def test_model_train_train_duplicate(self):
        """???????????????????????? ?????????????????????????? ???????????? ?????? ???????????????? ?????????? ???????????? ?? ???????????????????? travel_time"""
        train = Train(name='t1234', from_city=self.city_D, to_city=self.city_E, travel_time=3)

        with self.assertRaises(ValidationError):
            train.full_clean()

        try:
            train.full_clean()
        except ValidationError as e:
            self.assertEqual(
                {'__all__':
                     ['?????????? with this ?????????? ?? ????????, ???? ???????????? ???????????? and ?? ?????????? ?????????? already exists.']
                 },
                e.message_dict)
            self.assertIn('?????????? with this ?????????? ?? ????????, ???? ???????????? ???????????? and ?? ?????????? ?????????? already exists.',
                          e.messages)

    #             ?????? ?? ?????? ??????????????, ???? ?????????????????? ???????? ???? ?? e.messages ?????? ?????? ???????????? - ?????????? with this ?????????? ?? ????????...
    #             ?????? ???????????????? ?????? ?? self.assertEqual ?????? ?? ?? self.assertIn
    #             ?????????? ?????? ????????????????? ???? ?????????????? ?????? ???????? ???????? ???????????? ?????????????????? ????????????
    #             ???????????? assertEqual ?????????????????? ?????????? ???? ???????? ?????????? ????????????, ?? ???????? ?????? ???? ???????????????? ???????????? AssertionError
    #             assertEqual(<1 arg> == <2 arg>) --- True
    #             ?? assertIn ?????????????????? ???????? ???? ???????????? ???????????????? ?? ???????????????????????? ????????????????????.
    #             assertIn(<1 arg> in <2 arg>) --- True
    #             self.assertIn(1, [2,3,]) --- AssertionError: 1 not found in [2, 3]

    # ???????????????????????? ???? ???????????????????? routes.views
    def test_home_routes_views(self):
        """
        ?????????????????? ???? ???????????? reverse('home') ??????????????????:
        ?????? ???????????? ?????? 200
        ?????? ???????????????????????? ???????????? routes/home.html
        ?????? ???????????????????????? ?????????????? routes.home_view
        ??????????, ???????????????? AssertionError
        """
        # self.client - ???????????????? ??????????????
        # ?????????? ???????????? GET ???????????? ???? ???????? reverse('home')
        response = self.client.get(path=reverse('home'))
        # ????????????????????, ?????? ???????????? ?????? 200
        self.assertEqual(first=200, second=response.status_code)
        # ????????????????????, ?????? ???? ???????????????????? ???????????????????? ????????????
        self.assertTemplateUsed(response=response, template_name='routes/home.html')
        # ????????????????????, ?????? ???? ???????????????????? ???????????????????? ?????????????? - ????????????????????.
        # ?????? ???? reverse('home') ???????????????????? ?????????????? routes.home_view
        self.assertEqual(response.resolver_match.func, routes_views.home_view)

    # ???????????????????????? ???? ???????????????????? cities.views
    def test_cbv_detail_cities_views(self):
        response = self.client.get(reverse('cities:detail', kwargs={'pk': self.city_A.pk, }))
        self.assertEqual(first=200, second=response.status_code)
        self.assertTemplateUsed(response, 'cities/detail.html')
        # ???????? ?????? ???????? ???????????????? ???? ?????????????? ?? ?????????? (CBV ?? ??????????????), ???? ?????? ???????????????? ??????:
        self.assertEqual(response.resolver_match.func.__name__,
                         cities_views.CityDetailView.as_view().__name__)

    # ???????????????????????? ???? ???????????????????? routes.utils - graph, dfs_paths
    def test_find_all_routes(self):
        qs = Train.objects.all()
        graph = get_graph2(qs=qs)
        all_ways = list(dfs_paths(
            graph=graph, start=self.city_A.pk, goal=self.city_E.pk
        ))
        # assert len(all_ways) == 4
        self.assertEqual(len(all_ways), 4)

    # ???????????????????????? ???? ???????????????????? routes.forms - RouteForm
    def test_valid_route_form(self):
        data = {
            'from_city': self.city_A.pk,
            'to_city': self.city_B.pk,
            'cities': [self.city_D.pk, self.city_E.pk, ],
            'traveling_time': 9,
        }
        form = routes_forms.RouteForm(data=data)
        self.assertTrue(form.is_valid())

    # ???????????????????????? ???? ???????????????????????? routes.forms - RouteForm
    def test_invalid_route_form(self):
        data = {
            'from_city': self.city_A.pk,
            'to_city': self.city_B.pk,
            'cities': [self.city_D.pk, self.city_E.pk, ],
            #     ?????????????? traveling_time
        }
        form = routes_forms.RouteForm(data=data)
        self.assertFalse(form.is_valid())

        data['traveling_time'] = 4.3424
        form = routes_forms.RouteForm(data=data)
        self.assertFalse(form.is_valid())

    # ???????????????????????? ???? ???????????????????? routes.forms - RouteForm
    def test_message_error_more_time(self):
        """
        ???????? ???? ????, ?????? ???????? ?????? ?????????????????? ?? ???????????????????? ????????????????,
        ???? ???????????? ??????????????????, ?????????????? ?????????????????? ???? ????????
        """
        data = {
            'from_city': self.city_A.pk,
            'to_city': self.city_E.pk,
            'cities': [self.city_C.pk, ],
            'traveling_time': 9,
        }
        response = self.client.post(
            path='/find-route/',
            data=data
        )
        self.assertContains(
            response=response,
            text='?????? ?????????????????? ?? ???????????????????? ????????????????',
            count=1,
            status_code=200,
        )

    def test_message_error_from_cities(self):
        """
        ???????? ???? ????, ?????? ???????? ?????? ?????????????????? ?????????? ???????????????????????? ????????????,
        ???? ???????????? ??????????????????, ?????????????? ?????????????????? ???? ????????
        """
        data = {
            'from_city': self.city_B.pk,
            'to_city': self.city_E.pk,
            'cities': [self.city_C.pk, ],
            'traveling_time': 942342,
        }
        response = self.client.post(
            path='/find-route/',
            data=data
        )
        self.assertContains(
            response=response,
            text='?????????????? ?????????? ?????? ???????????? ???? ????????????????',
            # text='?????? ?????????????????? ?? ???????????????????? ????????????????',
            count=1,
            status_code=200,
        )


"""
?? ??????:

1 - ??????????, ?????? ???? ???????????? ?????????? ?????????????????????? ???? TestCase
2 - ?????????????????? ???? ???????? ???????? ???????????????? python manage.py test 
3 - ?????????? ???? ?????????????????? ????????, ???? ?????????????????? ?????????????????? ???????? ???????????? ?????????????????????????? ?????? ??????????
4 - ????, ?????? ?????????? ?????????????????????? ?????? ???? ???? ?????????????????????? ?? ?????????????? setUp
5 - ?? ?????????????? ???????????????????????? ???? test_ ???? ?????? ?????????????????? ???????? ??????????
6 - ?? ???????? ???????????????? ???????????? ?????????????????????? ???????????? 
(???? ????????. ???????????? ???????????????????? ????-????         with self.assertRaises(ValidationError):
                                                train.full_clean()                   )
7 - ???????????? ????????????????, ?????? ???? ???????????? ???????????????? ?????????????????? ????????????, ???? ???? ?????????????? INSERT ?? ????
8 - ?? ???????????????????? ???????????? ???????????????????? ?????????? full_clean()
9 - full_clean() ???????????????? clean_fields(), clean(), and validate_unique() ?? ???????????????? ValidationError 
???????? ???????? ???????? ???? ???????? ?????????????? ???????????????? ValidationError

?????????????? ??????????????:

?????? ???????????????? ???????? ???????????? ???? ?????????????????????????? ???????????? ???????????? 
???????????????????? ?? test_<your_info>, 
???????????????? - test_model_train_duplicate

?????????????????????? 

        with self.assertRaises(ValidationError):
            train.full_clean()
            
?????????????????? AssertionError. ??????? 
assertRaises ?????????? True ???????? ???????? ???????????????????? ValidationError
???????????? ?? ?????????????????? ?????????????????? ?????????? ???????????????????? ValidationError.
?????????? ?????????????????? AssertionError ?? ???????????? ?????????????????????? AssertionError: ValidationError not raised
??.??. ???????????? ???????????? ????????????????????, ?? ?????????? ?????? ?????????????? ??????????????????.
?? ??????????????, ?? ???????????? ?????????? ?? ?????????????????? A, ???????? ?? setUp ?????????? ?????????? ?????? ????????????????????
?????? ?????????????????? ?????????????? ?????????????? ???????? ?????????? ?? test_model_city_duplicate
?????????????????? ???????????? ?? ???????? ????????????????.

??.??. ?????????? ?????????????? ??????????, ?????? ?? ???????? ???????????????? test_...
???? ???????????????? ???????????? AssertionError 
?????????????????????? ?????????????????? ?? ???????????? ?????????? ???????? self.assertEqual ?????? self.assertIn ?? ??.??., ?????????? ????


?? ??????:

1 - ??????????, ?????? ???? ???????????? ?????????? ?????????????????????? ???? TestCase
2 - ?????????? ???? ?????????????????? ????????, ???? ?????????????????? ?????????????????? ???????? ???????????? ?????????????????????????? ?????? ?????????? 
    (???????? ?????? ?????????????? ???? ?????? ?????????? ??????????)
3 - ?? def setUp(self)  ???? ???????????????????? ???????????????????? ???????? ???? (?????????????????? ????)
4 - ?? ???????????????? ???????????????????????? ???? test_... ???? ???????????? ????????????????, ?? ?????? ???????????????????? ???????????? ???????????????? AssertionError
5 - AssertionError ???? ???????????????? ?????????????????????? ???????????????????? ?????????????? ???????? 
    self.assertionIn, self.assertionEqual ?????? self.assertTemplateUsed ?? ??.??.
6 - ?????????????????? ?????????????????? ?????????? self.assertRaises ?????????????? ???????????????????????? ?? ?????????????????????? ??????????????????
    ???????? ???????? self.assertRaises(ValidationError) ???? ?????????????????? ValidationError ???? ?????????????? ?????????????? AssertionError
    ?? ?????????? ???????????? ???????? ?? ????????
7 - ?????? ?????? ?????????????? ???????????????????? python manage.py test


                        Coverage
https://coverage.readthedocs.io/en/6.3.2/

????????????????????, ?????????????? ?????????????????? ????????????, ???? ?????????????? ?????????????????? ?????? ?????? ???????????? ??????????????

1 - pip install coverage
2 - coverage run manage.py test    -???????????? ???????????? ?? ?????????????? ???????????? (?????? ?????????? ?????? python manage.py test)
3 - coverage report                -????-???? ?? ?????? ???? ?????????????? ???????????? ???????? ???????????????????? ???????????? ??????????????
4 - coverage html                  -???????????????????? ?? ???????????? ?????????????? ?????????? htmlcov

?????? ?????????????? ?????????? ?????????????????????????? ?????????????? 'coverage html'
?? ?????????? ?????????????? ???????????????????? ?????????? htmlcov (pycharm ?????????? ???? ?????????? ??????????????)
?? ?????? ?????????? ???????????? html. 
?? ??????????????????, ?????? ???????? ???????? index.html
???? ?????????? ??????????, ???????? ?????????????? ?????? ?? ????????????????,
???? ???? ?????????????? ???????????????? ??????????????, ?????????? ?????????? ???????? ?????????????????? ?????????????????? ??????????, ?? ?????????? ??????

??????????????????, ?????? ???????????????????? ???????????? ???? Django?
"""
