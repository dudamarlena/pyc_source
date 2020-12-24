# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alteraparser/syntaxgraph/dockable.py
# Compiled at: 2015-12-30 04:57:43
# Size of source mod 2**32: 292 bytes


class Dockable(object):

    def connect(self, dockable):
        raise NotImplemented

    def __gt__(self, other):
        self.connect(other)
        return other

    def get_dock_vertex(self):
        """
        Return vertex that can be docked
        """
        raise NotImplemented