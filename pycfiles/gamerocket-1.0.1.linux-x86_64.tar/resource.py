# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gamerocket/resource.py
# Compiled at: 2013-08-09 04:10:05
from attribute_getter import AttributeGetter

class Resource(AttributeGetter):

    def __init__(self, gateway, attributes):
        AttributeGetter.__init__(self, attributes)
        self.gateway = gateway