# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/widget/stock/guitreewdg.py
# Compiled at: 2019-01-16 01:51:30
# Size of source mod 2**32: 5709 bytes
"""
General-purpose :mod:`QTreeWidget` subclasses.
"""
from PySide2.QtWidgets import QHeaderView, QTreeWidget, QTreeWidgetItem
from betse.util.type.types import type_check, GeneratorType
from betsee.util.widget.abc.guiwdgabc import QBetseeObjectMixin

@type_check
def remove_item(item: QTreeWidgetItem) -> None:
    """
    Remove the passed tree item from its parent tree item and hence the parent
    tree transitively containing those items.

    Parameters
    ----------
    item : QTreeWidgetItem
        Tree item to be removed from its parent tree item and tree widget.

    See Also
    ----------
    https://stackoverflow.com/a/8961820/2809027
        StackOverflow answer strongly inspiring this implementation.
    """
    from PySide2 import shiboken2
    shiboken2.delete(item)


class QBetseeTreeWidget(QBetseeObjectMixin, QTreeWidget):
    __doc__ = "\n    :mod:`QTreeWidget`-based widget marginally improving upon the stock\n    :mod:`QTreeWidget` functionality.\n\n    This application-specific widget augments the :class:`QTreeWidget` class\n    with additional support for:\n\n    * **Horizontal scrollbars,** automatically displaying horizontal scrollbars\n      for all columns whose content exceeds that column's width. For\n      inexplicable reasons, this functionality has been seemingly intentionally\n      omitted from the stock :class:`QTreeWidget`.\n    "

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        header_view = self.header()
        header_view.setSectionResizeMode(QHeaderView.ResizeToContents)

    def setColumnCount(self, column_count):
        super().setColumnCount(column_count)
        if column_count != 1:
            self.header().setStretchLastSection(True)

    def iter_items_top(self) -> GeneratorType:
        """
        Generator iteratively yielding each **top-level tree item** (i.e.,
        :class:`QTreeWidgetItem` owned by this tree such that the parent item
        of this child item is the invisible root item returned by the
        :meth:`invisibleRootItem` method) of this tree widget.

        Yields
        ----------
        QTreeWidgetItem
            Current top-level tree item of this tree widget.

        See Also
        ----------
        https://stackoverflow.com/a/8961820/2809027
            StackOverflow answer strongly inspiring this implementation.
        """
        item_root = self.invisibleRootItem()
        items_top_count = item_root.childCount()
        return (item_root.child(item_top_index) for item_top_index in range(items_top_count))