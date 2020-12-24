# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/core/utils.py
# Compiled at: 2020-04-15 09:53:56
# Size of source mod 2**32: 520 bytes
"""
Module that contains different utils functions related with Plot Twist project
"""
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