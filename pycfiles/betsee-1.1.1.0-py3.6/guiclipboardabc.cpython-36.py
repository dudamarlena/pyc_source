# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/widget/abc/guiclipboardabc.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 5259 bytes
"""
Abstract base classes of all **clipboardable widget** (i.e., widget
transparently supporting copying, cutting, and pasting into and from the
platform-specific system clipboard) subclasses.
"""
from PySide2.QtCore import Qt, QEvent
from PySide2.QtGui import QKeyEvent
from PySide2.QtWidgets import QApplication
from betse.exceptions import BetseMethodUnimplementedException
from betse.util.type.obj import objtest

class QBetseeClipboardWidgetMixin(object):
    __doc__ = "\n    Abstract base class of all **clipboardable widget** (i.e., widget\n    transparently supporting copying, cutting, and pasting into and from the\n    platform-specific system clipboard) subclasses.\n\n    Most subclasses of this class support only plaintext and hence integrate\n    only with the clipboard's plaintext buffer.\n\n    Design\n    ----------\n    This class is suitable for use as a multiple-inheritance mixin. To preserve\n    the expected method resolution order (MRO) semantics, this class should\n    typically be subclassed *first* rather than *last* in subclasses.\n    "

    def copy_selection_to_clipboard(self) -> None:
        """
        Copy this widget's **current selection** (i.e., currently selected
        subset of this widget's value(s)) to the system clipboard, silently
        replacing the prior contents if any.
        """
        raise BetseMethodUnimplementedException()

    def cut_selection_to_clipboard(self) -> None:
        """
        **Cut** (i.e., copy and then remove as a single atomic operation) the
        this widget's **current selection** (i.e., currently selected subset of
        this widget's value(s)) to the system clipboard, silently replacing the
        prior contents if any.
        """
        raise BetseMethodUnimplementedException()

    def paste_clipboard_to_selection(self) -> None:
        """
        Paste the contents of the system clipboard over this widget's **current
        selection** (i.e., currently selected subset of this widget's
        value(s)), silently replacing the prior selection if any.
        """
        raise BetseMethodUnimplementedException()


class QBetseeClipboardScalarWidgetMixin(QBetseeClipboardWidgetMixin):
    __doc__ = '\n    Abstract base class of all **scalar clipboardable widget** (i.e., scalar\n    :mod:`PySide2` widget transparently supporting copying, cutting, and\n    pasting into and from the platform-specific system clipboard) subclasses.\n\n    In this context, the term "scalar" encompasses all widget subclasses whose\n    contents reduce to a single displayed value (e.g., integer, floating point\n    number, string).\n\n    Design\n    ----------\n    All subclasses must support either (in order of descending preference):\n\n    #. Explicit clipboard integration via the ``copy``, ``cut``, or ``paste``\n       methods, typically supported by textual scalar widgets (e.g.,\n       :class:`QLineEdit`).\n    #. Implicit clipboard integration via the analogous Ctrl-c, Ctrl-x, and\n       Ctrl-v keyboard shortcus, typically supported by numeric scalar widgets\n       (e.g., :class:`QSpinBox`).\n\n    If the current subclass does *not* define the ``copy``, ``cut``, and\n    ``paste`` methods, this base class assumes this subclass to support the\n    standard clipboard keyboard shortcuts instead. If this subclass supports\n    neither, this base class silently reduces to a noop.\n    '

    def copy_selection_to_clipboard(self) -> None:
        if objtest.has_method(self, 'copy'):
            self.copy()
        else:
            QApplication.postEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_C, Qt.ControlModifier))

    def cut_selection_to_clipboard(self) -> None:
        if objtest.has_method(self, 'cut'):
            self.cut()
        else:
            QApplication.postEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_X, Qt.ControlModifier))

    def paste_clipboard_to_selection(self) -> None:
        if objtest.has_method(self, 'paste'):
            self.paste()
        else:
            QApplication.postEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_V, Qt.ControlModifier))