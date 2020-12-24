# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/io/guierror.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 13416 bytes
"""
High-level :mod:`QMessageBox`-based error handling facilities.

See Also
----------
:mod:`betsee.util.widget.guimessage`
    Error-agnostic :class:`QMessageBox` facilities.
"""
import re, sys, traceback
from PySide2.QtWidgets import QMessageBox
from betse.util.type.obj import objects
from betsee.util.app import guiapp

def install_exception_hook() -> None:
    """
    Install a global exception hook overriding :mod:`PySide2`'s default insane
    exception handling behaviour with sane exception handling.

    By default, :mod:`PySide2`:

    #. Catches **uncaught exceptions** (i.e., exceptions automatically
       propagated up the call stack without being caught) raised during the
       GUI's event loop processing.
    #. Prints the tracebacks for these exceptions to standard error.
    #. Ignores these exceptions by silently returning control back to the main
       event handling loop.

    This behaviour is entirely invisible to end users and hence insane. This
    function addresses this by installing a new handler both interactively
    displaying *and* non-interactively logging exceptions.

    Caveats
    ----------
    Ideally, this function should be called *before* entering this event loop
    (i.e., calling the :meth:`betsee.util.app.guiapp.GUI_APP._exec` method).
    """
    default_exception_handler = sys.excepthook

    def exception_hook(exception_type, exception, exception_traceback):
        try:
            from betse.util.io.log import logs
            logs.log_exception(exception)
            show_exception(exception)
        except Exception as exception_exception:
            default_exception_handler(type(exception_exception), exception_exception, traceback.extract_stack(exception_exception))
            sys.exit(1)

    sys.excepthook = exception_hook


def show_error(title: str, synopsis: str, exegesis: str=None, details: str=None) -> None:
    """
    Display the passed error message(s) as a :mod:`QMessageBox`-driven modal
    message box of the :class:`QApplication` singleton for this application.

    Caveats
    ----------
    This function necessarily instantiates and initializes this singleton if
    needed. Doing so commonly invites chicken-and-egg issues between the
    :func:`init` and :func:`betse.lib.libs.reinit` methods and hence is
    inadvisable; in this case, however, the need to instantiate this singleton
    to display critical errors subsumes the need to instantiate this singleton
    in a more controlled manner.

    Parameters
    ----------
    title : str
        Title of this error to be displayed as the title of this message box.
    synopsis : str
        Synopsis of this error to be displayed as the text of this message box.
    exegesis : optional[str]
        Exegesis (i.e., explanation) of this error to be displayed as the
        so-called "informative text" of this message box below the synopsis of
        this error. Defaults to ``None``, in which case no such text is
        displayed.
    details : optional[str]
        Technical details of this error to be displayed as the so-called
        "detailed text" of this message box in monospaced font below both the
        synopsis and exegesis of this error in a discrete fold-down text area.
        Defaults to ``None``, in which case no such text is displayed.
    """
    if not isinstance(title, str):
        raise AssertionError('"{}" not a string.'.format(title))
    else:
        assert isinstance(synopsis, str), '"{}" not a string.'.format(synopsis)
        TITLE_MAX_LEN = 80
        SYNOPSIS_MAX_LEN = 640
        EXEGESIS_MAX_LEN = 1280
        DETAILS_MAX_LEN = 2560
        guiapp.init()
        title_truncated = _truncate(text=title, max_len=TITLE_MAX_LEN)
        synopsis_truncated = _truncate(text=synopsis, max_len=SYNOPSIS_MAX_LEN)
        error_box = QMessageBox()
        error_box.setWindowTitle(title_truncated)
        error_box.setText(synopsis_truncated)
        error_box.setIcon(QMessageBox.Critical)
        error_box.setStandardButtons(QMessageBox.Ok)
        if exegesis is not None:
            assert isinstance(exegesis, str), '"{}" not a string.'.format(exegesis)
            exegesis_truncated = _truncate(text=exegesis, max_len=EXEGESIS_MAX_LEN)
            error_box.setInformativeText(exegesis_truncated)
        if details is not None:
            assert isinstance(details, str), '"{}" not a string.'.format(details)
            details_truncated = _truncate(text=details, max_len=DETAILS_MAX_LEN)
            error_box.setDetailedText(details_truncated)
    error_box.show()
    error_box.exec_()


def show_exception(exception: Exception) -> None:
    """
    Display the passed exception as a :mod:`QMessageBox`-driven modal message
    box in the current application widget, creating this widget if necessary.

    Parameters
    ----------
    exception : Exception
        Exception to be displayed.
    """
    if not isinstance(exception, Exception):
        raise AssertionError('"{}" not an exception.'.format(exception))
    else:
        exception_synopsis = getattr(exception, 'synopsis', None)
        exception_exegesis = getattr(exception, 'exegesis', None)
        if exception_synopsis is None:
            exception_synopsis = str(exception)
            if not exception_synopsis:
                exception_synopsis = objects.get_class_name_unqualified(exception)
        if hasattr(exception, 'title'):
            exception_title = exception.title
        else:
            exception_classname = type(exception).__name__
            exception_title = re.sub('([a-z])([A-Z])', '\\1 \\2', exception_classname)
        try:
            from betse.util.io import ioexceptions
            _, exception_traceback = ioexceptions.get_metadata(exception)
        except ImportError:
            exception_traceback = None

    show_error(title=exception_title,
      synopsis=exception_synopsis,
      exegesis=exception_exegesis,
      details=exception_traceback)


def _truncate(text: str, max_len: int) -> str:
    """
    Passed string truncated to the passed maximum length by replacing the
    substring of this string exceeding that length with the conventional ASCII
    ellipses (i.e., ``...``).

    Parameters
    ----------
    text : str
        String to be truncated.
    max_len : int
        Maximum number of characters to truncate this string to.

    Returns
    ----------
    str
        Passed string truncated to this maximum length, as detailed above.

    See Also
    ----------
    :func:`betse.util.type.text.strs.truncate`
        General-purpose truncater from which this error-specific equivalent is
        derived. As the top-level of this submodule suggests, BETSE modules are
        *not* guaranteed to exist at this point. Ergo, this function pastes the
        :func:`betse.util.type.text.strs.truncate` function into this codebase.
    """
    replacement = '...'
    if len(text) <= max_len:
        return text
    else:
        truncate_chars_count = len(text) - max_len + len(replacement)
        if truncate_chars_count > len(text):
            return replacement[:max_len]
        return text[:-truncate_chars_count] + replacement