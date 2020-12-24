# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\dlgAbsorption.py
# Compiled at: 2018-08-27 07:37:12
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
try:
    from pySAXS.LS import absorptionXRL as absorption
    USING_XRAYLIB = True
except:
    from pySAXS.LS import absorption
    USING_XRAYLIB = False

import numpy, pySAXS
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class dlgAbsorption(QtWidgets.QDialog):

    def __init__(self, parent, title='Absorption calculation', printout=None):
        QtWidgets.QDialog.__init__(self)
        self.ui = uic.loadUi(pySAXS.UI_PATH + 'dlgAbsorption.ui', self)
        self.parentwindow = parent
        self.printout = printout
        self.setWindowTitle(title)
        self.energy = 0
        self.lambdaValue = 0
        self.ActiveFormula = ''
        self.ActiveAtomes = numpy.zeros(120)
        self.verbose = True
        self.ConstructUI()
        self.UpdateElementDisplay('H')

    def ConstructUI(self):
        """
        construct the UI
        """
        self.lineEnergy.setValidator(QtGui.QDoubleValidator())
        self.lineEnergy.setText(str(absorption.getEnergyFromSource('Cu')))
        self.OnEnergyChanged()
        self.lineEnergy.textChanged.connect(self.UpdateFormula)
        sources = absorption.COMMON_XRAY_SOURCE_MATERIALS
        i = 1
        for name in sources:
            item = QtWidgets.QPushButton(name, self.groupBoxEnergy)
            item.setObjectName(name)
            item.clicked.connect(self.OnXRaysSourcesClicked)
            self.gridXraySources.addWidget(item, 0, i, 1, 1)
            i += 1

        table = absorption.MENDELEIEV_TABLE
        for j in range(len(table)):
            for i in range(len(table[0])):
                element = table[j][i]
                if element is not None:
                    item = QtWidgets.QPushButton(element, self.groupBoxTable)
                    item.setMaximumSize(30, 30)
                    item.setObjectName(element)
                    item.clicked.connect(self.OnElementClicked)
                    self.gridMendeleiev.addWidget(item, j, i, 1, 1)

        self.ElementSymbol.setText('-')
        self.ElementName.setText('-')
        self.ElementAtomicNumber.setText('-')
        self.lineNumberOfAtoms.setText(str(1.0))
        self.btnAdd.clicked.connect(self.OnAddElement)
        self.btnRemove.clicked.connect(self.OnRemoveElement)
        self.btnRemoveAll.clicked.connect(self.OnRemoveAllElement)
        self.lineDensity.setText(str(1.0))
        self.lineDensity.textChanged.connect(self.updateCalculation)
        self.lineCompoundMuRho.setStyleSheet('color: blue')
        self.lineElectronicDensity.setStyleSheet('color: blue')
        self.lineScatteringLengthDensity.setStyleSheet('color: red')
        self.lineThickness.setText(str(1.0))
        self.lineThickness.textChanged.connect(self.updateCalculation)
        self.lineXRayTransmission.setReadOnly(True)
        self.lineXRayTransmission.setStyleSheet('color: blue')
        self.lineXRayMeasuredTransmission.setText(str(1.0))
        self.lineXRayMeasuredTransmission.textChanged.connect(self.updateCalculation)
        self.lineEstimatedThickness.setReadOnly(True)
        self.lineEstimatedThickness.setStyleSheet('color: blue')
        self.lineActiveFormula.setStyleSheet(_fromUtf8('background-color: rgb(244, 255, 190);'))
        self.EmptyFormula()
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.blue)
        self.labelLib.setPalette(palette)
        if USING_XRAYLIB:
            self.labelLib.setText('Calculation made with XRAYLIB')
            self.labelLib.setStyleSheet('color: red')
        else:
            self.labelLib.setText('Calculation made with datas from the NIST')
        for compound in absorption.COMPOUNDS:
            self.listPreDefined.addItem(compound)

        self.AddPredefined.clicked.connect(self.selectCompound)
        return

    def OnEnergyChanged(self):
        """
        text for energy changed 
        -> change lambda
        """
        self.energy = float(self.lineEnergy.text())
        if self.energy != 0:
            self.lambdaValue = absorption.KEV2ANGST / self.energy
            self.lineLambda.setText(str(self.lambdaValue))

    def OnElementClicked(self):
        """
        user clicked on an element
        """
        sending_button = self.sender()
        symbol = str(sending_button.objectName())
        self.UpdateElementDisplay(symbol)

    def UpdateElementDisplay(self, symbol):
        """
        update the element display
        """
        Z = absorption.SymbolToAtomicNumber(symbol)
        self.ElementSymbol.setText(symbol)
        self.ElementName.setText(absorption.getNameZ(Z))
        self.ElementAtomicNumber.setText(str(Z))
        self.Z = Z
        self.lineElementAtomicWeight.setText(str(absorption.getMasseZ(Z)))
        self.lineElementMuRho.setText(str(absorption.getMuZ(Z, self.energy)))

    def OnXRaysSourcesClicked(self):
        sending_button = self.sender()
        source = str(sending_button.objectName())
        source = source.strip()
        energy = absorption.getEnergyFromSource(source)
        self.lineEnergy.setText(str(energy))

    def OnAddElement(self):
        an = float(str(self.lineNumberOfAtoms.text()))
        if self.Z != 0:
            if self.ActiveAtomes[(self.Z - 1)] != 0:
                self.ActiveAtomes[self.Z - 1] = self.ActiveAtomes[(self.Z - 1)] + an
            else:
                self.ActiveAtomes[self.Z - 1] = an
            self.UpdateFormula()

    def OnRemoveElement(self):
        if self.Z != 0:
            self.ActiveAtomes[self.Z - 1] = 0
            self.UpdateFormula()

    def OnRemoveAllElement(self):
        self.ActiveAtomes = numpy.zeros(120)
        self.EmptyFormula()

    def EmptyFormula(self):
        self.lineActiveFormula.setText('')
        self.lineCompoundMuRho.setText('')
        self.lineElectronicDensity.setText('')
        self.lineScatteringLengthDensity.setText('')
        self.lineXRayTransmission.setText('')

    def selectCompound(self):
        """ a compound is selected"""
        c = self.listPreDefined.currentText()
        ele = absorption.COMPOUNDS[c]
        self.ActiveFormula = str(ele[0])
        self.density = ele[1]
        self.lineActiveFormula.setText(self.ActiveFormula)
        self.lineDensity.setText(str(self.density))

    def updateCalculation(self):
        self.energy = float(self.lineEnergy.text())
        if self.energy != 0:
            self.lambdaValue = absorption.KEV2ANGST / self.energy
            self.lineLambda.setText(str(self.lambdaValue))
        self.ActiveFormula = str(self.lineActiveFormula.text())
        if self.ActiveFormula == '':
            return
        MuRho = absorption.getMuFormula(self.ActiveFormula, self.energy)
        self.lineCompoundMuRho.setText('%1.5e' % MuRho)
        density = float(self.lineDensity.text())
        ED = absorption.getElectronDensity(self.ActiveFormula, density)[0]
        self.lineElectronicDensity.setText('%1.5e' % ED)
        SLD = absorption.getElectronDensity(self.ActiveFormula, density)[1]
        self.lineScatteringLengthDensity.setText('%1.5e' % SLD)
        thickness = float(self.lineThickness.text())
        Tr = absorption.getTransmission(self.ActiveFormula, thickness, density, self.energy)
        self.lineXRayTransmission.setText('%8.7f' % Tr)
        TrM = float(self.lineXRayMeasuredTransmission.text())
        Thi = absorption.getThickness(self.ActiveFormula, TrM, density, self.energy)
        self.lineEstimatedThickness.setText('%6.7f' % Thi)
        if self.verbose:
            if USING_XRAYLIB:
                self.printTXT('------ Absorption tools using xraylib -----')
            else:
                self.printTXT('------ Absorption tools using NIST DATA -----')
            self.printTXT('Compound formula: ', self.ActiveFormula)
            self.printTXT('Energy : %6.3f (keV) ' % self.energy)
            self.printTXT('Density : %6.3f ' % density)
            self.printTXT('Compound Mu_en/rho  = %6.3f (cm2/g) ' % MuRho)
            self.printTXT('Electronic density  = %1.5e (1/cm3) ' % ED)
            self.printTXT('Scattering length density  = %1.5e (1/cm2) ' % SLD)
            self.printTXT('with thickness of %8.7f cm -> X-ray transmission  = %8.7f' % (thickness, Tr))
            self.printTXT('with X-ray transmission of %8.7f -> thickness  = %8.7f cm' % (TrM, Thi))

    def UpdateFormula(self, verbose=False):
        Tr = -1
        ED = -1
        SLD = -1
        self.ActiveFormula = ''
        if sum(self.ActiveAtomes) <= 0.0:
            self.EmptyFormula()
        else:
            N = self.ActiveAtomes.take(numpy.where(self.ActiveAtomes != 0)[0])
            ind = numpy.where(self.ActiveAtomes != 0)[0]
            j = 0
            for i in ind:
                self.ActiveFormula = self.ActiveFormula + absorption.AtomicNumberToSymbol(int(i) + 1) + ' ' + str(N[int(j)]) + ' '
                j = j + 1

            self.lineActiveFormula.setText(self.ActiveFormula.strip())
            self.updateCalculation()

    def printTXT(self, txt='', par=''):
        """
        for printing messages
        """
        if self.printout == None:
            print str(txt) + str(par)
        else:
            self.printout(txt, par)
        return


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dlg = dlgAbsorption(None)
    dlg.exec_()