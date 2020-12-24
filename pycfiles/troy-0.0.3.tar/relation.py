# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: troy/workload/relation.py
# Compiled at: 2014-02-24 20:40:00
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import radical.utils as ru, troy.utils as tu
from troy.constants import *
import troy

class Relation(tu.Properties):
    """
    The `Relation` class represents a logical, temporal or spacial dependency
    between two :class:`Task`s, and is part of a workload managed by Troy.

    Relation instances are created and owned by the :class:`Workload` class they
    are part of -- only that class should change its composition and state.
    Relations are created according to a :class:`RelationDescription`, i.e.
    a set of key-value pairs describing the represented task dependency.
    """

    def __init__(self, descr):
        """
        Create a new workload dependency element, aka Relation, according to 
        the description..

        Each new relation is assigned a new ID.

        Later implementations may allow for an additional id parameter, to
        reconnect to the thus identified relation instance.  
        """
        tid = ru.generate_id('r.')
        if 'head' not in descr:
            raise ValueError("no 'head' in RelationDescription")
        if 'tail' not in descr:
            raise ValueError("no 'tail' in RelationDescription")
        tu.Properties.__init__(self, descr)
        self.register_property('id')
        self.register_property('head')
        self.register_property('tail')
        self.register_property('description')
        self.id = tid
        self.head = descr.head
        self.tail = descr.tail
        self.description = descr

    def __str__(self):
        return '%-7s: %s' % (self.id, self.description)

    def __repr__(self):
        return str(self)