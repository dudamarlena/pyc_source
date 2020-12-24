# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/countries/viewsdispatcher.py
# Compiled at: 2016-12-06 14:21:44
# Size of source mod 2**32: 955 bytes
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.db.models import Q
from ohm2_handlers import utils as h_utils
from . import settings
from . import utils as countries_utils
from .decorators import countries_safe_request
from .definitions import CountriesRunException, CountriesMethodException
import os, time, random, datetime

@countries_safe_request
def view_base(request, method, function, keys):
    if request.method == method:
        params, holder = {'request': request}, getattr(request, method)
        for o in keys:
            params[o[0]] = holder.get(o[1], o[2])

        return function(params)
    raise CountriesMethodException(request.method, request.META.get('REMOTE_ADDR', ''))


def index(params):
    p = h_utils.cleaned(params, (('request', 'request', ''), ))
    request = p['request']
    ret = {}
    return ret