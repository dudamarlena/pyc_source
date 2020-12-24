# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/libs/pyblish/processors/modeling/scene/cleanscene.py
# Compiled at: 2020-04-17 19:10:58
# Size of source mod 2**32: 1112 bytes
__doc__ = '\nModule that contains clean scene processor implementation for Plot Twist\n'
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import pyblish.api

class RemoveUnusedReferences(pyblish.api.ContextPlugin):
    """RemoveUnusedReferences"""
    label = 'Scene - Remove Unused References'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    optional = False

    def process(self, context):
        import tpDcc.dccs.maya as maya
        maya.mel.eval('RNdeleteUnused')
        return True


class RemoveUnusedDeformers(pyblish.api.ContextPlugin):
    """RemoveUnusedDeformers"""
    label = 'Scene - Remove Unused Deformers'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    optional = False

    def process(self, context):
        import tpDcc.dccs.maya as maya
        maya.mel.eval('deleteUnusedDeformers')
        return True