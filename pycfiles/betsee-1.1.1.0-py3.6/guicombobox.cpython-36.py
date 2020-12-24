# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/widget/stock/guicombobox.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 9736 bytes
"""
General-purpose :mod:`QComboBox` widget subclasses.
"""
from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QComboBox
from betse.util.io.log import logs
from betse.util.type.iterable import iterables, itertest
from betse.util.type.types import type_check, GeneratorType, SequenceTypes, SequenceOrNoneTypes, SequenceStandardTypes
from betsee.guiexception import BetseePySideComboBoxException
from betsee.util.widget.mixin.guiwdgeditmixin import QBetseeEditWidgetMixin

class QBetseeComboBox(QBetseeEditWidgetMixin, QComboBox):
    __doc__ = '\n    General-purpose :mod:`QComboBox` widget implementing a Pythonic API.\n\n    Caveats\n    ----------\n    To guarantee a one-to-one correspondence between the currently selected\n    combo box item and the underlying model constraining these items, this\n    combo box defaults to:\n\n    * **Non-editability** (i.e., the text of each item is *not* interactively\n      editable by end users).\n    * **Uniqueness** (i.e., the text of each item is unique and hence differs\n      from the text of each other item).\n\n    Attributes\n    ----------\n    _is_items_added : bool\n        ``True`` only if the :meth:`addItems` method has been previously\n        called, implying this combo box to have been populated with one or more\n        icon-less items.\n    '

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._is_items_added = False
        self.setEditable(False)
        self.setDuplicatesEnabled(False)

    @type_check
    def _init_safe(self, items_iconless_text=None, *args, **kwargs):
        """
        Finalize the initialization of this widget.

        Parameters
        ----------
        items_iconless_text : SequenceOrNoneTypes
            Sequence of **icon-less item text** (i.e., human-readable text of
            every initial combo box item *without* corresponding icons) to
            prepopulate this combo box with. Defaults to ``None``, in which
            case this combo box initially contains no items and is thus empty.

        All remaining parameters are passed as is to the superclass method.
        """
        (super()._init_safe)(*args, **kwargs)
        logs.log_debug('Initializing combo box "%s"...', self.obj_name)
        if items_iconless_text is not None:
            self.clear()
            self.add_items_iconless(items_iconless_text)

    def _die_unless_items_added(self) -> None:
        """
        Raise an exception unless the :meth:`addItems` method has been
        previously called (i.e., unless this combo box has already been
        populated with one or more icon-less items).

        Equivalently, this method raises an exception if the :meth:`addItems`
        method has *not* been previously called.

        Raises
        ----------
        BetseePySideComboBoxException
            if the :meth:`addItems` method has *not* been previously called.
        """
        if not self._is_items_added:
            raise BetseePySideComboBoxException(QCoreApplication.translate('QBetseeComboBox', 'Combo box unpopulated (i.e., addItems() not called).'))

    def addItems(self, items_text):
        super().addItems(items_text)
        self._is_items_added = True

    def clear(self):
        super().clear()
        self._is_items_added = False

    @type_check
    def add_items_iconless(self, items_text: SequenceTypes) -> None:
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
        """
        logs.log_debug('Adding %d items to combo box "%s"...', len(items_text), self.obj_name)
        items_all_text = tuple(iterables.iter_items(items_text, self.iter_items_text()))
        itertest.die_unless_items_unique(items_all_text)
        if not isinstance(items_text, SequenceStandardTypes):
            items_text = tuple(items_text)
        self.addItems(items_text)

    @type_check
    def iter_items_text(self) -> GeneratorType:
        """
        Generator iteratively yielding the human-readable text associated with
        each item of this combo box.

        Yields
        ----------
        str
            Human-readable text associated with the currently iterated item of
            this combo box.
        """
        return (self.itemText(item_index) for item_index in range(self.count()))