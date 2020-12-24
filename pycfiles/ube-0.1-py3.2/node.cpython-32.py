# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ube/api/tree/node.py
# Compiled at: 2013-08-25 16:43:40
"""
Created on Nov 18, 2012

@author: nibo
"""

class node(object):
    """Node is the base class for all objects in UBPM that reside in the tree.
    This class is created and populated by a factory class."""
    nodeid = None
    parentnodeid = None
    nodeuuid = None
    nodetypeid = None
    nodename = None
    datamodelid = None

    def __init__(self, _nodeid=None, _parentnodeid=None, _nodeuuid=None, _nodetypeid=None, _nodename=None, _datamodelid=None, _create_original=True):
        """
        Constructor
        """
        self.nodeid = _nodeid
        self.parentnodeid = _parentnodeid
        self.nodeuuid = _nodeuuid
        self.nodetypeid = _nodetypeid
        self.nodename = _nodename
        self.datamodelid = _datamodelid
        if _create_original:
            self._node__original = node(_create_original=False)
            self.reassign_properties(self, self._node__original)

    def reassign_properties(self, _source, _dest):
        """Assign the properties and their valued from one node to another"""
        _source_properties = self._read_properties(_source)
        for curr_property in _source_properties:
            setattr(_dest, curr_property[0], curr_property[1])

    def _read_properties(self, _object):
        """Return a list of all properties of an object"""
        properties = list()
        for k in _object.__dict__.items():
            if not hasattr(k[1], '__call__') and k[0][0:1] != '_':
                properties.append(k)
                continue

        return properties