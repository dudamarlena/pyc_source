# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/entityaccessmanager.py
# Compiled at: 2012-10-12 07:02:39
import time, logging
from sqlalchemy import *
from exception import *
from coils.foundation import *
COILS_CORE_FULL_PERMISSIONS = [
 'r', 'w', 'l', 'd', 'a',
 'k', 't', 'x', 'i', 'v']

class EntityAccessManager(object):
    """ Calculate the access to an entity in the current context.
        There is no single point of the code more performance critical than
        this object.  The server actually spends most of its time
        right here.
    """
    __DebugOn__ = None

    def __init__(self, ctx):
        if hasattr(self, '__entity__'):
            if isinstance(self.__entity__, list):
                name = ''
                for e in self.__entity__:
                    if len(name) > 0:
                        name = '%s-%s' % (name, e.lower())
                    else:
                        name = e.lower()

            else:
                name = self.__entity__.lower()
            self.log = logging.getLogger('access.%s' % name)
        else:
            self.log = logging.getLogger('entityaccessmanager')
            self.log.warn(('{0} has not __entity__ attribute').format(repr(self)))
        if EntityAccessManager.__DebugOn__ is None:
            sd = ServerDefaultsManager()
            EntityAccessManager.__DebugOn__ = sd.bool_for_default('OGoAccessManagerDebugEnabled')
        self._ctx = ctx
        return

    @property
    def debug(self):
        return EntityAccessManager.__DebugOn__

    def materialize_rights(self, **params):
        if params.has_key('objects'):
            objects = params['objects']
        else:
            return {}
        if params.get('contexts', None) is not None:
            self.context_ids = params.get('contexts')
        else:
            if self._ctx.is_admin:
                if self.debug:
                    self.log.debug('administrative account has all rights to all objects if no contexts are specified')
                rights = {}
                for entity in objects:
                    rights[entity] = set()
                    for right in list('lrwadv'):
                        rights[entity].add(right)

                return rights
            self.context_ids = self._ctx.context_ids
        start = time.time()
        rights = self.implied_rights(objects)
        if self.debug:
            self.log.debug('duration of implied rights was %0.3f' % (time.time() - start))
        start = time.time()
        rights = self.asserted_rights(rights)
        if self.debug:
            self.log.debug('duration of asserted rights was %0.3f' % (time.time() - start))
        start = time.time()
        rights = self.revoked_rights(rights)
        if self.debug:
            self.log.debug('duration of revoked rights was %0.3f' % (time.time() - start))
        return rights

    def default_rights(self):
        return COILS_CORE_FULL_PERMISSIONS

    def implied_rights(self, objects):
        rights = {}
        for entity in objects:
            rights[entity] = set()

        return rights

    def asserted_rights(self, object_rights):
        for entity in object_rights.keys():
            if hasattr(entity, 'acls'):
                rights = object_rights[entity]
                permissions = set(list(self.get_acls('allowed', entity)))
                for right in permissions:
                    rights.add(right)

                object_rights[entity] = rights

        return object_rights

    def revoked_rights(self, object_rights):
        for entity in object_rights.keys():
            if hasattr(entity, 'acls'):
                asserted = object_rights[entity]
                denied = self.get_acls('denied', entity)
                object_rights[entity] = asserted.difference(denied)

        return object_rights

    def get_acls(self, action, entity):
        rights = set()
        counter = 0
        for acl in entity.acls:
            if acl.action == action:
                counter = counter + 1
                if acl.context_id in self.context_ids:
                    permissions = set(list(acl.permissions))
                    if permissions.issubset(rights):
                        continue
                    for right in permissions:
                        rights.add(right)

        return rights

    @staticmethod
    def List(ctx, properties):
        raise NotImplementedException('EntityAccessManager does not implement List')

    @staticmethod
    def ListSubquery(ctx, contexts=None, mask='r'):
        raise NotImplementedException('EntityAccessManager does not implement ListSubquery')