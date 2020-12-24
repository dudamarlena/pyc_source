# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treelib/exceptions.py
# Compiled at: 2019-12-01 01:08:08
# Size of source mod 2**32: 943 bytes


class NodePropertyError(Exception):
    __doc__ = 'Basic Node attribute error'


class NodeIDAbsentError(NodePropertyError):
    __doc__ = "Exception throwed if a node's identifier is unknown"


class NodePropertyAbsentError(NodePropertyError):
    __doc__ = "Exception throwed if a node's data property is not specified"


class MultipleRootError(Exception):
    __doc__ = 'Exception throwed if more than one root exists in a tree.'


class DuplicatedNodeIdError(Exception):
    __doc__ = 'Exception throwed if an identifier already exists in a tree.'


class LinkPastRootNodeError(Exception):
    __doc__ = '\n    Exception throwed in Tree.link_past_node() if one attempts\n    to "link past" the root node of a tree.\n    '


class InvalidLevelNumber(Exception):
    pass


class LoopError(Exception):
    __doc__ = "\n    Exception thrown if trying to move node B to node A's position\n    while A is B's ancestor.\n    "