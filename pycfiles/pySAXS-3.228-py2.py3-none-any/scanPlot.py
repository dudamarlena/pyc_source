# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\scanPlot.py
# Compiled at: 2018-08-23 04:07:58
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from scipy import optimize
import numpy, os
from numpy import *
import scipy, time, os, pySAXS
from pySAXS.guisaxs.qt import QtMatplotlib
from pySAXS.tools import specLogReader
from pySAXS.guisaxs.dataset import *
from pySAXS.models import Gaussian
from pySAXS.models import Trapez as MTRAPEZ
from pySAXS.models import Gaussian as MGAUSSIAN
from pySAXS.models import Capillary
from pySAXS.guisaxs.qt import dlgModel
from pySAXS.guisaxs.qt import preferences
ICON_PATH = pySAXS.__path__[0] + os.sep + 'guisaxs' + os.sep + 'images' + os.sep
import threading, time

class Intervallometre(threading.Thread):

    def __init__(self, duree, fonction, parent=None):
        threading.Thread.__init__(self)
        self.duree = duree
        self.fonction = fonction
        self.parent = parent
        self.encore = True

    def run(self):
        self.encore = True
        self.parent.ui.tableWidget.setEnabled(False)
        while self.encore:
            self.fonction()
            time.sleep(self.duree)

        self.parent.ui.tableWidget.setEnabled(True)
        print 'thread stopped'

    def stop(self):
        self.encore = False
        self.parent.ui.tableWidget.setEnabled(True)
        print 'thread stopped'


