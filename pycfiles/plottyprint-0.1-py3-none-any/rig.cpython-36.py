# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/files/rig.py
# Compiled at: 2020-04-15 09:53:56
# Size of source mod 2**32: 502 bytes
__doc__ = '\nModule that contains implementations for rig asset files\n'
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from artellapipe.core import assetfile

class PlotTwistRigAssetFile(assetfile.ArtellaAssetFile, object):

    def __init__(self, asset):
        super(PlotTwistRigAssetFile, self).__init__(file_asset=asset)