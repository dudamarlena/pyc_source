# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/taurusgui/conf/gui_noconf.py
# Compiled at: 2019-08-19 15:09:30
"""An example of usage of TaurusGui in which no configuration file is used
(everything is done programmatically)
This can be launched directly as a stand-alone python script"""
if __name__ == '__main__':
    from taurus.qt.qtgui.application import TaurusApplication
    from taurus.qt.qtgui.taurusgui import TaurusGui
    from taurus.external.qt import Qt
    app = TaurusApplication(app_name='MyGui', cmd_line_parser=None)
    gui = TaurusGui()
    panel = Qt.QWidget()
    gui.createPanel(panel, 'Foo')
    gui.show()
    app.exec_()