# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/widget/abc/control/guictlabc.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 2767 bytes
"""
High-level **controller** (i.e., :mod:`PySide2`-based object controlling the
flow of application execution ala the standard model-view-controller (MVC)
paradigm) hierarchy.
"""
from PySide2.QtCore import QObject
from PySide2.QtWidgets import QMainWindow
from betse.util.type.types import type_check
from betsee.util.widget.mixin.guiwdgmixin import QBetseeObjectMixin

class QBetseeControllerABC(QBetseeObjectMixin, QObject):
    __doc__ = '\n    Abstract base class of all **controller** (i.e., :mod:`PySide2`-based\n    object controlling the flow of application execution ala the standard\n    model-view-controller (MVC) paradigm) subclasses.\n\n    Each instance of this class is a controller encapsulating all abstract\n    state (including connective logic like signals and slots) required to\n    sanely display a separate physical view (i.e., widget). For integration\n    with Qt concurrency and signalling, this controller is a minimal\n    :class:`QObject` rather than full-fledged :class:`QWidget` instance.\n    '

    @type_check
    def init(self, main_window, *args, **kwargs):
        """
        Initialize this controller against the passed parent main window.

        To avoid circular references, this method is guaranteed to *not* retain
        a reference to this main window on returning. References to child
        widgets (e.g., simulation configuration stack widget) of this window
        may be retained, however.

        Parameters
        ----------
        main_window : QBetseeMainWindow
            Initialized application-specific parent :class:`QMainWindow` widget
            against which to initialize this controller.

        All remaining parameters are passed as is to the
        :meth:`QBetseeObjectMixin.init` method.
        """
        (super().init)(*args, **kwargs)