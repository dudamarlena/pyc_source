# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pilar/robocomp/components/learnbot/learnbot_dsl/functions/perceptual/camera/is_any_tag.py
# Compiled at: 2019-04-15 04:07:28
from __future__ import print_function, absolute_import

def is_any_tag(lbot):
    lbot.lookingLabel(0)
    return len(lbot.listTags()) is not 0