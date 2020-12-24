# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/widget/stock/tree/guitreeitem.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 26952 bytes
"""
High-level :class:`QTreeWidgetItem` functionality.
"""
from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QTreeWidgetItem, QTreeWidgetItemIterator
from betse.util.io.log import logs
from betse.util.py.module import pymodname
from betse.util.type.iterable import sequences
from betse.util.type.text.string import strjoin
from betse.util.type.types import type_check, GeneratorType, SequenceTypes
from betsee.guiexception import BetseePySideTreeWidgetItemException
from betsee.util.type.guitype import QTreeWidgetItemOrNoneTypes

@type_check
def die_if_parent_item(item: QTreeWidgetItem) -> None:
    """
    Raise an exception if the passed tree item is a **parent tree item** (i.e.,
    contains at least one child tree item).

    Parameters
    ----------
    item : QTreeWidgetItem
        Tree item to be tested.

    Raises
    ----------
    BetseePySideTreeWidgetItemException
        If this tree item contains one or more child tree items.
    """
    if is_parent_item(item):
        raise BetseePySideTreeWidgetItemException(QCoreApplication.translate('guitreeitem', 'Tree item "{0}" already a parent (i.e., contains {1} child tree items).'.format(item.text(0), item.childCount())))


@type_check
def die_unless_parent_item(item: QTreeWidgetItem) -> None:
    """
    Raise an exception unless the passed tree item is a **parent tree item**
    (i.e., contains at least one child tree item).

    Equivalently, this function raises an exception if this tree item contains
    no child tree items.

    Parameters
    ----------
    item : QTreeWidgetItem
        Tree item to be tested.

    Raises
    ----------
    BetseePySideTreeWidgetItemException
        If this tree item contains no child tree items.
    """
    if not is_parent_item(item):
        raise BetseePySideTreeWidgetItemException(QCoreApplication.translate('guitreeitem', 'Tree item "{0}" not a parent (i.e., contains no child tree items).'.format(item.text(0))))


@type_check
def is_parent_item(item: QTreeWidgetItem) -> bool:
    """
    ``True`` only if the passed tree item is a **parent tree item** (i.e.,
    contains at least one child tree item).

    Parameters
    ----------
    item : QTreeWidgetItem
        Tree item to be tested.

    Returns
    ----------
    bool
        ``True`` only if this tree item contains at least one child tree item.
    """
    return item.childCount() > 0


@type_check
def get_child_item_with_text_first(parent_item: QTreeWidgetItem, child_text: str) -> QTreeWidgetItem:
    """
    First child tree item with the passed **first-column text** (i.e., text in
    the first column) residing under the passed parent tree item if this parent
    contains at least one such child *or* raise an exception otherwise (i.e.,
    if this parent contains no such child).

    Caveats
    ----------
    **This function only returns the first such child of this parent.** If this
    parent contains multiple children with the same first-column text, this
    function silently ignores all but the first such child.

    **This function performs a linear search through the children of this
    parent** and hence exhibits ``O(n)`` worst-case time complexity, where
    ``n`` is the number of children of this parent. While negligible in the
    common case, this search may be a performance concern on large subtrees.

    Parameters
    ----------
    parent_item : QTreeWidgetItem
        Parent tree item to retrieve this child tree item from.
    child_text : str
        Text in the first column of the first child tree item to be retrieved
        from this parent tree item.

    Returns
    ----------
    QTreeWidgetItem
        First child tree item with this first-column text residing under this
        parent tree item.

    Raises
    ----------
    BetseePySideTreeWidgetItemException
        If this parent tree item contains no child tree item with this
        first-column text.
    """
    die_unless_parent_item(parent_item)
    for child_item in iter_child_items(parent_item):
        if child_item.text(0) == child_text:
            return child_item

    raise BetseePySideTreeWidgetItemException(QCoreApplication.translate('guitreeitem', 'Parent tree item "{0}" contains no child tree item with first-column text "{1}".'.format(parent_item.text(0), child_text)))


