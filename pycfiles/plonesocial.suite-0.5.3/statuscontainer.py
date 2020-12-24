# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.microblog/plonesocial/microblog/statuscontainer.py
# Compiled at: 2014-03-11 12:09:55
import threading, Queue, logging, time, math
from BTrees import LOBTree
from BTrees import OOBTree
from BTrees import LLBTree
from persistent import Persistent
import transaction
from Acquisition import Explicit
from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName
try:
    from zope.container.contained import ObjectAddedEvent
except ImportError:
    from zope.app.container.contained import ObjectAddedEvent

from zope.event import notify
from zope.interface import implements
from plone.uuid.interfaces import IUUID
from interfaces import IStatusContainer
from interfaces import IStatusUpdate
from interfaces import IMicroblogContext
from utils import longkeysortreverse
logger = logging.getLogger('plonesocial.microblog')
LOCK = threading.RLock()
STATUSQUEUE = Queue.PriorityQueue()
MAX_QUEUE_AGE = 1000

class BaseStatusContainer(Persistent, Explicit):
    """This implements IStatusUpdate storage, indexing and query logic.

    This is just a base class, the actual IStorageContainer used
    in the implementation is the QueuedStatusContainer defined below.

    StatusUpdates are stored in the private _status_mapping BTree.
    A subset of BTree accessors are exposed, see interfaces.py.
    StatusUpdates are keyed by longint microsecond ids.

    Additionally, StatusUpdates are indexed by users and tags.
    These indexes use the same longint microsecond IStatusUpdate.id.

    Special user_* prefixed accessors take an extra argument 'users',
    an interable of userids, and return IStatusUpdate keys, instances or items
    filtered by userids, in addition to the normal min/max statusid filters.
    """
    implements(IStatusContainer)

    def __init__(self, context=None):
        self._mtime = 0
        self._status_mapping = LOBTree.LOBTree()
        self._user_mapping = OOBTree.OOBTree()
        self._tag_mapping = OOBTree.OOBTree()
        self._uuid_mapping = OOBTree.OOBTree()

    def add(self, status, context=None):
        self._check_permission('add')
        self._check_status(status)
        self._store(status)

    def _store(self, status):
        while not self._status_mapping.insert(status.id, status):
            status.id += 1

        self._idx_user(status)
        self._idx_tag(status)
        self._idx_context(status)
        self._notify(status)

    def _check_status(self, status):
        if not IStatusUpdate.providedBy(status):
            raise ValueError('IStatusUpdate interface not provided.')

    def _check_permission(self, perm='read'):
        if perm == 'read':
            permission = 'Plone Social: View Microblog Status Update'
        else:
            permission = 'Plone Social: Add Microblog Status Update'
        if not getSecurityManager().checkPermission(permission, self):
            raise Unauthorized('You do not have permission <%s>' % permission)

    def _notify(self, status):
        event = ObjectAddedEvent(status, newParent=self, newName=status.id)
        notify(event)

    def _idx_user(self, status):
        userid = unicode(status.userid)
        self._user_mapping.insert(userid, LLBTree.LLTreeSet())
        self._user_mapping[userid].insert(status.id)

    def _idx_tag(self, status):
        for tag in [ unicode(tag) for tag in status.tags ]:
            self._tag_mapping.insert(tag, LLBTree.LLTreeSet())
            self._tag_mapping[tag].insert(status.id)

    def _idx_context(self, status):
        uuid = status.context_uuid
        if uuid:
            self._uuid_mapping.insert(uuid, LLBTree.LLTreeSet())
            self._uuid_mapping[uuid].insert(status.id)

    def _context2uuid(self, context):
        return IUUID(context)

    def clear(self):
        self._user_mapping.clear()
        self._tag_mapping.clear()
        self._uuid_mapping.clear()
        return self._status_mapping.clear()

    def insert(self, key, value):
        raise NotImplementedError("Can't allow that to happen.")

    def pop(self, k, d=None):
        raise NotImplementedError("Can't allow that to happen.")

    def setdefault(self, k, d):
        raise NotImplementedError("Can't allow that to happen.")

    def update(self, collection):
        raise NotImplementedError("Can't allow that to happen.")

    def get(self, key):
        self._check_permission('read')
        return self._status_mapping.get(key)

    def items(self, min=None, max=None, limit=100, tag=None):
        return ((key, self.get(key)) for key in self.keys(min, max, limit, tag))

    def values(self, min=None, max=None, limit=100, tag=None):
        return (self.get(key) for key in self.keys(min, max, limit, tag))

    def keys(self, min=None, max=None, limit=100, tag=None):
        self._check_permission('read')
        if tag and tag not in self._tag_mapping:
            return ()
        mapping = self._keys_tag(tag, self.allowed_status_keys())
        return longkeysortreverse(mapping, min, max, limit)

    iteritems = items
    iterkeys = keys
    itervalues = values

    def user_items(self, users, min=None, max=None, limit=100, tag=None):
        return ((key, self.get(key)) for key in self.user_keys(users, min, max, limit, tag))

    def user_values(self, users, min=None, max=None, limit=100, tag=None):
        return (self.get(key) for key in self.user_keys(users, min, max, limit, tag))

    def user_keys(self, users, min=None, max=None, limit=100, tag=None):
        if not users:
            return ()
        if tag and tag not in self._tag_mapping:
            return ()
        if users == str(users):
            userid = users
            mapping = self._user_mapping.get(userid)
            if not mapping:
                return ()
        else:
            treesets = (self._user_mapping.get(userid) for userid in users if userid in self._user_mapping.keys())
            mapping = reduce(LLBTree.union, treesets, LLBTree.TreeSet())
        mapping = self._keys_tag(tag, mapping)
        return longkeysortreverse(mapping, min, max, limit)

    def context_items(self, context, min=None, max=None, limit=100, tag=None, nested=True):
        return ((key, self.get(key)) for key in self.context_keys(context, min, max, limit, tag, nested))

    def context_values(self, context, min=None, max=None, limit=100, tag=None, nested=True):
        return (self.get(key) for key in self.context_keys(context, min, max, limit, tag, nested))

    def context_keys(self, context, min=None, max=None, limit=100, tag=None, nested=True):
        self._check_permission('read')
        if tag and tag not in self._tag_mapping:
            return ()
        if nested:
            nested_uuids = [ uuid for uuid in self.nested_uuids(context) if uuid in self._uuid_mapping
                           ]
            if not nested_uuids:
                return ()
        else:
            uuid = self._context2uuid(context)
            if uuid not in self._uuid_mapping:
                return ()
            nested_uuids = [
             uuid]
        keyset_tag = self._keys_tag(tag, self.allowed_status_keys())
        keyset_uuids = [ self._keys_uuid(uuid, keyset_tag) for uuid in nested_uuids
                       ]
        merged_set = LLBTree.multiunion(keyset_uuids)
        return longkeysortreverse(merged_set, min, max, limit)

    def nested_uuids(self, context):
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(path={'query': ('/').join(context.getPhysicalPath()), 'depth': -1}, object_implements=IMicroblogContext)
        return [ item.UID for item in results ]

    def _keys_tag(self, tag, keyset):
        if tag is None:
            return keyset
        else:
            return LLBTree.intersection(LLBTree.LLTreeSet(keyset), self._tag_mapping[tag])

    def _keys_uuid(self, uuid, keyset):
        if uuid is None:
            return keyset
        else:
            return LLBTree.intersection(LLBTree.LLTreeSet(keyset), self._uuid_mapping[uuid])

    def allowed_status_keys(self):
        """Return the subset of IStatusUpdate keys
        that are related to UUIDs of accessible contexts.
        I.e. blacklist all IStatusUpdate that has a context
        which we don't have permission to access.

        This method will be overridden in the tool implementation
        to filter on requesting user permissions.
        """
        return self._allowed_status_keys()

    def _allowed_status_keys(self, uuid_blacklist=[]):
        if not uuid_blacklist:
            return self._status_mapping.keys()
        else:
            blacklisted_treesets = (self._uuid_mapping.get(uuid) for uuid in uuid_blacklist if uuid in self._uuid_mapping.keys())
            blacklisted_statusids = reduce(LLBTree.union, blacklisted_treesets, LLBTree.TreeSet())
            all_statusids = LLBTree.LLSet(self._status_mapping.keys())
            return LLBTree.difference(all_statusids, blacklisted_statusids)


