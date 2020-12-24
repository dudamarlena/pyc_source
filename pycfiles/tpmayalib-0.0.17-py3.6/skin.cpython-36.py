# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpMayaLib/data/skin.py
# Compiled at: 2020-01-16 21:52:40
# Size of source mod 2**32: 471 bytes
"""
Module that contains skin weights data classes for Maya
"""
from __future__ import print_function, division, absolute_import
import tpMayaLib as maya
from tpMayaLib.data import base

class SkinWeightsData(base.MayaCustomData, object):

    def __init__(self, name=None, path=None):
        super(SkinWeightsData, self).__init__(name=name, path=path)

    def get_data_title(self):
        return 'maya_skin_weights'