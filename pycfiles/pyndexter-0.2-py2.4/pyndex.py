# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyndexter/indexers/pyndex.py
# Compiled at: 2007-02-15 02:00:13
"""
Pyndex
------

Pyndex_ is a pure-Python indexer written
by the busy Divmod folks. It is quite fast, but again, no longer supported.

**Note:** Pyndex does not support document deletion. I have hacked around this
by inserting an empty document but this is obviously not ideal.

.. _Pyndex: http://www.divmod.org/projects/pyndex

Usage
~~~~~

::

    pyndex://<path>

Installation
~~~~~~~~~~~~

::

    easy_install http://downloads.sourceforge.net/pyndex/Pyndex-0.3.2a.tar.gz
"""
import os
from pyndexter import *
import metakit
pyndex = __import__('pyndex')
__import__('pyndex.indexer')

class PyndexIndexer(Indexer):
    __module__ = __name__

    def __init__(self, framework, path):
        Indexer.__init__(self, framework)
        self.path = path
        self.pyndex_path = os.path.join(self.path, 'pyndex.db')
        self.state_path = os.path.join(self.path, 'state.db')
        if framework.mode == READWRITE:
            if not os.path.exists(self.path):
                os.makedirs(self.path)
        rw = framework.mode == READWRITE and 1 or 0
        self.db = pyndex.indexer.Index(metakit.storage(self.pyndex_path, rw))

    def index(self, document):
        uri = unicode(document.uri).encode('utf-8')
        self.db.index(uri, document.content.encode('utf-8'))

    def discard(self, uri):
        self.db.index(unicode(uri).encode('utf-8'), '')

    def search(self, query):
        qs = (' ').join(query.terms()).encode('utf-8')
        return PyndexResult(self, query, self.db.find(qs))

    def optimise(self):
        self.db.optimize()

    def flush(self):
        self.db.commit()

    def close(self):
        self.db.close()


indexer_factory = PluginFactory(PyndexIndexer)

class PyndexResult(Result):
    __module__ = __name__

    def __iter__(self):
        for hit in self.context:
            yield self._translate(hit)

    def __getitem__(self, index):
        return self._translate(self.context[index])

    def _translate(self, hit):
        return Hit(uri=URI(hit.doc.docname), score=hit.score, current=self.indexer.framework.fetch, indexed=self.indexer.fetch)