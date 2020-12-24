# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/qt/searchdialog.py
# Compiled at: 2011-04-23 08:43:29
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import geo
from ui_searchdialog import Ui_SearchDialog
d = lambda x: x.decode('utf-8')
logger = logging.getLogger('qtsearchdialog')

class QtSearchDialog(Ui_SearchDialog, QDialog):
    locationSelected = pyqtSignal(geo.Coordinate)

    def __init__(self, core, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.core = core
        self.pushButtonSearch.clicked.connect(self.__start_search)
        self.listWidgetResults.itemClicked.connect(self.__return_location)

    def __start_search(self):
        search_text = unicode(self.lineEditSearch.text()).strip()
        if search_text == '':
            return
        try:
            self.results = self.core.search_place(search_text)
        except Exception, e:
            QErrorMessage.qtHandler().showMessage(repr(e))
            logger.exception(repr(e))
            return

        self.listWidgetResults.clear()
        if len(self.results) == 0:
            QMessageBox.information(self, 'Search results', 'The search returned no results.')
            return
        i = 0
        if self.core.current_position == None:
            for res in self.results:
                m = QListWidgetItem('res.<i>name</i>', self.listWidgetResults)
                m.setData(Qt.UserRole, QVariant(i))
                i += 1

        else:
            pos = self.core.current_position
            for res in self.results:
                distance = geo.Coordinate.format_distance(res.distance_to(pos))
                direction = geo.Coordinate.format_direction(pos.bearing_to(res))
                text = '%s <b>(%s %s)</b>' % (res.name, distance, direction)
                m = QListWidgetItem(text, self.listWidgetResults)
                m.setData(Qt.UserRole, QVariant(i))
                i += 1

            return

    def __return_location(self, item):
        res = self.results[item.data(Qt.UserRole).toInt()[0]]
        logger.debug('Setting center to %s' % res)
        self.locationSelected.emit(res)