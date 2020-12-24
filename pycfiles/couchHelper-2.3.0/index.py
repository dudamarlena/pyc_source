# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/couchfti/index.py
# Compiled at: 2010-01-19 08:32:18
__doc__ = '\nIndex/search facility for CouchDB.\n'
import logging, os.path, xappy
from couchutil.changes import ChangesProcessor
log = logging.getLogger()

class Indexer(ChangesProcessor):
    """
    ChangesProcessor handler for managing a set of HyPy indexes.
    """

    def __init__(self, db, path, indexes, **kw):
        ChangesProcessor.__init__(self, db, os.path.join(path, 'statefile'), **kw)
        self.__path = path
        self.__indexes = indexes
        self.__open_indexes = {}
        if not os.path.exists(path):
            os.makedirs(path)

    def handle_changes(self, ids):
        try:
            return super(Indexer, self).handle_changes(ids)
        finally:
            for (path, index) in self.__open_indexes.iteritems():
                log.debug('flushing and closing index: %s', path)
                index.flush()
                index.close()

            self.__open_indexes.clear()

    def index(self, config):
        index = self.__open_indexes.get(config['path'])
        if index is None:
            log.debug('opening index: %s', config['path'])
            index = xappy.IndexerConnection(os.path.join(self.__path, config['path']))
            for (args, kwargs) in config['fields']:
                index.add_field_action(*args, **kwargs)

            self.__open_indexes[config['path']] = index
        return index

    def handle_delete(self, docid):
        log.debug('Handling delete for %s', docid)
        for (name, config) in self.__indexes.iteritems():
            self.index(config).delete(docid)
            log.info('Removed %s from %s index', docid, name)

    def handle_update(self, doc):
        log.debug('Handling update for %s@%s', doc['_id'], doc['_rev'])
        for (name, config) in self.__indexes.iteritems():
            classification = config['classifier'](doc)
            if classification is None:
                continue
            factory = config['factories'].get(classification)
            if factory is None:
                continue
            log.info('Adding %s@%s to %s index as %r', doc['_id'], doc['_rev'], name, classification)
            self.index(config).replace(factory(self.db, doc))

        return