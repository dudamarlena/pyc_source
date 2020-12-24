# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sendit/app/browser/json/search.py
# Compiled at: 2013-05-22 04:27:09
__docformat__ = 'restructuredtext'
from z3c.jsonrpc.publisher import MethodPublisher
from ztfy.security.search import findPrincipals

def getPrincipalTitle(principal):
    title = principal.title
    if '@' in principal.id:
        _name, domain = principal.id.split('@')
        title = '%s (%s)' % (title, domain)
    return title


class PrincipalSearchView(MethodPublisher):
    """Filtered principal search view"""

    def findFilteredPrincipals(self, query, names=None):
        app = self.context
        return [ {'value': principal.id, 'caption': getPrincipalTitle(principal)} for principal in findPrincipals(query, names) if principal.id not in (app.excluded_principals or ())
               ]