# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/nfs/terra.localdomain/home/rgomes/sources/frgomes/velruse/feature.kotti_auth/velruse/examples/kotti_velruse/kotti_velruse/views.py
# Compiled at: 2013-10-27 19:52:16
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.request import Request
from velruse.api import login_url
from velruse.app import find_providers
log = __import__('logging').getLogger(__name__)

def includeme(config):
    config.add_view(login, route_name='login', request_method='GET', renderer='kotti_velruse:templates/login.mako')
    config.add_view(login_, route_name='login_', renderer='json')
    config.add_view(logged_in, route_name='logged_in', renderer='json')
    config.add_view(logout, route_name='logout', permission='view')
    config.add_route('login', '/login')
    config.add_route('login_', '/login_')
    config.add_route('logged_in', '/logged_in')
    config.add_route('logout', '/logout')
    config.add_static_view(name='static', path='kotti_velruse:static')
    config.add_static_view(name='', path='kotti_velruse:openid-selector')


def login(request):
    settings = request.registry.settings
    project = settings['kotti.site_title']
    return {'project': project, 
       'login_url': request.route_url('login_')}


def login_(request):
    provider = request.params['method']
    settings = request.registry.settings
    if provider not in find_providers(settings):
        raise HTTPNotFound(('Provider "{}" is not configured').format(provider)).exception
    velruse_url = login_url(request, provider)
    payload = dict(request.params)
    if 'yahoo' == provider:
        payload['oauth'] = 'true'
    if 'facebook' == provider:
        payload['scope'] = 'email,publish_stream,read_stream,create_event,offline_access'
    if 'openid' == provider:
        payload['use_popup'] = 'false'
    payload['format'] = 'json'
    redirect = Request.blank(velruse_url, POST=payload)
    try:
        response = request.invoke_subrequest(redirect)
        return response
    except:
        message = ('Provider "{}" is probably misconfigured').format(provider)
        raise HTTPNotFound(message).exception


def logged_in(request):
    token = request.params['token']
    storage = request.registry.velruse_store
    try:
        return storage.retrieve(token)
    except KeyError:
        message = ('invalid token "{}"').format(token)
        log.error(message)
        return {'error': message}


def logout(request):
    from pyramid.security import forget
    request.session.invalidate()
    request.session.flash('Session logoff.')
    headers = forget(request)
    return HTTPFound(location=request.route_url('login'), headers=headers)