# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/statsd-tags/defaults/django.py
# Compiled at: 2019-11-08 09:56:25
# Size of source mod 2**32: 615 bytes
from __future__ import absolute_import
from django.conf import settings
from statsd import defaults
from statsd.client import StatsClient
statsd = None
if statsd is None:
    host = getattr(settings, 'STATSD_HOST', defaults.HOST)
    port = getattr(settings, 'STATSD_PORT', defaults.PORT)
    prefix = getattr(settings, 'STATSD_PREFIX', defaults.PREFIX)
    maxudpsize = getattr(settings, 'STATSD_MAXUDPSIZE', defaults.MAXUDPSIZE)
    ipv6 = getattr(settings, 'STATSD_IPV6', defaults.IPV6)
    statsd = StatsClient(host=host, port=port, prefix=prefix, maxudpsize=maxudpsize,
      ipv6=ipv6)