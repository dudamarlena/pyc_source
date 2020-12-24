# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/core/contexts.py
# Compiled at: 2020-05-03 00:26:03
# Size of source mod 2**32: 491 bytes
"""
Module that contains contexts for Qt
"""
from __future__ import print_function, division, absolute_import
import sys, contextlib
from Qt.QtWidgets import *
import tpDcc

@contextlib.contextmanager
def application():
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
        yield app
        app.exec_()
    else:
        yield app
    if tpDcc.is_standalone():
        app.exec_()