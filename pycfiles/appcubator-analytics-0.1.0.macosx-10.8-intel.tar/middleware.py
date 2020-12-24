# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kssworld93/Projects/appcubator-site/venv/lib/python2.7/site-packages/analytics/middleware.py
# Compiled at: 2013-07-23 20:43:55
from datetime import datetime, timedelta
import logging, re, traceback
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.utils import DatabaseError
from analytics import utils
from analytics.models import Visitor
title_re = re.compile('<title>(.*?)</title>')
logging.basicConfig(filename='analytics.log', level=logging.DEBUG)
log = logging.getLogger('analytics.middleware')

class VisitorAnalyticsMiddleware(object):
    """
    TODO: add dox
    """

    @property
    def prefixes(self):
        """Returns a list of URL prefixes that we should not track"""
        if not hasattr(self, '_prefixes'):
            self._prefixes = getattr(settings, 'NO_TRACKING_PREFIXES', [])
            if not getattr(settings, '_FREEZE_TRACKING_PREFIXES', False):
                for name in ('MEDIA_URL', 'STATIC_URL'):
                    url = getattr(settings, name)
                    if url and url != '/':
                        self._prefixes.append(url)

                try:
                    self._prefixes.append(reverse('tracking-refresh-active-users'))
                except NoReverseMatch:
                    pass

                settings.NO_TRACKING_PREFIXES = self._prefixes
                settings._FREEZE_TRACKING_PREFIXES = True
        return self._prefixes

    def process_request(self, request):
        if request.is_ajax():
            return
        else:
            ip_address = utils.get_ip(request)
            user_agent = unicode(request.META.get('HTTP_USER_AGENT', '')[:255], errors='ignore')
            if hasattr(request, 'session') and request.session.session_key:
                session_key = request.session.session_key
            else:
                session_key = '%s:%s' % (ip_address, user_agent)
                session_key = session_key[:40]
            for prefix in self.prefixes:
                if request.path.startswith(prefix):
                    log.debug('Not tracking request to: %s' % request.path)
                    return

            now = datetime.now()
            if getattr(settings, 'USE_TZ', False):
                import pytz
                tz = pytz.timezone(settings.TIME_ZONE)
                now = tz.localize(now)
            url = request.path
            attrs = {'session_key': session_key, 
               'ip_address': ip_address, 
               'url': url}
            try:
                visitor = Visitor.objects.get(**attrs)
            except Visitor.DoesNotExist:
                cutoff = now - timedelta(seconds=2)
                visitors = Visitor.objects.filter(ip_address=ip_address, user_agent=user_agent, url=url, last_update__gte=cutoff)
                if len(visitors):
                    visitor = visitors[0]
                    visitor.session_key = session_key
                    log.debug('Using existing visitor for IP %s / UA %s: %s' % (ip_address, user_agent, visitor.id))
                else:
                    visitor = Visitor(**attrs)
                    log.debug('Created a new visitor: %s' % attrs)
            except:
                return

            user = request.user
            if isinstance(user, AnonymousUser):
                user = None
            if user is None:
                visitor.user_id = None
            else:
                visitor.user_id = user.id
            visitor.user_agent = user_agent
            if not visitor.last_update:
                visitor.referrer = utils.u_clean(request.META.get('HTTP_REFERER', 'unknown')[:255])
                visitor.session_start = now
            visitor.page_views += 1
            visitor.last_update = now
            try:
                visitor.save()
            except DatabaseError:
                log.error('There was a problem saving visitor information:\n%s\n\n%s' % (traceback.format_exc(), locals()))

            return