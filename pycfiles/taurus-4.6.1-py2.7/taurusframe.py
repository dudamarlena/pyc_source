# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/container/taurusframe.py
# Compiled at: 2019-08-19 15:09:29
"""This module provides basic taurus container widgets"""
from __future__ import absolute_import
from taurus.external.qt import Qt
from .taurusbasecontainer import TaurusBaseContainer
__all__ = [
 'TaurusFrame']
__docformat__ = 'restructuredtext'

class TaurusFrame(Qt.QFrame, TaurusBaseContainer):
    """This is a Qt.QFrame that additionally accepts a model property.
    This type of taurus container classes are specially useful if you define
    a parent taurus model to them and set all contained taurus widgets to use parent
    model. Example::

        from taurus.qt.qtgui.container import *
        from taurus.qt.qtgui.display import *

        widget = TaurusFrame()
        layout = Qt.QVBoxLayout()
        widget.setLayout(layout)
        widget.model = 'sys/database/2'
        stateWidget = TaurusLabel()
        layout.addWidget(stateWidget)
        stateWidget.model = 'sys/database/2/state'
        """
    modelChanged = Qt.pyqtSignal('const QString &')

    def __init__(self, parent=None, designMode=False):
        name = self.__class__.__name__
        self.call__init__wo_kw(Qt.QFrame, parent)
        self.call__init__(TaurusBaseContainer, name, designMode=designMode)

    @Qt.pyqtSlot()
    def applyPendingChanges(self):
        self.applyPendingOperations()

    @Qt.pyqtSlot()
    def resetPendingChanges(self):
        self.resetPendingOperations()

    @classmethod
    def getQtDesignerPluginInfo(cls):
        ret = TaurusBaseContainer.getQtDesignerPluginInfo()
        if cls is TaurusFrame:
            ret['module'] = 'taurus.qt.qtgui.container'
            ret['group'] = 'Taurus Containers'
            ret['icon'] = 'designer:frame.png'
            ret['container'] = True
        return ret

    model = Qt.pyqtProperty('QString', TaurusBaseContainer.getModel, TaurusBaseContainer.setModel, TaurusBaseContainer.resetModel)
    useParentModel = Qt.pyqtProperty('bool', TaurusBaseContainer.getUseParentModel, TaurusBaseContainer.setUseParentModel, TaurusBaseContainer.resetUseParentModel)
    showQuality = Qt.pyqtProperty('bool', TaurusBaseContainer.getShowQuality, TaurusBaseContainer.setShowQuality, TaurusBaseContainer.resetShowQuality)


def demo():
    """Frame"""
    w = Qt.QWidget()
    w.setWindowTitle(Qt.QApplication.instance().applicationName())
    layout = Qt.QGridLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    w.setLayout(layout)
    frame = TaurusFrame()
    frame.model = 'sys/tg_test/1'
    layout.addWidget(frame)
    layout = Qt.QFormLayout()
    frame.setLayout(layout)
    import taurus.qt.qtgui.display
    state_led = taurus.qt.qtgui.display.TaurusLed()
    state_led.model = frame.model + '/state'
    status_label = taurus.qt.qtgui.display.TaurusLabel()
    status_label.model = frame.model + '/status'
    double_scalar_label = taurus.qt.qtgui.display.TaurusLabel()
    double_scalar_label.model = frame.model + '/double_scalar'
    layout.addRow('State:', state_led)
    layout.addRow('Status:', status_label)
    layout.addRow('Double scalar:', double_scalar_label)
    w.show()
    return w


def main():
    import sys, taurus.qt.qtgui.application
    Application = taurus.qt.qtgui.application.TaurusApplication
    app = Application.instance()
    owns_app = app is None
    if owns_app:
        import taurus.core.util.argparse
        parser = taurus.core.util.argparse.get_taurus_parser()
        parser.usage = '%prog [options] <full_device_name(s)>'
        app = Application(sys.argv, cmd_line_parser=parser, app_name='Taurus frame demo', app_version='1.0', org_domain='Taurus', org_name='Tango community')
    args = app.get_command_line_args()
    if len(args) == 0:
        w = demo()
    else:
        models = map(str.lower, args)
        w = Qt.QWidget()
        w.setWindowTitle(app.applicationName())
        layout = Qt.QGridLayout()
        w.setLayout(layout)
        for model in models:
            frame = TaurusFrame()
            frame.model = model
            layout.addWidget(frame)

    w.show()
    if owns_app:
        sys.exit(app.exec_())
    else:
        return w
    return


if __name__ == '__main__':
    main()