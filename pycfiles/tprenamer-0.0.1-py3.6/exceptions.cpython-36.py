# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpRenamer/core/exceptions.py
# Compiled at: 2019-12-22 00:17:48
# Size of source mod 2**32: 903 bytes
"""
Module that contains exceptions used by tpRenamer
"""
from __future__ import print_function, division, absolute_import
import tpDccLib as tp

class RenameException(Exception):
    __doc__ = '\n    Custom exception class that will handle errors when renaming elements using tpRenamer tool\n    '

    def __init__(self, nodes):
        error_text = '======= Renamer: Failed to rename one or more nodes ======='
        if not hasattr(nodes, '__iter__'):
            nodes = [
             nodes]
        for node in nodes:
            if not tp.Dcc.object_exists(node):
                error_text += "\t'%s' no longer exists.\n" % node
            else:
                if tp.Dcc.node_is_locked(node):
                    error_text += "\t'%s' is locked.\n" % node
                else:
                    error_text += "\t'%s' failure unknows.\n" % node

        Exception.__init__(self, error_text)