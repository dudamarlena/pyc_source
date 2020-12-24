# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/widget/abc/guicontrolabc.py
# Compiled at: 2019-01-16 01:51:30
# Size of source mod 2**32: 2468 bytes
"""
Abstract base classes of all :mod:`PySide2`-based controller subclasses.
"""
from PySide2.QtCore import QObject
from PySide2.QtWidgets import QMainWindow
from betse.util.type.types import type_check
from betsee.util.widget.abc.guiwdgabc import QBetseeObjectMixin

class QBetseeControllerABC(QBetseeObjectMixin, QObject):
    __doc__ = '\n    Abstract base class of all :mod:`PySide2`-based controller subclasses in the\n    standard model-view-controller (MVC) understanding of that term.\n\n    Each instance of this class is a controller encapsulating all abstract state\n    (including connective logic like signals and slots) required to sanely\n    display a separate physical view (i.e., widget). To minimally integrate with\n    Qt concurrency and signalling, this controller is a minimal :class:`QObject`\n    instance rather than a full-fledged :class:`QWidget` instance.\n    '

    @type_check
    def init(self, main_window):
        """
        Initialize this controller against the passed parent main window.

        To avoid circular references, this method is guaranteed to *not* retain
        a reference to this main window on returning. References to child
        widgets (e.g., simulation configuration stack widget) of this window may
        be retained, however.

        Parameters
        ----------
        parent: QBetseeMainWindow
            Initialized application-specific parent :class:`QMainWindow` widget
            against which to initialize this widget.
        """
        super().init()