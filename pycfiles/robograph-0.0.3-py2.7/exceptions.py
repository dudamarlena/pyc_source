# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/base/exceptions.py
# Compiled at: 2016-07-13 17:51:17


class NodeOutputLabelUndefinedError(Exception):
    """
    Marks that the label for a node's output is still not specified
    """
    pass


class GraphError(Exception):
    """
    Base class for Graph errors
    """
    pass


class NodeConnectionError(GraphError):
    """
    This is to mark an error in connecting nodes of a graph
    """
    pass


class NodeDeletionError(GraphError):
    """
    This is to mark an error in deleting nodes of a graph
    """
    pass


class StopGraphExecutionSignal(Exception):
    """
    This is to notify termination of graph execution due to ordinary reasons.
    """
    pass


class GraphExecutionError(GraphError):
    """
    This is to mark an unexpected error in graph execution.
    """
    pass