# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/assets/prop.py
# Compiled at: 2020-04-15 09:53:56
# Size of source mod 2**32: 516 bytes
"""
Module that contains definitions for prop assets in Plot Twist
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from plottwist.core import asset

class PlotTwistProp(asset.PlotTwistAsset, object):

    def __init__(self, project, asset_data):
        super(PlotTwistProp, self).__init__(project=project, asset_data=asset_data)