# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\cocos\utils.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 579 bytes
"""original code moved to cocos.scenes.sequences"""
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import warnings
import cocos.scenes.sequences as SQ

class SequenceScene(SQ):
    __doc__ = 'moved to cocos.scenes.sequences'

    def __init__(self, *scenes):
        warnings.warn('SequenceScene was moved from cocos.utils to cocos.scenes.sequences; The cocos.utils module will be removed in later cocos releases')
        (super(SequenceScene, self).__init__)(*scenes)