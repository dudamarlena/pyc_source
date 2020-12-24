# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\dlgCalculator.py
# Compiled at: 2019-03-22 09:19:31
__doc__ = '\nauthor : Olivier Tache\n(C) CEA 2013\n'
import sys
from PyQt5 import QtGui, QtCore, uic, QtWidgets
import numpy
from numpy import *
from scipy import interpolate
from pySAXS.guisaxs.dataset import *
import pySAXS

class dlgCalculator(QtWidgets.QDialog):

    def __init__(self, parent, datalist=None, newname='newname'):
        QtWidgets.QDialog.__init__(self)
        self.ui = uic.loadUi(pySAXS.UI_PATH + 'dlgCalculator.ui', self)
        self.parentwindow = parent
        self.listofdata = datalist
        self.EditNewName.setText(newname)
        self.EditFormula.setText('i0*1')
        txt = ''
        i = 0
        self.variableDict = {}
        for label in datalist:
            txt += 'i' + str(i) + ' = ' + label + '\n'
            self.variableDict['i' + str(i)] = label
            i += 1

        self.lblVariables.setText(txt)
        self.btnApply.clicked.connect(self.OnApply)
        self.btnQuit.clicked.connect(self.reject)

    def OnApply(self):
        newdatasetname = str(self.EditNewName.text())
        formula = str(self.EditFormula.text())
        newdatasetname = self.parentwindow.cleanString(newdatasetname)
        qref = numpy.copy(self.parentwindow.data_dict[self.listofdata[0]].q)
        formulaForComment = formula
        for var in list(self.variableDict.keys()):
            formulaForComment = formulaForComment.replace(var, self.variableDict[var])
            self.parentwindow.printTXT(formulaForComment)

        newdict = {}
        newerror = numpy.zeros(numpy.shape(qref))
        for var in self.variableDict:
            name = self.variableDict[var]
            if name not in self.parentwindow.data_dict:
                print 'error on mainGuisaxs.OnEditCalculator'
                return
            i = self.parentwindow.data_dict[name].i
            q = self.parentwindow.data_dict[name].q
            if str(q) != str(qref):
                self.parentwindow.printTXT('trying interpolation for ', name)
                newf = interpolate.interp1d(q, i, kind='linear', bounds_error=0)
                newi = newf(qref)
            else:
                newi = i
                error = self.parentwindow.data_dict[name].error
                RelativeError = error / i
                if error is not None and newerror is not None:
                    newerror += RelativeError
                else:
                    newerror = None
            newdict[var] = newi

        self.parentwindow.printTXT('trying evaluation of ', formula)
        safe_list = [
         'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees',
         'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log',
         'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']
        for k in safe_list:
            newdict[k] = locals().get(k)

        iout = numpy.array(eval(formula, newdict))
        newerror = iout * newerror
        self.parentwindow.data_dict[newdatasetname] = dataset(newdatasetname, qref, iout, comment=formulaForComment, type='calculated', error=newerror)
        self.parentwindow.redrawTheList()
        self.parentwindow.Replot()
        return

    def getValues(self):
        return (
         str(self.EditNewName.text()), str(self.EditFormula.text()), self.variableDict)