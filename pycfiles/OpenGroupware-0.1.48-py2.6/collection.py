# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/alchemy/collection.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from base import *

class Collection(Base, KVC):
    """ An OpenGroupare Collection object """
    __tablename__ = 'collection'
    __entityName__ = 'Collection'
    __internalName__ = 'Collection'
    object_id = Column('collection_id', Integer, Sequence('key_generator'), ForeignKey('collection_assignment.collection_id'), ForeignKey('log.object_id'), ForeignKey('object_acl.object_id'), primary_key=True)
    version = Column('object_version', Integer)
    owner_id = Column('owner_id', Integer, ForeignKey('person.company_id'), nullable=False)
    kind = Column('kind', String(50))
    title = Column('title', String(255))
    project_id = Column('project_id', Integer, ForeignKey('project.project_id'), nullable=True)
    auth_token = Column('auth_token', String(12))
    dav_enabled = Column('dav_enabled', Integer)
    comment = Column('comment', Text)

    def __repr__(self):
        return ('<Collection objectId={0} ownerId={1} "{2}">').format(self.object_id, self.owner_id, self.title)

    def get_display_name(self):
        return self.title


class CollectionAssignment(Base, KVC):
    __tablename__ = 'collection_assignment'
    __entityName__ = 'CollectionAssignment'
    __internalName__ = 'CollectionAssignment'
    object_id = Column('collection_assignment_id', Integer, Sequence('key_generator'), primary_key=True)
    collection_id = Column('collection_id', Integer)
    assigned_id = Column('assigned_id', Integer)
    sort_key = Column('sort_key', Integer)

    def __cmp__(self, other):
        if hasattr(other, 'object_id'):
            if other.object_id > self.object_id:
                return -1
            if other.object_id < self.object_id:
                return 1
            return 0
        else:
            return 0

    def __repr__(self):
        return ('<CollectionAssignment collectionId={0} assignedId={1} sortKey={2}>').format(self.collection_id, self.assigned_id, self.sort_key)