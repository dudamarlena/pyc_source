# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/daarmaan/daarmaan/server/views/sso.py
# Compiled at: 2012-11-20 10:20:07
import json, urllib, hashlib
from urlparse import urlparse, urlunparse, parse_qsl, ParseResult
from django.conf.urls import patterns, include, url
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.conf import settings
from vakhshour.base import Node
from vakhshour.amp.ampy import Proxy
from daarmaan.server.models import Service
from daarmaan.utils import DefaultValidation

class DaarmaanServer(object):
    """
    Daarmaan SSO service server class. This class take care of SSO activities.
    """
    node = Node(**settings.VAKHSHOUR)

    @property
    def urls(self):
        """
        Url dispatcher property.
        """
        urlpatterns = patterns('', url('^authenticate/$', self.authenticate, name='remote-auth'), url('^verification/$', self.verify, name='remote-auth'), url('^logout/$', self.logout, name='logout'))
        return urlpatterns

    def authenticate(self, request):
        """
        Check the request for authenticated user. If user is not authenticated
        then redirect user to login view.
        """
        next_url = request.GET.get('next', None)
        service = self._get_service(request)
        if not service:
            return HttpResponseForbidden('Invalid service')
        else:
            validator = DefaultValidation(service.key)
            try:
                next_url = urlparse(urllib.unquote(next_url).decode('utf8'))
            except AttributeError as e:
                if 'HTTP_REFERER' in request.META:
                    next_url = urlparse(request.META['REFERER'])
                else:
                    next_url = urlparse(service.default_url)

            params = dict(parse_qsl(next_url[4]))
            print '!!!>>>>>> ', params, next_url[:]
            if request.user.is_authenticated():
                ticket = request.session.session_key
                params.update({'ticket': ticket, 'hash': validator.sign(ticket)})
            else:
                params.update({'ack': ''})
            next_url = ParseResult(next_url[0], next_url[1], next_url[2], next_url[3], urllib.urlencode(params), next_url[5])
            print '>>>> ', next_url
            next_url = next_url.geturl()
            print '<<<< ', next_url
            return HttpResponseRedirect(next_url)

    def verify(self, request):
        """
        verify the user token that friend service sent.
        """
        hash_ = request.GET.get('hash', None)
        token = request.GET.get('token', None)
        service = self._get_service(request)
        if not hash_ or not token or not service:
            return HttpResponseForbidden()
        else:
            validator = DefaultValidation(service.key)
            if not validator.is_valid(token, hash_):
                return HttpResponseForbidden()
            try:
                session = Session.objects.get(session_key=token)
            except Session.DoesNotExist:
                pass

            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
            if user.is_authenticated():
                a = {'id': user.id, 
                   'username': user.username, 
                   'first_name': user.first_name, 
                   'last_name': user.last_name, 
                   'email': user.email, 
                   'id': user.pk, 
                   'is_staff': user.is_staff, 
                   'is_active': user.is_active}
                m = True
            else:
                a = {'username': ''}
                m = False
            result = {'data': a}
            if m:
                result.update({'hash': validator.sign(user.username)})
            else:
                result.update({'hash': ''})
            return HttpResponse(json.dumps(result))

    def logout(self, request):
        """
        Log the user out and send the logout event.
        """
        next_url = request.GET.get('next', None)
        service = request.GET.get('service', None)
        if request.user.is_authenticated():
            logout(request)
            try:
                self.node.send_event(name='logout', sender='daarmaan', ticket=request.session.session_key)
            except Proxy.ConnectionRefused:
                pass

        if not next_url:
            next_url = request.META.get('HTTP_REFERER', None)
        if not next_url:
            next_url = '/'
        return HttpResponseRedirect(next_url)

    def _get_service(self, request):
        """
        Extract the service object from request.
        """
        service = request.GET.get('service', None)
        if not service:
            return
        else:
            try:
                service = Service.objects.get(name=service, active=True)
            except Service.DoesNotExist:
                return

            return service


daarmaan_service = DaarmaanServer()