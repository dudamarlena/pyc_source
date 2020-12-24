# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyndexter/sources/metasource.py
# Compiled at: 2007-02-15 02:24:21
"""
The MetaSource is used internally by the Pyndexter framework.
"""
import pickle
from StringIO import StringIO
from pyndexter import *
from urlparse import urlsplit

class MetaSource(Source):
    """ A collection of sources. If sources serve the same documents the
    results will be undefined, and probably not good. """
    __module__ = __name__

    def __init__(self, framework, sources=None):
        Source.__init__(self, framework)
        self.sources = sources or []

    def add_source(self, source):
        """ Add an additional source to the collection. """
        self.sources.append(source)

    def __hash__(self):
        raise SourceError('MetaSource can not be hashed')

    def __iter__(self):
        for source in self.sources:
            for uri in source:
                yield uri

    def matches(self, uri):
        for source in self.sources:
            if source.matches(uri):
                return True

        return False

    def fetch(self, uri):
        for source in self.sources:
            if source.matches(uri):
                return source.fetch(uri)

        raise DocumentNotFound(uri)

    def exists(self, uri):
        for source in self.sources:
            if source.exists(uri):
                return True

        return False

    def marshal(self, file):
        state = {}
        for source in self.sources:
            stream = StringIO()
            source.marshal(stream)
            state[hash(source)] = stream.getvalue()

        file.write(pickle.dumps(state, 2))

    def difference(self, file):
        try:
            state = pickle.loads(file.read())
        except Exception, e:
            raise InvalidState('Invalid state provided to MetaSource. Exception was %s: %s' % (e.__class__.__name__, e))

        for source in self.sources:
            if hash(source) not in state:
                for uri in source:
                    yield (
                     ADDED, uri)

            else:
                pseudo_file = StringIO(state[hash(source)])
                for change in source.difference(pseudo_file):
                    yield change