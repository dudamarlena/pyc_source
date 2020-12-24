# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\hipgisaxs\hipgisaxs.py
# Compiled at: 2018-08-27 17:21:07
import json
from PySide.QtUiTools import QUiLoader
from PySide import QtGui
from PySide import QtCore
import yaml
from modpkgs.collectionsmod import UnsortableOrderedDict
import ui, featuremanager, display, customwidgets

class mainwindow:

    def __init__(self, app):
        self.app = app
        ui.loadUi()
        self.computationForm = None
        self._detectorForm = None
        self._scatteringForm = None
        self.app.setStyle('Plastique')
        with open('xicam/gui/style.stylesheet', 'r') as (f):
            self.app.setStyleSheet(f.read())
        featuremanager.layout = ui.mainwindow.featuresList
        featuremanager.load()
        self.newExperiment()
        ui.mainwindow.addFeatureButton.clicked.connect(featuremanager.addLayer)
        ui.mainwindow.addSubstrateButton.clicked.connect(featuremanager.addSubstrate)
        ui.mainwindow.addParticleButton.clicked.connect(featuremanager.addParticle)
        ui.mainwindow.showScatteringButton.clicked.connect(self.showScattering)
        ui.mainwindow.showComp50utationButton.clicked.connect(self.showComputation)
        ui.mainwindow.showDetectorButton.clicked.connect(self.showDetector)
        ui.mainwindow.addParticleButton.setMenu(ui.particlemenu)
        ui.mainwindow.runLocal.clicked.connect(self.runLocal)
        display.load()
        ui.mainwindow.latticeplaceholder.addWidget(display.viewWidget)
        ui.mainwindow.show()
        ui.mainwindow.raise_()
        return

    def newExperiment(self):
        pass

    def showFeature(self, index):
        self.showForm(index.internalPointer().form)

    def showComputation(self):
        if self.computationForm is None:
            self.computationForm = featuremanager.loadform('xicam/gui/guiComputation.ui')
        self.showForm(self.computationForm)
        return

    def showScattering(self):
        self.showForm(self.scatteringForm.form)

    def showDetector(self):
        self.showForm(self.detectorForm.form)

    def showForm(self, form):
        ui.mainwindow.featureWidgetHolder.addWidget(form)
        ui.mainwindow.featureWidgetHolder.setCurrentWidget(form)

    @property
    def detectorForm(self):
        if self._detectorForm is None:
            self._detectorForm = customwidgets.detector()
        return self._detectorForm

    @property
    def scatteringForm(self):
        if self._scatteringForm is None:
            self._scatteringForm = customwidgets.scattering()
        return self._scatteringForm