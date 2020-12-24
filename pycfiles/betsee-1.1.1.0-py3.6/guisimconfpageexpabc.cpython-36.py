# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/page/export/guisimconfpageexpabc.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 10057 bytes
"""
**Export item simulation configuration pager** (i.e., :mod:`PySide2`-based
controller for stack widget pages applicable to exports of a certain type
associated with tree widget items masquerading as dynamic list items)
hierarchy.
"""
from PySide2.QtWidgets import QMainWindow
from betse.science.pipe.export.pipeexpabc import SimPipeExportABC
from betse.util.type.decorator.deccls import abstractproperty
from betse.util.type.iterable import sequences
from betse.util.type.obj import objtest
from betse.util.type.types import type_check
from betsee.util.widget.abc.control.guictlpageabc import QBetseePagerItemizedABC

class QBetseeSimConfPagerExportABC(QBetseePagerItemizedABC):
    __doc__ = '\n    Abstract base class of all **simulation export configuration pager** (i.e.,\n    :mod:`PySide2`-based controller connecting all editable widgets of a\n    stack widget page applicable to simulation exports of a particular type\n    with corresponding settings of a YAML-backed list item of the currently\n    open simulation configuration) subclasses.\n\n    Attributes\n    ----------\n    _p : Parameters\n        Simulation configuration singleton.\n\n    Attributes (Widget)\n    ----------\n    _widget_kind : QBetseeSimConfComboBoxSequence\n        Combo box widget editing the type of this simulation export, whose Qt\n        object name is :meth:`_widget_name_prefix` appended by ``kind``.\n    _widget_name : QBetseeSimConfLineEdit\n        Line edit widget editing the name of this simulation export, whose Qt\n        object name is :meth:`_widget_name_prefix` appended by ``name``.\n    '

    @abstractproperty
    def _pipe_cls(self) -> SimPipeExportABC:
        """
        Type of simulation export pipeline exporting all possible simulation
        exports associated with this pager.
        """
        pass

    @abstractproperty
    def _widget_name_prefix(self) -> str:
        """
        Substring prefixing the name of all instance variables of the
        :class:`QBetseeMainWindow`` singleton whose values are all child
        widgets of the page controlled by this pager.
        """
        pass

    @abstractproperty
    def _yaml_list(self) -> str:
        """
        YAML-backed list subconfiguration (i.e., :class:`YamlList` instance) of
        the current simulation configuration whose currently selected item in
        the top-level tree widget is edited by the child widgets of the page
        controlled by this pager.

        Subclasses should note that the :attr:`_p` instance variable
        (guaranteed to be non-``None`` whenever this property is accessed)
        provides direct access to this list subconfiguration.
        """
        pass

    def __init__(self, *args, **kwargs):
        """
        Initialize this pager.
        """
        (super().__init__)(*args, **kwargs)
        self._p = None
        self._widget_kind = None
        self._widget_name = None

    @type_check
    def init(self, main_window):
        from betsee.gui.simconf.stack.widget.guisimconfcombobox import QBetseeSimConfComboBoxSequence
        from betsee.gui.simconf.stack.widget.guisimconflineedit import QBetseeSimConfLineEdit
        super().init(main_window)
        self._p = main_window.sim_conf.p
        self._widget_kind = main_window.get_widget(widget_name=(self._widget_name_prefix + 'kind'))
        self._widget_name = main_window.get_widget(widget_name=(self._widget_name_prefix + 'name'))
        objtest.die_unless_instance(obj=(self._widget_kind),
          cls=QBetseeSimConfComboBoxSequence)
        objtest.die_unless_instance(obj=(self._widget_name),
          cls=QBetseeSimConfLineEdit)
        export_confs_kind = self._pipe_cls.iter_runners_metadata_kind()
        self._widget_kind.add_items_iconless(items_text=export_confs_kind)

    @type_check
    def reinit(self, main_window: QMainWindow, list_item_index: int) -> None:
        export_conf = sequences.get_index(sequence=(self._yaml_list),
          index=list_item_index)
        export_conf_cls = type(export_conf)
        self._widget_name.init(sim_conf=(main_window.sim_conf),
          sim_conf_alias=(export_conf_cls.name),
          sim_conf_alias_parent=export_conf,
          is_reinitable=True)
        self._widget_kind.init(sim_conf=(main_window.sim_conf),
          sim_conf_alias=(export_conf_cls.kind),
          sim_conf_alias_parent=export_conf,
          is_reinitable=True)