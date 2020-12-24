# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/external/qt/QtUiTools.py
# Compiled at: 2019-08-19 15:09:29
"""This module exposes the QtUiTools module (deprecated in taurus).
It only makes sense when using PySide(2) (which were not supported before
taurus 4.5)
"""
from . import PYSIDE, PYSIDE2, API_NAME
from taurus.core.util import log as __log
__log.deprecated(dep='taurus.external.qt.QtUiTools', rel='4.5', alt='PySide(2).QtUiTools or PyQt(4,5).loadUi')
if PYSIDE2:
    from PySide2.QtUiTools import *
elif PYSIDE:
    from PySide.QtUiTools import *
else:
    raise ImportError(('QtUiTools not supported for {}').format(API_NAME))