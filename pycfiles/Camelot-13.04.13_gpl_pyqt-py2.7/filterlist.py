# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/filterlist.py
# Compiled at: 2013-04-11 17:47:52
"""Controls to filter data"""
import logging
logger = logging.getLogger('camelot.view.controls.filter')
from PyQt4 import QtGui, QtCore

class FilterList(QtGui.QWidget):
    """A list with filters that can be applied on a query in the tableview"""
    filters_changed_signal = QtCore.pyqtSignal()

    def __init__(self, items, parent):
        """
    :param items: list of tuples (filter, (name, choices)) for constructing the different filterboxes
    """
        super(FilterList, self).__init__(parent)
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(4)
        for filter, filter_data in items:
            filter_widget = filter.render(filter_data, parent=self)
            layout.addWidget(filter_widget)
            filter_widget.filter_changed_signal.connect(self.emit_filters_changed)

        layout.addStretch()
        self.setLayout(layout)
        if len(items) == 0:
            self.setMaximumWidth(0)
        else:
            self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)

    def decorate_query(self, query):
        for i in range(self.layout().count()):
            if self.layout().itemAt(i).widget():
                query = self.layout().itemAt(i).widget().decorate_query(query)

        return query

    @QtCore.pyqtSlot()
    def emit_filters_changed(self):
        logger.debug('filters changed')
        self.filters_changed_signal.emit()