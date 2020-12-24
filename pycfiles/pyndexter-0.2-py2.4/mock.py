# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyndexter/sources/mock.py
# Compiled at: 2007-02-15 02:24:43
"""
Used by the Pyndexter unit tests.
"""
from pyndexter import *
from pyndexter.tests.corpus import documents

class MockSource(Source):
    """A mock source class. Uses the documents in pyndexter.tests.corpus."""
    __module__ = __name__

    def __iter__(self):
        docs = documents.values()
        docs.sort(key=lambda row: row.uri)
        for doc in docs:
            if self._glob_predicate(doc.uri):
                self._state[unicode(doc.uri)] = doc.changed
                yield doc.uri

    def fetch(self, uri):
        try:
            return documents[unicode(uri)]
        except KeyError:
            raise DocumentNotFound(uri)

    def matches(self, uri):
        return uri.scheme == 'mock'

    def exists(self, uri):
        return unicode(uri) in documents

    def __hash__(self):
        uris = documents.keys()
        uris.sort()
        return hash((',').join(uris))


source_factory = PluginFactory(MockSource, include=PluginFactory.List(str), exclude=PluginFactory.List(str))