@type_check
def get_child_item_with_text_path(parent_item: QTreeWidgetItem, text_path: SequenceTypes) -> QTreeWidgetItem:
    """
    First transitive child tree item of the passed parent tree item with the
    passed **absolute first-column text path** (i.e., sequence of one or more
    strings uniquely identifying this child tree item in the subtree rooted at
    this parent tree item) if any *or* raise an exception otherwise (i.e., if
    this parent tree item transitively contains no such child tree item).

    Each passed string is the **first-column text** (i.e., text in the first
    column) of either the child tree item to be returned *or* a parent tree
    item of that item, such that:

    #. The first passed string is the first-column text of the top-level
       child tree item of this parent tree item transitively containing the
       child tree item to be returned.
    #. The second passed string is the first-column text of the next-level
       child tree item of the prior top-level child tree item transitively
       containing the child tree item to be returned.
    #. The second-to-last passed string is the first-column text of the
       direct parent tree item of the child tree item to be returned.
    #. The last passed string is the first-column text of the child tree item
       to be returned.

    Caveats
    ----------
    **This function only returns the first such item satisfying this path.** If
    this parent contains multiple children ambiguously satisfying this path,
    this function silently ignores all but the first such child tree item.

    **This function performs a linear search through the items of the subtree
    rooted at this parent tree item** and hence exhibits ``O(n)`` worst-case
    time complexity, where ``n`` is the number of items in this subtree. While
    negligible in the common case, this search may be a performance concern on
    large subtrees.

    Parameters
    ----------
    parent_item : QTreeWidgetItem
        Parent tree item to retrieve this child tree item from.
    text_path: SequenceTypes
        Sequence of one or more first-column texts uniquely identifying the
        child tree item of this parent tree item to be returned.

    Returns
    ----------
    QTreeWidgetItem
        First child tree item with this path.

    Raises
    ----------
    BetseePySideTreeWidgetItemException
        If either:

        * The passed ``text_path`` parameter is empty.
        * This parent tree item contains no child tree item with this path.
    """
    die_unless_parent_item(parent_item)
    logs.log_debug('Retrieving parent tree item "%s" child with path "%s"...', parent_item.text(0) or 'ROOT', (strjoin.join_on)(*text_path, **{'delimiter': '/'}))
    sequences.die_if_empty(sequence=text_path,
      exception_message=(QCoreApplication.translate('guitreeitem', 'Tree path empty.')))
    for child_item_text in text_path:
        parent_item = get_child_item_with_text_first(parent_item, child_item_text)

    return parent_item


@type_check
def get_parent_item(child_item: QTreeWidgetItem) -> QTreeWidgetItem:
    """
    Parent tree item of the passed child tree item if this child has a parent
    *or* raise an exception otherwise (i.e., if this child has *no* parent).

    Caveats
    ----------
    **This higher-level function should always be called in lieu of the
    low-level :meth:`QTreeWidgetItem.parent` method.** Whereas this function
    unambiguously returns the expected tree item or raises an exception, that
    method ambiguously returns ``None`` for both top-level tree items whose
    parent is the root tree item of the tree containing those items *and* tree
    items with no parent.

    Parameters
    ----------
    child_item : QTreeWidgetItem
        Child tree item to retrieve this parent tree item of.

    Returns
    ----------
    QTreeWidgetItem
        Either:

        * If this child tree item is a top-level tree item, the root tree item
          of the :class:`QTreeWidget` containing this item.
        * Else, the parent tree item of this child tree item.

    Raises
    ----------
    BetseePySideTreeWidgetItemException
        If this child tree item has no parent.

    See Also
    ----------
    https://stackoverflow.com/a/12134662/2809027
        StackOverflow answer mildly inspiring this implementation.
    """
    parent_item = get_parent_item_or_none(child_item)
    if parent_item is None:
        raise BetseePySideTreeWidgetItemException(QCoreApplication.translate('guitreeitem', 'Tree item "{0}" has no parent.'.format(child_item.text(0))))
    return parent_item


