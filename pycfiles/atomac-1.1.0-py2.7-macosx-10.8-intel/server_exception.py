# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/atomac/ldtpd/server_exception.py
# Compiled at: 2012-10-05 17:37:25
"""Exception class."""
import xmlrpclib
ERROR_CODE = 123

class LdtpServerException(xmlrpclib.Fault):

    def __init__(self, message):
        xmlrpclib.Fault.__init__(self, ERROR_CODE, message)