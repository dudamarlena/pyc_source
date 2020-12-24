# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/couchfti/search.py
# Compiled at: 2010-01-19 08:32:18
"""
Index/search facility for CouchDB.
"""
import logging, os.path, xapian, xappy
from query import tokenize
log = logging.getLogger()

class Searcher(object):
    """
    Search a set of indexes for matching documents.
    """

    def __init__(self, db, path, indexes):
        self.__db = db
        self.__path = path
        self.__indexes = indexes

    def search_docs(self, index, query, skip, max):
        rows = self.db.view('_all_docs', include_docs=True, keys=self.search_docids(index, query, skip, max))
        return [ row.doc for row in rows ]

    def search_docids(self, index, query, skip, max):
        return [ r.id for r in self.search(index, query, skip, max) ]

    def search(self, index, query, skip, max):
        config = self.__indexes[index]
        try:
            conn = xappy.SearchConnection(os.path.join(self.__path, config['path']))
        except xapian.DatabaseOpeningError, e:
            log.error(e)
            return

        try:
            q = list(tokenize(query))
            terms = [ i[1].encode('utf-8') for i in q if i[0] == 'term' ]
            attrs = [ i[1] for i in q if i[0] == 'field' ]
            order = ([ i[1] for i in q if i[0] == 'order' ] or [None])[0]
            query = conn.query_all()
            for term in terms:
                query = xapian.Query(xapian.Query.OP_AND, query, xapian.Query(term.lower()))

            for (field, op, value) in attrs:
                func = QUERY_FACTORIES[op]
                query = xapian.Query(xapian.Query.OP_AND, query, func(conn, field, value))

            if not order:
                sortby = None
            else:
                sortby = '-+'[order[1]] + order[0]
            return conn.search(query, skip, skip + max, sortby=sortby)
        finally:
            conn.close()

        return


def query_eq(conn, field, value):
    return conn.query_field(field, value)


def query_prefix(conn, field, value):
    return _query_range(conn, field, value, value + '香')


def query_gteq(conn, field, value):
    return _query_range(conn, field, value, None)


def query_lteq(conn, field, value):
    return _query_range(conn, field, None, value)


def _query_range(conn, field, begin, end):
    return conn.query_range(field, begin, end)


QUERY_FACTORIES = {'=': query_eq, '=*': query_prefix, 
   '>=': query_gteq, 
   '<=': query_lteq}