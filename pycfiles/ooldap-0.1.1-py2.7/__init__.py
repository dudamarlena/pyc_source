# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/ooldap/__init__.py
# Compiled at: 2015-10-07 16:05:24
import ldap
GLOBAL_GROUP = '-2147483646'
UNIVERSAL_GROUP = '-2147483640'

class Connection(object):

    def __init__(self, uri, dn, password):
        self.uri = uri
        self.dn = dn
        self.password = password
        assert uri and dn and password

    def bind(self):
        self.stream = ldap.open(self.uri)
        self.stream.simple_bind_s(self.dn, self.password)

    def unbind(self):
        self.stream.unbind_s()