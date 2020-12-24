# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/nacl/security.py
# Compiled at: 2007-12-02 16:26:59
from salamoia.h2o.logioni import Ione

class SecurityControl(object):
    __module__ = __name__

    def getACL(self, *ids):
        res = [ x.acl for x in self.fetch(list(ids)) ]
        return [ [ str(ace) for ace in acl ] for acl in res ]