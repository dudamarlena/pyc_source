# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\cocos\utils.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 579 bytes
__doc__ = 'original code moved to cocos.scenes.sequences'
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import warnings
import cocos.scenes.sequences as SQ

class SequenceScene(SQ):
    """SequenceScene"""

    def __init__(self, *scenes):
        warnings.warn('SequenceScene was moved from cocos.utils to cocos.scenes.sequences; The cocos.utils module will be removed in later cocos releases')
        (super(SequenceScene, self).__init__)(*scenes)