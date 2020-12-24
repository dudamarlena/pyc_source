# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eyefi/google_loc.py
# Compiled at: 2010-11-25 06:25:10
import simplejson
from twisted.web.client import getPage
LOC_BASE_URL = 'http://www.google.com/loc/json'

def google_loc(*macs, **args):
    """
    http://code.google.com/p/gears/wiki/GeolocationAPI
    """
    base = {'version': '1.1.0', 
       'host': 'maps.google.com'}
    base.update(args)
    for mac in macs:
        base.setdefault('wifi_towers', []).append({'mac_address': mac})

    d = getPage(LOC_BASE_URL, method='POST', postdata=simplejson.dumps(base))
    d.addCallback(simplejson.loads)
    return d


def main():
    from twisted.internet import reactor
    from twisted.python import log
    import sys
    log.startLogging(sys.stdout)
    google_loc(sys.argv[1:], request_address=True).addBoth(log.msg).addBoth(lambda e: reactor.callLater(0, reactor.stop))
    reactor.run()


if __name__ == '__main__':
    main()