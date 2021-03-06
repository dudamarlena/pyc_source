# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyogp/apps/web/django/pyogp_webbot/login/views.py
# Compiled at: 2009-12-22 03:50:08
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from pyogp.lib.client.agent import Agent
from pyogp.lib.client.settings import Settings
from pyogp.lib.base.helpers import Wait
from pyogp.lib.base.exc import LoginError
from eventlet import api
import time

def index(request):
    return render_to_response('index.html')


def login(request, firstname=None, lastname=None, error_message=None):
    return render_to_response('login.html', {'firstname': firstname, 'lastname': lastname, 'error_message': error_message})


def login_request(request, firstname=None, lastname=None, password=None, error_message=None):
    if request.POST:
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']
    try:
        bot_settings = Settings()
        bot_settings.ENABLE_INVENTORY_MANAGEMENT = True
        bot_settings.ENABLE_COMMUNICATIONS_TRACKING = False
        bot_settings.ENABLE_OBJECT_TRACKING = False
        bot_settings.ENABLE_UDP_LOGGING = True
        bot_settings.ENABLE_EQ_LOGGING = True
        bot_settings.ENABLE_CAPS_LOGGING = True
        bot_settings.MULTIPLE_SIM_CONNECTIONS = False
        client = Agent(settings=bot_settings, handle_signals=False)
        api.spawn(client.login, 'https://login.aditi.lindenlab.com/cgi-bin/login.cgi', firstname, lastname, password)
        now = time.time()
        start = now
        while now - start < 15:
            api.sleep()

    except LoginError, e:
        error_message = e
        return HttpResponse("would like to show the login form again, with any error message that's appropriate, like: %s" % error_message)