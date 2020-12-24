# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: examples/couchdbrouter.py
# Compiled at: 2011-05-05 17:34:06
import re
re_host = re.compile('Host:\\s*(.*)\r\n')

class CouchDBRouter(object):

    def lookup(self, name):
        """ do something """
        return ('127.0.0.1', 5984)


router = CouchDBRouter()

def proxy(data):
    matches = re_host.findall(data)
    if matches:
        host = router.lookup(matches.pop())
        return {'remote': host}
    else:
        return