# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/display/demo/taurusleddemo.py
# Compiled at: 2019-08-19 15:09:29
"""This module provides a demo for the :class:`taurus.qt.qtgui.display.TaurusLabel`
widget """
__all__ = [
 'demo', 'main']
__docformat__ = 'restructuredtext'
from taurus.external.qt import Qt

def demo():
    import sys, taurus.qt.qtgui.application, taurus.qt.qtgui.display
    Application = taurus.qt.qtgui.application.TaurusApplication
    TaurusLed = taurus.qt.qtgui.display.TaurusLed
    app = Application.instance()
    owns_app = app is None
    if owns_app:
        app = Application()
    M = 2

    class TaurusLedTestPanel(Qt.QWidget):

        def __init__(self, parent=None):
            Qt.QWidget.__init__(self, parent)
            panel_l = Qt.QVBoxLayout()
            self.setLayout(panel_l)
            panel_l.setContentsMargins(M, M, M, M)
            panel_l.setSpacing(M)
            w = TaurusLed()
            display_panel = Qt.QGroupBox('Taurus Led Display')
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
            inverted_widget = Qt.QCheckBox()
            model_widget = Qt.QLineEdit()
            model_index_widget = Qt.QLineEdit()
            fg_widget = Qt.QComboBox()
            on_color_widget = Qt.QComboBox()
            off_color_widget = Qt.QComboBox()
            control_l.addRow('inverted:', inverted_widget)
            control_l.addRow('model:', model_widget)
            control_l.addRow('model index:', model_index_widget)
            control_l.addRow('foreground role:', fg_widget)
            control_l.addRow('ON color:', on_color_widget)
            control_l.addRow('OFF color:', off_color_widget)
            panel_l.addWidget(display_panel, 1)
            panel_l.addWidget(control_panel, 0)
            fg_widget.addItems(['rvalue', 'wvalue', 'quality'])
            colors = ['green', 'blue', 'orange', 'red',
             'yellow', 'magenta', 'grenoble', 'black']
            on_color_widget.addItems(colors)
            off_color_widget.addItems(colors)
            inverted_widget.toggled.connect(w.setLedInverted)
            model_widget.textChanged.connect(w.setModel)
            fg_widget.currentIndexChanged['QString'].connect(w.setFgRole)
            model_index_widget.textChanged.connect(w.setModelIndex)
            on_color_widget.currentIndexChanged['QString'].connect(w.setOnColor)
            off_color_widget.currentIndexChanged['QString'].connect(w.setOffColor)
            inverted_widget.setChecked(False)
            model_widget.setText('sys/tg_test/1/state')
            fg_widget.setCurrentIndex(0)
            on_color_widget.setCurrentIndex(0)
            off_color_widget.setCurrentIndex(7)
            self.w_led = w
            self.w_model = model_widget
            self.w_fg = fg_widget
            self.w_model_index = model_index_widget
            self.w_on_color = on_color_widget
            self.w_off_color = off_color_widget

    panel = Qt.QWidget()
    layout = Qt.QGridLayout()
    panel.setLayout(layout)
    layout.setContentsMargins(M, M, M, M)
    layout.setSpacing(M)
    p1 = TaurusLedTestPanel()
    p1.w_model.setText('sys/tg_test/1/state')
    p2 = TaurusLedTestPanel()
    p2.w_model.setText('sys/tg_test/1/boolean_scalar')
    p3 = TaurusLedTestPanel()
    p3.w_model.setText('sys/tg_test/1/boolean_spectrum')
    p3.w_model_index.setText('4')
    layout.addWidget(p1, 0, 0)
    layout.addWidget(p2, 0, 1)
    layout.addWidget(p3, 0, 2)
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