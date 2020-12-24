# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/gui/qt/stylesheet_patcher.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 706 bytes
"""This is used to patch the QApplication style sheet.
It reads the current stylesheet, appends our modifications and sets the new stylesheet.
"""
from PyQt5 import QtWidgets

def patch_qt_stylesheet(use_dark_theme: bool) -> None:
    if not use_dark_theme:
        return
    app = QtWidgets.QApplication.instance()
    style_sheet = app.styleSheet()
    style_sheet = style_sheet + '\n    /* PayToEdit text was being clipped */\n    QAbstractScrollArea {\n        padding: 0px;\n    }\n    /* In History tab, labels while edited were being clipped (Windows) */\n    QAbstractItemView QLineEdit {\n        padding: 0px;\n        show-decoration-selected: 1;\n    }\n    '
    app.setStyleSheet(style_sheet)