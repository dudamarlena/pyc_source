# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/qcrash/qcrash/qt.py
# Compiled at: 2016-12-29 05:40:24
# Size of source mod 2**32: 929 bytes
import logging, sys
_logger = logging.getLogger(__name__)
try:
    from PyQt5 import QtWidgets, QtGui, QtCore
except (ImportError, RuntimeError):
    _logger.warning('failed to import PyQt5, going to try PyQt4')
    try:
        from PyQt4 import QtGui, QtGui as QtWidgets, QtCore
    except (ImportError, RuntimeError):
        _logger.warning('failed to import PyQt4, going to try PySide')
        try:
            from PySide import QtGui, QtCore, QtGui as QtWidgets
        except (ImportError, RuntimeError):
            _logger.warning('failed to import PySide')
            _logger.critical('No Qt bindings found, aborting...')
            try:
                from unittest.mock import MagicMock
                QtCore = MagicMock()
                QtGui = MagicMock()
                QtWidgets = MagicMock()
            except ImportError:
                sys.exit(1)

__all__ = [
 'QtCore', 'QtGui', 'QtWidgets']