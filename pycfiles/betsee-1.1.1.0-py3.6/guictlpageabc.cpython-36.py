# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/widget/abc/control/guictlpageabc.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 7724 bytes
"""
High-level **stacked widget pager** (i.e., controller controlling the flow of
application execution for a single page of a :mod:`QStackedWidget`) hierarchy.
"""
from PySide2.QtWidgets import QMainWindow
from betse.exceptions import BetseMethodUnimplementedException
from betse.util.type.types import type_check
from betsee.util.widget.abc.control.guictlabc import QBetseeControllerABC

class QBetseePagerItemizedMixin(object):
    __doc__ = '\n    Mixin of all **itemized stacked widget pager** (i.e., controller\n    controlling the flow of application execution for a single page of a\n    stacked widget associated with zero or more tree items of a tree widget\n    masquerading as list items dynamically defined at runtime) subclasses.\n\n    This class is suitable for use as a multiple-inheritance mixin. To preserve\n    the expected method resolution order (MRO) semantics, this class should\n    typically be inherited *first* rather than *last* in subclasses.\n\n    See Also\n    ----------\n    :class:`QBetseePagerItemizedABC`\n        Abstract base class conveniently mixing this mixin with the lower-level\n        abstract base :class:`QBetseePagerABC` class. Where\n        feasible, subclasses should typically inherit from this higher-level\n        superclass rather than this lower-level mixin.\n    '

    @type_check
    def reinit(self, main_window, list_item_index):
        """
        Reassociate this itemized pager with the **dynamic list item** (i.e.,
        tree item of a :mod:`QTreeWidget` masquerading as a list item
        dynamically defined at runtime) with the passed index against the
        passed parent main window.

        This method is typically called by the parent object owning this pager
        (e.g., :mod:`QStackedWidget`) from a slot signalled immediately
        *before* the page controlled by this pager is switched to, ensuring
        that page to be prepopulated *before* being displayed.

        To avoid circular references, this method is guaranteed to *not* retain
        a reference to this main window on returning. References to child
        widgets (e.g., simulation configuration stack widget) of this window
        may be retained, however.

        Caveats
        ----------
        **Subclasses are required to reimplement this method.** The subclass
        implementation typically synchronizes all editable widgets on the
        stacked widget page controlled by this pager with their current values
        in the underlying model (e.g., current simulation configuration).

        Parameters
        ----------
        main_window : QBetseeMainWindow
            Initialized application-specific parent :class:`QMainWindow` widget
            against which to initialize this controller.
        list_item_index: int
            0-based index of the list item to reassociate this pager with.
        """
        super().reinit(main_window=main_window,
          list_item_index=list_item_index)

    def deinit(self) -> None:
        """
        Deassociate this pager from the **dynamic list item** (i.e., tree item
        of a :mod:`QTreeWidget` masquerading as a list item dynamically defined
        at runtime) previously associated with this pager by the most recent
        call to the :meth:`reinit` method.

        This method is typically called by the parent object owning this pager
        (e.g., :mod:`QStackedWidget`) from a slot signalled immediately
        *after* the dynamic list item previously associated with this pager is
        removed, ensuring the page controlled by this pager to be depopulated
        *before* being subsequently displayed.

        Design
        ----------
        Subclasses are required to redefine this pseudo-abstract method
        *without* calling this superclass implementation, which unconditionally
        raises an exception to enforce such redefinition.

        Subclasses typically implement this method by desynchronizing all
        editable widgets on the stacked widget page controlled by this pager
        from any previous values in the underlying data model (e.g., the
        currently open simulation configuration).
        """
        raise BetseMethodUnimplementedException()


class QBetseePagerABC(QBetseeControllerABC):
    __doc__ = '\n    Abstract base class of all **stacked widget pager** (i.e., controller\n    controlling the flow of application execution for a single page of a\n    :mod:`QStackedWidget`) subclasses.\n    '


class QBetseePagerItemizedABC(QBetseePagerItemizedMixin, QBetseePagerABC):
    __doc__ = '\n    Abstract base class of all **itemized stacked widget pager** (i.e.,\n    controller controlling the flow of application execution for a single page\n    of a stacked widget associated with zero or more tree items of a tree\n    widget masquerading as list items dynamically defined at runtime)\n    subclasses.\n    '