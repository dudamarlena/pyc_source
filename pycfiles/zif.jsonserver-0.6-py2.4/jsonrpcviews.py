# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zif/jsonserver/tests/jsonrpcviews.py
# Compiled at: 2007-05-25 16:54:16
"""JSON-RPC Views test objects

adapted from zope.publisher.tests.xmlrpcviews
jwashin 2005-06-06
altered import to reflect zif namespace jmw 20061216

"""
from zope.interface import Interface, implements
from zif.jsonserver.interfaces import IJSONRPCPublisher

class IC(Interface):
    __module__ = __name__


class V1(object):
    __module__ = __name__
    implements(IJSONRPCPublisher)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def action(self):
        return 'done'

    def index(self):
        return 'V1 here'


class VZMI(V1):
    __module__ = __name__


class R1(object):
    __module__ = __name__

    def __init__(self, request):
        self.request = request

    implements(IJSONRPCPublisher)


class RZMI(R1):
    __module__ = __name__