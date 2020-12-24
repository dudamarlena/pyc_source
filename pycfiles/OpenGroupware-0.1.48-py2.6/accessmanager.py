# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/accessmanager.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import EntityAccessManager, Process, Message, Route, ACL, ObjectProperty

class MessageAccessManager(EntityAccessManager):
    __entity__ = 'Message'

    def __init__(self, ctx):
        EntityAccessManager.__init__(self, ctx)

    def implied_rights(self, objects):
        rights = {}
        for entity in objects:
            rights[entity] = set()
            rights[entity].add('w')
            rights[entity].add('d')
            rights[entity].add('t')
            rights[entity].add('l')
            rights[entity].add('r')
            rights[entity].add('v')

        return rights


class RouteAccessManager(EntityAccessManager):
    __entity__ = 'Route'

    def __init__(self, ctx):
        EntityAccessManager.__init__(self, ctx)

    def implied_rights(self, objects):
        rights = {}
        for entity in objects:
            rights[entity] = set()
            if entity.owner_id in self.context_ids:
                rights[entity].add('w')
                rights[entity].add('d')
                rights[entity].add('t')
                rights[entity].add('l')
                rights[entity].add('r')
                rights[entity].add('v')

        return rights

    @staticmethod
    def List(ctx, properties, contexts=None, mask='r', limit=None):
        db = ctx.db_session()
        if contexts is None:
            contexts = ctx.context_ids
        if mask is None:
            mask = 'r'
        routes = db.query(Route.object_id).enable_eagerloads(False).subquery()
        allowed = db.query(ACL.parent_id).filter(and_(ACL.context_id.in_(contexts), ACL.action == 'allowed', ACL.permissions.like(('%{0}%').format(mask)))).subquery()
        denied = db.query(ACL.parent_id).filter(and_(ACL.context_id.in_(contexts), ACL.action == 'denied', ACL.permissions.like(('%{0}%').format(mask)))).subquery()
        r_acls = db.query(ACL.parent_id).filter(and_(ACL.parent_id.in_(routes), ACL.parent_id.in_(allowed), not_(ACL.parent_id.in_(denied)))).distinct()
        if limit is None:
            enum = db.query(*properties).filter(or_(Route.owner_id.in_(contexts), Route.object_id.in_(r_acls)))
        else:
            enum = db.query(*properties).filter(or_(Route.owner_id.in_(contexts), Route.object_id.in_(r_acls))).limit(limit)
        return enum.all()


class ProcessAccessManager(EntityAccessManager):
    """ Meaning of permissions flags for Process entities
        r = read             [Implies "lv" for Process entities]
        w = write            [Modify; also implies "i"nsert for Process entities]
        l = list             [implied by "r" for Process entities]
        d = delete           [synonymous with t + x]
        a = administer
        k = create           [Not applicable to Process entities]
        t = delete object    [Ability to delete messages from the Process namespace]
        x = delete container [Owner of Process is the owner of the Route?
                              Not implemented.]
        i = insert           [Ability to create messages in the Process namespace.
                              Implied by "w" for Process entities]
        v = view   [Implied by "r" for Process entities]"""
    __entity__ = 'Process'

    def __init__(self, ctx):
        EntityAccessManager.__init__(self, ctx)

    def implied_rights(self, objects):
        rights = {}
        for entity in objects:
            rights[entity] = set()
            if entity.owner_id in self.context_ids:
                rights[entity].add('a')
                rights[entity].add('w')
                rights[entity].add('d')
                rights[entity].add('t')
                rights[entity].add('l')
                rights[entity].add('r')
                rights[entity].add('v')

        return rights

    @staticmethod
    def List(ctx, properties, contexts=None, mask='r', limit=None, route_group=None):
        db = ctx.db_session()
        if contexts is None:
            contexts = ctx.context_ids
        if mask is None:
            mask = 'r'
        processes = db.query(Process.object_id).enable_eagerloads(False)
        processes = processes.filter(Process.status != 'archived')
        processes = processes.subquery()
        allowed = db.query(ACL.parent_id).filter(and_(ACL.context_id.in_(contexts), ACL.action == 'allowed', ACL.permissions.like(('%{0}%').format(mask)))).subquery()
        denied = db.query(ACL.parent_id).filter(and_(ACL.context_id.in_(contexts), ACL.action == 'denied', ACL.permissions.like(('%{0}%').format(mask)))).subquery()
        r_acls = db.query(ACL.parent_id).filter(and_(ACL.parent_id.in_(processes), ACL.parent_id.in_(allowed), not_(ACL.parent_id.in_(denied)))).distinct()
        enum = db.query(*properties).filter(and_(Process.status != 'archived', or_(Process.owner_id.in_(contexts), Process.object_id.in_(r_acls))))
        if limit:
            enum = enum.limit(limit)
        if route_group:
            enum = enum.join(Route, Route.object_id == Process.route_id)
            enum = enum.join(ObjectProperty, ObjectProperty.parent_id == Route.object_id)
            enum = enum.filter(and_(ObjectProperty.namespace == 'http://www.opengroupware.us/oie', ObjectProperty.name == 'routeGroup', ObjectProperty._string_value == route_group))
        return enum.all()