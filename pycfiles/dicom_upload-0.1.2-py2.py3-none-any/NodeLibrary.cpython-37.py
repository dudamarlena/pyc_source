# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/flowchart/NodeLibrary.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2623 bytes
from ..pgcollections import OrderedDict
from .Node import Node

def isNodeClass(cls):
    try:
        if not issubclass(cls, Node):
            return False
    except:
        return False
        return hasattr(cls, 'nodeName')


class NodeLibrary:
    """NodeLibrary"""

    def __init__(self):
        self.nodeList = OrderedDict()
        self.nodeTree = OrderedDict()

    def addNodeType(self, nodeClass, paths, override=False):
        """
        Register a new node type. If the type's name is already in use,
        an exception will be raised (unless override=True).
        
        ============== =========================================================
        **Arguments:**
        
        nodeClass      a subclass of Node (must have typ.nodeName)
        paths          list of tuples specifying the location(s) this 
                       type will appear in the library tree.
        override       if True, overwrite any class having the same name
        ============== =========================================================
        """
        if not isNodeClass(nodeClass):
            raise Exception('Object %s is not a Node subclass' % str(nodeClass))
        name = nodeClass.nodeName
        if not override:
            if name in self.nodeList:
                raise Exception("Node type name '%s' is already registered." % name)
        self.nodeList[name] = nodeClass
        for path in paths:
            root = self.nodeTree
            for n in path:
                if n not in root:
                    root[n] = OrderedDict()
                root = root[n]

            root[name] = nodeClass

    def getNodeType(self, name):
        try:
            return self.nodeList[name]
        except KeyError:
            raise Exception("No node type called '%s'" % name)

    def getNodeTree(self):
        return self.nodeTree

    def copy(self):
        """
        Return a copy of this library.
        """
        lib = NodeLibrary()
        lib.nodeList = self.nodeList.copy()
        lib.nodeTree = self.treeCopy(self.nodeTree)
        return lib

    @staticmethod
    def treeCopy(tree):
        copy = OrderedDict()
        for k, v in tree.items():
            if isNodeClass(v):
                copy[k] = v
            else:
                copy[k] = NodeLibrary.treeCopy(v)

        return copy

    def reload(self):
        """
        Reload Node classes in this library.
        """
        raise NotImplementedError()