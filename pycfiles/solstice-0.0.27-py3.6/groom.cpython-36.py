# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solstice/files/groom.py
# Compiled at: 2020-05-04 03:27:08
# Size of source mod 2**32: 511 bytes
"""
Module that contains implementations for groom asset files
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from artellapipe.core import assetfile

class SolsticeGroomAssetFile(assetfile.ArtellaAssetFile, object):

    def __init__(self, asset=None):
        super(SolsticeGroomAssetFile, self).__init__(file_asset=asset)