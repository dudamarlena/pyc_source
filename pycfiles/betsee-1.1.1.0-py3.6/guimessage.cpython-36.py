# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/io/guimessage.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 5781 bytes
"""
High-level :mod:`QMessageBox`-based message handling facilities.

See Also
----------
:mod:`betsee.util.io.guierror`
    Error-specific :class:`QMessageBox` facilities.
"""
from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QMessageBox
from betse.util.type.types import type_check, StrOrNoneTypes
from betsee.guiexception import BetseePySideMessageBoxException

def show_query(*args, **kwargs) -> int:
    """
    Display the passed question(s) as a :mod:`QMessageBox`-driven modal message
    box in the current application widget.

    See Also
    ----------
    :func:`show_message`
        Further details.
    """
    return show_message(args, severity=QMessageBox.Question, **kwargs)


def show_info(*args, **kwargs) -> int:
    """
    Display the passed information as a :mod:`QMessageBox`-driven modal message
    box in the current application widget.

    See Also
    ----------
    :func:`show_message`
        Further details.
    """
    return show_message(args, severity=QMessageBox.Information, **kwargs)


def show_warning(*args, **kwargs) -> int:
    """
    Display the passed warning message(s) as a :mod:`QMessageBox`-driven modal
    message box in the current application widget.

    See Also
    ----------
    :func:`show_message`
        Further details.
    """
    return show_message(args, severity=QMessageBox.Warning, **kwargs)


@type_check
def show_message(title: str, synopsis: str, severity: QMessageBox.Icon=QMessageBox.NoIcon, buttons: QMessageBox.StandardButtons=QMessageBox.Ok, button_default: QMessageBox.StandardButton=QMessageBox.Ok, exegesis: StrOrNoneTypes=None, details: StrOrNoneTypes=None) -> int:
    """
    Display the passed warning message(s) as a :mod:`PySide2`-driven modal
    message box in the current application widget.

    Parameters
    ----------
    title : str
        Title of this message box.
    synopsis : str
        Synopsis (i.e., main text) of this of this message box.
    severity: optional[QMessageBox.Icon]
        Integer value of the :class:`QMessageBox.` enumeration member signifying
        the severity of the icon displayed by this message box. Defaults to
        :attr:`QMessageBox.NoIcon`, preventing an icon from being displayed.
    buttons : optional[QMessageBox.StandardButtons]
        Bit flag of the integer values of all OR-ed
        :class:`QMessageBox.StandardButton` enumeration members comprising the
        set of all buttons to be displayed by this message box. Defaults to
        :attr:`QMessageBox.Ok`, the conventional "OK" button.
    button_default : optional[QMessageBox.StandardButton]
        Bit value of the :class:`QMessageBox.StandardButton` enumeration member
        signifying the **default button** (i.e., button initially receiving the
        keyboard focus) displayed by this message box. If the passed ``buttons``
        bit field does *not* enable this bit, an exception is raised. Defaults
        to :attr:`QMessageBox.Ok`, the conventional "OK" button.
    exegesis : optional[str]
        Exegesis (i.e., explanation) of this warning to be displayed as the
        so-called "informative text" of this message box below the synopsis of
        this warning. Defaults to ``None``, in which case no such text is
        displayed.
    details : optional[str]
        Technical details of this warning to be displayed as the so-called
        "detailed text" of this message box in monospaced font below both the
        synopsis and exegesis of this warning in a discrete fold-down text area.
        Defaults to ``None``, in which case no such text is displayed.

    Returns
    ----------
    int
        Bit value of the :class:`QMessageBox.StandardButton` enumeration member
        signifying the button clicked by the user if any.
    """
    if buttons == 0:
        raise BetseePySideMessageBoxException(QCoreApplication.translate('show_message', 'Button bit field empty.'))
    else:
        if button_default & buttons == 0:
            raise BetseePySideMessageBoxException(QCoreApplication.translate('show_message', 'Default button bit "{0}" not enabled by button bit field "{1}".'.format(button_default, buttons)))
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(synopsis)
        message_box.setIcon(severity)
        message_box.setStandardButtons(buttons)
        message_box.setDefaultButton(button_default)
        if exegesis is not None:
            message_box.setInformativeText(exegesis)
        if details is not None:
            message_box.setDetailedText(details)
    message_box.show()
    return message_box.exec_()