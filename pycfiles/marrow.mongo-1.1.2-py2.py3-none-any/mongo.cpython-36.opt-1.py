# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/session/mongo.py
# Compiled at: 2016-12-03 23:01:42
# Size of source mod 2**32: 2518 bytes
"""Experimental WebCore session handler using MongoDB storage."""
from bson import ObjectId as oid
from marrow.mongo import Document, Index
from marrow.mongo.field import TTL, ObjectId
log = __import__('logging').getLogger(__name__)

class MongoSessionStorage(Document):
    id = ObjectId('_id', required=True, assign=False, default=None)
    expires = TTL('expires', default=None)
    _expires = Index('expires', expire=0)

    def __getattr__(self, name):
        try:
            return self.__dict__['__data__'][name]
        except KeyError:
            pass

        raise AttributeError('Session has no attribute: ' + name)

    def __setattr__(self, name, value):
        if name[0] == '_' or '__data__' not in self.__dict__:
            return super(MongoSessionStorage, self).__setattr__(name, value)
        self.__data__[name] = value


class MongoSession(object):
    needs = {
     'db'}

    def __init__(self, Document=MongoSessionStorage, collection=None, database=None):
        """"""
        self._Document = Document
        self._collection = collection or getattr(Document, '__collection__', 'sessions')
        self._database = database or getattr(Document, '__database__', 'default')

    def is_valid(self, context, sid):
        """"""
        D = self._Document
        db = context.db[self._database]
        docs = db[self._collection]
        result = docs.find(D.id == sid).count()
        return bool(result)

    def invalidate(self, context, sid):
        """"""
        D = self._Document
        db = context.db[self._database]
        docs = db[self._collection]
        result = docs.delete_one(D.id == sid)
        return result.deleted_count == 1

    def __get__(self, session, type=None):
        """Retrieve the session upon first access and cache the result."""
        if session is None:
            return self
        else:
            ctx = session._ctx
            D = self._Document
            db = ctx.db[self._database]
            docs = db[self._collection]
            project = D.__projection__
            result = docs.find_one(D.id == session._id, project)
            if not result:
                result = {'_id': oid(str(session._id))}
            result = session[self.name] = D.from_mongo(result, project.keys())
            return result

    def persist(self, context):
        """Update or insert the session document into the configured collection"""
        D = self._Document
        db = context.db[self._database]
        docs = db[self._collection]
        document = context.session[self.name]
        docs.replace_one(D.id == document.id, document, True)