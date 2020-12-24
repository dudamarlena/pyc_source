# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/qt/searchresultsdialog.py
# Compiled at: 2011-04-23 08:43:29
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import geo
from qt.mapwidget import QtGeocacheLayer
from qt.mapwidget import QtMap, QtOsdLayer
from ui_searchresultsdialog import Ui_SearchResultsDialog
logger = logging.getLogger('qtsearchresultsdialog')
d = lambda x: x.decode('utf-8')

class QtSearchResultsDialog(Ui_SearchResultsDialog, QDialog):

    def __init__(self, core, parent=None):
        QDialog.__init__(self, parent)
        self.core = core
        self.setupUi(self)
        self.setup_ui_custom()
        self.results = []
        self.selected_results = []

    def show(self, results):
        QDialog.show(self)
        self.results = results
        self.tableWidgetResults.clearContents()
        self.tableWidgetResults.setRowCount(len(results))
        row = 0
        max_size_first_col = 0
        for g in results:
            col = 0
            items = self.__make_items(g)
            max_size_first_col = max(max_size_first_col, items[0].sizeHint().width())
            for item in items:
                self.tableWidgetResults.setItem(row, col, item)
                col += 1

            row += 1

        self.tableWidgetResults.resizeColumnsToContents()
        self.tableWidgetResults.setColumnWidth(0, 300)
        self.tableWidgetResults.selectAll()

    def __make_items(self, cache):
        start = QTableWidgetItem(d(cache.title))
        if self.core.current_position != None:
            distance = geo.Coordinate.format_distance(self.core.current_position.distance_to(cache))
            direction = geo.Coordinate.format_direction(self.core.current_position.bearing_to(cache))
            last = QTableWidgetItem('%s %s' % (distance, direction))
        else:
            last = QTableWidgetItem('?')
        entries = [start,
         QTableWidgetItem(d(cache.get_size_string())),
         QTableWidgetItem(d(cache.get_terrain())),
         QTableWidgetItem(d(cache.get_difficulty())),
         last]
        cache.item = start
        return entries

    def setup_ui_custom(self):
        self.map = QtMap(self, geo.Coordinate(0, 0), 1)
        self.geocacheLayer = QtGeocacheLayer(self.__get_geocaches_callback, self.__show_cache)
        self.osdLayer = QtOsdLayer()
        self.map.add_layer(self.geocacheLayer)
        self.map.add_layer(self.osdLayer)
        self.layout().insertWidget(1, self.map)
        self.map.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.map.show()
        self.centralLayout = QVBoxLayout()
        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.tableWidgetResults)
        self.splitter.addWidget(self.map)
        self.centralLayout.addWidget(self.splitter)
        self.centralLayout.addWidget(self.pushButtonExportSelected)
        l = self.layout()
        l.deleteLater()
        QCoreApplication.sendPostedEvents(l, QEvent.DeferredDelete)
        self.setLayout(self.centralLayout)
        self.splitter.setSizes([1000, 1000])
        self.tableWidgetResults.itemSelectionChanged.connect(self.__selection_changed)

    def __selection_changed(self):
        self.selected_results = [ c for c in self.results if self.tableWidgetResults.isItemSelected(c.item) ]
        if len(self.selected_results) > 0:
            self.map.fit_to_bounds(*geo.Coordinate.get_bounds(self.selected_results))

    def __get_geocaches_callback(self, visible_area, maxresults):
        return [ x for x in self.selected_results if self.map.in_area(x, visible_area) ]

    def __show_cache(self, cache):
        pass