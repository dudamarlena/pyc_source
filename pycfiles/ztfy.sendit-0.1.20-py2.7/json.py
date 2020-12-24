# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sendit/client/browser/json.py
# Compiled at: 2013-05-31 13:02:11
from ztfy.sendit.client.interfaces import ISenditClient
from z3c.jsonrpc.publisher import MethodPublisher
from zope.component import queryUtility

class SenditClientMethodsPublisher(MethodPublisher):
    """Sendit client methods publisher"""

    def findSenditPrincipals(self, query, names=None):
        sendit = queryUtility(ISenditClient)
        if sendit is None:
            return ()
        else:
            return sendit.searchPrincipals(query, names, request=self.request)