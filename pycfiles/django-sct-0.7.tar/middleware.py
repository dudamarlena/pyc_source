# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/herbert/dev/python/sctdev/simpleproject/simpleproject/../../communitytools/sphenecoll/sphene/community/middleware.py
# Compiled at: 2012-03-17 12:42:14
from django.conf import settings
from django.conf.urls.defaults import *
from django.core import urlresolvers
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import SiteManager, Site
from sphene.community.models import Group
from sphene.community.sphsettings import get_sph_setting
import re, logging
logger = logging.getLogger('sphene.community.middleware')

def my_get_current(self):
    try:
        group = get_current_group()
    except AttributeError, e:
        group = None

    if not group:
        return self.get(pk=settings.SITE_ID)
    else:
        return Site(pk=settings.SITE_ID, domain=group.baseurl, name=group.name)
        return


SiteManager.get_current = my_get_current

class MultiHostMiddleware:

    def process_request(self, request):
        try:
            sphdata = get_current_sphdata()
            host = request.META['HTTP_HOST']
            if host[-3:] == ':80':
                host = host[:-3]
            urlconf = None
            urlconf_params = None
            if host in settings.SPH_HOST_MIDDLEWARE_URLCONF_MAP:
                urlconf = settings.SPH_HOST_MIDDLEWARE_URLCONF_MAP[host]
            else:
                for (key, value) in settings.SPH_HOST_MIDDLEWARE_URLCONF_MAP.iteritems():
                    regex = re.compile(key)
                    match = regex.match(host)
                    if not match:
                        continue
                    urlconf = value
                    urlconf_params = 'params' in urlconf and urlconf['params'].copy() or dict()
                    namedgroups = match.groupdict()
                    for (key, value) in namedgroups.iteritems():
                        urlconf_params[key] = value

                    break

                if not urlconf:
                    logging.info('Unable to find urlconf for %s / map: %s !!!' % (host, str(settings.SPH_HOST_MIDDLEWARE_URLCONF_MAP)))
                    return
                while 'alias' in urlconf:
                    urlconf = settings.SPH_HOST_MIDDLEWARE_URLCONF_MAP[urlconf['alias']]

                myparams = urlconf_params or urlconf['params']
                if myparams and 'groupName' in myparams:
                    try:
                        set_current_group(Group.objects.get(name__exact=myparams['groupName']))
                        sphdata['group_fromhost'] = True
                    except Group.DoesNotExist:
                        pass

                set_current_urlconf_params(urlconf_params or urlconf['params'])
            request.urlconf = urlconf['urlconf']
        except KeyError:
            pass

        return


class GroupMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        request.attributes = {}
        if 'urlPrefix' in view_kwargs:
            urlPrefix = view_kwargs['urlPrefix']
            if urlPrefix != '':
                urlPrefix = '/' + urlPrefix
            request.attributes['urlPrefix'] = urlPrefix
            del view_kwargs['urlPrefix']
        group = None
        groupName = None
        if get_current_urlconf_params() and 'groupName' in get_current_urlconf_params():
            groupName = get_current_urlconf_params()['groupName']
            group = get_current_group()
            if group is None or group.name != groupName:
                try:
                    group = get_object_or_404(Group, name=groupName)
                except Http404, e:
                    if not view_func.__module__.startswith('django.contrib.admin.'):
                        raise e

        if 'groupName' in view_kwargs:
            if view_kwargs.get('noGroup', False):
                del view_kwargs['groupName']
                del view_kwargs['noGroup']
            else:
                groupName = view_kwargs['groupName']
                if groupName == None:
                    groupName = get_current_urlconf_params()['groupName']
                sphdata = get_current_sphdata()
                if group == None:
                    group = get_object_or_404(Group, name=groupName)
                    sphdata['group_fromhost'] = not get_sph_setting('community_groups_in_url')
                del view_kwargs['groupName']
                view_kwargs['group'] = group
                request.attributes['group'] = group
        set_current_group(group)
        return


try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

def get_current_request():
    return getattr(_thread_locals, 'request', None)


def get_current_urlconf():
    return getattr(get_current_request(), 'urlconf', None)


