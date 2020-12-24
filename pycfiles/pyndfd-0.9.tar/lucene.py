# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyndexter/indexers/lucene.py
# Compiled at: 2007-02-14 19:17:27
__doc__ = "\nLucene\n------\n\nThe Lucene adapter relies on PyLucene_, which is a Swig interface to a gcj\ncompiled version of Java Lucene.\n\nPyLucene is good, but there are some serious compatibility issues with Python\nthreading due to Java threading wanting to be the only implementation running.\n\nUsage\n~~~~~\n\n::\n\n    lucene://<path>\n\nInstallation\n~~~~~~~~~~~~\n\nPyLucene_ is quite difficult to install. Either use your distributions\npackaging system or, if you're brave, attempt a source installation. Beyond the\nscope of this hint.\n\n.. _PyLucene: http://pylucene.osafoundation.org/\n\n"
import os, PyLucene
from pyndexter import *

class LuceneIndexer(Indexer):
    __module__ = __name__

    def __init__(self, framework, path):
        Indexer.__init__(self, framework)
        self.path = path
        self.db_path = os.path.join(path, 'lucene.db')
        self.state_path = os.path.join(path, 'store.db')
        create = not os.path.exists(self.db_path) and framework.mode == READWRITE
        self.lucene_store = PyLucene.FSDirectory.getDirectory(self.db_path, create)
        self.analyzer = PyLucene.StandardAnalyzer()
        if framework.mode == READWRITE:
            self.writer = PyLucene.IndexWriter(self.lucene_store, self.analyzer, create)
            self.writer.setMaxFieldLength(1048576)
        else:
            self.writer = None
        return

    def index(self, document):
        doc = PyLucene.Document()
        for (k, v) in document.attributes.iteritems():
            doc.add(PyLucene.Field(unicode(k), unicode(v), PyLucene.Field.Store.YES, PyLucene.Field.Index.TOKENIZED))

        reader = PyLucene.StringReader(document.content)
        doc.add(PyLucene.Field('content', reader))
        self.writer.addDocument(doc)

    def discard(self, uri):
        reader = PyLucene.IndexReader.open(self.db_path)
        reader.deleteDocuments(PyLucene.Term('uri', unicode(uri)))
        reader.close()

    def search(self, query):
        lq = query.as_string()
        searcher = PyLucene.IndexSearcher(self.lucene_store)
        lq = PyLucene.QueryParser('content', self.analyzer).parse(lq)
        search = searcher.search(lq)
        return LuceneResult(self, query, search)

    def optimise(self):
        self.writer.optimize()

    def flush(self):
        try:
            self.writer.flush()
        except AttributeError:
            pass

    def close(self):
        if self.writer:
            self.writer.close()


indexer_factory = PluginFactory(LuceneIndexer)

class LuceneResult(Result):
    __module__ = __name__

    def __iter__(self):
        for (id, hit) in self.context:
            yield self._translate(hit)

    def __getitem__(self, index):
        return self._translate(self.context[index])

    def _translate(self, hit):
        attributes = {}
        for field in hit.fields():
            attributes[field.name().encode('utf-8')] = field.stringValue()

        attributes['uri'] = URI(attributes['uri'])
        return Hit(current=self.indexer.framework.fetch, indexed=self.indexer.fetch, **attributes)