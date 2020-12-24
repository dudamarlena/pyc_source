# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/statsd-tags/defaults/env.py
# Compiled at: 2019-11-08 09:56:25
# Size of source mod 2**32: 573 bytes
from __future__ import absolute_import
import os
from statsd import defaults
from statsd.client import StatsClient
statsd = None
if statsd is None:
    host = os.getenv('STATSD_HOST', defaults.HOST)
    port = int(os.getenv('STATSD_PORT', defaults.PORT))
    prefix = os.getenv('STATSD_PREFIX', defaults.PREFIX)
    maxudpsize = int(os.getenv('STATSD_MAXUDPSIZE', defaults.MAXUDPSIZE))
    ipv6 = bool(int(os.getenv('STATSD_IPV6', defaults.IPV6)))
    statsd = StatsClient(host=host, port=port, prefix=prefix, maxudpsize=maxudpsize,
      ipv6=ipv6)