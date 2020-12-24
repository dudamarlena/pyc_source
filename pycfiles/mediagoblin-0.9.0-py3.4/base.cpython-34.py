# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/db/base.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 7259 bytes
import six, copy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect
from mediagoblin.tools.transition import DISABLE_GLOBALS
if not DISABLE_GLOBALS:
    from sqlalchemy.orm import scoped_session, sessionmaker
    Session = scoped_session(sessionmaker())

class FakeCursor(object):

    def __init__(self, cursor, mapper, filter=None):
        self.cursor = cursor
        self.mapper = mapper
        self.filter = filter

    def count(self):
        return self.cursor.count()

    def __copy__(self):
        return FakeCursor(copy.copy(self.cursor), self.mapper, self.filter)

    def __iter__(self):
        return six.moves.filter(self.filter, six.moves.map(self.mapper, self.cursor))

    def __getitem__(self, key):
        return self.mapper(self.cursor[key])

    def slice(self, *args, **kwargs):
        r = self.cursor.slice(*args, **kwargs)
        return list(six.moves.filter(self.filter, six.moves.map(self.mapper, r)))


class GMGTableBase(object):
    HARD_DELETE = 'hard-deletion'
    SOFT_DELETE = 'soft-deletion'
    deletion_mode = HARD_DELETE

    @property
    def _session(self):
        return inspect(self).session

    @property
    def _app(self):
        return self._session.bind.app

    if not DISABLE_GLOBALS:
        query = Session.query_property()

    def get(self, key):
        return getattr(self, key)

    def setdefault(self, key, defaultvalue):
        return getattr(self, key)

    def save(self, commit=True):
        sess = self._session
        if sess is None:
            if not DISABLE_GLOBALS:
                sess = Session()
        assert sess is not None, "Can't save, %r has a detached session" % self
        sess.add(self)
        if commit:
            sess.commit()
        else:
            sess.flush()

    def delete(self, commit=True, deletion=None):
        """ Delete the object either using soft or hard deletion """
        if deletion is None:
            deletion = self.deletion_mode
        from mediagoblin.db.models import CollectionItem, GenericModelReference, Report, Notification, Comment
        if hasattr(self, 'id'):
            gmr = GenericModelReference.query.filter_by(obj_pk=self.id, model_type=self.__tablename__).first()
            if gmr is not None:
                items = CollectionItem.query.filter_by(object_id=gmr.id)
                items.delete()
                notifications = Notification.query.filter_by(object_id=gmr.id)
                notifications.delete()
                comments = Comment.query.filter_by(comment_id=gmr.id)
                comments.delete()
                reports = Report.query.filter_by(object_id=gmr.id)
                for report in reports:
                    report.object_id = None
                    report.save(commit=commit)

        if deletion == self.HARD_DELETE:
            return self.hard_delete(commit=commit)
        if deletion == self.SOFT_DELETE:
            return self.soft_delete(commit=commit)
        raise ValueError('Invalid deletion mode {mode!r}'.format(mode=deletion))

    def soft_delete(self, commit):
        from mediagoblin.db.models import User, Graveyard, GenericModelReference
        tombstone = Graveyard()
        if getattr(self, 'public_id', None) is not None:
            tombstone.public_id = self.public_id
        if not isinstance(self, User):
            tombstone.actor = User.query.filter_by(id=self.actor).first()
        tombstone.object_type = self.object_type
        tombstone.save(commit=False)
        gmrs = GenericModelReference.query.filter_by(obj_pk=self.id, model_type=self.__tablename__).update({'obj_pk': tombstone.id, 
         'model_type': tombstone.__tablename__})
        return self.hard_delete(commit=commit)

    def hard_delete(self, commit):
        """Delete the object and commit the change immediately by default"""
        sess = self._session
        assert sess is not None, 'Not going to delete detached %r' % self
        sess.delete(self)
        if commit:
            sess.commit()


Base = declarative_base(cls=GMGTableBase)

class DictReadAttrProxy(object):
    __doc__ = "\n    Maps read accesses to obj['key'] to obj.key\n    and hides all the rest of the obj\n    "

    def __init__(self, proxied_obj):
        self.proxied_obj = proxied_obj

    def __getitem__(self, key):
        try:
            return getattr(self.proxied_obj, key)
        except AttributeError:
            raise KeyError('%r is not an attribute on %r' % (
             key, self.proxied_obj))