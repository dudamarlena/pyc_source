# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/app/guiappwindow.py
# Compiled at: 2019-08-22 00:51:38
# Size of source mod 2**32: 4497 bytes
"""
Submodule providing general-purpose access to the :class:`QMainWindow`
singleton for this application.
"""
from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QMainWindow
from betse.util.io.log import logs
from betse.util.type.types import type_check
from betsee.guiexception import BetseePySideWindowException
_MAIN_WINDOW = None

def get_main_window() -> QMainWindow:
    """
    Singleton main window widget for this application if already instantiated
    by the :class:`betsee.gui.guimain.BetseeGUI` class *or* raise an exception
    otherwise (i.e., if this widget is uninstantiated).

    Design
    ----------
    To avoid circular import dependencies, this getter intentionally resides in
    this submodule known *not* to be subject to these dependencies rather than
    in an arguably more germane submodule known to be subject to these
    dependencies (e.g., :mod:`betsee.gui.window.guiwindow`).

    Returns
    ----------
    QMainWindow
        This widget.

    Raises
    ----------
    BetseePySideWindowException
        If this widget has yet to be instantiated (i.e., if the
        :func:`set_main_window` function has yet to be called).
    """
    global _MAIN_WINDOW
    if _MAIN_WINDOW is None:
        raise BetseePySideWindowException(QCoreApplication.translate('guiappwindow', 'Main window singleton widget uninstantiated.'))
    return _MAIN_WINDOW


@type_check
def set_main_window(main_window: QMainWindow) -> None:
    """
    Set the main window singleton widget for this application.

    Parameters
    ----------
    main_window : QMainWindow
        Main window widget to set as this application's singleton.

    Raises
    ----------
    BetseePySideWindowException
        If this widget has already been instantiated (i.e., if the
        :class:`QApplication` singleton already defines the
        application-specific ``betsee_main_window`` attribute).
    """
    global _MAIN_WINDOW
    logs.log_debug('Preserving main window...')
    if _MAIN_WINDOW is not None:
        raise BetseePySideWindowException(QCoreApplication.translate('guiappwindow', 'Main window singleton widget already instantiated.'))
    _MAIN_WINDOW = main_window


@type_check
def unset_main_window() -> None:
    """
    Unset the main window singleton widget for this application.

    Caveats
    ----------
    **No Qt-specific logic may be performed after calling this method.** This
    method nullifies and hence schedules this singleton for garbage collection.
    Since this singleton ideally contains the only references (both direct and
    transitive) to every live Qt object, scheduling this singleton for garbage
    collection effectively schedules *each* live Qt object for similar garbage
    collection. This function is intended to be called only on application
    destruction as a safety measure to avoid garbage collection issues.
    """
    global _MAIN_WINDOW
    _MAIN_WINDOW = None