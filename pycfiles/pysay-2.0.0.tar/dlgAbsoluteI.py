# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\dlgAbsoluteI.py
# Compiled at: 2019-10-29 06:25:53
from PyQt5 import QtGui, QtCore, QtWidgets, uic
import pySAXS.LS.SAXSparametersXML as SAXSparameters, sys, pySAXS
from pySAXS.tools import isNumeric
from pySAXS.tools import filetools
from pySAXS.guisaxs import dataset
from pySAXS.LS import absolute
import os

class dlgAbsolute(QtWidgets.QDialog):

    def __init__(self, parent, saxsparameters=None, datasetname=None, printout=None, referencedata=None, backgrounddata=None, datasetlist=None, referenceValue=None):
        QtWidgets.QDialog.__init__(self)
        self.ui = uic.loadUi(pySAXS.UI_PATH + 'dlgAbsoluteI.ui', self)
        self.datasetname = datasetname
        self.parentwindow = parent
        self.workingdirectory = self.parentwindow.getWorkingDirectory()
        self.params = saxsparameters
        self.datasetlist = datasetlist
        self.referenceValue = referenceValue
        self.paramscopy = None
        if self.params is not None:
            self.paramscopy = self.params.copy()
        self.referencedata = referencedata
        self.backgrounddata = backgrounddata
        self.printout = parent.printTXT
        if self.params is None:
            self.params = getTheParameters(self.datasetname, parent, referencedata=self.referencedata, printout=self.printout, workingdirectory=self.workingdirectory)
        self.params.printout = self.printout
        self.ConstructUI()
        self.params.calculate_All()
        self.Params2Control()
        self.ui.buttonBox.clicked.connect(self.click)
        return

    def ConstructUI(self):
        if self.datasetname is not None:
            self.ui.labelDataset.setText(self.datasetname)
        if self.datasetlist is not None:
            txt = ''
            for t in self.datasetlist:
                txt += str(t) + '\n'

            self.ui.labelDataset.setText(txt)
        self.listStaticText = {}
        self.listTextCtrl = {}
        paramslist = self.params.order()
        i = 0
        for name in paramslist:
            par = self.params.parameters[name]
            self.listStaticText[name] = QtWidgets.QLabel(par.description + ' : ', self.ui.groupBox)
            self.listStaticText[name].setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            self.listStaticText[name].setMinimumHeight(20)
            self.listStaticText[name].setMaximumHeight(20)
            self.ui.formLayout.setWidget(i, QtWidgets.QFormLayout.LabelRole, self.listStaticText[name])
            self.listTextCtrl[name] = QtWidgets.QLineEdit(str(par.value), self.ui.groupBox)
            self.listTextCtrl[name].setMinimumHeight(20)
            self.listTextCtrl[name].setMaximumHeight(20)
            self.ui.formLayout.setWidget(i, QtWidgets.QFormLayout.FieldRole, self.ui.listTextCtrl[name])
            if par.formula is not None:
                self.listTextCtrl[name].setReadOnly(True)
                self.listTextCtrl[name].setStyleSheet('color: blue')
                self.listStaticText[name].setStyleSheet('color: blue')
            else:
                self.listTextCtrl[name].setReadOnly(False)
                self.listTextCtrl[name].textChanged.connect(self.onParamEdited)
            if self.datasetlist is not None:
                if name != 'K' and name != 'thickness':
                    self.listStaticText[name].setEnabled(False)
                else:
                    self.listTextCtrl[name].setStyleSheet('color: red')
                    self.listStaticText[name].setStyleSheet('color: red')
            i += 1

        self.ui.checkIrange.setChecked(True)
        if self.backgrounddata is not None:
            self.ui.groupBoxBack.setEnabled(True)
            self.ui.checkSubtractBack.setChecked(True)
            self.ui.txtBackground.setText(str(self.backgrounddata))
        else:
            self.ui.groupBoxBack.setEnabled(True)
            self.ui.txtBackground.setText('not defined')
        if self.referencedata is not None and self.referencedata != self.datasetname + ' scaled':
            self.ui.groupBoxReference.setEnabled(True)
            self.ui.checkSubstractRef.setChecked(self.parentwindow.referencedataSubtract)
            self.ui.txtReference.setText(str(self.referencedata))
        else:
            self.ui.groupBoxReference.setEnabled(False)
            self.ui.txtReference.setText(str('not defined'))
        if self.datasetlist is not None:
            self.ui.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Close | QtWidgets.QDialogButtonBox.YesToAll)
        self.ui.btnDefineAsReference.clicked.connect(self.DefineAsReference)
        if self.referenceValue is not None:
            self.ui.txtValue.setText(str(self.referenceValue))
        return

    def eraseUI(self):
        """
        erase the UI
        """
        for name in self.listStaticText:
            self.ui.formLayout.removeWidget(self.listStaticText[name])
            self.listStaticText[name].deleteLater()
            self.ui.formLayout.removeWidget(self.listTextCtrl[name])
            self.listTextCtrl[name].deleteLater()

        self.listStaticText = {}
        self.listTextCtrl = {}

    def accepted(self):
        """
        user click on an accepted button (ok, open,...)
        do nothing
        """
        pass

    def onParamEdited(self):
        self.Control2Params()
        self.params.calculate_All(verbose=False)
        self.ParamsWithFormula2Control()

    def onParamChanged(self):
        self.Control2Params()
        self.params.calculate_All()
        self.Params2Control()

    def click(self, obj=None):
        name = obj.text()
        if name == 'OK':
            self.close()
        elif name == 'Cancel':
            if self.paramscopy is not None:
                self.params = self.paramscopy.copy()
            else:
                self.params = None
            self.parentwindow.data_dict[self.datasetname].parameters = self.params
            self.close()
        elif name == 'Close':
            self.close()
        elif name == 'Apply':
            self.onParamChanged()
            if self.parentwindow is None:
                return
            if self.datasetname != None:
                self.parentwindow.data_dict[self.datasetname].parameters = self.params
                if self.ui.checkSubtractBack.isChecked():
                    self.backgroundname = str(self.ui.txtBackground.text())
                else:
                    self.backgroundname = None
                if self.ui.checkSubstractRef.isChecked():
                    self.referencedata = str(self.ui.txtReference.text())
                    self.parentwindow.referencedataSubtract = True
                else:
                    self.referencedata = None
                    self.parentwindow.referencedataSubtract = False
                if self.ui.chkReferenceValue.isChecked():
                    self.DefineAsReference()
                OnScalingSAXSApply(self.parentwindow, self.ui.checkQrange.isChecked(), self.ui.checkIrange.isChecked(), self.datasetname, parameters=self.params.parameters, backgroundname=self.backgroundname, referencedata=self.referencedata, referenceValue=self.referenceValue)
                self.parentwindow.redrawTheList()
                self.parentwindow.Replot()
        elif name == 'Yes to &All':
            self.onParamChanged()
            if self.parentwindow is None:
                return
            if self.ui.checkSubtractBack.isChecked():
                self.backgroundname = str(self.ui.txtBackground.text())
            else:
                self.backgroundname = None
            if self.ui.checkSubstractRef.isChecked():
                self.referencedata = str(self.ui.txtReference.text())
            else:
                self.referencedata = None
            thickness = self.params.parameters['thickness']
            k = self.params.parameters['K']
            self.printTXT('Applying for ALL thickness : ' + str(thickness) + ' and K factor :' + str(k))
            for n in self.datasetlist:
                self.parentwindow.data_dict[n].parameters = self.params.copy()
                newfn = filetools.getFilenameOnly(self.parentwindow.data_dict[n].filename)
                newfn += '.rpt'
                if filetools.fileExist(newfn):
                    self.params.getfromRPT(newfn)
                else:
                    print 'filename rpt ' + newfn + ' not found'
                    newfn = filetools.getFilenameOnly(self.workingdirectory + os.sep + filetools.getFilename(self.parentwindow.data_dict[n].filename))
                    newdataname = newfn
                    newfn += '.rpt'
                    print ('trying : ', newfn)
                    if filetools.fileExist(newfn):
                        self.params.getfromRPT(newfn)
                        self.parentwindow.data_dict[n].filename = newdataname
                    else:
                        print 'filename rpt ' + newfn + ' not found'
                OnScalingSAXSApply(self.parentwindow, self.ui.checkQrange.isChecked(), self.ui.checkIrange.isChecked(), n, parameters=self.params.parameters, backgroundname=self.backgroundname, referencedata=self.referencedata)

            self.parentwindow.redrawTheList()
            self.parentwindow.Replot()
        elif name == 'Save':
            self.saveClicked()
        elif name == 'Open':
            self.openClicked()
        return

    def openClicked(self):
        fd = QtGui.QFileDialog(self)
        filename = fd.getOpenFileName(self, caption='SAXS parameter', filter='*.xml', directory=self.workingdirectory)
        filename = str(filename)
        if len(filename) > 0:
            self.printTXT('loading parameters file ', str(filename))
            ext = filetools.getExtension(filename)
            self.params = SAXSparameters.SAXSparameters(printout=self.printTXT)
            self.params.openXML(filename)
            self.params.parameters['filename'].value = filename
            self.params.printout = self.printTXT
            self.eraseUI()
            self.ConstructUI()

    def saveClicked(self):
        """
        User click on save button
        """
        self.Control2Params()
        fd = QtGui.QFileDialog(self)
        filename = fd.getSaveFileName(self, caption='SAXS parameter', filter='*.xml')
        wc = 'Save parameters file(*.xml)|*.xml'
        filename = str(filename)
        if len(filename) <= 0:
            return
        if filetools.fileExist(filename):
            ret = QtWidgets.QMessageBox.question(self, 'pySAXS', 'file ' + str(filename) + ' exist. Replace ?', buttons=QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel, defaultButton=QtWidgets.QMessageBox.NoButton)
            if ret == QtGui.QMessageBox.No:
                self.printTXT('file ' + str(filename) + ' exist. Datas was NOT replaced')
                return
            if ret == QtGui.QMessageBox.Cancel:
                return self.saveClicked()
        self.params.saveXML(filename)
        if 'filename' in self.params.parameters:
            self.params.parameters['filename'].value = filename
            self.onParamEdited()
        self.printTXT('parameters was saved in ' + filename)
        self.parent.setWorkingDirectory(filename)

    def Params2Control(self):
        for key, value in list(self.params.parameters.items()):
            if key in self.listTextCtrl:
                self.listTextCtrl[key].setText(str(self.params.parameters[key].value))

    def ParamsWithFormula2Control(self):
        for key, value in list(self.params.parameters.items()):
            if key in self.listTextCtrl:
                if self.params.parameters[key].formula is not None:
                    self.listTextCtrl[key].setText(str(self.params.parameters[key].value))

        return

    def Control2Params(self):
        for key, value in list(self.params.parameters.items()):
            if self.params.parameters[key].datatype == 'float' or self.params.parameters[key].datatype == 'int':
                if isNumeric.isNumeric(self.listTextCtrl[key].text()):
                    self.params.parameters[key].value = float(self.listTextCtrl[key].text())
            elif isNumeric.isNumeric(self.listTextCtrl[key].text()):
                self.params.parameters[key].value = float(self.listTextCtrl[key].text())
            else:
                self.params.parameters[key].value = str(self.listTextCtrl[key].text())

    def printTXT(self, txt='', par=''):
        """
        for printing messages
        """
        if self.printout == None:
            print str(txt) + str(par)
        else:
            self.printout(txt, par)
        return

    def DefineAsReference(self):
        try:
            self.referenceValue = float(self.ui.txtValue.text())
            self.parentwindow.referenceValue = self.referenceValue
            self.ui.chkReferenceValue.setChecked(True)
        except:
            print 'not a float value'
            self.referenceValue = None
            self.parentwindow.referenceValue = None

        return


