# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/taurusgui/conf/gui_pureconf.py
# Compiled at: 2019-08-19 15:09:30
"""An example of usage of TaurusGui in which the current file is a pure
declarative configuration file that should be interpreted by the tarusgui
script by running `taurusgui gui_pureconf` (if gui_pureconf.py is in the
PYTHONPATH) or `taurusgui <full_path_to_gui_pureconf.py>` (if it is not
in the PYTHONPATH)"""
from taurus.qt.qtgui.taurusgui.utils import PanelDescription
GUI_NAME = 'MyGui'
panel = PanelDescription('Foo', classname='taurus.external.qt.Qt.QWidget')