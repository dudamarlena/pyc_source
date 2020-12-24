# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yash/Desktop/django-query-profiler/tests/testapp/food/views.py
# Compiled at: 2020-01-04 02:30:17
# Size of source mod 2**32: 911 bytes
from django.http import HttpRequest, HttpResponse
from tests.testapp.food.models import Pizza, Restaurant

def index(request: HttpRequest) -> HttpResponse:
    pizzas = Pizza.objects.all()
    [pizza.spicy_toppings_db_filtering() for pizza in pizzas]
    [pizza.spicy_toppings_python_filtering() for pizza in pizzas]
    [pizza.toppings_of_best_pizza_serving_restaurants() for pizza in pizzas]
    [pizza.spicy_toppings_db_filtering() for pizza in Pizza.objects.prefetch_related('toppings').all()]
    [pizza.spicy_toppings_python_filtering() for pizza in Pizza.objects.prefetch_related('toppings').all()]
    [pizza.toppings_of_best_pizza_serving_restaurants() for pizza in Pizza.objects.prefetch_related('toppings').all()]
    list(Restaurant.objects.all())
    return HttpResponse('Made all the db calls, now test the calls made via profiler')