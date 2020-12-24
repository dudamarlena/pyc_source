# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/ipauth/backend.py
# Compiled at: 2012-12-03 15:51:39
from logging import getLogger
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from ipauth.models import Range, IP
log = getLogger('ipauth.backend')

class RangeBackend(ModelBackend):
    supports_anonymous_user = False

    def authenticate(self, ip=None):
        try:
            ip = IP(ip)
            current = Range.objects.get(Q(lower=ip) | Q(lower__lte=ip, upper__gte=ip))
            log.info('Authenticating %s from %s' % (unicode(current.user), unicode(ip)))
            return current.user
        except Range.DoesNotExist:
            log.error('Authentication failed for %s' % (unicode(ip),))

        return