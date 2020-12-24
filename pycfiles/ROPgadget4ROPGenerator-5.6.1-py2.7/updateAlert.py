# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ropgadget/updateAlert.py
# Compiled at: 2018-03-17 16:59:29
import re
try:
    import httplib
except ImportError:
    import http.client as httplib

from ropgadget.version import *

class UpdateAlert(object):

    @staticmethod
    def checkUpdate():
        try:
            conn = httplib.HTTPSConnection('raw.githubusercontent.com', 443)
            conn.request('GET', '/JonathanSalwan/ROPgadget/master/ropgadget/version.py')
        except:
            print "Can't connect to raw.githubusercontent.com"
            return

        d = conn.getresponse().read()
        majorVersion = re.search('MAJOR_VERSION.+=.+(?P<value>[\\d])', d).group('value')
        minorVersion = re.search('MINOR_VERSION.+=.+(?P<value>[\\d])', d).group('value')
        webVersion = int('%s%s' % (majorVersion, minorVersion))
        curVersion = int('%s%s' % (MAJOR_VERSION, MINOR_VERSION))
        if webVersion > curVersion:
            print 'The version %s.%s is available. Currently, you use the version %d.%d.' % (majorVersion, minorVersion, MAJOR_VERSION, MINOR_VERSION)
        else:
            print 'Your version is up-to-date.'