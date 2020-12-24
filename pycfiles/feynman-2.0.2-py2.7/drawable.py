# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/feynman/core/drawable.py
# Compiled at: 2017-02-15 21:24:33
__all__ = ['Drawable']

class Drawable(object):
    """
    A drawable object that belongs to a certain diagram.
    """
    _diagram = None

    @property
    def diagram(self):
        """The diagram it belongs to."""
        if not self._diagram:
            raise Exception('Diagram not found.')
        return self._diagram

    @diagram.setter
    def diagram(self, D):
        self._diagram = D

    def draw(self):
        pass