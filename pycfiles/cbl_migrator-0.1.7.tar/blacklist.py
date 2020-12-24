# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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