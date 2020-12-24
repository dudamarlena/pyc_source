# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/epscComp/plotEngine.py
# Compiled at: 2009-05-29 13:49:17
import utility
from scipy import *
import config

class PlotEngine:
    """ class which controls plotting functions

    """

    def __init__(self, controller):
        self.controller = controller
        if self.controller.epscData.phaseNum == 201:
            self.file_dir = config.dirEpscCore_phase1
        elif self.controller.epscData.phaseNum == 203:
            self.file_dir = config.dirEpscCore

    def plotMacroTop(self, frame, mode):
        if self.controller.epscData.expData.checkFlagOn('expData') == True and mode != 1:
            self.controller.epscOpt.colData.collectExpData()
            if mode == 2:
                self.controller.epscOpt.colData.collectMacroModelData()
                self.plotExpMacro(frame, 'macro', list(self.controller.epscData.expData.macroExpX), list(self.controller.epscData.expData.macroExpY))
                self.plotModelMacro(frame, 'macro', list(self.controller.epscOpt.colData.macroMdlX), list(self.controller.epscOpt.colData.macroMdlY))
            elif mode == 3:
                self.plotExpMacro(frame, 'macro', list(self.controller.epscData.expData.macroExpX), list(self.controller.epscData.expData.macroExpY))
        else:
            self.controller.epscOpt.colData.collectMacroModelData()
            self.plotModelMacro(frame, 'macro', list(self.controller.epscOpt.colData.macroMdlX), list(self.controller.epscOpt.colData.macroMdlY))

    def plotNeutronTop(self, frame, mode):
        if self.controller.epscData.expData.checkFlagOn('expData') == True and mode != 1:
            self.controller.epscOpt.colData.collectExpData()
            if mode == 2:
                self.controller.epscOpt.colData.collectHKLModelData()
                self.plotExpHKL(frame, 'HKL-Long', self.controller.epscData.expData.HKLExpX['LongPhase1'], list(self.controller.epscData.expData.HKLExpY))
                self.plotExpHKL(frame, 'HKL-Trans', self.controller.epscData.expData.HKLExpX['TransPhase1'], list(self.controller.epscData.expData.HKLExpY))
                self.plotModelHKL(frame, 'HKL-Long', self.controller.epscOpt.colData.HKLMdlX['LongPhase1'], list(self.controller.epscOpt.colData.HKLMdlY))
                self.plotModelHKL(frame, 'HKL-Trans', self.controller.epscOpt.colData.HKLMdlX['TransPhase1'], list(self.controller.epscOpt.colData.HKLMdlY))
                if self.controller.epscData.phaseNum != 201:
                    self.plotExpHKL(frame, 'HKL-Long', self.controller.epscData.expData.HKLExpX['LongPhase2'], list(self.controller.epscData.expData.HKLExpY))
                    self.plotModelHKL(frame, 'HKL-Long', self.controller.epscOpt.colData.HKLMdlX['LongPhase2'], list(self.controller.epscOpt.colData.HKLMdlY))
            elif mode == 3:
                self.plotExpHKL(frame, 'HKL-Long', self.controller.epscData.expData.HKLExpX['LongPhase1'], list(self.controller.epscData.expData.HKLExpY))
                self.plotExpHKL(frame, 'HKL-Trans', self.controller.epscData.expData.HKLExpX['TransPhase1'], list(self.controller.epscData.expData.HKLExpY))
        else:
            self.controller.epscOpt.colData.collectHKLModelData()
            self.plotModelHKL(frame, 'HKL-Long', self.controller.epscOpt.colData.HKLMdlX['LongPhase1'], list(self.controller.epscOpt.colData.HKLMdlY))
            self.plotModelHKL(frame, 'HKL-Trans', self.controller.epscOpt.colData.HKLMdlX['TransPhase1'], list(self.controller.epscOpt.colData.HKLMdlY))
            if self.controller.epscData.phaseNum != 201:
                self.plotModelHKL(frame, 'HKL-Long', self.controller.epscOpt.colData.HKLMdlX['LongPhase2'], list(self.controller.epscOpt.colData.HKLMdlY))

    def plotOptMacroTop(self, frame, mode):
        if mode == 1:
            if self.controller.epscData.expData.checkFlagOn('expData') == True:
                self.controller.epscOpt.colData.collectExpData()
                self.plotExpMacro(frame, 'macro', list(self.controller.epscData.expData.macroExpX), list(self.controller.epscData.expData.macroExpY))
        elif mode == 2:
            if self.controller.epscData.expData.checkFlagOn('expData') == True:
                self.controller.epscOpt.colData.collectExpData()
                self.plotExpMacro(frame, 'macro', list(self.controller.epscData.expData.macroExpX), list(self.controller.epscData.expData.macroExpY))
            self.controller.epscOpt.colData.collectMacroModelData()
            self.plotModelMacro(frame, 'macro', list(self.controller.epscOpt.colData.macroMdlX), list(self.controller.epscOpt.colData.macroMdlY))
        elif mode == 3:
            self.controller.epscOpt.colData.collectMacroModelData()
            self.plotModelMacro(frame, 'macro', list(self.controller.epscOpt.colData.macroMdlX), list(self.controller.epscOpt.colData.macroMdlY))

    def plotOptHKLTop(self, frame, mode):
        if mode == 1:
            if self.controller.epscData.expData.checkFlagOn('expData') == True:
                self.controller.epscOpt.colData.collectExpData()
                self.plotExpHKL(frame, 'HKL-Long', self.controller.epscData.expData.HKLExpX['LongPhase1'], list(self.controller.epscData.expData.HKLExpY))
                self.plotExpHKL(frame, 'HKL-Trans', self.controller.epscData.expData.HKLExpX['TransPhase1'], list(self.controller.epscData.expData.HKLExpY))
        elif mode == 2:
            if self.controller.epscData.expData.checkFlagOn('expData') == True:
                self.controller.epscOpt.colData.collectExpData()
                self.plotExpHKL(frame, 'HKL-Long', self.controller.epscData.expData.HKLExpX['LongPhase1'], list(self.controller.epscData.expData.HKLExpY))
                self.plotExpHKL(frame, 'HKL-Trans', self.controller.epscData.expData.HKLExpX['TransPhase1'], list(self.controller.epscData.expData.HKLExpY))
            self.controller.epscOpt.colData.collectHKLModelData()
            self.plotModelHKL(frame, 'HKL-Long', self.controller.epscOpt.colData.HKLMdlX['LongPhase1'], list(self.controller.epscOpt.colData.HKLMdlY))
            self.plotModelHKL(frame, 'HKL-Trans', self.controller.epscOpt.colData.HKLMdlX['TransPhase1'], list(self.controller.epscOpt.colData.HKLMdlY))
        elif mode == 3:
            self.controller.epscOpt.colData.collectHKLModelData()
            self.plotModelHKL(frame, 'HKL-Long', self.controller.epscOpt.colData.HKLMdlX['LongPhase1'], list(self.controller.epscOpt.colData.HKLMdlY))
            self.plotModelHKL(frame, 'HKL-Trans', self.controller.epscOpt.colData.HKLMdlX['TransPhase1'], list(self.controller.epscOpt.colData.HKLMdlY))

    def plotExpMacro(self, frame, plotname, X, Y):
        """ Plot macro stress/strain data from extensometer."""
        plotinfo = {'name': 'exp', 'x': X, 'y': Y, 'type': 'marker', 'color': 'blue', 'width': 1}
        frame.centerPanels['plot'].updatePlot(plotname, plotinfo)

    def plotModelMacro(self, frame, plotname, X, Y):
        """ Plot macro stress/strain data from EPSC calculation."""
        plotinfo = {'name': 'model', 'x': X, 'y': Y, 'type': 'line', 'color': 'red', 'width': 1}
        frame.centerPanels['plot'].updatePlot(plotname, plotinfo)

    def updateModelMacro(self, X, Y, lineModel):
        """ Plot macro stress/strain data from EPSC calculation."""
        self.graph.Show(True)
        line = self.graph.updateData(lineModel, X, Y)
        self.graph.replot()

    def updateModelHKL(self, listX, Y, lineModel):
        """ Plot macro stress/strain data from EPSC calculation."""
        self.graph_hkl.Show(True)
        for i in range(self.controller.epscData.numDiffractionData['LongPhase1']):
            self.graph_hkl.updateData(lineModel[i], listX[i], Y)

        self.graph_hkl.replot()

    def plotExpHKL(self, frame, plotname, listX, Y):
        """ Plot hkl specific strain from single peak fitting."""
        colorsList = [
         'blue', 'red', 'green', 'black', 'brown', 'magenta', 'cyan', 'dark grey', 'khaki', 'maroon', 'navy', 'orange',
         'blue', 'red', 'green', 'black', 'brown', 'magenta', 'cyan', 'dark grey', 'khaki', 'maroon', 'navy', 'orange',
         'blue', 'red', 'green', 'black', 'brown', 'magenta', 'cyan', 'dark grey', 'khaki', 'maroon', 'navy', 'orange']
        if plotname == 'HKL-Long':
            index = 'LongPhase1_exp'
        else:
            index = 'TransPhase1_exp'
        for i in range(self.controller.epscData.numDiffractionData[index]):
            name = str(self.controller.epscData.listDiffractionData[index][i].name)
            plotinfo = {'name': 'exp' + name, 'x': list(listX[i]), 'y': Y, 'type': 'marker', 'color': colorsList[i], 'width': 1}
            frame.centerPanels['plot'].updatePlot(plotname, plotinfo)

    def plotModelHKL(self, frame, plotname, listX, Y):
        """ Plot hkl specific strain from EPSC calculation."""
        colorsList = [
         'blue', 'red', 'green', 'black', 'brown', 'magenta', 'cyan', 'dark grey', 'khaki', 'maroon', 'navy', 'orange',
         'blue', 'red', 'green', 'black', 'brown', 'magenta', 'cyan', 'dark grey', 'khaki', 'maroon', 'navy', 'orange',
         'blue', 'red', 'green', 'black', 'brown', 'magenta', 'cyan', 'dark grey', 'khaki', 'maroon', 'navy', 'orange']
        if plotname == 'HKL-Long':
            index = 'LongPhase1'
            type = 'Long'
        else:
            index = 'TransPhase1'
            type = 'Trans'
        for i in range(self.controller.epscData.numDiffractionData[index]):
            name = str(self.controller.epscData.listDiffractionData[index][i].name)
            plotinfo = {'name': type + '_' + name, 'x': list(listX[i]), 'y': Y, 'type': 'line', 'color': colorsList[i], 'width': 1}
            frame.centerPanels['plot'].updatePlot(plotname, plotinfo)


if __name__ == '__main__':
    pass