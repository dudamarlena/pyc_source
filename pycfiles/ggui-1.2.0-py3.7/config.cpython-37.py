# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ggui\config.py
# Compiled at: 2019-08-03 12:38:58
# Size of source mod 2**32: 521 bytes
from glue.config import settings, preference_panes
from qtpy import QtWidgets
from glue.config import viewer_tool
from glue.viewers.common.qt.tool import Tool

@viewer_tool
class GGUIAutoChop(Tool):
    icon = 'myicon.png'
    tool_id = 'custom_tool'
    action_text = 'Does cool stuff'
    tool_tip = 'Does cool stuff'
    shortcut = 'D'

    def __init__(self, viewer):
        super(MyCustomMode, self).__init__(viewer)

    def activate(self):
        pass

    def close(self):
        pass