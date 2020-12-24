# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/widget/stock/guitextedit.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 2781 bytes
"""
General-purpose :mod:`QTextEdit` widget subclasses.
"""
from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QPlainTextEdit

class QBetseePlainTextEdit(QPlainTextEdit):
    __doc__ = '\n    :mod:`QPlainTextEdit`-based widget optimized for intelligent display of\n    plaintext (rather than rich text or hypertext).\n\n    This application-specific widget augments the stock :class:`QPlainTextEdit`\n    widget with additional support for intelligent text appending, including:\n\n    * **Auto-scrolling,** automatically scrolling this widget to the most\n      recently appended text.\n    * **Thread-safe appending,** permitting different threads other than the\n      thread owning this widget to safely append text to this widget via a\n      preconfigured text appending signal and slot.\n    '

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.append_text_signal.connect(self.append_text)

    append_text_signal = Signal(str)

    @Slot(str)
    def append_text(self, text: str) -> None:
        """
        Append the passed plain text to the text currently displayed by this
        widget and scroll this widget to display that text.

        This slot is connected to the :attr:`append_text_signal` signal at
        widget initialization time, permitting callers in different threads to
        thread-safely append text to this widget.

        Parameters
        ----------
        text : str
            Text to be appended.
        """
        self.appendPlainText(text)
        self.ensureCursorVisible()