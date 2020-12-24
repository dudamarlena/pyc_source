# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/assets/prop.py
# Compiled at: 2020-04-15 09:53:56
# Size of source mod 2**32: 516 bytes
__doc__ = '\nModule that contains definitions for prop assets in Plot Twist\n'
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from plottwist.core import asset

class PlotTwistProp(asset.PlotTwistAsset, object):

    def __init__(self, project, asset_data):
        super(PlotTwistProp, self).__init__(project=project, asset_data=asset_data)