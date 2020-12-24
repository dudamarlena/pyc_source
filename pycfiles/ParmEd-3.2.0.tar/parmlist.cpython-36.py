# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/tools/parmlist.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 3454 bytes
"""
List of topology file objects that can be edited in ParmEd. They can be indexed
via either the name of the topology file or by the order in which they were
loaded.
"""
from __future__ import print_function, division, absolute_import
from parmed.utils.six import string_types
from parmed.structure import Structure
from parmed.formats.registry import load_file
from parmed.exceptions import FormatNotFound
from parmed.tools.exceptions import DuplicateParm, ParmIndexError, ParmError

class ParmList(object):
    __doc__ = '\n    List of Structure objects index-able via either file name or file index\n    (based on order added)\n    '

    def __init__(self):
        """ Must be instantiated by itself """
        self._parm_names = []
        self._parm_instances = []
        self.parm = None
        self.current_index = 0

    def set_new_active(self, idx):
        """ Sets a new active parm """
        self.current_index = self.index(idx)
        self.parm = self[self.current_index]

    def add_parm(self, parm, name=None):
        """ Add a parm to the list """
        if isinstance(parm, string_types):
            name = parm
            if name in self._parm_names:
                raise DuplicateParm('%s already in ParmList' % name)
            try:
                parm = load_file(name, structure=True)
            except FormatNotFound:
                raise ParmError('Could not determine file type of %s' % name)

            if not isinstance(parm, Structure):
                raise ParmError('Added parm must be Structure or a subclass')
        else:
            if not isinstance(parm, Structure):
                raise ParmError('Added parm must be Structure or a subclass')
            else:
                name = name or str(parm)
        if name in self._parm_names:
            raise DuplicateParm('%s already in ParmList' % parm)
        self._parm_names.append(name)
        self._parm_instances.append(parm)
        self.current_index = len(self._parm_instances) - 1
        self.parm = parm

    def index(self, idx):
        """ See what the index of the requested parm is (can be int or str) """
        if isinstance(idx, int):
            if idx < -len(self._parm_instances) or idx >= len(self._parm_instances):
                raise ParmIndexError('index out of range for ParmList')
            return idx
        try:
            return self._parm_names.index(str(idx))
        except ValueError:
            raise ParmIndexError('%s prmtop not in ParmList' % idx)

    def __getitem__(self, idx):
        """ Allow an integer index or string index to identify a parm """
        return self._parm_instances[self.index(idx)]

    def __contains__(self, name):
        """ See if a given parm name is in the list """
        if isinstance(name, int):
            return name >= 0 and name < len(self)
        else:
            return str(name) in self._parm_names

    def __iter__(self):
        """ Iterate through the prmtop names """
        return iter(self._parm_instances)

    def __len__(self):
        return len(self._parm_instances)

    def empty(self):
        """ Returns True if the list is empty; False otherwise """
        return len(self._parm_instances) == 0