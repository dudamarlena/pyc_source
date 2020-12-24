# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solstice/core/shelf.py
# Compiled at: 2020-05-03 22:16:37
# Size of source mod 2**32: 936 bytes
"""
Module that contains implementation for Solstice Shelf
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import tpDcc

class SolsticeShelf(tpDcc.Shelf, object):
    ICONS_PATHS = tpDcc.ResourcesMgr().get_resources_paths()

    def __init__(self, name='SolsticeShelf', label_background=(0, 0, 0, 0), label_color=(0.9, 0.9, 0.9), category_icon=None):
        enable_labels = False
        if tpDcc.is_houdini():
            enable_labels = True
        super(SolsticeShelf, self).__init__(name=name,
          label_background=label_background,
          label_color=label_color,
          category_icon=category_icon,
          enable_labels=enable_labels)