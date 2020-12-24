# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wehrle/opt/pyZiagn/pyZiagn/ziagn.py
# Compiled at: 2019-11-06 18:11:26
# Size of source mod 2**32: 29676 bytes
import numpy as np
import matplotlib.pyplot as plt
from tikzplotlib import save as tikz_save
import pandas as pd

class uniaxialTensileTest:

    def __init__(self, TestMachine='unibz MTS E0.10', Title='', length0=10, Area0=10):
        self.Area0 = Area0
        self.TestMachine = TestMachine
        self.Title = Title
        self.Area0 = Area0
        self.length0 = length0
        self.strain0 = 0
        self.strainLinLim = []
        self.strainTrueLinLim = []
        self.strainRP02 = []
        self.strainUltimate = []
        self.dispUnit = 'mm'
        self.ForceUnit = 'kN'
        self.dataSets = ['disp', 'Force']
        self.strainEngBreak = None
        self.strainTrueBreak = None

    def loadExample(self):
        self.Area0 = 10
        self.length0 = 10
        self.nSamples = 10001
        self.Force = np.linspace(0, 1000, self.nSamples)
        self.disp = np.linspace(0, 1, self.nSamples)
        self.ForceUnit = 'N'
        self.dispUnit = 'mm'
        self.Title = 'Test 1'
        self.TestMachine = 'None'

    def changeUnits(self, UnitSystem='MPa'):
        if UnitSystem == 'MPa':
            if self.dispUnit == 'm':
                self.disp *= 1000
                self.dispUnit = 'mm'
            if self.dispUnit == 'cm':
                self.disp *= 10
                self.dispUnit = 'mm'
            if self.ForceUnit == 'kN':
                self.Force *= 1000
                self.ForceUnit = 'N'
        if UnitSystem == 'SI':
            if self.dispUnit == 'mm':
                self.disp /= 1000
                self.dispUnit = 'm'
            if self.dispUnit == 'cm':
                self.disp /= 10
                self.dispUnit = 'm'
            if self.ForceUnit == 'kN':
                self.Force *= 1000
                self.ForceUnit = 'N'
        if self.TestMachine == 'unibz MTS E0.10 upper':
            self.disp *= -1

    def calcStressEng(self):
        self.stressEng = self.Force / self.Area0

    def calcStressTrue(self):
        self.stressTrue = self.stressEng * (1 + self.strainEng)

    def calcStrainEng(self):
        self.strainEng = self.disp / self.length0

    def calcStrainTrue(self):
        self.strainTrue = np.log(1 + self.strainEng)

    def calcElasticModulus(self, strain0=0, strain1=0.1):
        self.ElasticModulusStrain0 = strain0
        self.ElasticModulusStrain1 = strain1
        self.ElasticModulus = np.zeros((self.nSamples - 1,))
        for i in range(self.nSamples - 1):
            self.ElasticModulus[i] = (self.stressEng[(i + 1)] - self.stressEng[i]) / (self.strainEng[(i + 1)] - self.strainEng[i])

        stressEngElastic = self.stressEng[(self.strainEng > strain0)]
        strainEngElastic = self.strainEng[(self.strainEng > strain0)]
        stressEngElastic = stressEngElastic[(strainEngElastic < strain1)]
        strainEngElastic = strainEngElastic[(strainEngElastic < strain1)]
        self.ElasticTrend = np.poly1d(np.polyfit(strainEngElastic, stressEngElastic, 1))
        self.YoungsModulus = (self.ElasticTrend(strain1) - self.ElasticTrend(strain0)) / (strain1 - strain0)

    def calcStressUltimate(self):
        self.stressUltimate = max(self.stressEng)
        self.strainUltimate = self.strainEng[np.where(self.stressEng == self.stressUltimate)]

    def calcArea(self):
        self.Area = self.Area0 * self.length0 / self.length

    def calcLength(self):
        self.length = self.length0 + self.disp

    def calcRP02(self):
        stressRP02 = self.stressEng[np.argwhere(np.diff(np.sign(self.ElasticTrend(self.strainEng - 0.002) - self.stressEng)) != 0)]
        strainRP02 = self.strainEng[np.argwhere(np.diff(np.sign(self.ElasticTrend(self.strainEng - 0.002) - self.stressEng)) != 0)]
        if len(stressRP02) > 0:
            self.stressRP02 = stressRP02[0][0]
            self.strainRP02 = strainRP02[0][0]
        else:
            self.stressRP02 = max(self.stressEng)
            self.strainRP02 = max(self.strainEng)

    def calcLinearLimit(self, eps=0.01, strainRangeMax=0.02):
        self.stressLinLimit = self.stressEng[(abs(self.ElasticTrend(self.strainEng) - self.stressEng) / max(self.stressEng) < eps)][(-1)]
        self.strainLinLimit = self.strainEng[(abs(self.ElasticTrend(self.strainEng) - self.stressEng) / max(self.stressEng) < eps)][(-1)]
        self.stressTrueLinLimit = self.stressLinLimit * (1 + self.strainLinLimit)
        self.strainTrueLinLimit = np.log(1 + self.strainLinLimit)
        self.strainTruePlastic = self.strainTrue[(self.strainTrue > self.strainTrueLinLimit)] - self.strainTrueLinLimit
        self.stressTruePlastic = self.stressTrue[(self.strainTrue > self.strainTrueLinLimit)]

    def calcBreak(self, eps=0.001):
        from scipy import signal
        self.stressEng[signal.find_peaks(self.stressEng[(self.stressEng > max(self.stressEng) / 10)])[0]][(-1)]
        self.stressEng[signal.find_peaks(self.stressEng[(self.stressEng > max(self.stressEng) / 10)])[0]][(-1)]
        self.strainEngBreak = self.strainEng[signal.find_peaks(self.stressEng[(self.stressEng > max(self.stressEng) / 10)])[0]][(-1)]
        self.strainTrueBreak = self.strainTrue[signal.find_peaks(self.stressTrue[(self.stressTrue > max(self.stressTrue) / 10)])[0]][(-1)]

    def smoothForce(self):
        from scipy.signal import savgol_filter
        self.ForceRaw = self.Force.copy()
        self.Force = savgol_filter(self.ForceRaw, 101, 3)

    def cutData(self, parameter, value):
        if parameter == 'disp':
            self.dispAll = self.disp.copy()
            self.ForceAll = self.Force.copy()
            self.nSamplesAll = self.nSamples
            self.disp = self.disp[(self.dispAll < value)]
            self.Force = self.Force[(self.dispAll < value)]
            self.nSamples = len(self.disp)

    def resetCutData(self):
        self.disp = self.dispAll.copy()
        self.Force = self.ForceAll.copy()
        self.nSamples = len(self.disp)

    def importTestData(self, FileName, FileFormat='MTScsv', ForceUnit='N', dispUnit='mm', decimalSeparator=','):
        self.FileFormat = FileFormat
        self.rawData = pd.read_csv(FileName, sep='\t', header=None, decimal=decimalSeparator,
          skiprows=(0, 1, 2, 3, 4, 5, 6, 7))
        for i, datai in enumerate(self.dataSets):
            setattr(self, datai, self.rawData[i].values)

        self.nSamples = len(self.rawData[0])

    def zeroStrain(self):
        stress0 = self.stressEng[0].copy()
        self.strain0 = stress0 / self.YoungsModulus
        self.strainEng += self.strain0
        self.strainTrue += self.strain0
        if hasattr(self, 'strainRP02'):
            self.strainRP02 += self.strain0
        if hasattr(self, 'strainLinLimit'):
            self.strainLinLimit += self.strain0
        if hasattr(self, 'strainTrueLinLimit'):
            self.strainTrueLinLimit += self.strain0
        if hasattr(self, 'strainUltimate'):
            self.strainUltimate += self.strain0
        if hasattr(self, 'YoungsModulus'):
            self.calcElasticModulus(self.ElasticModulusStrain0 + self.strain0, self.ElasticModulusStrain1 + self.strain0)

    def calcResilienceModulus(self):
        self.ResilienceModulus = self.stressLinLimit * self.strainLinLimit / 2.0

    def calcToughnessModulus(self):
        self.ToughnessModulus = np.trapz((self.stressEng), x=(self.strainEng))

    def approxRambergOsgood(self):
        from scipy.optimize import curve_fit
        self.stressRambergOsgood = np.linspace(0, self.stressUltimate, 10000)
        self.alphaRambergOsgood = 0.002 * self.YoungsModulus / self.stressRP02

        def fRambergOsgood(stress, nRambergOsgood):
            return stress / self.YoungsModulus + self.alphaRambergOsgood * self.stressRP02 / self.YoungsModulus * (stress / self.stressRP02) ** nRambergOsgood

        stressEngCut = self.stressEng[(self.stressEng < self.stressUltimate)]
        strainEngCut = self.strainEng[(self.stressEng < self.stressUltimate)]
        self.nRambergOsgood, pcov = curve_fit(fRambergOsgood, stressEngCut, strainEngCut,
          p0=5)
        self.strainRambergOsgood = self.stressRambergOsgood / self.YoungsModulus + self.alphaRambergOsgood * self.stressRP02 / self.YoungsModulus * (self.stressRambergOsgood / self.stressRP02) ** self.nRambergOsgood

    def approxHockettSherby(self):
        from scipy.optimize import curve_fit
        self.stressPlastic = max(self.stressTrue) - self.stressTrueLinLimit

        def fHockettSherby(strain, cHockettSherby, nHockettSherby):
            return self.stressTrueLinLimit + self.stressPlastic - self.stressPlastic * np.exp(-cHockettSherby * strain ** nHockettSherby)

        stressPlastic = self.stressTrue[(self.strainTrue > self.strainTrueLinLimit)]
        strainPlastic = self.strainTrue[(self.strainTrue > self.strainTrueLinLimit)] - self.strainTrueLinLimit
        (self.cHockettSherby, self.nHockettSherby), pcov = curve_fit(fHockettSherby, strainPlastic, stressPlastic, maxfev=1000000)
        self.strainHockettSherby = strainPlastic
        self.stressHockettSherby = self.stressTrueLinLimit + self.stressPlastic - self.stressPlastic * np.exp(-self.cHockettSherby * self.strainHockettSherby ** self.nHockettSherby)

    def approxGhosh(self):
        from scipy.optimize import curve_fit
        self.stressPlastic = max(self.stressTrue) - self.stressTrueLinLimit

        def fGhosh(strain, aGhosh, bGhosh, cGhosh, nGhosh):
            return aGhosh * (bGhosh + strain) ** nGhosh - cGhosh

        stressPlastic = self.stressTrue[(self.strainTrue > self.strainTrueLinLimit)]
        strainPlastic = self.strainTrue[(self.strainTrue > self.strainTrueLinLimit)] - self.strainTrueLinLimit
        (self.aGhosh, self.bGhosh, self.cGhosh, self.nGhosh), pcov = curve_fit(fGhosh, strainPlastic, stressPlastic, maxfev=1000000)
        self.strainGhosh = strainPlastic
        self.stressGhosh = self.aGhosh * (self.bGhosh + self.strainGhosh) ** self.nGhosh - self.cGhosh

    def plotForceDisp(self, Show=True, SaveTex=True, SavePng=True, SaveSvg=True, Grid=False, plotSize=(7, 5)):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=plotSize)
        plt.grid(Grid)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        plt.plot(self.disp, self.Force)
        plt.ylabel('force $F$ [N]')
        plt.xlabel('displacement $u$ [mm]')
        plt.title(self.Title)
        plt.xlim(xmin=0)
        plt.ylim(ymin=0)
        plt.tight_layout()
        if SaveTex:
            tikz_save((self.Title + '_ForceDisp.tex'), show_info=False, strict=False,
              figureheight='\\figureheight',
              figurewidth='\\figurewidth',
              extra_axis_parameters={
             'axis lines*=left'})
        if SavePng:
            plt.savefig((self.Title + '_ForceDisp.png'), format='png')
        if SaveSvg:
            plt.savefig((self.Title + '_ForceDisp.svg'), format='svg')
        if Show:
            plt.show()

    def plotStressStrainEng(self, Show=True, SaveTex=True, SavePng=True, SaveSvg=True, Grid=False, plotSize=(7, 5)):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=plotSize)
        plt.grid(Grid)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        plt.plot(self.strainEng, self.stressEng)
        plt.ylabel('engineering stress $\\sigma_{\\mathrm{eng}}$ [MPa]')
        plt.xlabel('engineering strain $\\varepsilon_{\\mathrm{eng}}$ [-]')
        plt.title(self.Title)
        plt.xlim(xmin=0)
        plt.ylim(ymin=0)
        plt.tight_layout()
        if SaveTex:
            tikz_save((self.Title + '_StressStrainEng.tex'), show_info=False, strict=False,
              figureheight='\\figureheight',
              figurewidth='\\figurewidth',
              extra_axis_parameters={
             'axis lines*=left'})
        if SavePng:
            plt.savefig((self.Title + '_StressStrainEng.png'), format='png')
        if SaveSvg:
            plt.savefig((self.Title + '_StressStrainEng.svg'), format='svg')
        if Show:
            plt.show()

    def plotStressStrainTrue(self, Show=True, SaveTex=True, SavePng=True, SaveSvg=True, Grid=False, plotSize=(7, 5)):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=plotSize)
        plt.grid(Grid)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        plt.plot(self.strainTrue, self.stressTrue)
        plt.ylabel('true stress $\\sigma_{\\mathrm{true}}$ [MPa]')
        plt.xlabel('true strain $\\varepsilon_{\\mathrm{true}}$ [-]')
        plt.title(self.Title)
        plt.xlim(xmin=0)
        plt.ylim(ymin=0)
        plt.tight_layout()
        if SaveTex:
            tikz_save((self.Title + '_StressStrainTrue.tex'), show_info=False, strict=False,
              figureheight='\\figureheight',
              figurewidth='\\figurewidth',
              extra_axis_parameters={
             'axis lines*=left'})
        if SavePng:
            plt.savefig((self.Title + '_StressStrainTrue.png'), format='png')
        if SaveSvg:
            plt.savefig((self.Title + '_StressStrainTrue.svg'), format='svg')
        if Show:
            plt.show()

    def plotStressStrainEngTrue(self, Show=True, SaveTex=True, SavePng=True, SaveSvg=True, Grid=False, plotSize=(7, 5)):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=plotSize)
        plt.grid(Grid)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        plt.plot((self.strainEng), (self.stressEng), label='engineering stress–strain')
        plt.plot((self.strainTrue), (self.stressTrue), label='true stress–strain')
        plt.ylabel('stress $\\sigma$ [MPa]')
        plt.xlabel('strain $\\varepsilon$ [-]')
        plt.legend(frameon=False)
        plt.title(self.Title)
        plt.xlim(xmin=0)
        plt.ylim(ymin=0)
        plt.tight_layout()
        if SaveTex:
            tikz_save((self.Title + '_StressStrainEngTrue.tex'), show_info=False, strict=False,
              figureheight='\\figureheight',
              figurewidth='\\figurewidth',
              extra_axis_parameters={
             'axis lines*=left'})
        if SavePng:
            plt.savefig((self.Title + '_StressStrainEngTrue.png'), format='png')
        if SaveSvg:
            plt.savefig((self.Title + '_StressStrainEngTrue.svg'), format='svg')
        if Show:
            plt.show()

    def plotStressStrainTruePlastic(self, Show=True, SaveTex=True, SavePng=True, SaveSvg=True, Grid=False, plotSize=(7, 5)):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=plotSize)
        plt.grid(Grid)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        plt.plot(self.strainTruePlastic, self.stressTruePlastic)
        plt.ylabel('true plastic stress $\\sigma_{\\mathrm{true,pl}}$ [MPa]')
        plt.xlabel('true plastic strain $\\varepsilon_{\\mathrm{true,pl}}$ [-]')
        plt.title(self.Title)
        plt.xlim(xmin=0)
        plt.ylim(ymin=0)
        plt.tight_layout()
        if SaveTex:
            tikz_save((self.Title + '_StressStrainTruePlastic.tex'), show_info=False,
              strict=False,
              figureheight='\\figureheight',
              figurewidth='\\figurewidth',
              extra_axis_parameters={
             'axis lines*=left'})
        if SavePng:
            plt.savefig((self.Title + '_StressStrainTruePlastic.png'), format='png')
        if SaveSvg:
            plt.savefig((self.Title + '_StressStrainTruePlastic.svg'), format='svg')
        if Show:
            plt.show()

    def plotForceDispSmoothRaw(self, Show=True, SaveTex=True, SavePng=True, SaveSvg=True, Grid=False, plotSize=(7, 5)):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=plotSize)
        plt.grid(Grid)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        plt.plot((self.dispAll), (self.ForceAll), label='raw data')
        plt.plot((self.disp), (self.Force), label='smoothed and cut')
        plt.ylabel('force $F$ [N]')
        plt.xlabel('displacement $u$ [mm]')
        plt.legend(frameon=False)
        plt.title(self.Title)
        plt.xlim(xmin=0)
        plt.ylim(ymin=0)
        plt.tight_layout()
        if SaveTex:
            tikz_save((self.Title + '_ForceDispSmoothRaw.tex'), show_info=False, strict=False,
              figureheight='\\figureheight',
              figurewidth='\\figurewidth',
              extra_axis_parameters={
             'axis lines*=left'})
        if SavePng:
            plt.savefig((self.Title + '_ForceDispSmoothRaw.png'), format='png')
        if SaveSvg:
            plt.savefig((self.Title + '_ForceDispSmoothRaw.svg'), format='svg')
        if Show:
            plt.show()

    def plotStressStrainEngYoungs(self, stressMin=0, strainMin=0, stressMax=50, strainMax=0.075, Show=True, SaveTex=True, SavePng=True, SaveSvg=True, Grid=False, plotSize=(7, 5)):
        strain1 = np.linspace(0.0, max(self.strainEng), self.nSamples)
        strain2 = np.linspace(0.002, max(self.strainEng), self.nSamples)
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=plotSize)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        plt.plot((self.strainEng), (self.stressEng), label='material behavior')
        plt.plot(strain1, (self.ElasticTrend(strain1)), '--', label="Young's modulus")
        plt.ylabel('engineering stress $\\sigma_{\\mathrm{eng}}$ [MPa]')
        plt.xlabel('engineering strain $\\varepsilon_{\\mathrm{eng}}$ [-]')
        plt.title(self.Title)
        plt.xlim(xmin=strainMin, xmax=strainMax)
        plt.ylim(ymin=stressMin, ymax=stressMax)
        plt.grid(Grid)
        plt.legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        if SaveTex:
            tikz_save((self.Title + '_StressStrainEng02.tex'), show_info=False, strict=False,
              figureheight='\\figureheight',
              figurewidth='\\figurewidth',
              extra_axis_parameters={
             'axis lines*=left'})
        if SavePng:
            plt.savefig((self.Title + '_StressStrainEng02.png'), format='png')
        if SaveSvg:
            plt.savefig((self.Title + '_StressStrainEng02.svg'), format='svg')
        if Show:
            plt.show()

    def plotStressStrainEngRP02(self, stressMin=0, strainMin=0, stressMax=50, strainMax=0.075, Show=True, SaveTex=True, SavePng=True, SaveSvg=True, Grid=False, plotSize=(7, 5)):
        strain1 = np.linspace(0.0, max(self.strainEng), self.nSamples)
        strain2 = np.linspace(0.002, max(self.strainEng), self.nSamples)
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=plotSize)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        plt.plot((self.strainEng), (self.stressEng), label='material behavior')
        plt.plot(strain1, (self.ElasticTrend(strain1)), '--', label="Young's modulus")
        plt.plot(strain2, (self.ElasticTrend(strain2 - 0.002)), '--', label='0.2% offset')
        plt.plot((self.strainRP02), (self.stressRP02), 'o', label='$R_{P0.2}$')
        plt.plot((self.strainLinLimit), (self.stressLinLimit), 'o', label='linear limit')
        plt.ylabel('engineering stress $\\sigma_{\\mathrm{eng}}$ [MPa]')
        plt.xlabel('engineering strain $\\varepsilon_{\\mathrm{eng}}$ [-]')
        plt.title(self.Title)
        plt.xlim(xmin=strainMin, xmax=strainMax)
        plt.ylim(ymin=stressMin, ymax=stressMax)
        plt.grid(Grid)
        plt.legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        if SaveTex:
            tikz_save((self.Title + '_StressStrainEng02.tex'), show_info=False, strict=False,
              figureheight='\\figureheight',
              figurewidth='\\figurewidth',
              extra_axis_parameters={
             'axis lines*=left'})
        if SavePng:
            plt.savefig((self.Title + '_StressStrainEng02.png'), format='png')
        if SaveSvg:
            plt.savefig((self.Title + '_StressStrainEng02.svg'), format='svg')
        if Show:
            plt.show()

    def plotStressStrainEngAll(self, yMax=None, xMax=None, Show=True, SaveTex=True, SavePng=True, SaveSvg=True, Grid=False, plotSize=(7, 5)):
        strain1 = np.linspace(0.0, max(self.strainEng), self.nSamples)
        strain2 = np.linspace(0.002, max(self.strainEng), self.nSamples)
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=plotSize)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        plt.plot((self.strainEng), (self.stressEng), label='material behavior')
        plt.plot(strain1, (self.ElasticTrend(strain1)), '--', label="Young's modulus")
        plt.plot(strain2, (self.ElasticTrend(strain2 - 0.002)), '--', label='0.2% offset')
        plt.plot((self.strainEng[0]), (self.stressEng[0]), '.', label='initial state of test')
        plt.plot((self.strainRP02), (self.stressRP02), 'o', label='$R_{P0.2}$')
        plt.plot((self.strainLinLimit), (self.stressLinLimit), 'o', label='linear limit')
        plt.plot((self.strainUltimate), (self.stressUltimate), 'o', label='ultimate strength')
        if self.strainEngBreak is not None:
            plt.plot((self.strainEngBreak), (self.stressEng[(self.strainEng == self.strainEngBreak)][(-1)]),
              'x',
              label='break')
        else:
            plt.ylabel('engineering stress $\\sigma_{\\mathrm{eng}}$ [MPa]')
            plt.xlabel('engineering strain $\\varepsilon_{\\mathrm{eng}}$ [-]')
            plt.title(self.Title)
            if xMax is not None:
                plt.xlim(xmin=0)
            else:
                plt.xlim(xmin=0, xmax=xMax)
            if yMax is None:
                plt.ylim(ymin=0, ymax=(max(self.stressEng) * 1.05))
            else:
                plt.ylim(ymin=0, ymax=yMax)
        plt.grid(Grid)
        plt.legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        if SaveTex:
            tikz_save((self.Title + '_StressStrainEng02.tex'), show_info=False, strict=False,
              figureheight='\\figureheight',
              figurewidth='\\figurewidth',
              extra_axis_parameters={
             'axis lines*=left'})
        if SavePng:
            plt.savefig((self.Title + '_StressStrainEng02.png'), format='png')
        if SaveSvg:
            plt.savefig((self.Title + '_StressStrainEng02.svg'), format='svg')
        if Show:
            plt.show()


