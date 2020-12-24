# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/tools/playblastmanager/core/defines.py
# Compiled at: 2020-05-03 22:03:42
# Size of source mod 2**32: 609 bytes
"""
Module that contains definitions used by PlayblastManager
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'

class TimeRanges(object):
    RANGE_TIME_SLIDER = 'Time Slider'
    RANGE_START_END = 'Start/End'
    CURRENT_FRAME = 'Current Frame'
    CUSTOM_FRAMES = 'Custom Frames'


class ScaleSettings(object):
    SCALE_WINDOW = 'From Window'
    SCALE_RENDER_SETTINGS = 'From Render Settings'
    SCALE_CUSTOM = 'Custom'