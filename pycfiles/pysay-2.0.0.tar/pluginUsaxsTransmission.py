# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Python27\lib\site-packages\pySAXS\guisaxs\qt\pluginUsaxsTransmission.py
# Compiled at: 2013-02-04 05:50:44
from PyQt4 import QtGui, QtCore
import guidata
from guidata.dataset import datatypes
from guidata.dataset import dataitems
import numpy
from pySAXS.LS import LSusaxs
from pySAXS.guisaxs.dataset import *
from pySAXS.guisaxs.qt import plugin

class USAXSTransmission(plugin.pySAXSplugin):

    def execute(self):
        """
        The user click on "USAXS - Data correction"
        """
        if self.selectedData is None:
            QtGui.QMessageBox.information(self.parent, 'pySAXS', 'No data are selected', buttons=QtGui.QMessageBox.Ok, defaultButton=QtGui.QMessageBox.NoButton)
            return
        else:
            if not self.data_dict.has_key('rock'):
                QtGui.QMessageBox.information(self.parent, 'pySAXS', "Load data and rocking curve before correcting by transmission \n            (Try to rename the rocking curve datas in 'rock')", buttons=QtGui.QMessageBox.Ok, defaultButton=QtGui.QMessageBox.NoButton)
                return
            items = {'wavelength': dataitems.FloatItem('Wavelength', 1.542), 
               'thickness': dataitems.FloatItem('Thickness of sample (cm)', 0.1), 
               'backgroundData': dataitems.FloatItem('Background data(cps/s)', 0.0), 
               'backgroundRC': dataitems.FloatItem('Background Rocking curve (cps/s) ', 0.0), 
               'shiftdata': dataitems.FloatItem('Shift Data (steps)', 0.0), 
               'shiftrock': dataitems.FloatItem('Shift Rocking curve (steps)', 0.0)}
            clz = type('Transmission and Data correction :', (datatypes.DataSet,), items)
            self.form = clz()
            if self.form.edit():
                self.calculate()
            return

    def calculate(self):
        """
        do the tramsission correction after dialog box LSTransmissionDlg
        """
        self.printTXT('-----USAXS Data correction --------')
        self.thick = self.form.thickness
        self.steprock = self.form.shiftrock
        self.stepexp = self.form.shiftdata
        self.backgrdData = self.form.backgroundData
        self.backgrdRC = self.form.backgroundRC
        n = 15
        a1 = 10000.0
        a2 = 1e-10
        it = 2000
        tol = 1e-15
        qminimum = 0.0001
        Iexp = self.data_dict[self.selectedData].i - self.backgrdData
        qexp = self.data_dict[self.selectedData].q
        Irock = self.data_dict['rock'].i - self.backgrdRC
        qrock = self.data_dict['rock'].q
        a0exp = Iexp[numpy.argmax(Iexp)]
        a0rock = Irock[numpy.argmax(Irock)]
        Thetaexp = qexp
        Thetarock = qrock
        Fitexp, Thetaexp_sel, Iexp_sel, FitParamexp = LSusaxs.FitGauss(Thetaexp, Iexp, n, a0exp, a1, a2, tol, it)
        Fitrock, Thetarock_sel, Irock_sel, FitParamrock = LSusaxs.FitGauss(Thetarock, Irock, n, a0rock, a1, a2, tol, it)
        self.printTXT('Data center found at ', FitParamexp[2])
        self.printTXT('RC center found at ', FitParamrock[2])
        DeltaThetaexp = -FitParamexp[2]
        DeltaThetarock = -FitParamrock[2]
        shiftexp = abs(Thetaexp_sel[0] - Thetaexp_sel[1])
        shiftrock = abs(Thetarock_sel[0] - Thetarock_sel[1])
        NewThetaexp_sel = LSusaxs.Qscalemod(DeltaThetaexp, Thetaexp_sel, self.stepexp * shiftexp)
        NewThetarock_sel = LSusaxs.Qscalemod(DeltaThetarock, Thetarock_sel, self.steprock * shiftrock)
        CorrThetaexp_positive = numpy.repeat(NewThetaexp_sel, NewThetaexp_sel > 0.0)
        Iexp_sel_positive = numpy.repeat(Iexp_sel, NewThetaexp_sel > 0.0)
        qnewexp = LSusaxs.Qscalemod(DeltaThetaexp, Thetaexp, self.stepexp * shiftexp)
        qnewrock = LSusaxs.Qscalemod(DeltaThetarock, Thetarock, self.steprock * shiftexp)
        self.data_dict[self.selectedData + ' centered'] = dataset(self.selectedData + ' centered', qnewexp, Iexp, 'centered datas', type='calculated', parent=[self.selectedData])
        self.data_dict['rock centered'] = dataset('rock centered', qnewrock, Irock, 'rock datas', type='calculated', parent=['rock'])
        self.TransmissionValue = FitParamexp[0] / FitParamrock[0]
        self.printTXT('Transmission of the sample (%)= ', self.TransmissionValue)
        self.printTXT('Sample thickness (cm.)=', self.thick)
        qnewpos = numpy.repeat(qnewrock, qnewrock >= 0.0)
        Inewpos = numpy.repeat(Irock, qnewrock >= 0.0)
        self.printTXT('minimum Theta taken for central beam calculation= ', qnewpos[0])
        somme = 2.0 * LSusaxs.somme(qnewpos, Inewpos)
        self.printTXT('Central beam area(counts.s^-1.rad^-2)= ', somme)
        qnew, ITcorr = LSusaxs.TrCorrectedProf(qnewexp, Iexp, qnewrock, Irock, self.thick, somme, self.TransmissionValue)
        self.data_dict[self.selectedData + ' substracted'] = dataset(self.selectedData + ' substracted', numpy.repeat(qnew, qnew > qminimum), numpy.repeat(ITcorr, qnew > qminimum), 'substracted datas', type='scaled', parent=[
         self.selectedData])
        self.redrawTheList()
        self.Replot()