def export2Excel(TestList, FileName='TestSummary.xlsx', PrintData=True):
    TestData = {'test':[i.Title for i in TestList], 
     "Young's modulus":[i.YoungsModulus for i in TestList], 
     'initial stress of test':[i.stressEng[0] for i in TestList], 
     'stress at linear limit':[i.stressLinLimit for i in TestList], 
     'Rp0.2':[i.stressRP02 for i in TestList], 
     'ultimate stress':[i.stressUltimate for i in TestList], 
     'breaking stress':[i.stressEng[(-1)] for i in TestList], 
     'breaking strain':[i.strainEng[(-1)] for i in TestList]}
    TestDataFrame = pd.DataFrame(TestData, columns=['test', "Young's modulus",
     'initial stress of test',
     'stress at linear limit',
     'Rp0.2', 'ultimate stress',
     'breaking stress',
     'breaking strain'])
    TestDataFrame.to_excel(FileName, index=None, header=True)
    if PrintData:
        print(TestDataFrame)


def plotMulti(TestList, Show=True, SaveTex=True, SavePng=True, SaveSvg=True, PlotName='Comparison', Grid=False, strainMin=0.0, strainMax=0.75, stressMin=0.0, stressMax=55, plotSize=(10, 10)):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=plotSize)
    plt.grid(Grid)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    markers = ['s', 'v', '^', 'o', 'D', '+']
    for i, test in enumerate(TestList):
        plt.plot((test.strainEng), (test.stressEng), marker=(markers[(int(test.Title[(-1)]) - 1)]),
          markevery=500,
          color=('C' + str(int(test.Title[0]) - 1)),
          label=(test.Title))

    plt.ylabel('engineering stress $\\sigma_{\\mathrm{eng}}$ [MPa]')
    plt.xlabel('engineering strain $\\varepsilon_{\\mathrm{eng}}$ [-]')
    plt.xlim(xmin=strainMin, xmax=strainMax)
    plt.ylim(ymin=stressMin, ymax=stressMax)
    plt.legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    if SaveTex:
        tikz_save((PlotName + '_.tex'), show_info=False, strict=False, figureheight='\\figureheight',
          figurewidth='\\figurewidth',
          extra_axis_parameters={
         'axis lines*=left'})
    if SavePng:
        plt.savefig((PlotName + '.png'), format='png')
    if SaveSvg:
        plt.savefig((PlotName + '.svg'), format='svg')
    if Show:
        plt.show()


if __name__ == '__main__':
    print('Test of package')
    Test = uniaxialTensileTest()
    Test.loadExample()
    Test.changeUnits()
    Test.calcStressEng()
    Test.calcStrainEng()
    Test.calcStressTrue()
    Test.calcStrainTrue()
    Test.calcElasticModulus(strain0=0.01, strain1=0.02)
    Test.calcRP02()
    Test.calcLinearLimit()
    Test.calcToughnessModulus()
    Test.calcResilienceModulus()
    Test.plotForceDisp()
    Test.plotStressStrainEng()