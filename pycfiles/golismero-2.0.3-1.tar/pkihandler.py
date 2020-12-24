# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/request/pkihandler.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
import httplib, urllib2
from lib.core.data import conf

class HTTPSPKIAuthHandler(urllib2.HTTPSHandler):

    def __init__(self, key_file):
        urllib2.HTTPSHandler.__init__(self)
        self.key_file = key_file

    def https_open(self, req):
        return self.do_open(self.getConnection, req)

    def getConnection(self, host, timeout=None):
        return httplib.HTTPSConnection(host, key_file=self.key_file, timeout=conf.timeout)