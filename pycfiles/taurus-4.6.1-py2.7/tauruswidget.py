# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/container/tauruswidget.py
# Compiled at: 2019-08-19 15:09:29
"""This module provides basic taurus container widget"""
from __future__ import absolute_import
from taurus.external.qt import Qt
from .taurusbasecontainer import TaurusBaseContainer
__all__ = [
 'TaurusWidget']
__docformat__ = 'restructuredtext'

class TaurusWidget(Qt.QWidget, TaurusBaseContainer):
    """This is a Qt.QWidget that additionally accepts a model property.
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

    def __init__(self, parent=None, designMode=False):
        name = self.__class__.__name__
        self.call__init__wo_kw(Qt.QWidget, parent)
        self.call__init__(TaurusBaseContainer, name, designMode=designMode)

    @classmethod
    def getQtDesignerPluginInfo(cls):
        ret = TaurusBaseContainer.getQtDesignerPluginInfo()
        if cls is TaurusWidget:
            ret['module'] = 'taurus.qt.qtgui.container'
            ret['group'] = 'Taurus Containers'
            ret['icon'] = 'designer:frame.png'
            ret['container'] = True
        return ret

    @Qt.pyqtSlot()
    def applyPendingChanges(self):
        self.applyPendingOperations()

    @Qt.pyqtSlot()
    def resetPendingChanges(self):
        self.resetPendingOperations()

    model = Qt.pyqtProperty('QString', TaurusBaseContainer.getModel, TaurusBaseContainer.setModel, TaurusBaseContainer.resetModel)
    useParentModel = Qt.pyqtProperty('bool', TaurusBaseContainer.getUseParentModel, TaurusBaseContainer.setUseParentModel, TaurusBaseContainer.resetUseParentModel)
    showQuality = Qt.pyqtProperty('bool', TaurusBaseContainer.getShowQuality, TaurusBaseContainer.setShowQuality, TaurusBaseContainer.resetShowQuality)
    modifiableByUser = Qt.pyqtProperty('bool', TaurusBaseContainer.isModifiableByUser, TaurusBaseContainer.setModifiableByUser, TaurusBaseContainer.resetModifiableByUser)