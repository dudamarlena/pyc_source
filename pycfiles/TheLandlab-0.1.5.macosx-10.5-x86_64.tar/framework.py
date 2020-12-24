# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/framework/framework.py
# Compiled at: 2014-09-23 12:37:24
import inspect
from landlab.framework.component import load_landlab_components
from landlab import Palette, Arena

class Error(Exception):
    """
    Base exception for this module
    """
    pass


class Framework(object):
    """
    A framework for connecting and running component from The Landlab.
    """

    def __init__(self):
        self._palette = Palette(**load_landlab_components())
        self._arena = Arena()

    def instantiate(self, name):
        """
        Instantiate a component called *name* from the palette and move it to
        the arena.
        """
        try:
            self._arena.instantiate(self._palette.get(name), name)
        except KeyError:
            pass

    def remove(self, name):
        """
        Remove a component called *name* from the arena.
        """
        try:
            self._arena.remove(name)
        except KeyError:
            pass

    def list_palette(self):
        """
        Get a list of names of the components in the palette.
        """
        return self._palette.list()

    def list_arena(self):
        """
        Get a list of names of the components in the arena.
        """
        return self._arena.list()

    def arena_uses(self):
        """
        Get a list of variable names that components in the arena use.
        """
        return self._arena.uses()

    def arena_provides(self):
        """
        Get a list of variable names that components in the arena provide.
        """
        return self._arena.provides()

    def palette_uses(self):
        """
        Get a list of variable names that components in the palette use.
        """
        return self._palette.uses()

    def palette_provides(self):
        """
        Get a list of variable names that components in the palette provide.
        """
        return self._palette.provides()

    def __repr__(self):
        return 'Framework(%s)' % (', ').join(self._palette.keys())