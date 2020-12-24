# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/linkmanager.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.foundation import ObjectLink

class LinkManager(object):
    __slots__ = '_ctx'

    def __init__(self, ctx):
        self._ctx = ctx

    def links_to(self, entity):
        db = self._ctx.db_session()
        query = db.query(ObjectLink).filter(ObjectLink.target_id == entity.object_id)
        data = query.all()
        query = None
        return data

    def links_from(self, entity):
        db = self._ctx.db_session()
        query = db.query(ObjectLink).filter(ObjectLink.source_id == entity.object_id)
        data = query.all()
        query = None
        return data

    def links_to_and_from(self, entity):
        db = self._ctx.db_session()
        query = db.query(ObjectLink).filter(or_(ObjectLink.source_id == entity.object_id, ObjectLink.target_id == entity.object_id))
        query = query.order_by(ObjectLink.source_id, ObjectLink.target_id, ObjectLink.kind)
        data = query.all()
        query = None
        return data

    def links_between(self, entity1, entity2):
        db = self._ctx.db_session()
        query = db.query(ObjectLink).filter(and_(ObjectLink.source_id.in_((entity1.object_id, entity2.object_id)), ObjectLink.target_id.in_((entity1.object_id, entity2.object_id))))
        query = query.order_by(ObjectLink.source_id, ObjectLink.target_id, ObjectLink.kind)
        data = query.all()
        query = None
        return data

    def link(self, source, target, kind='generic', label=None):
        db = self._ctx.db_session()
        if kind is None:
            query = db.query(ObjectLink).filter(and_(ObjectLink.source_id == source.object_id, ObjectLink.target_id == target.object_id))
        else:
            query = db.query(ObjectLink).filter(and_(ObjectLink.source_id == source.object_id, ObjectLink.target_id == target.object_id, ObjectLink.kind == kind))
        links = query.all()
        if links:
            link = links[0]
            link.label = label
        else:
            print source.object_id, target.object_id, kind, label
            link = ObjectLink(source, target, kind, label)
            self._ctx.db_session().add(link)
        return

    def unlink(self, source, target, kind='generic'):
        db = self._ctx.db_session()
        if kind is None:
            query = db.query(ObjectLink).filter(and_(ObjectLink.source_id == source.object_id, ObjectLink.target_id == target, object_id))
        else:
            query = db.query(ObjectLink).filter(and_(ObjectLink.source_id == source.object_id, ObjectLink.target_id == target.object_id, ObjectLink.kind == kind))
        link = query.one()
        if link is not None:
            self._ctx.db_session().delete(link)
        return

    def _is_linked(self, source_id, target_id, kind):
        db = self._ctx.db_session()
        if kind:
            query = db.query(ObjectLink).filter(and_(ObjectLink.source_id == source_id, ObjectLink.target_id == target_id))
        else:
            query = db.query(ObjectLink).filter(and_(ObjectLink.source_id == source_id, ObjectLink.target_id == target_id, ObjectLink.kind == kind))
        result = query.all()
        if query.all():
            return result[0]
        else:
            return False

    def _get_entity(self, object_id):
        kind = self._ctx.type_manager.get_kind(object_id)
        return self._ctx.run_command('{0}::get', format(kind.lower()), id=object_id)

    def sync_links(self, entity, links_b):
        db = self._ctx.db_session()
        removes = [ link.object_id for link in self.links_to_and_from(entity) ]
        for link_b in links_b:
            if isinstance(link_b, dict):
                source_id = link_b.get('source_id')
                target_id = link_b.get('target_id')
                kind = link_b.get('kind')
                label = link_b.get('label')
            else:
                source_id = link_b.source_id
                target_id = link_b.target_id
                kind = link_b.kind
                label = link_b.label
            link = self._is_linked(source_id, target_id, kind)
            if link:
                link.label = label
                removes.remove(link.object_id)
            else:
                if entity.object_id == source_id:
                    source = entity
                    target = self._get_entity(target_id)
                else:
                    target = entity
                    source = self._get_entity(source_id)
                if target and source:
                    link = ObjectLink(source, target, kind, label)
                    db.add(link)
                else:
                    raise CoilsException('Unable to create new link from provided type.')

        if removes:
            db.query(ObjectLink).filter(ObjectLink.object_id.in_(removes)).delete()