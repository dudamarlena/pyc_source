# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/container/taurusbasecontainer.py
# Compiled at: 2019-08-19 15:09:29
"""This module provides base class for all taurus container widgets"""
__all__ = [
 'TaurusBaseContainer']
__docformat__ = 'restructuredtext'
from taurus.external.qt import Qt
from taurus.qt.qtgui.base import TaurusBaseComponent, TaurusBaseWidget

class TaurusBaseContainer(TaurusBaseWidget):
    """Base class for the Taurus container widgets.
    This type of taurus container classes are specially useful if you define
    a parent taurus model to them and set all contained taurus widgets to use parent
    model. Example::

        from taurus.qt.qtgui.container import *
        from taurus.qt.qtgui.display import *

        widget = TaurusWidget()
        layout = Qt.QVBoxLayout()
        widget.setLayout(layout)
        widget.model = 'sys/database/2'
        stateWidget = TaurusLabel()
        layout.addWidget(stateWidget)
        stateWidget.model = 'sys/database/2/state'
    """

    def __init__(self, name='', parent=None, designMode=False):
        name = name or self.__class__.__name__
        self.call__init__(TaurusBaseWidget, name, parent, designMode=designMode)
        self.defineStyle()
        self.designMode = designMode

    def taurusChildren(self, objs=None):
        """
        returns a list of all taurus children of this taurus container (recurses down
        skipping non-taurus widgets)

        :param objs: (list<objects>) if given, the search starts at the objects
                     passed in this list

        :return: (list<TaurusBaseWidget>)
        """
        if objs is None:
            objs = self.children()
        result = []
        for o in objs:
            if isinstance(o, TaurusBaseWidget):
                result.append(o)
            else:
                result += self.taurusChildren(o.children())

        return result

    def defineStyle(self):
        self.updateStyle()

    def sizeHint(self):
        return Qt.QWidget.sizeHint(self)

    def isReadOnly(self):
        return True

    def updateStyle(self):
        if self.getShowQuality():
            self.setAutoFillBackground(True)
        else:
            self.setAutoFillBackground(False)
        TaurusBaseWidget.updateStyle(self)

    def getPendingOperations(self):
        pending_ops = []
        for child in Qt.QObject.children(self):
            if isinstance(child, TaurusBaseComponent):
                pending_ops += child.getPendingOperations()

        return pending_ops

    def resetPendingOperations(self):
        self.debug('Reset changes')
        for child in Qt.QObject.children(self):
            if isinstance(child, TaurusBaseComponent):
                child.resetPendingOperations()

    def hasPendingOperations(self):
        ret = False
        for child in Qt.QObject.children(self):
            if isinstance(child, TaurusBaseComponent):
                ret |= child.hasPendingOperations()

        return ret

    def handleEvent(self, evt_src, evt_type, evt_value):
        if not self._setText or not self.getShowText():
            return
        modelObj = self.getModelObj()
        if modelObj:
            txt = modelObj.getDisplayName(complete=False)
        else:
            txt = self.getNoneValue()
        self._setText(txt)