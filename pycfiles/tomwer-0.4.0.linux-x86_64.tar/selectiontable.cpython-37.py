# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/samplemoved/selectiontable.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 9078 bytes
"""Some widget construction to check if a sample moved"""
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '19/03/2018'
import os
from collections import OrderedDict
import functools
from silx.gui import qt
from silx.io.url import DataUrl
from tomwer.gui.imagefromfile import FileWithImage, ImageFromFile
from tomwer.core.log import TomwerLogger
logger = TomwerLogger(__name__)

class SelectionTable(qt.QTableWidget):
    __doc__ = 'Table used to select the color channel to be displayed for each'
    COLUMS_INDEX = OrderedDict([
     ('url', 0),
     ('img A', 1),
     ('img B', 2)])
    sigImageAChanged = qt.Signal(str)
    sigImageBChanged = qt.Signal(str)

    def __init__(self, parent=None):
        qt.QTableWidget.__init__(self, parent)
        self.clear()

    def clear(self):
        qt.QTableWidget.clear(self)
        self.setRowCount(0)
        self.setColumnCount(len(self.COLUMS_INDEX))
        self.setHorizontalHeaderLabels(list(self.COLUMS_INDEX.keys()))
        self.verticalHeader().hide()
        if hasattr(self.horizontalHeader(), 'setSectionResizeMode'):
            self.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        else:
            self.horizontalHeader().setResizeMode(0, qt.QHeaderView.Stretch)
        self.setSortingEnabled(True)
        self._checkBoxes = {}

    def addRadio(self, name, **kwargs):
        if isinstance(name, DataUrl):
            (self.addUrl)(name, **kwargs)
        else:
            if not os.path.isfile(name):
                raise AssertionError
            else:
                os.path.isfile(name) or logger.error('%s is not a file path' % name)
                return
            imgFile = FileWithImage(name)
            for imgFrmFile in imgFile.getImages(_load=False):
                (self.addUrl)((imgFrmFile.url), **kwargs)

    def addUrl(self, url, **kwargs):
        """
        
        :param url: 
        :param args: 
        :return: index of the created items row
        :rtype int
        """
        assert isinstance(url, DataUrl)
        row = self.rowCount()
        self.setRowCount(row + 1)
        data_path_label = qt.QLabel(url.path())
        self.setCellWidget(row, self.COLUMS_INDEX['url'], data_path_label)
        widgetImgA = qt.QCheckBox(self)
        self.setCellWidget(row, self.COLUMS_INDEX['img A'], widgetImgA)
        callbackImgA = functools.partial(self._activeImgAChanged, url.path())
        widgetImgA.toggled.connect(callbackImgA)
        widgetImgB = qt.QCheckBox(self)
        self.setCellWidget(row, self.COLUMS_INDEX['img B'], widgetImgB)
        callbackImgB = functools.partial(self._activeImgBChanged, url.path())
        widgetImgB.toggled.connect(callbackImgB)
        self._checkBoxes[url.path()] = {'img A':widgetImgA, 
         'img B':widgetImgB}
        return row

    def _activeImgAChanged(self, name):
        self._updatecheckBoxes('img A', name)
        self.sigImageAChanged.emit(name)

    def _activeImgBChanged(self, name):
        self._updatecheckBoxes('img B', name)
        self.sigImageBChanged.emit(name)

    def _updatecheckBoxes(self, whichImg, name):
        assert name in self._checkBoxes
        assert whichImg in self._checkBoxes[name]
        if self._checkBoxes[name][whichImg].isChecked():
            for radioUrl in self._checkBoxes:
                if radioUrl != name:
                    self._checkBoxes[radioUrl][whichImg].blockSignals(True)
                    self._checkBoxes[radioUrl][whichImg].setChecked(False)
                    self._checkBoxes[radioUrl][whichImg].blockSignals(False)

    def getSelection(self):
        """

        :return: url selected for img A and img B.
        """
        imgA = imgB = None
        for radioUrl in self._checkBoxes:
            if self._checkBoxes[radioUrl]['img A'].isChecked():
                imgA = radioUrl
            if self._checkBoxes[radioUrl]['img B'].isChecked():
                imgB = radioUrl

        return (
         imgA, imgB)

    def setSelection(self, url_img_a, url_img_b):
        """

        :param ddict: key: image url, values: list of active channels
        """
        for radioUrl in self._checkBoxes:
            for img in ('img A', 'img B'):
                self._checkBoxes[radioUrl][img].blockSignals(True)
                self._checkBoxes[radioUrl][img].setChecked(False)
                self._checkBoxes[radioUrl][img].blockSignals(False)

        self._checkBoxes[radioUrl][img].blockSignals(True)
        self._checkBoxes[url_img_a]['img A'].setChecked(True)
        self._checkBoxes[radioUrl][img].blockSignals(False)
        self._checkBoxes[radioUrl][img].blockSignals(True)
        self._checkBoxes[url_img_b]['img B'].setChecked(True)
        self._checkBoxes[radioUrl][img].blockSignals(False)
        self.sigImageAChanged.emit(url_img_a)
        self.sigImageBChanged.emit(url_img_b)


