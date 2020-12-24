# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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