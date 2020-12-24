# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/transmute/resolver.py
# Compiled at: 2014-02-20 18:49:35
import os.path, transmute.basket, transmute.bootstrap, sys

class Resolver:
    """Find and manage lists of updated packages."""

    def __init__(self, requirements=None, sources=None):
        """Initialize a new Resolver object.

        requirements: string or list of strings listing package requirements.
        """
        self.baskets = []
        self.entries = [ entry for entry in sys.path if os.path.isfile(entry) ]
        if sources:
            self.add_source(*sources)
        if requirements:
            self.require(requirements)

    @classmethod
    def _get_basket(cls, source):
        if isinstance(source, basestring):
            return transmute.basket.get_basket(source)
        return source

    @classmethod
    def _get_baskets(cls, *sources):
        return [ cls._get_basket(s) for s in sources ]

    def add_source(self, *sources):
        self.baskets.extend(self._get_baskets(sources))

    def require(self, requirements, sources=None):
        baskets = self.baskets
        if sources:
            baskets = baskets + self._get_baskets(*sources)
        transmute.bootstrap.require(baskets, requirements, self.entries)