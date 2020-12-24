# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/google_maps/overlay/info_window_tab.py
# Compiled at: 2013-04-04 15:36:36


class InfoWindowTab(object):

    def __init__(self, parent, content, label=None, selected=False):
        self._content = content
        self._content.setParent(parent)
        self._label = label
        self._selected = selected

    def getContent(self):
        return self._content

    def getLabel(self):
        return self._label

    def setLabel(self, label):
        self._label = label

    def isSelected(self):
        return self._selected

    def setSelected(self, selected):
        self._selected = selected