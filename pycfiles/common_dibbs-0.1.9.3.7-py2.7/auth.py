# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/common_dibbs/auth/auth.py
# Compiled at: 2016-09-09 12:17:45
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template, TemplateDoesNotExist
from django.shortcuts import redirect
from common_dibbs.config.configuration import Configuration
import base64, requests

class ClientAuthenticationBackend(object):

    def authenticate(self, username=None, password=None, session_key=None):
        data = {'username': username, 
           'password': password, 
           'session_key': session_key}
        result = None
        response = requests.post('%s/authenticate/' % Configuration().get_central_authentication_service_url(), data=data)
        if response.status_code < 400:
            result = response.json()
        user = None
        if result and result['response']:
            user = User()
            user.username = result['username']
        return {'user': user, 
           'token': result['token']}


default_redirect_form_value = '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <title>Redirection to authentication server</title>\n</head>\n<body>\n    <form id="redirect_form" action="{{ cas_service_target_url }}" method="POST">\n        <input type="hidden" name="session_key" value="{{ session_key }}">\n        <input type="hidden" name="redirect_url" value="{{ redirect_url }}">\n        <button type="submit">You will be redirected to the authentication server</button>\n    </form>\n</body>\n</html>\n'

class CentralAuthenticationMiddleware(object):

    def process_request(self, request):
        session_key = request.session.session_key
        username = None
        password = None
        if 'HTTP_AUTHORIZATION' in request.META and 'Basic ' in request.META.get('HTTP_AUTHORIZATION'):
            s = base64.b64decode(request.META.get('HTTP_AUTHORIZATION').split('Basic ')[1])
            username = s.split(':')[0]
            password = s.split(':')[1]
        auth_backend = ClientAuthenticationBackend()
        authentication_resp = auth_backend.authenticate(username, password, session_key)
        if authentication_resp['user'] is not None and authentication_resp['user'].username not in ('',
                                                                                                    'anonymous'):
            request.user = authentication_resp['user']
            return
        else:
            redirect_url = 'http://%s%s' % (request.META.get('HTTP_HOST'), request.path)
            cas_service_target_url = '%s' % (Configuration().get_central_authentication_service_url(),)
            data = {'request': request, 
               'session_key': session_key, 
               'redirect_url': redirect_url, 
               'cas_service_target_url': cas_service_target_url}
            try:
                t = get_template('redirect_form.html')
            except TemplateDoesNotExist:
                t = Template(default_redirect_form_value)

            c = Context(data)
            html_source = str(t.render(c))
            return HttpResponse(html_source)


def session_logout_view(request):
    session_key = request.session.session_key
    data = {'session_key': session_key}
    result = None
    response = requests.post('%s/session_logout/' % Configuration().get_central_authentication_service_url(), data=data)
    if response.status_code < 400:
        result = response.json()
    return redirect('/')


LOGGED_USERS = {}