class scanPlot(QtWidgets.QDialog):

    def __init__(self, parent=None):
        self.data_dict = {}
        self.SelectedKey = None
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = uic.loadUi(pySAXS.UI_PATH + 'scanPlot.ui', self)
        if parent is not None:
            self.setWindowIcon(parent.windowIcon())
        filename = pySAXS.__path__[0] + os.sep + 'saxsdata' + os.sep + 'saxs_20170202.log'
        self.parent = parent
        if parent is not None:
            self.workingdirectory = parent.workingdirectory
            filename = self.parent.get('scanfile', section='spec')
        self.ui.changeFileButton.clicked.connect(self.OnClickFileButton)
        self.ui.tableWidget.cellClicked[(int, int)].connect(self.cellClicked)
        self.ui.BtnGaussian.clicked.connect(self.OnClickFitGaussian)
        self.ui.BtnTrapez.clicked.connect(self.OnClickFitTrapez)
        self.ui.BtnCapillary.clicked.connect(self.OnClickFitCapillary)
        self.ui.BtnRefresh.clicked.connect(self.OnClickRefresh)
        self.ui.buttonBox.clicked.connect(self.click)
        self.ui.BtnStartAuto.clicked.connect(self.StartAuto)
        self.ui.BtnStopAuto.clicked.connect(self.StopAuto)
        self.ui.BtnExport.clicked.connect(self.ExportData)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setRange(0, 1)
        self.move(QtCore.QPoint(100, 100))
        self.plotframe = QtMatplotlib.QtMatplotlib()
        self.plotframe.move(self.width() + self.x() + 15, self.y())
        self.plotframe.resize(self.plotframe.width(), self.height())
        self.plotframe.show()
        self.plotframe.set_marker('.')
        self.plotframe.setWindowTitle('SPEC Plot')
        self.ui.logfileEdit.setText(filename)
        self.FillList()
        self.th = None
        self.ui.show()
        return

    def click(self, obj=None):
        name = obj.text()
        if name == 'Close':
            self.close()
            self.plotframe.close()
        else:
            self.close()
            self.plotframe.close()

    def closeEvent(self, event):
        """
        when window is closed
        """
        if self.parent is not None:
            self.parent.pref.set('scanfile', section='spec', value=str(self.ui.logfileEdit.text()))
            self.parent.pref.save()
        try:
            self.th.encore = False
            self.plotframe.close()
        except:
            pass

        return

    def OnClickFileButton(self):
        """
        select a log file
        """
        filters = 'log Files (*.log);;All Files (*)'
        selected_filter = 'log (*.log)'
        fd = QtWidgets.QFileDialog(self)
        filename, truc = fd.getOpenFileName(filter='log Files (*.log);;All files *.* (*.*)')
        self.workingdirectory = filename
        self.ui.logfileEdit.setText(filename)
        self.FillList()

    def FillList(self):
        filename = self.ui.logfileEdit.text()
        self.scanList = specLogReader.readScanLog(filename)
        self.ui.tableWidget.setColumnCount(2)
        self.ui.tableWidget.setRowCount(len(self.scanList))
        headerNames = ['No', 'Scan']
        self.ui.tableWidget.setHorizontalHeaderLabels(headerNames)
        self.ui.tableWidget.setColumnWidth(0, 50)
        self.ui.tableWidget.setColumnWidth(1, 300)
        i = 0
        for item in sorted(self.scanList, reverse=True):
            scan = self.scanList[item]
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(scan.No)))
            self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(scan.description))
            self.ui.tableWidget.setRowHeight(i, 20)
            i += 1

        self.cellClicked(0, 0)

    def cellClicked(self, row, col):
        self.SelectedKey = int(self.ui.tableWidget.item(row, 0).text())
        self.data_dict = {}
        self.data_dict[self.SelectedKey] = dataset(str(self.SelectedKey))
        self.data_dict[self.SelectedKey].q = array(self.scanList[self.SelectedKey].x)
        self.data_dict[self.SelectedKey].i = array(self.scanList[self.SelectedKey].y)
        datax = self.data_dict[self.SelectedKey].q
        datay = self.data_dict[self.SelectedKey].i
        self.Replot()

    def OnClickRefresh(self):
        self.FillList()
        self.OnClickFitTrapez()

    def OnClickFitGaussian(self):
        if self.SelectedKey is not None:
            self.M = MGAUSSIAN()
            datax = self.data_dict[self.SelectedKey].q
            datay = self.data_dict[self.SelectedKey].i
            self.M.Arg = self.M.prefit(datax, datay)
            self.M.q = datax
            b = self.M.fit(datay)
            self.data_dict['pysaxs'] = dataset('pysaxs', datax, self.M.getIntensity(datax, b))
            self.Replot()
            reporttext = 'TRAPEZ Fit\n'
            for i in range(len(b)):
                reporttext += self.M.Doc[i] + ' : ' + str(b[i]) + '\n'

            self.plotframe.text(0.05, 0.05, reporttext)
        return

    def OnClickFitTrapez(self):
        if self.SelectedKey is not None:
            self.M = MTRAPEZ()
            datax = self.data_dict[self.SelectedKey].q
            datay = self.data_dict[self.SelectedKey].i
            if len(datax) > 10:
                self.M.Arg = self.M.prefit(datax, datay)
                self.M.q = datax
                b = self.M.fit(datay)
                self.data_dict['pysaxs'] = dataset('pysaxs', datax, self.M.getIntensity(datax, b))
                self.Replot()
                reporttext = ''
                for i in range(len(b)):
                    reporttext += self.M.Doc[i] + ' : ' + str(b[i]) + '\n'

                self.plotframe.text(0.05, 0.05, reporttext)
        return

    def OnClickFitCapillary(self):
        if self.SelectedKey is not None:
            self.M = Capillary()
            self.DisplayModelBox()
        return

    def DisplayModelBox(self):
        data_selected_for_model = self.SelectedKey
        new_dataname = str(data_selected_for_model) + '-' + self.M.name + ' model'
        q = self.data_dict[data_selected_for_model].q
        self.M.q = q
        i = self.M.getIntensity()
        filename = self.data_dict[data_selected_for_model].filename
        self.data_dict[new_dataname] = dataset(new_dataname, copy(q), copy(i), filename, True, self.M, parent=[
         data_selected_for_model], rawdata_ref=data_selected_for_model, type='model')
        self.childmodel = dlgModel.dlgModel(self, new_dataname, type='data')
        self.childmodel.show()

    def Replot(self):
        if self.SelectedKey is not None:
            self.plotframe.clearData()
            for key in self.data_dict:
                self.plotframe.addData(self.data_dict[key].q, self.data_dict[key].i)

            self.plotframe.replot()
        return

    def printTXT(self, txt='', par=''):
        """
        for printing messages
        """
        print str(txt) + str(par)

    def StartAuto(self):
        self.th = Intervallometre(5.0, self.OnClickRefresh, self)
        self.th.start()
        self.ui.progressBar.setRange(0, 0)

    def StopAuto(self):
        self.ui.tableWidget.setEnabled(True)
        self.th.encore = False
        self.ui.progressBar.setRange(0, 1)

    def ExportData(self):
        if self.SelectedKey is not None:
            datax = self.data_dict[self.SelectedKey].q
            datay = self.data_dict[self.SelectedKey].i
            filters = 'txt (*.txt);;log Files (*.log);;All Files (*)'
            fd = QtWidgets.QFileDialog(self)
            filename = fd.getSaveFileName(filter=filters)
            if filename != '':
                D = array([datax, datay])
                D = D.transpose()
                numpy.savetxt(str(filename), D, header='X\tY')
        return


