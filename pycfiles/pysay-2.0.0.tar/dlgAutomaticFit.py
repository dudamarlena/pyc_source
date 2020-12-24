# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\dlgAutomaticFit.py
# Compiled at: 2019-10-10 09:24:55
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pySAXS
from time import *
import sys
from pySAXS.tools import isNumeric
from pySAXS.tools import filetools
from pySAXS.guisaxs import dataset
from pySAXS.tools.isNumeric import *
from copy import copy
import numpy
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.patches as patches
from pySAXS.models import SpherePolyWBC
MODEL = SpherePolyWBC.SphereOTBackgdBC()
MODEL_PARAM = [0, 1, 2]

class dlgAutomaticFit(QtWidgets.QDialog):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(pySAXS.UI_PATH + 'dlgAutomaticFit.ui', self)
        self.parent = parent
        self.Model = MODEL
        self.imodel = None
        self.i = None
        self.oldI = None
        self.err = None
        self.FitParamList = []
        self.FitParamName = []
        self.par = self.Model.getArg()
        self.argbounds = self.Model.getArgBounds()
        self.itf = self.Model.getIstofit()
        self.qbase = copy(self.Model.q)
        self.ParDoc = []
        self.ParText = []
        self.MinText = []
        self.MaxText = []
        self.ParUncert = []
        self.SlideMax = 1000
        self.CheckFit = []
        self.slider = []
        self.fitexp = 0
        self.qmax = None
        self.backupArg = None
        self.type = type
        self.setWindowTitle(self.Model.Description)
        self.constructUI()
        self.ui.show()
        return

    def constructUI(self):
        """
        construct the UI
        """
        self.plt = self.ui.matplotlibwidget.figure
        self.canvas = FigureCanvas(self.plt)
        self.axes = self.plt.add_subplot(111)
        self.clbar = None
        self.plt.tight_layout()
        self.axes.hold()
        self.plt2 = self.ui.matplotlibwidget_2.figure
        self.canvas2 = FigureCanvas(self.plt2)
        self.axes2 = self.plt2.subplots(len(MODEL_PARAM), 1)
        self.lines = []
        for ax in self.axes2:
            ll, = ax.plot([], [], '.')
            self.lines.append(ll)

        for i in range(len(self.par)):
            item = QtWidgets.QLabel(self.ui.gbParameters)
            item.setText(self.Model.Doc[i] + ' : ')
            self.ui.gridParameters.addWidget(item, i + 1, 0, 1, 1)
            self.ParDoc.append(item)
            item = QtWidgets.QLineEdit(self.ui.gbParameters)
            item.setText(self.Model.Format[i] % self.par[i])
            self.ui.gridParameters.addWidget(item, i + 1, 1, 1, 1)
            item.textChanged.connect(self.onModelUpdate)
            item.setFixedWidth(75)
            self.ParText.append(item)
            item = QtWidgets.QLabel(self.ui.gbParameters)
            item.setText('-')
            item.setFixedWidth(70)
            item.setStyleSheet('color: blue')
            self.ui.gridParameters.addWidget(item, i + 1, 2, 1, 1)
            self.ParUncert.append(item)
            item = QtWidgets.QCheckBox(self.ui.gbParameters)
            item.setFixedWidth(20)
            item.setChecked(self.Model.istofit[i])
            self.ui.gridParameters.addWidget(item, i + 1, 3, 1, 1)
            self.ui.CheckFit.append(item)
            item = QtWidgets.QLineEdit(self.ui.gbParameters)
            if self.argbounds[i] is None:
                min = 0.0 * self.par[i]
            else:
                min = self.argbounds[i][0]
            item.setText(self.Model.Format[i] % min)
            item.setFixedWidth(75)
            self.ui.MinText.append(item)
            item.editingFinished.connect(self.onModelUpdate)
            self.ui.gridParameters.addWidget(item, i + 1, 4, 1, 1)
            item = QtWidgets.QLineEdit(self.ui.gbParameters)
            item.setFixedWidth(75)
            if self.argbounds[i] is None:
                max = 2.0 * self.par[i]
            else:
                max = self.argbounds[i][1]
            item.setText(self.Model.Format[i] % max)
            self.ui.MaxText.append(item)
            item.editingFinished.connect(self.onModelUpdate)
            self.ui.gridParameters.addWidget(item, i + 1, 5, 1, 1)

        choicelist = ['Normal', 'I/q', 'I/q^2', 'I/q^3', 'I/q^4', 'log(I)']
        self.radioList = []
        i = 0
        for choice in choicelist:
            item = QtWidgets.QRadioButton(self.ui.groupPlotExp)
            self.ui.gridLayoutPlotExp.addWidget(item, 0, i, 1, 1)
            item.setText(choice)
            self.ui.radioList.append(item)
            i += 1

        self.ui.radioList[0].setChecked(True)
        self.ui.btnBack.setEnabled(False)
        self.ui.btnBack.clicked.connect(self.onBack)
        self.qbase = self.Model.q
        qmin = self.qbase[0]
        qmax = self.qbase[(-1)]
        self.qminIndex = 0
        self.qmaxIndex = len(self.qbase) - 1
        self.ui.editQmin.setText('%6.5f' % qmin)
        self.ui.editQmax.setText('%6.5f' % qmax)
        self.ui.editQminVal.setText('%6.5f' % qmin)
        self.ui.editQmaxVal.setText('%6.5f' % qmax)
        self.ui.sliderQmin.setMinimum(0)
        self.ui.sliderQmax.setMinimum(0)
        self.ui.sliderQmin.setMaximum(self.qmaxIndex)
        self.ui.sliderQmax.setMaximum(self.qmaxIndex)
        self.ui.sliderQmin.setValue(0)
        self.ui.sliderQmax.setValue(self.qmaxIndex)
        self.ui.sliderQmin.valueChanged.connect(self.onSliderQminChange)
        self.ui.sliderQmax.valueChanged.connect(self.onSliderQmaxChange)
        self.ui.editQminVal.textChanged.connect(self.onQminEditChange)
        self.ui.editQmaxVal.textChanged.connect(self.onQmaxEditChange)
        self.ui.edit_subConstant.textChanged.connect(self.Replot)
        self.ui.btnFit.clicked.connect(self.onFitLMFIT)
        self.ui.btnBack.setEnabled(False)
        self.ui.btnBack.clicked.connect(self.onBack)
        self.onModelUpdate()
        return

    def onModelUpdate(self, calculate=True):
        """
        when a parameter is updated
        """
        if not self.updateFit.isChecked():
            return
        self.bounds = []
        for i in range(len(self.Model.Arg)):
            if not isNumeric(str(self.ParText[i].text())):
                return
            self.par[i] = float(eval(str(self.ParText[i].text())))
            self.itf[i] = self.CheckFit[i].isChecked()
            bmin = str(self.MinText[i].text())
            bmax = str(self.MaxText[i].text())
            self.bounds.append((bmin, bmax))

        self.Model.setIstofit(self.itf)
        self.Model.setArg(self.par)
        qmin = float(self.ui.editQmin.text())
        qmax = float(self.ui.editQmax.text())
        self.qminIndex = self.ui.sliderQmin.value()
        self.qmaxIndex = self.ui.sliderQmax.value()
        if self.qminIndex != 0 or self.qmaxIndex != len(self.qbase) - 1:
            self.Model.q = self.qbase[self.qminIndex:self.qmaxIndex]
        if not calculate:
            return
        self.imodel = self.Model.getIntensity(self.Model.q)
        self.qmodel = copy(self.Model.q)
        self.Replot()

    def Replot(self):
        self.axes.cla()
        if self.i is not None:
            if self.ui.chkSubstractConstant.isChecked():
                self.axes.plot(self.qbase, self.i, 'b*')
            else:
                self.axes.plot(self.qbase, self.i - float(self.ui.edit_subConstant.text()), '*')
        if self.oldI is not None:
            self.axes.plot(self.qbase, self.oldI, 'g.')
        if self.imodel is not None:
            self.axes.plot(self.qmodel, self.imodel, 'r-')
        self.axes.set_xscale('log')
        self.axes.set_yscale('log')
        self.axes.get_xaxis().grid(True)
        self.axes.get_yaxis().grid(True)
        self.ui.matplotlibwidget.draw()
        return

    def ReplotFit(self):
        if len(self.FitParamList) <= 0:
            return
        aa = numpy.array(self.FitParamList).transpose()
        n = 0
        for i in MODEL_PARAM:
            self.axes2[n].cla()
            self.axes2[n].plot(aa[i])
            n += 1

        self.ui.matplotlibwidget_2.draw()
        self.ui.matplotlibwidget_2.flush_events()

    def tryFitThis(self, dataname):
        data = self.parent.data_dict[dataname]
        self.dataname = dataname
        self.setQbase(data.q)
        if self.i is not None:
            self.oldI = self.i
        if self.ui.chkSubstractConstant.isChecked():
            self.i = data.i - float(self.ui.edit_subConstant.text())
        else:
            self.i = data.i
        self.err = data.error
        self.ui.btnFit.setEnabled(True)
        self.Replot()
        if self.ui.chkSubstractConstant.isChecked():
            self.onFitLMFIT()
        return

    def setQbase(self, q):
        if self.i is None:
            self.qbase = q
            qmin = self.qbase[0]
            qmax = self.qbase[(-1)]
            self.qminIndex = 0
            self.qmaxIndex = len(self.qbase) - 1
            self.ui.editQmin.setText('%6.5f' % qmin)
            self.ui.editQmax.setText('%6.5f' % qmax)
            self.ui.editQminVal.setText('%6.5f' % qmin)
            self.ui.editQmaxVal.setText('%6.5f' % qmax)
            self.ui.sliderQmin.setMinimum(0)
            self.ui.sliderQmax.setMinimum(0)
            self.ui.sliderQmin.setMaximum(self.qmaxIndex)
            self.ui.sliderQmax.setMaximum(self.qmaxIndex)
            self.ui.sliderQmin.setValue(0)
            self.ui.sliderQmax.setValue(self.qmaxIndex)
        return

    def onSliderQminChange(self, value):
        q = self.qbase[value]
        self.ui.editQmin.setText('%6.5f' % q)
        self.onModelUpdate()

    def onSliderQmaxChange(self, value):
        q = self.qbase[value]
        self.ui.editQmax.setText('%6.5f' % q)
        self.onModelUpdate()

    def onQminEditChange(self):
        if isNumeric(self.ui.editQminVal.text()):
            qmin = float(self.ui.editQminVal.text())
            try:
                self.ui.sliderQmin.setValue(numpy.where(self.qbase >= qmin)[0][0])
            except:
                pass

    def onQmaxEditChange(self):
        if isNumeric(self.ui.editQmaxVal.text()):
            qmax = float(self.ui.editQmaxVal.text())
            try:
                self.ui.sliderQmax.setValue(numpy.where(self.qbase <= qmax)[0][(-1)])
            except:
                pass

    def backup(self):
        self.backupArg = []
        for a in self.Model.Arg:
            self.backupArg.append(a)

    def onBack(self):
        if self.backupArg is not None:
            for i in range(min([len(self.backupArg), len(self.Model.Arg)])):
                self.Model.Arg[i] = self.backupArg[i]
                self.ParText[i].setText(str(self.Model.Arg[i]))

            self.onModelUpdate()
        if len(self.FitParamList) > 0:
            self.FitParamList.pop()
        self.onResultUpdate()
        return

    def clearResult(self):
        self.FitParamList = []

    def getPlotExp(self):
        for i in range(len(self.radioList)):
            if self.ui.radioList[i].isChecked():
                return i

        return 0

    def onFitLMFIT(self):
        if self.i is None:
            return
        else:
            self.ui.btnBack.setEnabled(True)
            self.backup()
            self.onModelUpdate(calculate=False)
            useError = self.ui.chkUseError.isChecked()
            if self.err is None:
                useError = False
            self.fitexp = self.getPlotExp()
            i = self.i[self.qminIndex:self.qmaxIndex]
            err = self.err[self.qminIndex:self.qmaxIndex]
            self.Model.q = self.qbase[self.qminIndex:self.qmaxIndex]
            if useError:
                res, resLMFIT, uncertainties = self.Model.fitLMFIT(i, self.fitexp, err=err)
            else:
                res, resLMFIT, uncertainties = self.Model.fitLMFIT(i, self.fitexp)
            print (
             'fitted parameters : ', res)
            chi = self.Model.chi_carre(res, i)
            self.ui.lblChi.setText(str(chi))
            self.UpdateAfterFit(res, resLMFIT, uncertainties)
            return

    def UpdateAfterFit(self, result, res_err=None, uncertainties=None):
        val = numpy.array(result).copy()
        for i in range(len(val)):
            self.ParText[i].setText(self.Model.Format[i] % val[i])
            if res_err is not None:
                if res_err[i] is not None:
                    try:
                        if val[i] != 0:
                            spercent = ('({0:.2%})').format(abs(res_err[i] / val[i]))
                        else:
                            spercent = ''
                    except ZeroDivisionError:
                        spercent = ''

                    self.ParUncert[i].setText(('+/-' + self.Model.Format[i] + ' %s') % (res_err[i], spercent))
                else:
                    self.ParUncert[i].setText('-')
            else:
                self.ParUncert[i].setText('-')

        self.FitParamList.append(result)
        print result
        self.FitParamName.append(self.dataname)
        self.onResultUpdate()
        self.onModelUpdate()
        return

    def onResultUpdate(self):
        for n in range(len(self.FitParamList)):
            print self.FitParamName[n], ' ',
            print self.FitParamList[n]

        self.ReplotFit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = dlgAutomaticFit()
    myapp.show()
    sys.exit(app.exec_())