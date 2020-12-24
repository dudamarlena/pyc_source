# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/external/qt/Qwt5.py
# Compiled at: 2019-08-19 15:09:29
"""This module exposes Qwt5 module"""
from . import PYQT4, API_NAME
from taurus.core.util import log as __log
if PYQT4:
    __log.deprecated(dep='taurus.external.qt.Qwt5', rel='4.5')
    from PyQt4.Qwt5 import *
else:
    raise ImportError(('Qwt5 bindings not supported for {}').format(API_NAME))