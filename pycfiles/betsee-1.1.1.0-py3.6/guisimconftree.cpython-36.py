# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/guisimconftree.py
# Compiled at: 2019-01-16 01:51:29
# Size of source mod 2**32: 6841 bytes
"""
:mod:`PySide2`-based tree widget exposing all high-level features of a
simulation configuration.
"""
from PySide2.QtWidgets import QMainWindow
from betse.util.io.log import logs
from betse.util.type.types import type_check
from betsee.util.widget.stock.guitreewdg import QBetseeTreeWidget

class QBetseeSimConfTreeWidget(QBetseeTreeWidget):
    __doc__ = '\n    :mod:`PySide2`-based tree widget exposing all high-level features of the\n    current simulation configuration.\n\n    This application-specific widget augments the stock :class:`QTreeWidget`\n    with support for handling simulation configurations, including:\n\n    * Auto-axpansion of all tree items by default.\n    * Integration with the corresponding :class:`QStackedWidget`, exposing all\n      low-level configuration settings for the high-level simulation feature\n      currently selected from this tree.\n    '

    @type_check
    def init(self, main_window):
        """
        Initialize this tree widget against the passed parent main window.

        This method is principally intended to perform **post-population
        initialization** (i.e., initialization performed *after* this widget
        has been completely pre-populated with all initial tree items).

        To avoid circular references, this method is guaranteed to *not* retain
        a reference to this main window on returning. References to child
        widgets (e.g., simulation configuration stack widget) of this window
        may be retained, however.

        Parameters
        ----------
        main_window: QBetseeMainWindow
            Initialized application-specific parent :class:`QMainWindow` widget
            against which to initialize this widget.
        """
        super().init()
        logs.log_debug('Initializing top-level tree widget...')
        self._init_widgets(main_window)
        self._init_connections(main_window)

    @type_check
    def _init_widgets(self, main_window: QMainWindow) -> None:
        """
        Create all widgets owned directly by this tree widget *and* initialize
        all other widgets (not necessarily owned by this tree widget) whose
        internal state pertains to the high-level state of this tree widget.

        Parameters
        ----------
        main_window : QBetseeMainWindow
            Initialized application-specific parent :class:`QMainWindow` widget
            against which to initialize this widget.
        """
        items_top_todo = []
        for item_top in self.iter_items_top():
            if items_top_todo or item_top.text(0) == '--[TODO]--':
                items_top_todo.append(item_top)

        for item_top_todo in items_top_todo:
            logs.log_debug('Removing top-level placeholder tree widget item "%s"...', item_top_todo.text(0))
            self.takeTopLevelItem(self.indexOfTopLevelItem(item_top_todo))

        self.expandAll()

    def _init_connections(self, main_window: QMainWindow) -> None:
        """
        Connect all relevant signals and slots of this tree widget and the
        corresponding simulation configuration stack widget.

        Parameters
        ----------
        main_window: QBetseeMainWindow
            Parent :class:`QMainWindow` widget to initialize this widget with.
        """
        self.currentItemChanged.connect(main_window.sim_conf_stack.switch_page_to_tree_item)
        tree_item_first = self.topLevelItem(0)
        self.setCurrentItem(tree_item_first)