class QueuedStatusContainer(BaseStatusContainer):
    """A write performance optimized IStatusContainer.

    This separates the queuing logic from the base class to make
    the code more readable (and testable).

    For performance reasons, an in-memory STATUSQUEUE is used.
    StatusContainer.add() puts StatusUpdates into the queue.

    MAX_QUEUE_AGE is the commit window in milliseconds.
    To disable batch queuing, set MAX_QUEUE_AGE = 0

    .add() calls .autoflush(), which flushes the queue when
    ._mtime is longer than MAX_QUEUE_AGE ago.

    So each .add() checks the queue. In a low-traffic site this will
    result in immediate disk writes (msg frequency < timeout).
    In a high-traffic site this will result on one write per timeout,
    which makes it possible to attain > 100 status update inserts
    per second.

    Note that the algorithm is structured in such a way, that the
    system automatically adapts to low/high traffic conditions.

    Additionally, a non-interactive queue flush is set up via
    _schedule_flush() which uses a volatile thread timer _v_timer
    to set up a non-interactive queue flush. This ensures that
    the "last Tweet of the day" also gets committed to disk.

    An attempt is made to make self._mtime and self._v_timer
    thread-safe. These function as a kind of ad-hoc locking
    mechanism so that only one thread at a time is flushing the
    memory queue into persistent storage.
    """
    implements(IStatusContainer)

    def add(self, status):
        self._check_permission('add')
        self._check_status(status)
        if MAX_QUEUE_AGE > 0:
            self._queue(status)
            self._schedule_flush()
            return self._autoflush()
        else:
            self._store(status)
            return 1

    def _queue(self, status):
        STATUSQUEUE.put((status.id, status))

    def _schedule_flush(self):
        """A fallback queue flusher that runs without user interactions"""
        if not MAX_QUEUE_AGE > 0:
            return
        else:
            try:
                self._v_timer
            except AttributeError:
                self._v_timer = None

            if self._v_timer is not None:
                return
            timeout = int(math.ceil(float(MAX_QUEUE_AGE) / 1000))
            with LOCK:
                self._v_timer = threading.Timer(timeout, self._scheduled_autoflush)
                self._v_timer.start()
            return

    def _scheduled_autoflush(self):
        """This method is run from the timer, outside a normal request scope.
        This requires an explicit commit on db write"""
        if self._autoflush():
            transaction.commit()

    def _autoflush(self):
        if int(time.time() * 1000) - self._mtime > MAX_QUEUE_AGE:
            return self.flush_queue()
        return 0

    def flush_queue(self):
        with LOCK:
            self._mtime = int(time.time() * 1000)
            if self._v_timer is not None:
                self._v_timer.cancel()
                self._v_timer = None
        if STATUSQUEUE.empty():
            return 0
        else:
            while True:
                try:
                    id, status = STATUSQUEUE.get(block=False)
                    self._store(status)
                except Queue.Empty:
                    break

            return 1