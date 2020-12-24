# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/widgets/asset.py
# Compiled at: 2020-04-15 09:53:56
# Size of source mod 2**32: 671 bytes
"""
Module that contains widgets related with Plot Twist assets
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import logging, artellapipe.register
from artellapipe.widgets import asset
LOGGER = logging.getLogger()

class PlotTwistAssetWidget(asset.ArtellaAssetWidget, object):

    def __init__(self, asset, text=None, parent=None):
        super(PlotTwistAssetWidget, self).__init__(asset=asset, text=text, parent=parent)


artellapipe.register.register_class('AssetWidget', PlotTwistAssetWidget)