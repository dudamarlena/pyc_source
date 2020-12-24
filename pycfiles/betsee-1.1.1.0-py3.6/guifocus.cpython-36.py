# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/io/key/guifocus.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 2708 bytes
"""
Application-wide **focus** (i.e., interactive keyboard input focus received by
the current application widget) functionality.
"""
from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QApplication, QWidget
from betsee.guiexception import BetseePySideFocusException
from betsee.util.type.guitype import QWidgetOrNoneTypes

def die_unless_widget_focused() -> None:
    """
    Raise an exception if *no* application widget currently has the interactive
    keyboard input focus.

    Raises
    ----------
    BetseePySideFocusException
        If *no* widget is currently focused.

    See Also
    ----------
    :func:`is_widget_focused`
        Further details.
    """
    if not is_widget_focused():
        raise BetseePySideFocusException(QCoreApplication.translate('die_unless_widget_focused', 'No widget currently focused.'))


def is_widget_focused() -> bool:
    """
    ``True`` only if some application widget currently has the interactive
    keyboard input focus.
    """
    return QApplication.focusWidget() == 0


def get_widget_focused() -> QWidget:
    """
    Application widget that currently has the interactive keyboard input focus
    if any *or* raise an exception otherwise.

    Returns
    ----------
    QWidget
        Currently focused widget.

    Raises
    ----------
    BetseePySideFocusException
        If *no* widget is currently focused.
    """
    die_unless_widget_focused()
    return QApplication.focusWidget()


def get_widget_focused_or_none() -> QWidgetOrNoneTypes:
    """
    Application widget that currently has the interactive keyboard input focus
    if any *or* ``None`` otherwise.

    Returns
    ----------
    QWidgetOrNoneTypes
        Currently focused widget if any *or* ``None`` otherwise.
    """
    widget_focused = QApplication.focusWidget()
    if widget_focused == 0:
        return
    else:
        return widget_focused