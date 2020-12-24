# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/rdf/serializer.py
# Compiled at: 2008-03-16 19:10:10
"""
This module defines the serializer plugin interface.

The module is useful for those wanting to write a serializer that can
plugin to rdf. If you are wanting to invoke a serializer you likely
want to do so through the Graph class serialize method.

TODO: info for how to write a serializer that can plugin to rdf.

"""
from rdf.term import URIRef

class Serializer(object):

    def __init__(self, store):
        self.store = store
        self.encoding = 'UTF-8'
        self.base = None
        return

    def serialize(self, stream, base=None, encoding=None, **args):
        """Abstract method"""
        pass

    def relativize(self, uri):
        base = self.base
        if base is not None and uri.startswith(base):
            uri = URIRef(uri.replace(base, '', 1))
        return uri