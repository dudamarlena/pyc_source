# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solstice/core/assetsviewer.py
# Compiled at: 2019-10-05 11:59:30
# Size of source mod 2**32: 676 bytes
"""
Module that contains widget implementation for asset viewer for Solstice
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from artellapipe.core import assetsviewer
from solstice.core import asset

class SolsticeAssetsViewer(assetsviewer.AssetsViewer, object):
    ASSET_WIDGET_CLASS = asset.SolsticeAssetWidget

    def __init__(self, project, column_count=3, parent=None):
        super(SolsticeAssetsViewer, self).__init__(project=project, column_count=column_count, parent=parent)