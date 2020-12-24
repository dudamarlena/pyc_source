# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/guisimconfstack.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 19641 bytes
"""
High-level **stacked simulation configuration** (i.e., partitioning of the
simulation configuration into multiple pages, each displaying and editing all
settings associated with a single simulation feature  of the current such
configuration) facilities.
"""
from PySide2.QtCore import QCoreApplication, Slot
from PySide2.QtWidgets import QMainWindow, QStackedWidget, QTreeWidgetItem
from betse.util.io.log import logs
from betse.util.type.iterable.mapping import mappings
from betse.util.type.obj import objects, objtest
from betse.util.type.types import type_check, MappingType
from betsee.guiexception import BetseePySideStackedWidgetException
from betsee.util.app import guiappwindow
from betsee.util.widget.mixin.guiwdgmixin import QBetseeObjectMixin
from betsee.util.widget.abc.control.guictlpageabc import QBetseePagerItemizedMixin
from betsee.util.widget.stock.tree import guitreeitem

class QBetseeSimConfStackedWidget(QBetseeObjectMixin, QStackedWidget):
    __doc__ = "\n    :mod:`PySide2`-based stack widget containing multiple pages, each\n    displaying and editing all settings associated with a single simulation\n    feature (e.g., ions, plots, tissue) of the current simulation\n    configuration.\n\n    This application-specific widget augments the stock :class:`QStackedWidget`\n    with support for handling simulation configurations, including:\n\n    * Integration with the corresponding :class:`QTreeWidget`, exposing all\n      low-level configuration settings for the high-level simulation feature\n      currently selected from this tree.\n\n    Caveats\n    ----------\n    The name of each child page widget of this stack widget must be prefixed by\n    a prefix uniquely identifying that widget to be a child page widget of this\n    stack widget *and* the name of the parent page widget of that child if any.\n    Spepcifically:\n\n    * If this child page widget is top-level (i.e., has no parent), that\n      widget's name must be prefixed by the\n      :attr:`SIM_CONF_STACK_PAGE_NAME_PREFIX` substring.\n    * If this child page widget is *not* top-level (i.e., has a parent), that\n      widget's name must be prefixed by the name of that parent page widget\n      followed by a delimiting underscore.\n\n    As a corrolary, this implies that the names of all page widgets regardless\n    of hierarchical nesting are all prefixed by at least the same\n    :attr:`SIM_CONF_STACK_PAGE_NAME_PREFIX` substring. No other widgets should\n    have such names. Failure to comply may be met with an unutterable anguish.\n\n    Attributes\n    ----------\n    _sim_conf : QBetseeSimConf\n        High-level object controlling simulation configuration state.\n\n    Attributes (Container)\n    ----------\n    _pagers : tuple\n        Container of all high-level objects controlling the state of each stack\n        widget page, preserved to prevent Python from erroneously garbage\n        collecting these objects. Since these objects are *not* explicitly\n        accessed after instantiation, this simplistic scheme suffices.\n\n    Attributes (Container: Dictionary)\n    ----------\n    _stack_page_name_to_page : dict\n        Dictionary mapping from the object name of each page widget of this\n        stack widget to that widget.\n    _stack_page_name_to_pager : dict\n        Dictionary mapping from the object name of each page widget of this\n        stack widget to the **pager** (i.e., high-level object controlling the\n        flow of application execution for a page widget) controlling that\n        widget. This dictionary also serves as the principal **pager\n        container** (i.e., container of all pager objects, preventing Python\n        from erroneously garbage collecting these objects).\n    _tree_item_static_to_stack_page : dict\n        Dictionary mapping from each **static tree item** (i.e., item\n        statically defined via Qt (Creator|Designer) rather than dynamically\n        defined at application runtime) of the :class:`QTreeWidget` associated\n        with this stack widget to the corresponding child page widget of this\n        stack widget.\n    _tree_item_list_root_to_stack_page_list_leaf : dict\n        Dictionary mapping from each **dynamic list tree item** (i.e., item\n        masquerading as a list dynamically defined at application runtime\n        rather than statically defined via Qt (Creator|Designer)) of the\n        :class:`QTreeWidget` associated with this stack widget to the\n        corresponding **itemized page widget** (i.e., page configuring these\n        tree items) of this stack widget.\n\n    See Also\n    ----------\n    :class:`QBetseeSimConfTreeWidget`\n        Corresponding :class:`QTreeWidget` instance, exposing all high-level\n        features of the current simulation configuration which this\n        :class:`QStackedWidget` instance then exposes the settings of.\n    "

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._sim_conf = None
        self._stack_page_name_to_page = None
        self._stack_page_name_to_pager = None
        self._tree_item_static_to_stack_page = None
        self._tree_item_list_root_to_stack_page_list_leaf = None

    @type_check
    def init(self, main_window):
        """
        Initialize this stacked widget against the passed parent main window.

        This method is principally intended to perform **post-population
        initialization** (i.e., initialization performed *after* the main
        window has been fully pre-populated with all initial child widgets).

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
        from betsee.gui.simconf.stack.page.guisimconfpagepath import QBetseeSimConfPagerPath
        from betsee.gui.simconf.stack.page.guisimconfpagetime import QBetseeSimConfPagerTime
        from betsee.gui.simconf.stack.page.export.guisimconfpageexport import QBetseeSimConfPagerExport
        from betsee.gui.simconf.stack.page.export.guisimconfpageexpanim import QBetseeSimConfPagerAnim, QBetseeSimConfPagerAnimCells, QBetseeSimConfPagerAnimCellsExport
        from betsee.gui.simconf.stack.page.export.guisimconfpageexpcsv import QBetseeSimConfPagerCSV, QBetseeSimConfPagerCSVExport
        from betsee.gui.simconf.stack.page.export.guisimconfpageexpplot import QBetseeSimConfPagerPlot, QBetseeSimConfPagerPlotCell, QBetseeSimConfPagerPlotCellExport, QBetseeSimConfPagerPlotCells, QBetseeSimConfPagerPlotCellsExport
        from betsee.gui.simconf.stack.page.space.guisimconfpageion import QBetseeSimConfPagerIon
        from betsee.gui.simconf.stack.page.space.guisimconfpagespace import QBetseeSimConfPagerSpace
        from betsee.gui.simconf.stack.page.space.guisimconfpagetis import QBetseeSimConfPagerTissueDefault, QBetseeSimConfPagerTissueCustom
        super().init()
        logs.log_debug('Initializing top-level stacked widget...')
        self._sim_conf = main_window.sim_conf
        self._stack_page_name_to_pager = {'sim_conf_stack_page_Export':QBetseeSimConfPagerExport(self), 
         'sim_conf_stack_page_Export_Anim':QBetseeSimConfPagerAnim(self), 
         'sim_conf_stack_page_Export_Anim_Cells':QBetseeSimConfPagerAnimCells(self), 
         'sim_conf_stack_page_Export_Anim_Cells_item':QBetseeSimConfPagerAnimCellsExport(self), 
         'sim_conf_stack_page_Export_CSV':QBetseeSimConfPagerCSV(self), 
         'sim_conf_stack_page_Export_CSV_item':QBetseeSimConfPagerCSVExport(self), 
         'sim_conf_stack_page_Export_Plot':QBetseeSimConfPagerPlot(self), 
         'sim_conf_stack_page_Export_Plot_Cell':QBetseeSimConfPagerPlotCell(self), 
         'sim_conf_stack_page_Export_Plot_Cell_item':QBetseeSimConfPagerPlotCellExport(self), 
         'sim_conf_stack_page_Export_Plot_Cells':QBetseeSimConfPagerPlotCells(self), 
         'sim_conf_stack_page_Export_Plot_Cells_item':QBetseeSimConfPagerPlotCellsExport(self), 
         'sim_conf_stack_page_Paths':QBetseeSimConfPagerPath(self), 
         'sim_conf_stack_page_Space':QBetseeSimConfPagerSpace(self), 
         'sim_conf_stack_page_Space_Ions':QBetseeSimConfPagerIon(self), 
         'sim_conf_stack_page_Space_Tissue':QBetseeSimConfPagerTissueDefault(self), 
         'sim_conf_stack_page_Space_Tissue_item':QBetseeSimConfPagerTissueCustom(self), 
         'sim_conf_stack_page_Time':QBetseeSimConfPagerTime(self)}
        self._stack_page_name_to_page = {stack_page_name:main_window.get_widget(stack_page_name) for stack_page_name in self._stack_page_name_to_pager.keys()}
        for stack_pager in self._stack_page_name_to_pager.values():
            stack_pager.init(main_window)

    @Slot(QTreeWidgetItem, QTreeWidgetItem)
    def switch_page_to_tree_item(self, tree_item_curr: QTreeWidgetItem, tree_item_prev: QTreeWidgetItem) -> None:
        """
        Switch to the child page widget of this stack widget associated with
        the passed current tree widget item recently clicked by the end user
        and passed previous tree widget item previously clicked by that user.

        Parameters
        ----------
        tree_item_curr : QTreeWidgetItem
            Current tree widget item clicked by the end user.
        tree_item_prev : QTreeWidgetItem
            Previous tree widget item clicked by the end user.

        Raises
        ----------
        BetseePySideStackedWidgetException
            If no such page exists (e.g., due to this tree widget item being a
            placeholder container for child items for which pages do exist).
        """
        stack_page = self._tree_item_static_to_stack_page.get(tree_item_curr, None)
        if stack_page is None:
            tree_item_list_leaf = tree_item_curr
            tree_item_list_leaf_name = tree_item_list_leaf.text(0)
            tree_item_list_root = guitreeitem.get_parent_item(tree_item_list_leaf)
            stack_page = self._tree_item_list_root_to_stack_page_list_leaf.get(tree_item_list_root, None)
            if stack_page is None:
                raise BetseePySideStackedWidgetException(QCoreApplication.translate('QBetseeSimConfStackedWidget', 'Tree item "{0}" stacked page not found.'.format(tree_item_list_leaf_name)))
            stack_page_name = stack_page.objectName()
            stack_page_pager = self._stack_page_name_to_pager.get(stack_page_name, None)
            logs.log_debug('Reinitializing tree item "%s" stacked page "%s" pager "%s"...', tree_item_list_leaf_name, stack_page_name, objects.get_class_name_unqualified(stack_page_pager))
            if stack_page_pager is None:
                raise BetseePySideStackedWidgetException(QCoreApplication.translate('QBetseeSimConfStackedWidget', 'Stacked page "{0}" pager not found.'.format(stack_page_name)))
            objtest.die_unless_instance(obj=stack_page_pager,
              cls=QBetseePagerItemizedMixin)
            tree_item_list_leaf_index = tree_item_list_root.indexOfChild(tree_item_list_leaf)
            stack_page_pager.reinit(main_window=(guiappwindow.get_main_window()),
              list_item_index=tree_item_list_leaf_index)
        self.setCurrentWidget(stack_page)

    @type_check
    def set_tree_item_to_stack_page(self, tree_item_static_to_stack_page_name: MappingType, tree_item_list_root_to_stack_page_name_list_leaf: MappingType) -> None:
        """
        Establish all mappings required by this stack widget to seamlessly map
        from each tree item of the tree widget associated with this stack
        widget to the corresponding child page widget of this stack widget.

        Parameters
        ----------
        tree_item_static_to_stack_page_name : dict
            Dictionary mapping from each **static tree item** (i.e., item
            statically defined via Qt (Creator|Designer) rather than
            dynamically defined at application runtime) of the tree widget
            associated with this stack widget to the object name of the
            corresponding child page widget of this stack widget.
        tree_item_list_root_to_stack_page_name_list_leaf : dict
            Dictionary mapping from each **dynamic list tree item** (i.e., item
            masquerading as a list dynamically defined at application runtime
            rather than statically defined via Qt (Creator|Designer)) of the
            tree widget associated with this stack widget to the object name of
            the corresponding **itemized page widget** (i.e., page configuring
            these tree items) of this stack widget.
        """
        self._tree_item_static_to_stack_page = self._convert_mapping_values_stack_page_name_to_page(tree_item_static_to_stack_page_name)
        self._tree_item_list_root_to_stack_page_list_leaf = self._convert_mapping_values_stack_page_name_to_page(tree_item_list_root_to_stack_page_name_list_leaf)

    @type_check
    def _convert_mapping_values_stack_page_name_to_page(self, mapping: MappingType) -> MappingType:
        """
        Dictionary mapping from arbitrary keys to stack widget pages converted
        from the passed dictionary mapping from arbitrary keys to object names
        of stack widget pages.

        Succinctly, this method creates and returns a new dictionary whose
        values are stack widget pages whose object names are the values of the
        passed dictionary.
        """
        return {key:mappings.get_key_value(mapping=(self._stack_page_name_to_page), key=stack_page_name) for key, stack_page_name in mapping.items()}