def getTheParameters(datasetname, parentwindow, referencedata=None, printout=None, workingdirectory=None):
    """
            get the parameters from rpt file
            """
    params = SAXSparameters.SAXSparameters(printout=printout)
    if referencedata is not None:
        if referencedata in parentwindow.data_dict:
            if parentwindow.data_dict[referencedata].parameters is not None:
                params = parentwindow.data_dict[referencedata].parameters.copy()
            else:
                father = parentwindow.data_dict[referencedata].parent
                if father is not None:
                    if parentwindow.data_dict[father[0]].parameters is not None:
                        params = parentwindow.data_dict[father[0]].parameters.copy()
    newfn = filetools.getFilenameOnly(parentwindow.data_dict[datasetname].filename)
    newfn += '.rpt'
    if filetools.fileExist(newfn):
        params.getfromRPT(newfn)
    else:
        print (
         'filename rpt ', newfn + ' not found')
        newfn = filetools.getFilenameOnly(workingdirectory + os.sep + filetools.getFilename(parentwindow.data_dict[datasetname].filename))
        newdataname = newfn
        newfn += '.rpt'
        print ('trying : ', newfn)
        if filetools.fileExist(newfn):
            params.getfromRPT(newfn)
            parentwindow.data_dict[datasetname].filename = newdataname
        else:
            print (
             'filename rpt ', newfn + ' not found')
    return params