def line(x, p):
    return p[0] * x + p[1]


def linef(x, p0, p1):
    return p0 * x + p1


def Gauss(x, p):
    h, w, f, b = p
    return Gaussf(x, h, w, f, b)


def Gaussf(q, h, w, f, b):
    sigm = f * (2 * numpy.log(2)) ** 0.5 / 2
    return (h - b) * numpy.exp(-(q - w) ** 2 / sigm ** 2) + b


def Trapez(x, p):
    c, f, s, h, z = p
    return Trapezf(x, c, f, s, h, z)


def Trapezf(x, center=0, fwmh=1, slope=1, height=1, zero=0):
    y = numpy.zeros(numpy.shape(x))
    for i in range(len(x)):
        if x[i] < center:
            y[i] = scipy.special.erf((x[i] - center + fwmh * 0.5) / slope)
        else:
            y[i] = -scipy.special.erf((x[i] - center - fwmh * 0.5) / slope)

    y = (y + 1) * 0.5 * height + zero
    return y


def fit_function(p0, datax, datay, function, **kwargs):
    errfunc = lambda p, x, y: function(x, p) - y
    pfit, pcov, infodict, errmsg, success = optimize.leastsq(errfunc, p0, args=(datax, datay), full_output=1, diag=1 / numpy.array(p0))
    if len(datay) > len(p0) and pcov is not None:
        s_sq = (errfunc(pfit, datax, datay) ** 2).sum() / (len(datay) - len(p0))
        pcov = pcov * s_sq
    else:
        pcov = inf
    error = []
    for i in range(len(pfit)):
        try:
            error.append(numpy.absolute(pcov[i][i]) ** 0.5)
        except:
            error.append(0.0)

    pfit_leastsq = pfit
    perr_leastsq = numpy.array(error)
    datayerrors = kwargs.get('datayerrors', None)
    curve_fit_function = kwargs.get('curve_fit_function', function)
    if datayerrors is None:
        pfit, pcov = optimize.curve_fit(curve_fit_function, datax, datay, p0=p0)
    else:
        pfit, pcov = optimize.curve_fit(curve_fit_function, datax, datay, p0=p0, sigma=datayerrors)
    error = []
    for i in range(len(pfit)):
        try:
            error.append(numpy.absolute(pcov[i][i]) ** 0.5)
        except:
            error.append(0.0)

    pfit_curvefit = pfit
    perr_curvefit = numpy.array(error)
    residuals = errfunc(pfit, datax, datay)
    s_res = numpy.std(residuals)
    ps = []
    for i in range(100):
        if datayerrors is None:
            randomDelta = numpy.random.normal(0.0, s_res, len(datay))
            randomdataY = datay + randomDelta
        else:
            randomDelta = numpy.array([ numpy.random.normal(0.0, derr, 1)[0] for derr in datayerrors
                                      ])
            randomdataY = datay + randomDelta
        randomfit, randomcov = optimize.leastsq(errfunc, p0, args=(datax, randomdataY), full_output=0)
        ps.append(randomfit)

    ps = numpy.array(ps)
    mean_pfit = numpy.mean(ps, 0)
    Nsigma = 1.0
    err_pfit = Nsigma * numpy.std(ps, 0)
    pfit_bootstrap = mean_pfit
    perr_bootstrap = err_pfit
    return (
     pfit_leastsq, pfit_bootstrap)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = scanPlot()
    myapp.show()
    sys.exit(app.exec_())