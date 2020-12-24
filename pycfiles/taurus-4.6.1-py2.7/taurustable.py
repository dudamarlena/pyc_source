# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/table/taurustable.py
# Compiled at: 2019-08-19 15:09:30
"""This module provides a base widget that can be used to display a taurus
model in a table widget"""
from __future__ import absolute_import
from taurus.qt.qtgui.model import TaurusBaseModelWidget
from .qtable import QBaseTableWidget
__all__ = [
 'TaurusBaseTableWidget']
__docformat__ = 'restructuredtext'

class TaurusBaseTableWidget(QBaseTableWidget, TaurusBaseModelWidget):
    """A class:`taurus.qt.qtgui.tree.QBaseTableWidget` that connects to a
    taurus model.

    Filters can be inserted into this widget to restrict the items that are
    seen."""

    def __init__(self, parent=None, designMode=False, with_filter_widget=True, perspective=None, proxy=None):
        self.call__init__(QBaseTableWidget, parent, designMode=designMode, with_filter_widget=with_filter_widget, perspective=perspective, proxy=proxy)
        self.call__init__(TaurusBaseModelWidget, designMode=designMode)