def OnScalingSAXSApply(parentwindow, applyQ=False, applyI=True, dataname=None, parameters=None, backgroundname=None, referencedata=None, referenceValue=None, background_by_s=None, thickness=None):
    """
        child dialog box ask to apply parameters
        """
    workingdirectory = parentwindow.getWorkingDirectory()
    q = parentwindow.data_dict[dataname].q
    i = parentwindow.data_dict[dataname].i
    error = parentwindow.data_dict[dataname].error
    if background_by_s is not None:
        parameters['backgd_by_s'].value = float(background_by_s)
    if thickness is not None:
        parameters['thickness'].value = float(thickness)
    abs = absolute.absolute(q=q, i=i, ierr=error, parameters=parameters)
    parentwindow.printTXT('------ absolute intensities ------')
    if applyQ:
        parentwindow.printTXT('--set q range --')
        q = saxsparameters.calculate_q(q)
    if applyI:
        if backgroundname is not None:
            qb = parentwindow.data_dict[backgroundname].q
            ib = parentwindow.data_dict[backgroundname].i
            eb = parentwindow.data_dict[backgroundname].error
            abs.subtractBackground(qb, ib, eb, backgroundname)
        if referencedata is not None:
            thickness = parameters['thickness'].value
            parameters['thickness'].value = 1.0
            newi, newerr = abs.calculate()
            isolv = parentwindow.data_dict[referencedata].i
            qsolv = parentwindow.data_dict[referencedata].q
            esolv = parentwindow.data_dict[referencedata].error
            newi, newerr = abs.subtractSolvent(qsolv, isolv, esolv, referencedata, thickness)
        elif referenceValue is not None:
            thickness = parameters['thickness'].value
            parameters['thickness'].value = 1.0
            newi, newerr = abs.calculate()
            newi, newerr = abs.subtractSolventValue(referenceValue, thickness)
        else:
            newi, newerr = abs.calculate()
        parentwindow.printTXT('------ absolute intensities END ------')
    try:
        datafile = parentwindow.data_dict[dataname].filename
        print (
         'datafile:', datafile)
        abs.saveRPT(datafile)
    except:
        parentwindow.printTXT('Error when trying to write rpt file for ', dataname)

    col = parentwindow.data_dict[dataname].color
    if dataname + ' scaled' in parentwindow.data_dict:
        col = parentwindow.data_dict[(dataname + ' scaled')].color
    parentwindow.data_dict[dataname + ' scaled'] = dataset.dataset(dataname + ' scaled', q, newi, dataname + ' scaled', parameters=None, error=newerr, type='scaled', parent=[dataname], color=col, abs=abs)
    parentwindow.data_dict[dataname].abs = abs
    return dataname + ' scaled'