def get_current_session():
    req = get_current_request()
    if req == None:
        return
    else:
        return req.session


def get_current_user():
    user = getattr(_thread_locals, 'user', None)
    if user != None:
        return user
    else:
        req = get_current_request()
        if req == None:
            return
        return req.user


def get_current_group():
    try:
        return _thread_locals.group
    except AttributeError, e:
        logger.error('Unable to retrieve group. Is GroupMiddleware enabled?')
        raise e


def get_current_urlconf_params():
    return getattr(_thread_locals, 'urlconf_params', None)


def set_current_urlconf_params(urlconf_params):
    _thread_locals.urlconf_params = urlconf_params


def set_current_group(group):
    _thread_locals.group = group


def get_current_sphdata():
    return getattr(_thread_locals, 'sphdata', None)


class ThreadLocals(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""

    def process_request(self, request):
        _thread_locals.request = request
        _thread_locals.user = getattr(request, 'user', None)
        _thread_locals.sphdata = {}
        try:
            delattr(_thread_locals, 'urlconf_params')
        except AttributeError:
            pass

        _thread_locals.group = None
        return


import re
from operator import add
from time import time
from django.db import connection
import logging
logger = logging.getLogger('sphene.community.middleware')

class StatsMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        from django.conf import settings
        debug = settings.DEBUG
        settings.DEBUG = True
        n = len(connection.queries)
        start = time()
        response = None
        try:
            response = view_func(request, *view_args, **view_kwargs)
        finally:
            if request.path.startswith('/static'):
                return response
            totTime = time() - start
            queries = len(connection.queries) - n
            if queries:
                dbTime = reduce(add, [ float(q['time']) for q in connection.queries[n:]
                                     ])
            else:
                dbTime = 0.0
            pyTime = totTime - dbTime
            settings.DEBUG = debug
            stats = {'totTime': totTime, 
               'pyTime': pyTime, 
               'dbTime': dbTime, 
               'queries': queries}
            if response and response.content:
                s = response.content
                regexp = re.compile('(?P<cmt><!--\\s*STATS:(?P<fmt>.*?)-->)')
                match = regexp.search(s)
                if match:
                    s = s[:match.start('cmt')] + match.group('fmt') % stats + s[match.end('cmt'):]
                    out = match.group('fmt') % stats
                    response.content = s
            querystr = ''
            for query in connection.queries:
                sql = query['sql']
                if sql is None:
                    sql = ' ?WTF?None?WTF? '
                querystr += '\t' + query['time'] + '\t' + sql + '\n'

            logger.debug('All Queries: %s' % (querystr,))
            logger.info('Request %s: %s' % (request.get_full_path(), stats))

        return response


from django.core.handlers.modpython import ModPythonRequest

class ModPythonSetLoggedinUser(object):

    def process_request(self, request):
        if not isinstance(request, ModPythonRequest):
            return
        else:
            if not hasattr(request, '_req'):
                return
            if not hasattr(request, 'user') or not request.user.is_authenticated():
                return
            request._req.user = str(request.user.username)
            return


class PsycoMiddleware(object):

    def process_request(self, request):
        import psyco
        psyco.profile()
        return


from sphene.community import PermissionDenied
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.template import loader
from django.http import HttpResponseForbidden

class PermissionDeniedMiddleware(object):

    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):
            return HttpResponseForbidden(loader.render_to_string('sphene/community/permissiondenied.html', {'exception': exception}, context_instance=RequestContext(request)))
        else:
            return


class LastModified(object):
    """ Middleware that sets the Last-Modified and associated headers,
    if requested by the view. (By setting the sph_lastmodified attribute
    of the response object.

    based on a contribution of Andrew Plotkin:
    http://eblong.com/zarf/boodler/sitework/
    """

    def process_response(self, request, response):
        stamp = getattr(response, 'sph_lastmodified', None)
        if not stamp:
            return response
        else:
            import rfc822, calendar
            if stamp is True:
                val = rfc822.formatdate()
            else:
                val = rfc822.formatdate(calendar.timegm(stamp.timetuple()))
            response['Last-Modified'] = val
            response['Cache-Control'] = 'private, must-revalidate, max-age=0'
            return response