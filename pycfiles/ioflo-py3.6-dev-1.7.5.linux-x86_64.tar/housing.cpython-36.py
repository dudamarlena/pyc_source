# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/housing.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 7003 bytes
"""housing.py framework entity module

"""
import pdb, copy
from collections import deque
from ..aid.sixing import *
from ..aid.odicting import odict
from . import excepting
from . import registering
from . import storing
from . import acting
from . import poking
from . import needing
from . import goaling
from . import traiting
from . import fiating
from . import wanting
from . import completing
from . import doing
from . import tasking
from . import framing
from . import logging
from .. import trim
from ..aid.consoling import getConsole
console = getConsole()
Registries = odict(store=(storing.Store), tasker=(tasking.Tasker),
  log=(logging.Log))

def ClearRegistries():
    """Clear the registries in Registries

    """
    for value in Registries.values():
        value.Clear()


class House(registering.StoriedRegistrar):
    __doc__ = 'House Class for managing framework(s)\n       includes store for framework and name registries for framers, frames, and actions\n\n\n       iherited instance attributes\n          .name = unique name for machine\n          .store = data store for house should be same for all frameworks\n\n         instance attributes\n          .taskers = list of taskers in house for resolve links\n          .framers = list of framers needed to trace outlines\n\n          .fronts = list of taskables to go in front of taskables\n          .mids = list of taskables to go in middle of taskables\n          .backs = list of taskables to go in back of taskables\n\n          .taskables = list of active/inactive taskers (fronts + mids + backs)\n          .auxes = list of aux  framers in house subset of .taskers\n          .slaves = list of slave taskers in house subset of .taskers\n          .moots = list of moot framers in house subset of .taskers\n\n          .clones = list of tuples for cloning (original, clone, human, count)\n\n          .names = dictonary of names from each name registry\n          .counters = dictionary of counters from each name registry\n\n          .metas = dictionary of (name, share) items of meta data for access by skedder\n                  name is how skedder accesses the associated share\n    '
    Counter = 0
    Names = {}

    def __init__(self, **kw):
        (super(House, self).__init__)(**kw)
        self.taskers = []
        self.framers = []
        self.fronts = []
        self.mids = []
        self.backs = []
        self.taskables = []
        self.auxes = []
        self.slaves = []
        self.moots = []
        self.presolvables = deque()
        self.resolvables = deque()
        self.names = odict()
        self.counters = odict()
        self.metas = odict()
        for key in Registries:
            self.names[key] = odict()
            self.counters[key] = 0

        if not self.store:
            self.store = storing.Store(name=(self.name))
        self.store.house = self

    def orderTaskables(self):
        """Place taskables in order
        """
        console.terse("   Ordering taskable taskers for House '{0}' ...\n".format(self.name))
        self.taskables = self.fronts + self.mids + self.backs

    def assignRegistries(self):
        """Point class Names registries dicts and counters to local version in house
           Subsequent creation of instances will then be registered locally
           Idempotent operation
        """
        for key, value in Registries.items():
            value.Names = self.names[key]
            value.Counter = self.counters[key]

    def resolve(self):
        """ resolves links from building where links are name strings of objects
            resolution looks up name string in appropriate registry and replaces
            name string with link to object
        """
        console.terse("   Resolving House '{0}' ...\n".format(self.name))
        self.assignRegistries()
        for tasker in self.taskers:
            if not tasker.presolved and tasker not in self.moots:
                self.presolvables.append(tasker)

        self.presolvePresolvables()
        self.resolveResolvables()

    def presolvePresolvables(self):
        """
        Continually presolve presolvables deque until empty.
        Because a tasker (framer) may clone new framers
        each presolve may add more presolvables

        Once presolved add to resolvables
        """
        while self.presolvables:
            tasker = self.presolvables.popleft()
            tasker.presolve()
            self.resolvables.append(tasker)

    def resolveResolvables(self):
        """
        Continually resolve resolvables deque until empty.
        Because a tasker (framer) may clone new framers
        each resolve may add more resolvables
        """
        while self.resolvables:
            tasker = self.resolvables.popleft()
            tasker.resolve()

    def showAllTaskers(self):
        """Show all Taskers and Slaves and Auxes and Moots and Framers."""
        console.terse("Taskables in House '{0}':\n     {1}\n".format(self.name, ' '.join([tasker.name for tasker in self.taskables])))
        console.terse("Slaves in House '{0}':\n     {1}\n".format(self.name, ' '.join([tasker.name for tasker in self.slaves])))
        console.terse("Auxes in House '{0}':\n     {1}\n".format(self.name, ' '.join([tasker.name for tasker in self.auxes])))
        console.terse("Moots in House '{0}':\n     {1}\n".format(self.name, ' '.join([tasker.name for tasker in self.moots])))
        console.terse("Framers in House '{0}':\n     {1}\n".format(self.name, ' '.join([tasker.name for tasker in self.framers])))