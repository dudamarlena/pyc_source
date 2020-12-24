# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treelib/plugins.py
# Compiled at: 2020-02-27 08:49:21
# Size of source mod 2**32: 1253 bytes
"""
This is a public location to maintain contributed
utilities to extend the basic Tree class.

Deprecated! We prefer a unified processing of Tree object.
"""
from __future__ import unicode_literals
from .misc import deprecated

@deprecated(alias='tree.to_graphviz()')
def export_to_dot(tree, filename=None, shape='circle', graph='digraph'):
    """Exports the tree in the dot format of the graphviz software"""
    tree.to_graphviz(filename=filename, shape=shape, graph=graph)