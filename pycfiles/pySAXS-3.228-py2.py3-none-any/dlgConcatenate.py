# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\dlgConcatenate.py
# Compiled at: 2019-03-21 10:02:02
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from pySAXS.tools import isNumeric
from pySAXS.guisaxs import dataset
import numpy, pySAXS

class DataElement:
    enabled = True
    qmin = 0.0
    qmax = 1.1

    def __init__(self, enabled, qmin, qmax):
        self.enabled = enabled
        self.qmin = qmin
        self.qmax = qmax


class dlgConcatenate(QtWidgets.QDialog):

    def __init__(self, parentwindow, newdatasetname=''):
        QtWidgets.QDialog.__init__(self)
        self.ui = uic.loadUi(pySAXS.UI_PATH + 'dlgConcatenate.ui', self)
        self.parentwindow = parentwindow
        self.data_dict = parentwindow.data_dict
        self.newdatasetname = newdatasetname
        self.mydata = {}
        self.dataInWidget = []
        self.ConstructUI()
        self.ui.buttonBox.clicked.connect(self.click)
        self.pushButtonDOWN.clicked.connect(self.OnPushButtonDOWNclicked)
        self.pushButtonUP.clicked.connect(self.OnPushButtonUPclicked)
        self.tableWidget.cellChanged.connect(self.OnCellChanged)

    def ConstructUI(self):
        self.lineEditNewName.setText(self.newdatasetname)
        for label in self.data_dict:
            if self.data_dict[label].checked:
                self.dataInWidget.append(label)
                qmin = self.data_dict[label].q.min()
                qmax = self.data_dict[label].q.max()
                self.mydata[label] = DataElement(True, qmin, qmax)

        self.ConstructTableWidget()

    def ConstructTableWidget(self):
        self.tableWidget.clearContents()
        m = 0
        self.tableWidget.setRowCount(len(self.dataInWidget))
        for label in self.dataInWidget:
            vitem = QtWidgets.QTableWidgetItem()
            vitem.setText(label)
            self.tableWidget.setVerticalHeaderItem(m, vitem)
            newitem = QtWidgets.QTableWidgetItem('')
            newitem.setCheckState(QtCore.Qt.Checked)
            self.tableWidget.setItem(m, 0, newitem)
            newitem = QtWidgets.QTableWidgetItem(str(self.mydata[label].qmin))
            self.tableWidget.setItem(m, 1, newitem)
            newitem = QtWidgets.QTableWidgetItem(str(self.mydata[label].qmax))
            self.tableWidget.setItem(m, 2, newitem)
            m += 1

    def OnCellChanged(self, row=None, column=None):
        if row is None or column is None:
            return
        label = self.dataInWidget[row]
        val = str(self.tableWidget.item(row, column).text())
        if column == 0:
            self.mydata[label].enabled = self.tableWidget.item(row, column).checkState() == 2
            return
        else:
            if not isNumeric.isNumeric(val):
                brush = QtGui.QBrush(QtGui.QColor(QtCore.Qt.cyan))
                brush.setStyle(QtCore.Qt.SolidPattern)
                self.tableWidget.item(row, column).setBackground(brush)
                return
            val = float(val)
            if column == 1:
                self.mydata[label].qmin = val
            elif column == 2:
                self.mydata[label].qmax = val
            brush = QtGui.QBrush(QtGui.QColor(QtCore.Qt.white))
            brush.setStyle(QtCore.Qt.SolidPattern)
            self.tableWidget.item(row, column).setBackground(brush)
            return

    def click(self, obj=None):
        """
        user clicked on the button box
        """
        name = obj.text()
        if name == 'Close':
            self.close()
        elif name == 'Apply':
            self.concatenateDatas()
            self.newdatasetname = str(self.lineEditNewName.text())
            self.parentwindow.data_dict[self.newdatasetname] = dataset.dataset(self.newdatasetname, self.newdatasetq, self.newdataseti, error=self.newdatasete)
            self.parentwindow.redrawTheList()
            self.parentwindow.Replot()
        else:
            self.close()

    def OnPushButtonDOWNclicked(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            return
        if row >= len(self.dataInWidget) - 1:
            return
        temp = self.dataInWidget[row]
        self.dataInWidget[row] = self.dataInWidget[(row + 1)]
        self.dataInWidget[row + 1] = temp
        self.ConstructTableWidget()
        self.tableWidget.setCurrentCell(row + 1, 0)

    def OnPushButtonUPclicked(self):
        row = self.tableWidget.currentRow()
        if row <= 0:
            return
        temp = self.dataInWidget[row]
        self.dataInWidget[row] = self.dataInWidget[(row - 1)]
        self.dataInWidget[row - 1] = temp
        self.ConstructTableWidget()
        self.tableWidget.setCurrentCell(row - 1, 0)

    def concatenateDatas(self):
        """
        create the new datas
        """
        first = True
        for label in self.mydata:
            dataset = self.mydata[label]
            if dataset.enabled:
                print 'clip : ' + label
                newq, newi, newe = self.clipDatas(label, dataset.qmin, dataset.qmax)
                if first:
                    self.newdatasetq = newq
                    self.newdataseti = newi
                    self.newdatasete = newe
                    first = False
                else:
                    self.newdatasetq = numpy.concatenate((self.newdatasetq, newq))
                    self.newdataseti = numpy.concatenate((self.newdataseti, newi))
                    if newe is not None and self.newdatasete is not None:
                        self.newdatasete = numpy.concatenate((self.newdatasete, newe))

        sortedIndexes = numpy.argsort(self.newdatasetq)
        print sortedIndexes
        print len(sortedIndexes)
        print len(self.newdatasete)
        self.newdatasetq = self.newdatasetq[sortedIndexes]
        self.newdataseti = self.newdataseti[sortedIndexes]
        if self.newdatasete is not None:
            self.newdatasete = self.newdatasete[sortedIndexes]
        return

    def clipDatas(self, datasetname, qmin, qmax):
        """
        return q and i clipped
        """
        q = self.data_dict[datasetname].q
        i = self.data_dict[datasetname].i
        if self.data_dict[datasetname].error is not None:
            e = self.data_dict[datasetname].error
            e = numpy.repeat(e, (q >= qmin) & (q <= qmax))
        else:
            e = None
        i = numpy.repeat(i, (q >= qmin) & (q <= qmax))
        q = numpy.repeat(q, (q >= qmin) & (q <= qmax))
        return (
         q, i, e)

    def getValues(self):
        return (
         self.listCheckBox, self.listlabel0, self.listQmin, self.listQmax)