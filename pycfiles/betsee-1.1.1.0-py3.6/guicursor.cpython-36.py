# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/io/mouse/guicursor.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 1593 bytes
"""
High-level :mod:`PySide2`-based mouse cursor facilities.
"""
from PySide2.QtCore import Qt
from PySide2.QtGui import QApplication
from betse.util.type.types import GeneratorType
from contextlib import contextmanager

@contextmanager
def waiting_cursor() -> GeneratorType:
    """
    Context manager changing the mouse cursor to the prototypical wait cursor
    (e.g., animated hourglass) for the duration of this context.

    This context manager guaranteeably reverts the cursor to the prior cursor
    even when fatal exceptions are raised (e.g., by the caller's block).

    Returns
    -----------
    contextlib._GeneratorContextManager
        Context manager changing the cursor as described above.

    Yields
    -----------
    None
        Since this context manager yields no values, the caller's ``with``
        statement must be suffixed by *no* ``as`` clause.
    """
    try:
        QApplication.setOverrideCursor(Qt.WaitCursor)
        yield
    finally:
        QApplication.restoreOverrideCursor()