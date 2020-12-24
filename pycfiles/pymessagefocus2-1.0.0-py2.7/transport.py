# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymessagefocus2/transport.py
# Compiled at: 2016-08-14 13:02:21
from xmlrpclib import SafeTransport
from fault import Fault

class Transport(SafeTransport):

    def __init__(self, **kwargs):
        SafeTransport.__init__(self, **kwargs)

    @Fault.parse
    def single_request(self, *args, **kwargs):
        return SafeTransport.single_request(self, *args, **kwargs)