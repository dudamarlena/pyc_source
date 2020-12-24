# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flappy/ui/mouse.py
# Compiled at: 2014-03-13 10:09:15
from flappy.display import Stage

class Mouse(object):

    @staticmethod
    def hide():
        stage = Stage._current_stage
        if stage is not None:
            stage.showCursor(False)
        return

    @staticmethod
    def show():
        stage = Stage._current_stage
        if stage is not None:
            stage.showCursor(True)
        return