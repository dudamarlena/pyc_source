# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/aiozmq_util.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 522 bytes
"""Utilities related to aiozmq.
"""
import re, socket

def resolve_endpoint(endpoint):
    """aiozmq does not allow connecting to endpoints via host names, so resolve
    them beforehand...
    """
    TCP_RE = re.compile('^tcp://(.+):(\\d+)|\\*$')
    match = TCP_RE.match(endpoint)
    if not match:
        return endpoint
    return 'tcp://%s:%s' % (
     socket.gethostbyname(match.group(1)),
     match.group(2))