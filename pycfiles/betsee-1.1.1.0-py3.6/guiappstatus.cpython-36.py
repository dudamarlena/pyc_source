# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/app/guiappstatus.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 3761 bytes
"""
Application **status bar** (i.e., :class:`QStatusBar` widget synopsizing
application status in the :class:`QMainWindow` singleton for this application)
facilities.
"""
from PySide2.QtWidgets import QStatusBar
from betse.util.type.types import type_check

def get_status_bar() -> QStatusBar:
    """
    Singleton status bar widget for this application.

    Specifically, this function returns either:

    * If this main window defines an instance variable named ``status_bar``,
      the value of this variable.
    * Else, the value returned by the :meth:`QMainWindow.statusBar` method.
      Since this method is `considered problematic`_ by some in the Qt
      development community, this method is *only* called as a fallback.

    .. _considered problematic:
       https://plashless.wordpress.com/2013/09/14/qt-qmainwindow-statusbar-dont-use-it

    Design
    ----------
    To avoid circular import dependencies, this getter intentionally resides in
    this submodule known *not* to be subject to these dependencies rather than
    in an arguably more germain submodule known to be subject to these
    dependencies (e.g., :mod:`betsee.gui.window.guiwindow`).

    Returns
    ----------
    QStatusBar
        This widget.

    Raises
    ----------
    BetseePySideWindowException
        If the main window widget for this application is uninstantiated.
    """
    from betsee.util.app import guiappwindow
    main_window = guiappwindow.get_main_window()
    status_bar = getattr(main_window, 'status_bar', None)
    if status_bar is None:
        status_bar = main_window.statusBar()
    return status_bar


@type_check
def show_status(text: str) -> None:
    """
    Display the passed string as a **temporary message** (i.e., string
    temporarily replacing any normal message currently displayed) in the
    status bar.
    """
    status_bar = get_status_bar()
    status_bar.showMessage(text)


def clear_status() -> None:
    """
    Remove the temporary message currently displayed in the status bar if any
    *or* reduce to a noop otherwise.

    This function restores any "permanent" message displayed in the status bar
    (if any) prior to the recent temporary message displayed in the status bar
    (if any) by calls to the :func:`show_status` function. (It's complicated.)
    """
    status_bar = get_status_bar()
    status_bar.clearMessage()