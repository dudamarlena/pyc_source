# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cblog/spamfilters/blacklist.py
# Compiled at: 2006-12-06 04:38:00
blacklist = [
 '127.0.0.1']
import logging
log = logging.getLogger('turbogears.controllers')

def filter(value, state=None):
    request = state.get('request')
    log.info('Comment submission from IP %s' % getattr(request, 'remote_addr', '<unknown>'))
    if request and request.remote_addr in blacklist:
        return 10
    return 0