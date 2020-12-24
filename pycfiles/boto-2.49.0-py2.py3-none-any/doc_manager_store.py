# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/doc_manager_store.py
# Compiled at: 2012-08-16 08:03:16
__doc__ = '\nDocument Manager Store connection wrapper class\n'
import pymongo, logging
from standard_document import StandardDocument
from botnee import debug

class DocManagerStore(object):
    """
    Connects to the Document Manager's mongo store
    """

    def __init__(self, server='localhost', port=27017, db_name='documentstore', verbose=False):
        self.logger = logging.getLogger(__name__)
        self._port = port
        self._server = server
        self._db_name = db_name
        msg = 'Initialising connection to document manager store'
        debug.print_verbose(msg, verbose, self.logger, logging.INFO)
        msg = 'Connecting to database:\n' + server + ': ' + str(port) + '\ndb: ' + db_name
        debug.print_verbose(msg, verbose, self.logger, logging.INFO)
        self._connection = None
        self._database = None
        self.reconnect(verbose)
        return

    def reconnect(self, verbose=False):
        if self._connection and self._database:
            return
        try:
            self._connection = pymongo.Connection(server, port)
            self._database = self._connection[db_name]
        except:
            debug.print_verbose('Cannot connect to document manager mongo', verbose, self.logger, logging.WARNING)

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    def close(self):
        if self._connection is not None:
            self._connection.close()
        return

    def find_one(self, verbose=False):
        """
        For testing only - pulls a single document out
        """
        self.reconnect(verbose)
        try:
            cursor = self._database.standardDocument.find_one()
            return StandardDocument(dict(cursor))
        except:
            return

        return

    def get_guids(self, verbose=False):
        self.reconnect(verbose)
        try:
            cursor = self._database.standardDocument.find(None, {'_id': 1})
            return [ c['_id'] for c in cursor ]
        except:
            return

        return

    def get_doc_count(self, verbose=False):
        """
        Count of all documents
        """
        self.reconnect(verbose)
        try:
            return self._database.standardDocument.count()
        except:
            return

        return