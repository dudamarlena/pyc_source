# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/marcel/projects/quatix/django-shipping/shipping/views.py
# Compiled at: 2013-03-16 14:41:33
import json, logging
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, Http404
from shipping.models import Country, State
from shipping.carriers import InterfaceError

def countries(request):
    countries = Country.objects.filter(zone__status=1).filter(status=1).order_by('name')
    response = {'countries': []}
    for country in countries:
        response['countries'].append({'iso': country.iso, 'name': country.name})

    return HttpResponse(json.dumps(response), mimetype='application/json;charset=utf-8')


def states(request, country_code):
    country = get_object_or_404(Country, iso=country_code)
    states = country.states.order_by('name').all()
    response = {'states': []}
    for state in states:
        response['states'].append({'iso': state.iso, 'name': state.name, 'id': state.id})

    return HttpResponse(json.dumps(response), mimetype='application/json;charset=utf-8')


@csrf_protect
def estimation(request):
    dimensions = request.POST.getlist('dimensions')
    zipcode = request.POST.get('zipcode')
    state = request.POST.get('state')
    country_code = request.POST.get('country_code')
    country = get_object_or_404(Country, iso=country_code)
    if state:
        state = get_object_or_404(State, id=state)
    if len(dimensions) < 1:
        raise Http404()
    try:
        carrier = country.zone.get_carrier()
        price, currency = carrier.estimate_shipping(dimensions, country, zipcode=zipcode, state=state)
        response = json.dumps({'price': price, 'currency': currency})
    except InterfaceError as ie:
        logging.exception('oops, problem when estimate shipping')
        response = json.dumps({'error': str(ie), 'code': 'interface'})
    except ValueError as ve:
        logging.exception('oops, problem when estimate shipping')
        response = json.dumps({'error': str(ve), 'code': 'value'})
    except:
        logging.exception('oops, problem when estimate shipping')
        response = json.dumps({'error': str(ve), 'code': 'except'})

    return HttpResponse(response, mimetype='application/json;charset=utf-8')