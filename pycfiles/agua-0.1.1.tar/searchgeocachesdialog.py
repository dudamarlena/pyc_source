# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/qt/searchgeocachesdialog.py
# Compiled at: 2011-04-23 08:43:29
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import geocaching
from searchresultsdialog import QtSearchResultsDialog
from ui_searchgeocachesdialog import Ui_SearchGeocachesDialog
d = lambda x: x.decode('utf-8')
logger = logging.getLogger('qtsearchgeocachesdialog')

class QtSearchGeocachesDialog(Ui_SearchGeocachesDialog, QDialog):
    RADI = [
     1, 2, 3, 5, 10, 15, 20, 50, 100]
    TYPELIST = [
     (
      'traditional', geocaching.GeocacheCoordinate.TYPE_REGULAR),
     (
      'multi stage', geocaching.GeocacheCoordinate.TYPE_MULTI),
     (
      'virtual', geocaching.GeocacheCoordinate.TYPE_VIRTUAL),
     (
      'earth', geocaching.GeocacheCoordinate.TYPE_EARTH),
     (
      'event', geocaching.GeocacheCoordinate.TYPE_EVENT),
     (
      'mystery', geocaching.GeocacheCoordinate.TYPE_MYSTERY),
     (
      'webcam', geocaching.GeocacheCoordinate.TYPE_WEBCAM),
     (
      'all/other', geocaching.GeocacheCoordinate.TYPE_UNKNOWN)]

    def __init__(self, core, map_position, user_position, parent=None):
        QDialog.__init__(self, parent)
        self.core = core
        self.setupUi(self)
        self.populateUi()
        self.setModal(True)
        self.dialogButtonBox.clicked.connect(self.__button_clicked)
        self.map_position = map_position
        self.user_position = user_position

    def populateUi(self):
        for (name, type) in self.TYPELIST:
            m = QListWidgetItem(name, self.listWidgetType)
            m.setCheckState(Qt.Unchecked if type == geocaching.GeocacheCoordinate.TYPE_UNKNOWN else Qt.Checked)

        self.comboBoxLocation.currentIndexChanged.connect(self.__combo_box_changed)

    def __combo_box_changed(self, index):
        self.spinBoxRadius.setEnabled(index != 0)
        if index == 1:
            text = self.map_position.get_latlon() if self.map_position != None else 'not available'
        elif index == 2:
            text = self.user_position.get_latlon() if self.user_position != None else 'not available'
        else:
            text = ''
        self.labelLocation.setText(d(text))
        return

    def show(self):
        QDialog.show(self)

    def __button_clicked(self, button):
        id = self.dialogButtonBox.standardButton(button)
        if id == QDialogButtonBox.Ok:
            self.__start_search()

    def __start_search(self):
        name = str(self.lineEditName.text()).strip().lower()
        if name == '':
            name = None
        logger.debug('Name: %s' % name)
        i = self.comboBoxLocation.currentIndex()
        if i == 1 and self.map_position != None:
            center = self.map_position
        elif i == 2 and self.user_position != None:
            center = self.user_position
        else:
            center = None
        if center != None:
            radius = self.spinBoxRadius.value()
            sqrt_2 = 1.41421356
            c1 = center.transform(-45, radius * 1000 * sqrt_2)
            c2 = center.transform(135, radius * 1000 * sqrt_2)
            location = (c2, c1)
            logger.debug('Location: %s %s' % location)
        else:
            location = None
            logger.debug('Location: None')
        types = [ self.TYPELIST[x][1] for x in range(self.listWidgetType.count()) if self.listWidgetType.item(x).checkState() == Qt.Checked ]
        if geocaching.GeocacheCoordinate.TYPE_UNKNOWN in types:
            types = None
        logger.debug('Types: %s' % types)
        if self.checkBoxHideFound.checkState() == Qt.Checked:
            found = False
        else:
            found = None
        logger.debug('Found: %s' % found)
        if self.checkBoxShowOnlyMarked.checkState() == Qt.Checked:
            marked = True
        else:
            marked = False
        logger.debug('Marked: %s' % marked)
        sizes = [ x + 1 for x in range(self.listWidgetSize.count()) if self.listWidgetSize.item(x).checkState() == Qt.Checked ]
        if sizes == [1, 2, 3, 4, 5]:
            sizes = None
        logger.debug('Sizes: %s' % sizes)
        r = lambda x: int(x / 0.5) * 0.5
        diff_min = r(self.doubleSpinBoxDifficultyMin.value())
        diff_max = r(self.doubleSpinBoxDifficultyMax.value() + 0.5)
        if diff_min == 1 and diff_max == 5.5:
            difficulties = None
        else:
            difficulties = [ x / 10.0 for x in range(int(diff_min * 10), int(diff_max * 10), 5) ]
        logger.debug('Difficulties: %s' % difficulties)
        terr_min = r(self.doubleSpinBoxTerrainMin.value())
        terr_max = r(self.doubleSpinBoxTerrainMax.value() + 0.5)
        if terr_min == 1 and terr_max == 5.5:
            terrains = None
        else:
            terrains = [ x / 10.0 for x in range(int(terr_min * 10), int(terr_max * 10), 5) ]
        logger.debug('Terrains: %s' % terrains)
        results = self.core.get_points_filter(found=found, name_search=name, size=sizes, terrain=terrains, diff=difficulties, ctype=types, marked=marked, location=location)
        logger.debug('Found %d results' % len(results[0]))
        self.__show_results(results)
        return

    def __show_results(self, results):
        d = QtSearchResultsDialog(self.core)
        d.show(results[0])