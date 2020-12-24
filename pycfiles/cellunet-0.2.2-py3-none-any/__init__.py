# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cellulose/__init__.py
# Compiled at: 2007-06-07 19:19:14
__doc__ = '\ncellulose\nCopyright 2006 by Matthew Marshall <matthew@matthewmarshall.org>\n\nA light weight library providing lazy evaluation and caching with automatic\ndependency discovery and cache expiration.\n\nBe sure to check out the docs directory of the distribution.\n'
import threading, weakref, types, warnings
from cellulose.cells import DependantCell, DependencyCell, InputCell, ComputedCell
from cellulose.cells import get_dependant_stack, CyclicDependencyError
from cellulose.descriptors import InputCellDescriptor, ComputedCellDescriptor, wake_cell_descriptors
from cellulose.celltypes import CellList, CellDict, CellSet, ComputedDict
from cellulose.observers import ObserverBank, default_observer_bank, Observer

class AutoCells(object):
    """ A class for automatically cellifing attributes.

    All assigned attributes that do not start with an underscore become a cell.
    Also, all functions that start with '_get_' create computed cells.

    This class really doesn't belong in this module... if it belongs in
    cellulose at all.
    """

    def __init__(self):
        self._cells = {}
        for name in [ n for n in dir(self) if n.startswith('_get_') ]:
            getf = getattr(self, name)
            cell_name = name[5:]
            cell = ComputedCell(getf)
            self._cells[cell_name] = cell

    def __setattr__(self, name, value):
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            if name not in self._cells:
                self._cells[name] = InputCell()
            self._cells[name].value = value

    def __getattr__(self, name):
        if name not in self._cells:
            return object.__getattribute__(self, name)
        else:
            return self._cells[name].value