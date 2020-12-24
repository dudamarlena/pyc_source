# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/scheduler/security.py
# Compiled at: 2012-10-22 06:18:07
__docformat__ = 'restructuredtext'
from hurry.query.interfaces import IQuery
from zope.authentication.interfaces import IAuthentication
from ztfy.security.interfaces import IGrantedRoleEvent, IRevokedRoleEvent
from hurry.query.set import AnyOf
from zope.component import adapter, getUtility, getUtilitiesFor
from ztfy.security.indexer import ALL_ROLES_INDEX_NAME

@adapter(IGrantedRoleEvent)
def handleGrantedOperatorRole(event):
    if event.role in ('ztfy.SchedulerManager', 'ztfy.SchedulerOperator'):
        for _name, auth in getUtilitiesFor(IAuthentication):
            operators = auth.get('groups', {}).get('operators', None)
            if operators and event.principal not in operators.principals:
                operators.principals = operators.principals + (event.principal,)

    return


@adapter(IRevokedRoleEvent)
def handleRevokedOperatorRole(event):
    if event.role in ('ztfy.SchedulerManager', 'ztfy.SchedulerOperator'):
        query = getUtility(IQuery)
        objects = query.searchResults(AnyOf(('SecurityCatalog', ALL_ROLES_INDEX_NAME), (
         event.principal,)))
        if not objects or len(objects) == 1 and event.object in objects:
            for _name, auth in getUtilitiesFor(IAuthentication):
                operators = auth.get('groups', {}).get('operators', None)
                if operators is not None and event.principal in operators.principals:
                    principals = list(operators.principals)
                    principals.remove(event.principal)
                    operators.principals = tuple(principals)

    return