# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/core/utils.py
# Compiled at: 2020-04-15 09:53:56
# Size of source mod 2**32: 520 bytes
__doc__ = '\nModule that contains different utils functions related with Plot Twist project\n'
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import tpDcc as tp

def clean_scene():
    """
    Clean current scene
    """
    if not tp.is_maya():
        return
    from tpDcc.dccs.maya.core import scene
    scene.clean_scene()
    extra_node_types_to_delete = []