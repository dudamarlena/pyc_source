# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/filter/guifiltertooltip.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 5281 bytes
"""
Low-level tooltip-specific event filters globally applicable to the entire
application as a whole and hence *all* tooltips for *all* widgets.
"""
from PySide2.QtCore import QEvent, QObject
from PySide2.QtWidgets import QWidget
from betse.util.type.obj import objtest
from betse.util.type.text import mls

class QBetseePlaintextTooltipEventFilter(QObject):
    __doc__ = '\n    Tooltip-specific event filter dramatically improving the tooltips of all\n    widgets for which this filter is installed.\n\n    Motivation\n    ----------\n    **Rich text tooltips** (i.e., tooltips containing one or more HTML-like\n    tags) are implicitly wrapped by Qt to the width of their parent windows and\n    hence typically behave as expected.\n\n    **Plaintext tooltips** (i.e., tooltips containing no such tags), however,\n    are not. For unclear reasons, plaintext tooltips are implicitly truncated\n    to the width of their parent windows. The only means of circumventing this\n    obscure constraint is to manually inject newlines at the appropriate\n    80-character boundaries of such tooltips -- which has the distinct\n    disadvantage of failing to scale to edge-case display and device\n    environments (e.g., high-DPI). Such tooltips *cannot* be guaranteed to be\n    legible in the general case and hence are blatantly broken under *all* Qt\n    versions to date. This is a `well-known long-standing issue <issue_>`__ for\n    which no official resolution exists.\n\n    This filter globally addresses this issue by implicitly converting *all*\n    intercepted plaintext tooltips into rich text tooltips in a general-purpose\n    manner, thus wrapping the former exactly like the latter. To do so, this\n    filter (in order):\n\n    #. Auto-detects whether the:\n\n       * Current event is a :class:`QEvent.ToolTipChange` event.\n       * Current widget has a **non-empty plaintext tooltip**.\n\n    #. When these conditions are satisfied:\n\n       #. Escapes all HTML syntax in this tooltip (e.g., converting all ``&``\n          characters to ``&amp;`` substrings).\n       #. Embeds this tooltip in the Qt-specific ``<qt>...</qt>`` tag, thus\n          implicitly converting this plaintext tooltip into a rich text\n          tooltip.\n\n    .. _issue:\n        https://bugreports.qt.io/browse/QTBUG-41051\n    '

    def eventFilter(self, widget, event):
        """
        Tooltip-specific event filter handling the passed Qt object and event.
        """
        from betsee.util.type.text import guistr
        if event.type() == QEvent.ToolTipChange:
            objtest.die_unless_instance(obj=widget, cls=QWidget)
            tooltip = widget.toolTip()
            if tooltip:
                if not guistr.is_rich(tooltip):
                    tooltip = '<qt>{}</qt>'.format(mls.tagify_newlines(mls.escape_ml(tooltip)))
                    widget.setToolTip(tooltip)
                    return True
        return super().eventFilter(widget, event)