@type_check
def get_parent_item_or_none(child_item: QTreeWidgetItem) -> QTreeWidgetItemOrNoneTypes:
    """
    Parent tree item of the passed child tree item if this child has a parent
    *or* ``None`` otherwise (i.e., if this child has *no* parent).

    Caveats
    ----------
    **This higher-level function should always be called in lieu of the
    low-level :meth:`QTreeWidgetItem.parent` method.** Whereas this function
    unambiguously returns either the expected tree item or ``None``, that
    method ambiguously returns ``None`` for both top-level tree items whose
    parent is the root tree item of the tree containing those items *and* tree
    items with no parent.

    Parameters
    ----------
    child_item : QTreeWidgetItem
        Child tree item to retrieve this parent tree item of.

    Returns
    ----------
    QTreeWidgetItemOrNoneTypes
        Either:

        * If this child tree item is a top-level tree item, the root tree item
          of the :class:`QTreeWidget` containing this item.
        * Else if this child tree item has a parent tree item, that item.
        * Else, ``None``.

    Raises
    ----------
    BetseePySideTreeWidgetItemException
        If this child tree item is the root tree item and hence has no parent.

    See Also
    ----------
    https://stackoverflow.com/a/12134662/2809027
        StackOverflow answer strongly inspiring this implementation.
    """
    parent_item = child_item.parent()
    if parent_item is None:
        tree_widget = child_item.treeWidget()
        if tree_widget is not None:
            parent_item = tree_widget.invisibleRootItem()
            assert parent_item.indexOfChild(child_item) != -1
    return parent_item


@type_check
def get_item_preceding(item: QTreeWidgetItem) -> QTreeWidgetItemOrNoneTypes:
    """
    Tree item preceding the passed tree item in the tree widget containing that
    tree item if the passed tree item is *not* the first top-level item of this
    tree widget *or* raise an exception otherwise (i.e., if this is the first
    top-level item of this tree widget).

    Raises
    ----------
    BetseePySideTreeWidgetItemException
        If the passed tree item is the first top-level item of its tree widget.

    See Also
    ----------
    :func:`get_item_preceding_or_none`
        Further details.
    """
    item_preceding = get_item_preceding_or_none(item)
    if item_preceding is None:
        raise BetseePySideTreeWidgetItemException(QCoreApplication.translate('guitreeitem', 'Tree item "{0}" preceded by no tree item (i.e., due to being the first top-level tree item).'.format(item.text(0))))
    return item_preceding


@type_check
def get_item_preceding_or_none(item: QTreeWidgetItem) -> QTreeWidgetItemOrNoneTypes:
    """
    Tree item preceding the passed tree item in the tree widget containing that
    tree item if the passed tree item is *not* the first top-level item of this
    tree widget *or* ``None`` otherwise (i.e., if this is the first top-level
    item of this tree widget).

    Specifically, this function returns:

    * If the passed tree item has a **preceding sibling** (i.e., a child tree
      item with the same parent tree item as the passed tree item whose index
      in the parent is one less than that of the passed tree item), this
      sibling.
    * Else if the passed tree item has a **non-root parent** (i.e., a parent
      tree item that is *not* the invisible root tree item of this tree widget,
      in which case the passed tree item is *not* a top-level tree item), this
      parent.
    * Else, the passed tree item is the first top-level tree item of this tree
      widget, in which case an exception is raised.

    Parameters
    ----------
    item : QTreeWidgetItem
        Tree item to retrieve the preceding tree item of.

    Returns
    ----------
    QTreeWidgetItem
        Tree item preceding the passed tree item.
    """
    item_iter = QTreeWidgetItemIterator(item, QTreeWidgetItemIterator.All)
    item_iter -= 1
    item_preceding = item_iter.value()
    return item_preceding


@type_check
def delete_child_items(parent_item: QTreeWidgetItem) -> None:
    """
    Permanently delete *all* child tree items of the passed parent tree item.

    Parameters
    ----------
    parent_item : QTreeWidgetItem
        Parent tree item to delete all child tree items of.

    See Also
    ----------
    :func:`delete_item`
        Further details.
    """
    logs.log_debug('Recursively deleting tree item "%s" children...', parent_item.text(0))
    child_items = parent_item.takeChildren()
    for child_item in child_items:
        delete_item(child_item)


