# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/springboard/springboard/events.py
# Compiled at: 2015-11-17 11:55:31
from uuid import uuid4
from pyramid.events import NewResponse, NewRequest
from pyramid.events import subscriber
from unicore.google.tasks import pageview
from springboard import utils
ONE_YEAR = 31556952

@subscriber(NewRequest)
def new_request(event):
    request = event.request
    registry = request.registry
    profile_id = registry.settings.get('ga.profile_id')
    if not profile_id:
        request.google_analytics = {}
        return
    request.google_analytics = {'path': request.path, 
       'uip': request.remote_addr, 
       'dr': request.referer or '', 
       'dh': request.domain, 
       'user_agent': request.user_agent, 
       'ul': request.accept_language}


@subscriber(NewResponse)
def new_response(event):
    request = event.request
    registry = request.registry
    response = event.response
    excluded_paths = registry.settings.get('ga.excluded_paths', '')
    profile_id = registry.settings.get('ga.profile_id')
    if profile_id and not utils.is_excluded_path(request.path, excluded_paths):
        client_id = request.cookies.get('ga_client_id', uuid4().hex)
        response.set_cookie('ga_client_id', value=client_id, max_age=ONE_YEAR)
        pageview.delay(profile_id, client_id, request.google_analytics)