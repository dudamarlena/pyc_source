# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/widget/guiwdg.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 5270 bytes
"""
Low-level :mod:`PySide2`-specific widget facilities universally applicable to
all (or at least most) widget types.
"""
from PySide2.QtWidgets import QWidget
from betse.util.type.types import type_check, CallableTypes
from betsee.guiexception import BetseePySideWidgetException
from betsee.util.type.guitype import QWidgetOrNoneTypes

@type_check
def die_unless_widget_parent_satisfies(widget: QWidget, predicate: CallableTypes) -> None:
    """
    Raise an exception unless some transitive parent widget of the passed widget
    satisfies the passed predicate.

    Equivalently, this function raises an exception if *no* transitive parent
    widget of the passed widget satisfies the passed predicate.

    Parameters
    ----------
    widget : QWidgetOrNoneTypes
        Child widget to be inspected.
    predicate : CallableTypes
        Callable accepting one passed parent widget, returning ``True`` only if
        this widget satisfies this predicate. Hence, this predicate should have
        a signature resembling: ``def predicate(widget: QWidget) -> bool``.

    Raises
    ----------
    BetseePySideWidgetException
        If *no* transitive parent widget of this child widget satisfies this
        boolean predicate.
    """
    if not is_widget_parent_satisfies(widget=widget, predicate=predicate):
        raise BetseePySideWidgetException('Parent widget of child widget "{0}" satsifying predicate {1!r} not found.'.format(widget.objectName(), predicate))


@type_check
def is_widget_parent_satisfies(widget: QWidget, predicate: CallableTypes) -> bool:
    """
    ``True`` only if some transitive parent widget of the passed widget
    satisfies the passed predicate.

    For each transitive parent widget of the passed widget in ascending order
    from the immediate to root parent widget (e.g., :class:`QMainWindow`
    widget) of the passed widget, this function iteratively:

    #. Passes that parent widget to the passed predicate.
    #. If that predicate returns ``True``, this function halts searching and
       immediately returns ``True``.
    #. Else if that parent widget itself has a parent widget, this function
       continues searching by iterating up the widget ownership hierarchy to
       that parent parent widget and repeating the above logic.
    #. Else, returns ``False``.

    Parameters
    ----------
    widget : QWidgetOrNoneTypes
        Child widget to be inspected.
    predicate : CallableTypes
        Callable accepting one passed parent widget, returning ``True`` only if
        this widget satisfies this predicate. Hence, this predicate should have
        a signature resembling: ``def predicate(widget: QWidget) -> bool``.

    Returns
    ----------
    bool
        ``True`` only if some parent of this widget satisfies this predicate.
    """
    widget_child = widget
    widget_parent = None
    while True:
        widget_parent = widget_child.parentWidget()
        if predicate(widget_parent):
            return True
        widget_child = widget_parent

    return False


@type_check
def get_label(widget: QWidgetOrNoneTypes) -> str:
    """
    Human-readable label synopsizing the passed widget if any.

    Parameters
    ----------
    widget : QWidgetOrNoneTypes
        Widget to be synopsized *or* ``None``, in which case the absence of a
        widget is synopsized.

    Returns
    ----------
    str
        Human-readable label synopsizing this widget if any.
    """
    if widget is not None:
        return 'widget "{}"'.format(widget.objectName())
    else:
        return 'no widget'