# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/linseed/snapshot.py
# Compiled at: 2011-01-16 05:32:28
from .battery import Battery
from .cpu import CPU
from .memory import Memory, Swap
from .wicd import WICD
import pkg_resources

class Snapshot(object):
    """A Snapshot is a quasi-dict-like mapping of info_source
    extension names to instances of the associated info_source
    extensions.

    In other words, it maps names to objects that provide different
    pieces of system information. 

    To use a Snapshot, simply instantiate one and start using it.

    TODO: The name "snapshot" is a bit misleading at this point and should probably be changed.
    """

    def __init__(self):
        self.sources = {}
        for p in pkg_resources.iter_entry_points('linseed.info_source'):
            p = p.load()
            self.sources[p.name()] = (p, None)

        return

    def keys(self):
        return self.sources.keys()

    def items(self):
        for k in self.keys():
            yield (k, self[k])

    def values(self):
        for k in self.keys():
            yield self[k]

    def __len__(self):
        return len(self.sources)

    def __iter__(self):
        return iter(self.sources)

    def __getitem__(self, key):
        current = self.sources[key]
        if current[1] is None:
            self.sources[key] = (
             current[0], current[0]())
            current = self.sources[key]
        return current[1]