# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/display/demo/tauruslcddemo.py
# Compiled at: 2019-08-19 15:09:29
"""This module provides a demo for the :class:`~taurus.qt.qtgui.display.TaurusLCD`
widget """
__all__ = [
 'demo', 'main']
__docformat__ = 'restructuredtext'
from taurus.external.qt import Qt

def demo():
    import sys, taurus.qt.qtgui.application, taurus.qt.qtgui.display
    Application = taurus.qt.qtgui.application.TaurusApplication
    TaurusLCD = taurus.qt.qtgui.display.TaurusLCD
    app = Application.instance()
    owns_app = app is None
    if owns_app:
        app = Application()
    M = 2

    class TaurusLCDTestPanel(Qt.QWidget):

        def __init__(self, parent=None):
            Qt.QWidget.__init__(self, parent)
            panel_l = Qt.QVBoxLayout()
            self.setLayout(panel_l)
            panel_l.setContentsMargins(M, M, M, M)
            panel_l.setSpacing(M)
            w = TaurusLCD()
            display_panel = Qt.QGroupBox('Taurus LCD Display')
            display_l = Qt.QHBoxLayout()
            display_l.setContentsMargins(M, M, M, M)
            display_l.setSpacing(M)
            display_panel.setLayout(display_l)
            display_l.addWidget(w, 1)
            control_panel = Qt.QGroupBox('Control Panel')
            control_l = Qt.QFormLayout()
            control_l.setContentsMargins(M, M, M, M)
            control_l.setSpacing(M)
            control_panel.setLayout(control_l)
            model_widget = Qt.QLineEdit()
            model_index_widget = Qt.QLineEdit()
            fg_widget = Qt.QComboBox()
            bg_widget = Qt.QComboBox()
            control_l.addRow('model:', model_widget)
            control_l.addRow('model index:', model_index_widget)
            control_l.addRow('foreground role:', fg_widget)
            control_l.addRow('background role:', bg_widget)
            panel_l.addWidget(display_panel)
            panel_l.addWidget(control_panel)
            fg_widget.addItems(['value', 'w_value', 'none'])
            bg_widget.addItems(['quality', 'state', 'none'])
            model_widget.textChanged.connect(w.setModel)
            model_index_widget.textChanged.connect(w.setModelIndex)
            fg_widget.currentIndexChanged['QString'].connect(w.setFgRole)
            bg_widget.currentIndexChanged['QString'].connect(w.setBgRole)
            model_widget.setText('sys/tg_test/1/double_scalar')
            fg_widget.setCurrentIndex(0)
            bg_widget.setCurrentIndex(0)
            self.w_label = w
            self.w_model = model_widget
            self.w_model_index = model_index_widget
            self.w_fg = fg_widget
            self.w_bg = bg_widget

    panel = Qt.QWidget()
    layout = Qt.QGridLayout()
    panel.setLayout(layout)
    layout.setContentsMargins(M, M, M, M)
    layout.setSpacing(M)
    p1 = TaurusLCDTestPanel()
    p1.w_model.setText('sys/tg_test/1/double_scalar')
    p2 = TaurusLCDTestPanel()
    p2.w_model.setText('sys/tg_test/1/double_scalar#min_value')
    p2.w_bg.setCurrentIndex(2)
    layout.addWidget(p1, 0, 0)
    layout.addWidget(p2, 0, 1)
    layout.setRowStretch(0, 1)
    panel.show()
    if owns_app:
        sys.exit(app.exec_())
    else:
        return panel
    return


def main():
    return demo()


if __name__ == '__main__':
    main()