# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solstice/assets/character.py
# Compiled at: 2020-05-03 22:16:37
# Size of source mod 2**32: 525 bytes
"""
Module that contains definitions for character assets in Solstice
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from solstice.core import asset

class SolsticeCharacter(asset.SolsticeAsset, object):

    def __init__(self, project, asset_data):
        super(SolsticeCharacter, self).__init__(project=project, asset_data=asset_data)