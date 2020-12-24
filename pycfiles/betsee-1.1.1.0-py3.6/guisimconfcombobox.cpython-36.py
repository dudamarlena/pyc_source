# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/widget/guisimconfcombobox.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 11611 bytes
"""
:class:`QComboBox`-based simulation configuration widget subclasses.
"""
from PySide2.QtCore import QCoreApplication, Signal
from betse.util.io.log import logs
from betse.util.type.types import type_check, ClassOrNoneTypes, SequenceTypes
from betsee.guiexception import BetseePySideComboBoxException
from betsee.gui.simconf.stack.widget.mixin.guisimconfwdgeditenum import QBetseeSimConfEditEnumWidgetMixin
from betsee.gui.simconf.stack.widget.mixin.guisimconfwdgeditscalar import QBetseeSimConfEditScalarWidgetMixin
from betsee.util.widget.stock.guicombobox import QBetseeComboBox
from collections import OrderedDict

class QBetseeSimConfComboBoxABC(QBetseeSimConfEditScalarWidgetMixin, QBetseeComboBox):
    __doc__ = '\n    Abstract base class of all **simulation configuration combo box widget**\n    (i.e., :class:`QComboBox` widget transparently mapping from arbitrary\n    objects defined by the currently open simulation configuration file to\n    human-readable items of this combo box) subclasses.\n    '

    @property
    def undo_synopsis(self) -> str:
        return QCoreApplication.translate('QBetseeSimConfComboBoxEnum', 'changes to a combo box')

    @property
    def _finalize_widget_change_signal(self) -> Signal:
        return self.currentIndexChanged

    @property
    def widget_value(self) -> int:
        return self.currentIndex()

    @widget_value.setter
    @type_check
    def widget_value(self, widget_value):
        super().setCurrentIndex(widget_value)

    def _reset_widget_value(self) -> None:
        self.widget_value = 0


class QBetseeSimConfComboBoxSequence(QBetseeSimConfComboBoxABC):
    __doc__ = '\n    **Simulation configuration combo box widget** (i.e., :class:`QComboBox`\n    widget transparently mapping from a sequence of all possible strings\n    constraining exactly one setting of the current simulation configuration\n    file to human-readable items of this combo box).\n\n    Attributes\n    ----------\n    _item_index_min : int\n        0-based index of the last combo box item at initialization time (i.e.,\n        the time of the :meth:`_init_safe` call) with respect to negative indexing.\n    _item_index_max : int\n        0-based index of the last combo box item at initialization time (i.e.,\n        the time of the :meth:`_init_safe` call) with respect to positive indexing.\n    _item_text_to_index : MappingType\n        Dictionary mapping from the text to 0-based index of each combo box\n        item at initialization time (i.e., the time of the :meth:`_init_safe` call).\n    '

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._item_index_min = None
        self._item_index_max = None
        self._item_text_to_index = None

    def addItems(self, items_text):
        """
        Add **icon-less items** (i.e., plaintext combo box items with *no*
        corresponding icons) specified by the passed human-readable strings to
        this combo box after the index of this combo box defined by the
        :meth:`insertPolicy` property, defaulting to appending these items
        *after* any existing items of this combo box.

        Specifically, for each element of this sequence, this method adds a new
        combo box item whose human-readable text is that element.

        Parameters
        ----------
        items_text : SequenceTypes
            Sequence of the text of each item to be added to this combo box.

        Raises
        ----------
        BetseMappingException
            If this dictionary is *not* safely invertible (i.e., if any value
            of this dictionary is non-uniquely assigned to two or more keys).
        BetseePySideRadioButtonException
            If the number of members in this enumeration differs from the
            number of members mapped by (i.e., of keys in) this dictionary.
        """
        super().addItems(items_text)
        logs.log_debug('Populating sequential combo box "%s"...', self.obj_name)
        self._item_index_min = -len(items_text)
        self._item_index_max = len(items_text) - 1
        self._item_text_to_index = {item_text:item_index for item_index, item_text in enumerate(items_text)}

    @property
    def _sim_conf_alias_type_strict(self) -> ClassOrNoneTypes:
        return str

    def _get_alias_from_widget_value(self) -> object:
        self._die_unless_items_added()
        item_index = self.widget_value
        if not self._item_index_min <= item_index <= self._item_index_max:
            raise BetseePySideComboBoxException(QCoreApplication.translate('QBetseeSimConfComboBoxSequence', 'Combo box item index "{0}" invalid (i.e., not in [{1}, {2}]).'.format(item_index, self._item_index_min, self._item_index_max)))
        return self.itemText(item_index)

    def _get_widget_from_alias_value(self) -> object:
        self._die_unless_items_added()
        item_text = self._sim_conf_alias.get()
        if item_text not in self._item_text_to_index:
            raise BetseePySideComboBoxException(QCoreApplication.translate('QBetseeSimConfComboBoxSequence', 'Combo box item text "{0}" unrecognized.'.format(item_text)))
        return self._item_text_to_index[item_text]


class QBetseeSimConfComboBoxEnum(QBetseeSimConfEditEnumWidgetMixin, QBetseeSimConfComboBoxABC):
    __doc__ = '\n    **Simulation configuration enumeration-backed combo box widget** (i.e.,\n    :class:`QComboBox` widget transparently mapping from enumeration members\n    defined by the current simulation configuration file to human-readable\n    items of this combo box).\n    '

    @type_check
    def _init_safe(self, enum_member_to_item_text, *args, **kwargs):
        """
        Finalize the initialization of this widget.

        Parameters
        ----------
        enum_member_to_item_text : OrderedDict
            Ordered dictionary mapping from each member of the enumeration
            encapsulated by the passed ``sim_conf_alias`` parameter to the
            human-readable text of the combo box item describing that member.
            The dictionary ordering of these enumeration members exactly
            defines the order in which the corresponding combo box items are
            listed.

        All remaining parameters are passed as is to the superclass method.

        Raises
        ----------
        BetseMappingException
            If this dictionary is *not* safely invertible (i.e., if any value
            of this dictionary is non-uniquely assigned to two or more keys).
        BetseePySideComboBoxException
            If the number of members in this enumeration differs from the
            number of members mapped by (i.e., of keys in) this dictionary.
        """
        logs.log_debug('Initializing enumerated combo box "%s"...', self.obj_name)
        enum_member_to_widget_value = {enum_member:item_index for item_index, enum_member in enumerate(enum_member_to_item_text.keys())}
        items_text = tuple(enum_member_to_item_text.values())
        (super()._init_safe)(args, enum_member_to_widget_value=enum_member_to_widget_value, 
         items_iconless_text=items_text, **kwargs)