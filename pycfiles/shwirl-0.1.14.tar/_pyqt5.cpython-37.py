# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/app/backends/_pyqt5.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 1582 bytes
""" PyQt5 proxy backend for the qt backend. 
"""
import sys
from .. import backends
from ...util import logger
from ... import config
USE_EGL = config['gl_backend'].lower().startswith('es')
try:
    for lib in ('PySide', 'PyQt4'):
        lib += '.QtCore'
        if lib in sys.modules:
            raise RuntimeError('Refusing to import PyQt5 because %s is already imported.' % lib)

    if not USE_EGL:
        from PyQt5 import QtOpenGL
    from PyQt5 import QtGui, QtCore
except Exception as exp:
    try:
        available, testable, why_not, which = (
         False, False, str(exp), None)
    finally:
        exp = None
        del exp

else:
    available, testable, why_not = (True, True, None)
    has_uic = True
    which = ('PyQt5', QtCore.PYQT_VERSION_STR, QtCore.QT_VERSION_STR)
    sys.modules.pop(__name__.replace('_pyqt5', '_qt'), None)
    if backends.qt_lib is None:
        backends.qt_lib = 'pyqt5'
        from . import _qt
        from ._qt import *
    else:
        logger.info('%s already imported, cannot switch to %s' % (
         backends.qt_lib, 'pyqt5'))