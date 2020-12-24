# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyndexter/indexers/lupy.py
# Compiled at: 2007-02-14 19:20:28
"""
Lupy
----

Lupy_ is a (deprecated) pure-Python indexer. It is excruciatingly slow,
presumably because of its desire to be compatible with Lucene. Included
as an excercise mostly :)

.. _Lupy: http://www.divmod.org/projects/lupy

Usage
~~~~~

::

    lupy://<path>

Installation
~~~~~~~~~~~~

::

    easy_install http://gentoo.prz.rzeszow.pl/distfiles/Lupy-0.2.1.tar.gz
"""
import os
from pyndexter import *
lupy = __import__('lupy', {}, {}, [''])
lupy.indexer = __import__('lupy.indexer', {}, {}, [''])
lupy.search = __import__('lupy.search', {}, {}, [''])

class LupyIndexer(Indexer):
    __module__ = __name__

    def __init__(self, framework, path):
        Indexer.__init__(self, framework)
        self.path = path
        self.db_path = os.path.join(self.path, 'lupy.db').encode('utf-8')
        self.state_path = os.path.join(self.path, 'state.db')
        if framework.mode == READWRITE and not os.path.exists(self.path):
            os.makedirs(self.path)
        self.db = lupy.indexer.Index(self.db_path, create=framework.mode == READWRITE and not os.path.exists(self.db_path))

    def index(self, document):
        attributes = dict([ ('_' + k.encode('utf-8'), unicode(v)) for (k, v) in document.attributes.iteritems() if v is not None ])
        self.discard(uri=document.uri)
        self.db.index(text=document.content, **attributes)
        return

    def discard(self, uri):
        self.db.delete(uri=unicode(uri))

    def search(self, query):
        lupy_query = lupy.indexer.BooleanQuery()
        self._compile_query(query, (True, False), lupy_query)
        searcher = lupy.search.indexsearcher.IndexSearcher(self.db_path)
        hits = searcher.search(lupy_query)
        return LupyResult(self, query, hits)

    def optimise(self):
        self.db.optimize()

    def close(self):
        self.db.close()

    def _compile_query(self, node, op, query):
        if not node or node.type == node.NULL:
            return
        if node.type == node.AND:
            self._compile_query(node.left, (True, False), query)
            self._compile_query(node.right, (True, False), query)
        elif node.type == node.OR:
            self._compile_query(node.left, (False, False), query)
            self._compile_query(node.right, (False, False), query)
        elif node.type == node.NOT:
            self._compile_query(node.left, (False, True), query)
        elif node.type == node.TERM:
            query.add(lupy.indexer.TermQuery(lupy.indexer.Term('text', node.value)), *op)
        else:
            raise NotImplementedError


indexer_factory = PluginFactory(LupyIndexer)

class LupyResult(Result):
    __module__ = __name__

    def __iter__(self):
        for (index, doc) in enumerate(self.context):
            yield self._translate(index, doc)

    def __getitem__(self, index):
        return self._translate(index, self.context[index])

    def _translate(self, index, doc):
        fields = dict([ (str(k), doc.get(k)) for k in doc.fieldNames ])
        fields['score'] = self.context.score(index)
        fields['uri'] = URI(fields['uri'])
        return Hit(current=self.indexer.framework.fetch, indexed=self.indexer.fetch, **fields)