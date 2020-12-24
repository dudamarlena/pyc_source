# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/transmute/transmuter.py
# Compiled at: 2014-02-20 18:49:35
import os, pkg_resources, sys, transmute.bootstrap

class Transmuter(object):
    """Manage updates to Python's module search path."""

    def __init__(self, entries):
        self.working_set = pkg_resources.WorkingSet(entries)

    @staticmethod
    def _dist_conflicts(dist):
        return any(module in sys.modules for module in dist._get_metadata('top_level.txt'))

    def _has_conflicts(self):
        return any(self._dist_conflicts(dist) for dist in self.working_set)

    def _reset_path(self):
        sys.path[0:0] = self.working_set.entries

    def soft_transmute(self):
        for dist in self.working_set:
            dist.activate()

        self._reset_path()
        reload(pkg_resources)

    def hard_transmute(self):
        self.executable = sys.executable
        self.arguments = [self.executable] + sys.argv
        self.environment = os.environ.copy()
        self._reset_path()
        self.environment['PYTHONPATH'] = os.pathsep.join(sys.path)
        os.execve(self.executable, self.arguments, self.environment)
        assert False

    def transmute(self):
        """Inject packages in working set."""
        if self._has_conflicts():
            self.hard_transmute()
        else:
            self.soft_transmute()