@type_check
def delete_item(item: QTreeWidgetItem) -> None:
    """
    Permanently delete the passed tree item.

    Specifically, this function (in order):

    #. Removes this item from its parent tree item and hence the
       :class:`QTreeWidget` containing both items.
    #. Schedules this item for garbage collection.

    Caveats
    ----------
    **This function should always be called in lieu of lower-level Qt methods
    (e.g., :meth:`QTreeWidgetItem.removeChild`,
    :meth:`QTreeWidgetItem.takeChild`, :meth:`QTreeWidgetItem.takeChildren`).**
    Why? Because those methods are *not* guaranteed to schedule this item for
    garbage collection. Hidden references to this item preventing Python from
    garbage collecting this item may continue to silently persist -- notably,
    circular references between this item and its child tree items (if any).

    Parameters
    ----------
    item : QTreeWidgetItem
        Tree item to be deleted.

    Raises
    ----------
    BetseePySideTreeWidgetItemException
        If this tree item is the root tree item and hence cannot be deleted.

    See Also
    ----------
    https://stackoverflow.com/a/8961820/2809027
        StackOverflow answer mildly inspiring this implementation.
    """
    logs.log_debug('Deleting tree item "%s"...', item.text(0))
    parent_item = get_parent_item_or_none(item)
    if parent_item is not None:
        parent_item.removeChild(item)
    if pymodname.is_module('PySide2.shiboken2'):
        from PySide2 import shiboken2
        shiboken2.delete(item)
    elif is_parent_item(item):
        logs.log_warning('Suboptimally deleting subtree (i.e., as PySide2 submodule "shiboken2" not found)...')
        _delete_item_subtree(item)


@type_check
def _delete_item_subtree(parent_item: QTreeWidgetItem) -> None:
    """
    Recursively delete the **subtree** (i.e., abstract collection of one or
    more tree items) rooted at the passed tree item.

    This recursive function manually reimplements the convenient deletion
    algorithm implemented by the technically optional :mod:`PySide2.shiboken2`
    submodule. Specifically, this function (in order):

    #. Removes all child tree items from this item.
    #. Recursively calls this function on each such item.

    Parameters
    ----------
    parent_item : QTreeWidgetItem
        Tree item to recursively delete the entire subtree of.
    """
    logs.log_debug('Recursively deleting tree item "%s" subtree...', parent_item.text(0))
    child_items = parent_item.takeChildren()
    for child_item in child_items:
        _delete_item_subtree(child_item)


@type_check
def iter_child_items(parent_item: QTreeWidgetItem) -> GeneratorType:
    """
    Generator iteratively yielding each child tree item of the passed parent
    tree item (in ascending order).

    Caveats
    ----------
    **Avoiding deleting items yielded by this generator,** as doing so is
    guaranteed to raise an exception. Consider calling the
    :func:`iter_child_items_reversed` function instead, which suffers no such
    synchronization issues.

    Parameters
    ----------
    parent_item : QTreeWidgetItem
        Parent tree item to iterate all child tree items of.

    Yields
    ----------
    QTreeWidgetItem
        Current top-level tree item of this tree widget.

    Raises
    ----------
    BetseePySideTreeWidgetItemException
        If the current child tree item to be yielded no longer exists (e.g.,
        due to having been erroneously deleted by the caller).
    """
    child_items_count = parent_item.childCount()
    for child_item_index in range(child_items_count):
        child_item = parent_item.child(child_item_index)
        if child_item is None:
            raise BetseePySideTreeWidgetItemException(QCoreApplication.translate('guitreeitem', 'Parent tree item "{0}" child "{1}" no longer exists.'.format(parent_item.text(0), child_item_index)))
        yield child_item


@type_check
def iter_child_items_reversed(parent_item: QTreeWidgetItem) -> GeneratorType:
    """
    Generator iteratively yielding each child tree item of the passed parent
    tree item (in descending and hence "reversed" order).

    This function explicitly permits callers to safely delete items yielded by
    this generator, unlike the :func:`iter_child_items` function. Indeed, item
    deletion is the principal use case for this function.

    Parameters
    ----------
    parent_item : QTreeWidgetItem
        Parent tree item to iterate all child tree items of.

    Yields
    ----------
    QTreeWidgetItem
        Current top-level tree item of this tree widget.

    Raises
    ----------
    BetseePySideTreeWidgetItemException
        If the current child tree item to be yielded no longer exists (e.g.,
        due to having been erroneously deleted by the caller). This edge case
        may occur when the caller attempts to delete any child tree item
        excluding the previously yielded tree item, which may *always* be
        safely deleted.
    """
    child_items_count = parent_item.childCount()
    for child_item_index in reversed(range(child_items_count)):
        child_item = parent_item.child(child_item_index)
        if child_item is None:
            raise BetseePySideTreeWidgetItemException(QCoreApplication.translate('guitreeitem', 'Parent tree item "{0}" child "{1}" no longer exists.'.format(parent_item.text(0), child_item_index)))
        yield child_item