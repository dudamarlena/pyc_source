# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/libs/pyblish/processors/modeling/scene/cleanscene.py
# Compiled at: 2020-04-17 19:10:58
# Size of source mod 2**32: 1112 bytes
"""
Module that contains clean scene processor implementation for Plot Twist
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import pyblish.api

class RemoveUnusedReferences(pyblish.api.ContextPlugin):
    __doc__ = '\n    Forces the cleanup of unused reference nodes\n    '
    label = 'Scene - Remove Unused References'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    optional = False

    def process(self, context):
        import tpDcc.dccs.maya as maya
        maya.mel.eval('RNdeleteUnused')
        return True


class RemoveUnusedDeformers(pyblish.api.ContextPlugin):
    __doc__ = '\n    Forces the cleanup of unused reference nodes\n    '
    label = 'Scene - Remove Unused Deformers'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    optional = False

    def process(self, context):
        import tpDcc.dccs.maya as maya
        maya.mel.eval('deleteUnusedDeformers')
        return True