# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/request/basicauthhandler.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
import urllib2

class SmartHTTPBasicAuthHandler(urllib2.HTTPBasicAuthHandler):
    """
    Reference: http://selenic.com/hg/rev/6c51a5056020
    Fix for a: http://bugs.python.org/issue8797
    """

    def __init__(self, *args, **kwargs):
        urllib2.HTTPBasicAuthHandler.__init__(self, *args, **kwargs)
        self.retried_req = set()
        self.retried_count = 0

    def reset_retry_count(self):
        pass

    def http_error_auth_reqed(self, auth_header, host, req, headers):
        if hash(req) not in self.retried_req:
            self.retried_req.add(hash(req))
            self.retried_count = 0
        elif self.retried_count > 5:
            raise urllib2.HTTPError(req.get_full_url(), 401, 'basic auth failed', headers, None)
        else:
            self.retried_count += 1
        return urllib2.HTTPBasicAuthHandler.http_error_auth_reqed(self, auth_header, host, req, headers)