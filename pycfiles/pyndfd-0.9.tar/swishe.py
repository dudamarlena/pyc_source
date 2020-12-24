# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyndexter/indexers/swishe.py
# Compiled at: 2007-02-15 02:18:37
import SwishE
from pyndexter import *

class SwishEIndexer(Indexer):
    __module__ = __name__

    def __init__(self, framework, path):
        Indexer.__init__(self, framework)
        self.path = path
        self.db = SwishE.new(path)

    def search(self, query):
        results = self.db.query(query.phrase)
        return SwishEResult(self, query, results)


class SwishEResult(Result):
    __module__ = __name__

    def __iter__(self):
        for row in self.context:
            uri = row.getproperty('swishdocpath')
            yield Hit(current=self.indexer.framework.fetch, indexed=self.indexer.fetch, uri=uri)

    def len(self):
        return self.context.hits()


indexer_factory = PluginFactory(SwishEIndexer)