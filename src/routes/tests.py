from datetime import datetime

from django.urls import reverse
from django.test import TestCase
from django.core.exceptions import ValidationError

from cities.models import City
from trains.models import Train
from cities import views as cities_views
from routes import forms as routes_forms, views as routes_views
from routes.utils import get_graph2, dfs_paths


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
        """Тестирование возникновения ошибки при создании дубля города"""
        city = City(name='A')

        with self.assertRaises(ValidationError):
            city.full_clean()
            # full_clean - Call clean_fields(), clean(), and validate_unique() on the model.
            #              Raise a ValidationError for any errors that occur.

    def test_model_train_duplicate(self):
        """Тестирование возникновения ошибки при создании дубля поезда с одинаковым name"""
        train = Train(name='t9', from_city=self.city_D, to_city=self.city_E, travel_time=12131)

        with self.assertRaises(ValidationError):
            train.full_clean()

    def test_model_train_train_duplicate(self):
        """Тестирование возникновения ошибки при создании дубля поезда с одинаковым travel_time"""
        train = Train(name='t1234', from_city=self.city_D, to_city=self.city_E, travel_time=3)

        with self.assertRaises(ValidationError):
            train.full_clean()

        try:
            train.full_clean()
        except ValidationError as e:
            self.assertEqual(
                {'__all__':
                     ['Поезд with this Время в пути, Из какого города and В какой город already exists.']
                 },
                e.message_dict)
            self.assertIn('Поезд with this Время в пути, Из какого города and В какой город already exists.',
                          e.messages)

    #             тут я так понимаю, мы проверяем есть ли в e.messages вот эта запись - Поезд with this Время в пути...
    #             это делается как в self.assertEqual так и в self.assertIn
    #             зачем это делается? может мы ожидаем что этот тест выдаст ожидаемую ошибку
    #             Причём assertEqual проверяет равна ли одна часть другой, и если нет то вызывает ошибку AssertionError
    #             assertEqual(<1 arg> == <2 arg>) --- True
    #             self.assertIn(1, [2,3,]) --- AssertionError: 1 not found in [2, 3]
    #             А assertIn проверяет есть ли первый аргумент в итерабильном контейнере.
    #             assertIn(<1 arg> in <2 arg>) --- True
    # тестирование на валидность routes.views
    def test_home_routes_views(self):
        """
        Проверяем по адресу reverse('home') следующее:
        что статус код 200
        что используемый шаблон routes/home.html
        что используемая функция routes.home_view
        иначе, вызываем AssertionError
        """
        # self.client - эмулятор клиента
        # здесь делаем GET запрос по пути reverse('home')
        response = self.client.get(path=reverse('home'))
        # убеждаемся, что статус код 200
        self.assertEqual(first=200, second=response.status_code)
        # убеждаемся, что мы исполбзуем правильный шаблон
        self.assertTemplateUsed(response=response, template_name='routes/home.html')
        # убеждаемся, что мы исполбзуем правильную функцию - обработчик.
        # Что по reverse('home') вызывается функция routes.home_view
        self.assertEqual(response.resolver_match.func, routes_views.home_view)

    # тестирование на валидность cities.views
    def test_cbv_detail_cities_views(self):
        response = self.client.get(reverse('cities:detail', kwargs={'pk': self.city_A.pk, }))
        self.assertEqual(first=200, second=response.status_code)
        self.assertTemplateUsed(response, 'cities/detail.html')
        # если нам надо сравнить не функцию а класс (CBV к примеру), то это делается так:
        self.assertEqual(response.resolver_match.func.__name__,
                         cities_views.CityDetailView.as_view().__name__)

    # тестирование на валидность routes.utils - graph, dfs_paths
    def test_find_all_routes(self):
        qs = Train.objects.all()
        graph = get_graph2(qs=qs)
        all_ways = list(dfs_paths(
            graph=graph, start=self.city_A.pk, goal=self.city_E.pk
        ))
        # assert len(all_ways) == 4
        self.assertEqual(len(all_ways), 4)

    # тестирование на валидность routes.forms - RouteForm
    def test_valid_route_form(self):
        data = {
            'from_city': self.city_A.pk,
            'to_city': self.city_B.pk,
            'cities': [self.city_D.pk, self.city_E.pk, ],
            'traveling_time': 9,
        }
        form = routes_forms.RouteForm(data=data)
        self.assertTrue(form.is_valid())

    # тестирование на НЕвалидность routes.forms - RouteForm
    def test_invalid_route_form(self):
        data = {
            'from_city': self.city_A.pk,
            'to_city': self.city_B.pk,
            'cities': [self.city_D.pk, self.city_E.pk, ],
            #     убираем traveling_time
        }
        form = routes_forms.RouteForm(data=data)
        self.assertFalse(form.is_valid())

        data['traveling_time'] = 4.3424
        form = routes_forms.RouteForm(data=data)
        self.assertFalse(form.is_valid())

    # тестирование на валидность routes.forms - RouteForm
    def test_message_error_more_time(self):
        """
        тест на то, что если нет маршрутов с подходящим временем,
        то придёт сообщение, которое оповистит об этом
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
            text='Нет маршрутов с подходящим временем',
            count=1,
            status_code=200,
        )

    def test_message_error_from_cities(self):
        """
        тест на то, что если нет маршрутов через определённые города,
        то придёт сообщение, которое оповистит об этом
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
            text='Маршрут через эти города не возможен',
            # text='Нет маршрутов с подходящим временем',
            count=1,
            status_code=200,
        )