class AngleSelectionTable(SelectionTable):
    __doc__ = 'The selection table but with the angle column.\n    Allows to make selection on angles to\n    '

    class _AngleItem(qt.QTableWidgetItem):
        __doc__ = 'Simple QTableWidgetItem allowing ordering on angles'

        def __init__(self, type=qt.QTableWidgetItem.Type):
            qt.QTableWidgetItem.__init__(self, type=type)

        def __lt__(self, other):
            a1 = IntAngle(self.text())
            a2 = IntAngle(other.text())
            return a1 < a2

    COLUMS_INDEX = OrderedDict([
     ('angle', 0),
     ('file name', 1),
     ('url', 2),
     ('img A', 3),
     ('img B', 4)])

    def __init__(self, parent):
        SelectionTable.__init__(self, parent)
        self._anglesToUrl = {}

    def addUrl(self, url, **kwargs):
        assert 'angle' in kwargs
        row = (SelectionTable.addUrl)(self, url, **kwargs)
        _item = qt.QTableWidgetItem()
        _item.setText(os.path.basename(url.file_path()))
        _item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
        self.setItem(row, self.COLUMS_INDEX['file name'], _item)
        angle = '???'
        if 'angle' in kwargs:
            angle = kwargs['angle']
        item = self._AngleItem()
        item.setText(str(angle))
        self.setItem(row, self.COLUMS_INDEX['angle'], item)
        self._anglesToUrl[angle] = url.path()

    def setAngleSelection(self, angle_a, angle_b):
        url_angle_a = url_angle_b = None
        if angle_a in self._anglesToUrl:
            url_angle_a = self._anglesToUrl[angle_a]
        if angle_b in self._anglesToUrl:
            url_angle_b = self._anglesToUrl[angle_b]
        self.setSelection(url_angle_a, url_angle_b)

    def clear(self):
        SelectionTable.clear(self)
        self._anglesToUrl = {}


class IntAngle(str):
    __doc__ = 'Simple class used to order angles'

    def __new__(cls, *args, **kwargs):
        return (str.__new__)(cls, *args, **kwargs)

    def getAngle(self):
        """Return the acquisition angle as an int"""
        val = self
        if '(' in self:
            val = self.split('(')[0]
        if val.isdigit() is False:
            return False
        return int(val)

    def getAngleN(self):
        """Return the second information if the acquisition is the first
        one taken at this angle or not."""
        if '(' not in self:
            return 0
        return int(self.split('(')[1][:-1])

    def __lt__(self, other):
        if self.getAngle() == other.getAngle():
            return self.getAngleN() < other.getAngleN()
        return self.getAngle() < other.getAngle()