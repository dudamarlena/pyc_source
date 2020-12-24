# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/couchdbsession/session.py
# Compiled at: 2010-02-26 07:34:29
import logging, itertools, uuid, couchdb
from couchdbsession import a8n
log = logging.getLogger(__name__)

class Session(object):
    tracker_factory = a8n.Tracker

    def __init__(self, db, pre_flush_hook=None, post_flush_hook=None, encode_doc=None, decode_doc=None):
        self._db = db
        self._pre_flush_hook = pre_flush_hook
        self._post_flush_hook = post_flush_hook
        self._encode_doc = encode_doc
        self._decode_doc = decode_doc
        self.reset()

    def __getattr__(self, name):
        return getattr(self._db, name)

    def __iter__(self):
        return iter(self._db)

    def __len__(self):
        return len(self._db)

    def __delitem__(self, id):
        self.delete(self[id])

    def __getitem__(self, id):
        doc = self.get(id)
        if doc is None:
            raise couchdb.ResourceNotFound()
        return doc

    def __setitem__(self, id, content):
        if '_rev' in content:
            return
        doc = dict(content)
        doc['_id'] = id
        self.create(doc)

    def create(self, doc):
        if '_id' not in doc:
            doc['_id'] = uuid.uuid4().hex
        self._created.add(doc['_id'])
        return self._tracked_and_cached(doc)['_id']

    def delete(self, doc):
        if doc['_id'] in self._created:
            self._created.remove(doc['_id'])
        else:
            self._changed.discard(doc['_id'])
            self._deleted[doc['_id']] = doc
        del self._cache[doc['_id']]

    def get(self, id, default=None, **options):
        doc = self._cache.get(id)
        if doc is not None:
            return doc
        else:
            if id in self._deleted:
                return
            doc = self._db.get(id, default, **options)
            if doc is default:
                return doc
            doc = self.decode_doc(doc)
            return self._tracked_and_cached(doc)

    def delete_attachment(self, doc, filename):
        raise NotImplementedError()

    def get_attachment(self, id_or_doc, filename, default=None):
        raise NotImplementedError()

    def put_attachment(self, doc, content, filename=None, content_type=None):
        raise NotImplementedError()

    def query(self, *a, **k):
        return SessionViewResults(self, self._db.query(*a, **k))

    def update(self, documents):
        raise NotImplementedError()

    def view(self, *a, **k):
        return SessionViewResults(self, self._db.view(*a, **k))

    def encode_doc(self, doc):
        """
        Encode document hook, called whenever a doc is sent to the CouchDB.
        """
        if self._encode_doc:
            return self._encode_doc(doc)
        return doc

    def decode_doc(self, doc):
        """
        Decode document hook, called whenever a doc is retrieved from the
        CouchDB.
        """
        if self._decode_doc:
            return self._decode_doc(doc)
        return doc

    def reset(self):
        """
        Reset the session, forgetting everything it knows.
        """
        self._trackers = {}
        self._cache = {}
        self._created = set()
        self._changed = set()
        self._deleted = {}

    def flush(self):
        while True:
            (deleted, created, changed) = self._pre_flush()
            if not (deleted or created or changed):
                break
            deletions = [ {'_id': id, '_rev': doc['_rev'], '_deleted': True} for (id, doc) in deleted.iteritems() ]
            additions = (self._cache[doc_id].__subject__ for doc_id in created)
            changes = (self._cache[doc_id].__subject__ for doc_id in changed)
            updates = itertools.chain(additions, changes)
            updates = (self.encode_doc(doc) for doc in updates)
            updates = list(updates)
            if deletions:
                self._db.update(deletions)
            if updates:
                for (success, docid, rev_or_exc) in self._db.update(updates):
                    if success:
                        self._cache[docid].__subject__['_rev'] = rev_or_exc
                    else:
                        log.error('bulk update error: docid=%r, exc=%r', docid, rev_or_exc)

            self._post_flush(deleted, created, changed)

    def pre_flush_hook(self, deletions, additions, changes):
        if self._pre_flush_hook is not None:
            self._pre_flush_hook(self, deletions, additions, changes)
        return

    def post_flush_hook(self, deletions, additions, changes):
        if self._post_flush_hook is not None:
            self._post_flush_hook(self, deletions, additions, changes)
        return

    def _tracked_and_cached(self, doc):

        def callback():
            if doc['_id'] in self._created:
                return
            self._changed.add(doc['_id'])

        tracker = self.tracker_factory(callback)
        doc = tracker.track(doc)
        self._trackers[doc['_id']] = tracker
        return self._cached(doc)

    def _cached(self, doc):
        self._cache[doc['_id']] = doc
        return doc

    def _freeze(self):
        deleted, self._deleted = self._deleted, {}
        created, self._created = self._created, set()
        changed, self._changed = self._changed, set()
        return (deleted, created, changed)

    def _pre_flush(self):
        all_deleted = {}
        all_created = set()
        all_changed = set()
        while True:
            (deleted, created, changed) = self._freeze()
            if not (deleted or created or changed):
                break
            all_deleted.update(deleted)
            all_created.update(created)
            all_changed.update(changed)

            def gen_deletions():
                return deleted.itervalues()

            def gen_additions():
                return (self._cache[doc_id].__subject__ for doc_id in created)

            def gen_changes():
                changes = (self._cache[doc_id].__subject__ for doc_id in changed)
                changes = ((doc, iter(self._trackers[doc['_id']])) for doc in changes)
                return changes

            if self.pre_flush_hook is not None:
                self.pre_flush_hook(gen_deletions(), gen_additions(), gen_changes())

        return (
         all_deleted, all_created, all_changed)

    def _post_flush(self, deleted, created, changed):
        actions_by_doc = dict((doc_id, self._trackers[doc_id].freeze()) for doc_id in changed)

        def gen_deletions():
            return deleted.itervalues()

        def gen_additions():
            return (self._cache[doc_id] for doc_id in created)

        def gen_changes():
            changes = (self._cache[doc_id] for doc_id in changed)
            changes = ((doc, actions_by_doc[doc['_id']]) for doc in changes)
            return changes

        if self.post_flush_hook is not None:
            self.post_flush_hook(gen_deletions(), gen_additions(), gen_changes())
        return


class SessionViewResults(object):

    def __init__(self, session, view_results):
        self._session = session
        self._view_results = view_results

    def __getattr__(self, name):
        return getattr(self._view_results, name)

    def __len__(self):
        return len(self._view_results)

    def __getitem__(self, key):
        return SessionViewResults(self._session, self._view_results(key))

    def __iter__(self):
        for row in self._view_results:
            yield SessionRow(self._session, row)

    @property
    def rows(self):
        return [ SessionRow(self._session, row) for row in self._view_results.rows ]


class SessionRow(object):

    def __init__(self, session, row):
        self._session = session
        self._row = row

    def __getattr__(self, name):
        return getattr(self._row, name)

    @property
    def doc(self):
        doc = self._row.doc
        if doc is not None:
            cached = self._session._cache.get(doc['_id'])
            if cached is not None:
                return cached
            doc = self._session.decode_doc(doc)
            return self._session._tracked_and_cached(doc)
        else:
            return