"""
И так:

1 - класс, где ты пишешь тесты наследуется от TestCase
2 - включаешь ты этот тест командой python manage.py test 
3 - когда ты включаешь тест, то создаётся временная база данных исключительно для теста
4 - то, чем будет заполняться эта бд ты определяешь в функции setUp
5 - в функция начинающихся на test_ ты уже проводишь сами тесты
6 - в этих функциях должна происходить ошибка 
(не факт. ошибка происходит из-за         with self.assertRaises(ValidationError):
                                                train.full_clean()                   )
7 - обрати внимание, что ты просто создаёшь экземпляр модели, ты не делаешь INSERT в бд
8 - у экземпляра модели появляется метод full_clean()
9 - full_clean() вызывает clean_fields(), clean(), and validate_unique() и вызывает ValidationError 
если хоть одна из этих функций вызывает ValidationError

Главные условия:

эти названия этих тестов на возникновения ошибок должны 
начинаться с test_<your_info>, 
например - test_model_train_duplicate

Конструкция 

        with self.assertRaises(ValidationError):
            train.full_clean()
            
вызываает AssertionError. Как? 
assertRaises будет True если туда передастся ValidationError
Точнее в менеджере контекста будет вызываться ValidationError.
Иначе вызовется AssertionError с такими пояснениями AssertionError: ValidationError not raised
т.е. ошибка должна возникнуть, и тогда всё пройдёт нормально.
к примеру, я создаю гордо с названием A, хотя в setUp такой город уже создавался
при повторной попытке создать этот город в test_model_city_duplicate
возникает ошибка и тест проходит.

Т.е. можно сделать вывод, что в этих функциях test_...
мы вызываем ошибки AssertionError 
посредством доступных в классе метов типа self.assertEqual или self.assertIn и т.д., много их


И так:

1 - класс, где ты пишешь тесты наследуется от TestCase
2 - когда ты включаешь тест, то создаётся временная база данных исключительно для теста
3 - в def setUp(self)  мы определяем содержимое этой бд (наполняем её)
4 - в функциях начинающихся на test_... мы делаем проверки, и при невалидных данных вызываем AssertionError
5 - AssertionError мы вызываем посредством встроенных методов типа 
self.assertionIn, self.assertionEqual или self.assertTemplateUsed и т.д.
6 - Отдельным особняком стоит self.assertRaises который используется в контекстном менеджере
если ниже self.assertRaises(ValidationError) не вызовется ValidationError то функция вызовет AssertionError
в общем смотри выше в коде

7 - все эти функции вызываются python manage.py test


                        Coverage
https://coverage.readthedocs.io/en/6.3.2/

библиотека, которая позволяет понять, на сколько процентов наш код покрыт тестами

1 - pip install coverage
2 - coverage run manage.py test    -проход тестов в обычном режиме (всё равно что python manage.py test)
3 - coverage report                -ин-фа о том на сколько каждый файл приложения покрыт тестами
4 - coverage html                  -записывает вкорень проекта папку htmlcov

Вся мякотка после использования команды 'coverage html'
В корне проекта появляется папка htmlcov (pycharm может не сразу увидеть)
и там много файлов html. 
В частности, там есть файл index.html
По этому файлу, если открыть его в браузере,
то ты сможешь наглядно увидеть, какую часть кода конкретно покрывают тесты, а какую нет

Интересно, эта библиотека только на Django?
"""
