# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/networking/net/managers.py
# Compiled at: 2013-09-08 06:03:46
from netfields.managers import NetQuery, NetWhere, NetManager
from nodeshot.core.base.managers import ExtendedManagerMixin, ACLMixin, AccessLevelQuerySet

class NetAccessLevelManager(NetManager, ExtendedManagerMixin, ACLMixin):
    """ NetManager + AccessLevelManager """

    def get_query_set(self):
        q = NetQuery(self.model, NetWhere)
        return AccessLevelQuerySet(self.model, using=self._db, query=q)