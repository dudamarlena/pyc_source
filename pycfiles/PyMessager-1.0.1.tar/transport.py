# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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