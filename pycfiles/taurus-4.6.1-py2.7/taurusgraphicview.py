# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/graphic/taurusgraphicview.py
# Compiled at: 2019-08-19 15:09:29
"""
taurusgraphicview.py:
"""
__all__ = [
 'TaurusGraphicsView']
__docformat__ = 'restructuredtext'
from taurus.external.qt import Qt
from taurus.qt.qtgui.base import TaurusBaseWidget

class TaurusGraphicsView(Qt.QGraphicsView, TaurusBaseWidget):

    def __init__(self, parent=None, designMode=False):
        name = self.__class__.__name__
        self.call__init__wo_kw(Qt.QGraphicsView, parent)
        self.call__init__(TaurusBaseWidget, name, designMode=designMode)
        self.defineStyle()

    def defineStyle(self):
        self.updateStyle()

    def isReadOnly(self):
        return True

    def updateStyle(self):
        self.update()

    @classmethod
    def getQtDesignerPluginInfo(cls):
        ret = TaurusBaseWidget.getQtDesignerPluginInfo()
        ret['module'] = 'taurus.qt.qtgui.graphic'
        ret['group'] = 'Taurus Display'
        ret['icon'] = 'designer:graphicsview.png'
        return ret