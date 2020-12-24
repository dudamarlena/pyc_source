# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/cursor.py
# Compiled at: 2013-12-05 16:32:18
# Size of source mod 2**32: 4756 bytes
import logging
from .document import Document
from .exceptions import AqlQueryError
__all__ = ('Cursor', )
logger = logging.getLogger(__name__)

class Cursor(object):
    __doc__ = '\n    Work with **Cursors** in ArangoDB.\n    At the moment, it\'s\n    common routine to work with **AQL** from this driver.\n\n    .. note:: the server will also destroy abandoned\n              cursors automatically after a certain\n              server-controlled timeout to\n              avoid resource leakage.\n\n    - ``query`` - contains the query string to be executed (mandatory)\n    - ``count`` - boolean flag that indicates whether the\n            number of documents found should be\n            returned as "count" attribute in the\n            result set (optional). Calculating the\n            "count" attribute might have a performance\n            penalty for some queries so this option\n            is turned off by default.\n\n    - ``batchSize`` - maximum number of result documents to be\n                transferred from the server to the client in\n                one roundtrip (optional).\n                If this attribute is not set, a server-controlled\n                default value will be used.\n    - ``bindVars`` - key/value list of bind parameters (optional).\n    - ``wrapper`` - by default it\'s ``Document.load``\n              class, wrap result into\n    '
    CREATE_CURSOR_PATH = '/_api/cursor'
    DELETE_CURSOR_PATH = '/_api/cursor/{0}'
    READ_NEXT_BATCH_PATH = '/_api/cursor/{0}'

    def __init__(self, connection, query, count=True, batchSize=None, bindVars=None, wrapper=Document.load):
        self.connection = connection
        self.query = query
        self.count = count
        self.wrapper = wrapper
        self.batchSize = batchSize
        self.bindVars = bindVars if isinstance(bindVars, dict) else {}
        self._position = 0
        self._cursor_id = None
        self._has_more = True
        self._dataset = []
        self._count = 0
        return

    def bind(self, bind_vars):
        """
        Bind variables to the cursor
        """
        self.bindVars = bind_vars
        return self

    def __iter__(self):
        return self

    @property
    def first(self):
        """
        Get first element from resultset
        """
        if not self._dataset:
            self.bulk()
        try:
            return self.wrapper(self.connection, self._dataset[0])
        except IndexError:
            return

        return

    @property
    def last(self):
        """
        Return last element from ``current bulk``. It's
        **NOT** last result in *entire dataset*.
        """
        if not self._dataset:
            self.bulk()
        try:
            return self.wrapper(self.connection, self._dataset[(-1)])
        except IndexError:
            return

        return

    def next(self):
        """
        Iterator though resultset (lazy)
        """
        self._position += 1
        try:
            item = self._dataset.pop(0)
            return self.wrapper(self.connection, item)
        except IndexError:
            if self._has_more:
                self.bulk()
                return self.next()

        raise StopIteration

    __next__ = next

    def bulk(self):
        """
        Getting initial or next bulk of results from Database
        """
        if not self._cursor_id:
            response = self.connection.post(self.CREATE_CURSOR_PATH, data={'query': self.query, 
             'count': self.count, 
             'batchSize': self.batchSize, 
             'bindVars': self.bindVars})
            self._cursor_id = response.get('id', None)
        else:
            response = self.connection.put(self.READ_NEXT_BATCH_PATH.format(self._cursor_id))
        if response.status not in (200, 201):
            raise AqlQueryError(response.data.get('errorMessage', 'Unknown error'), num=response.data.get('errorNum', -1), code=response.status)
        self._has_more = response.get('hasMore', False)
        self._count = int(response.get('count', 0))
        self._dataset = response['result'] if 'result' in response else []
        return

    def __len__(self):
        if not self._cursor_id:
            self.bulk()
        return self._count

    def __repr__(self):
        return '<ArangoDB Cursor Object: {0}>'.format(self.query)