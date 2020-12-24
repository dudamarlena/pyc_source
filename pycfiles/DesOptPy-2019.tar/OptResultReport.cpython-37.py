# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wehrle/opt/DesOptPy/DesOptPy/OptResultReport.py
# Compiled at: 2019-06-04 13:16:18
# Size of source mod 2**32: 43045 bytes
"""
-------------------------------------------------------------------------------
Title:          OptResultReport.py
Units:          Unitless
Date:           July 9, 2016
Authors:        E. J. Wehrle, S. Rudolph, F. Wachter
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
Description
-------------------------------------------------------------------------------
Make result report for the optimization run

-------------------------------------------------------------------------------
To do and ideas
-------------------------------------------------------------------------------
"""
from __future__ import absolute_import, division, print_function
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.colors as colors
from matplotlib import cm
from matplotlib.font_manager import FontProperties
import numpy as np, sys, os
try:
    import _pickle as pickle
except:
    try:
        import cPickle as pickle
    except:
        import pickle

import shutil, subprocess, time, platform
from subprocess import Popen
try:
    from matplotlib2tikz import save as tikz_save
    TikzRendered = True
except:
    TikzRendered = False

TikzRendered = False
ListBadInkscape = [
 0.91, 0.92]
try:
    InkscapeVersion = float(subprocess.Popen('inkscape --version', shell=True,
      stdout=(subprocess.PIPE)).stdout.read()[8:13])
    FigureSubfolders = True
except:
    InkscapeVersion = None
    FigureSubfolders = False

operatingSystem = platform.uname()[0]
if operatingSystem != 'Windows':
    InkscapeCall = 'inkscape'
    LyxCall = 'lyx'
else:
    if operatingSystem == 'Windows':
        InkscapeCall = 'inkscape'
        LyxCall = 'lyx.exe'
    fontP = FontProperties()
    fontP.set_size(10)
    fontPP = FontProperties()
    fontPP.set_size(10)
    FileTypeRendered = ['png', 'svg']
    FileTypeRaw = ['pdf', 'svg']

    def BarPlot(figName, fun0, funOpt, funLabel0, funLabelOpt, xLabel, yLabel, ResultsFolder, OptName, figType=FileTypeRendered, Color0='#FAA43A', ColorOpt='#5DA5DA', figsizex=6, figsizey=3, width=0.5, xspacing=0.25, dpi=200, xtick=True, usetex=False, Tikz=False):
        plt.rc('text', usetex=usetex)
        Plot = plt.figure(figsize=(figsizex, figsizey), dpi=dpi)
        ax = Plot.add_subplot(111)
        nf = np.size(fun0)
        ind = np.arange(nf)
        rects1 = ax.bar((ind + xspacing * 2.5), fun0, width, color=Color0)
        rects2 = ax.bar((ind + xspacing * 2.5 + width / 2), funOpt, width, color=ColorOpt)
        lgd = ax.legend((rects1[0], rects2[0]), (funLabel0, funLabelOpt), frameon=False,
          prop=fontP,
          bbox_to_anchor=(1.05, 1),
          loc=2,
          borderaxespad=0.0)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        plt.xlim(xmin=(xspacing * 2), xmax=(nf + width / 2 + xspacing))
        plt.ylim(ymin=(np.min((np.min(fun0), np.min(funOpt), 0.0))), ymax=(np.max((np.max(fun0), np.max(funOpt)))))
        if xtick == False:
            plt.tick_params(axis='x', which='both', bottom='off', labelbottom='off')
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        for ii in range(np.size(figType)):
            plt.savefig((ResultsFolder + OptName + '_' + figName + '.' + figType[ii]), bbox_extra_artists=(
             lgd,),
              bbox_inches='tight')

        if Tikz == True:
            tikz_save(ResultsFolder + OptName + '_' + figName + '.tikz')
        plt.close()
        fail = 0
        return fail


    def SingleConvPlot(figName, data, dataLabel, xLabel, yLabel, ResultsFolder, OptName, figType=FileTypeRendered, figsizex=6, figsizey=3, width=0.5, xspacing=0.25, dpi=200, xtick=True, usetex=False, Tikz=False, labelSubscripts=True):
        plt.rc('text', usetex=usetex)
        Plot = plt.figure(figsize=(figsizex, figsizey), dpi=dpi)
        ax = Plot.add_subplot(111)
        jet = plt.get_cmap('jet')
        cNorm = colors.Normalize(vmin=0, vmax=(data[0].size))
        scalarMap = cm.ScalarMappable(norm=cNorm, cmap=jet)
        if len(data.shape) > 1:
            for n in range(np.size(data[0])):
                if labelSubscripts == True:
                    if usetex == True:
                        ax.plot((data.T[n]), color=(scalarMap.to_rgba(n)), label=(dataLabel % str(n + 1)))
                    else:
                        ax.plot((data.T[n]), color=(scalarMap.to_rgba(n)), label=(dataLabel % str(n + 1)))
                else:
                    ax.plot((data.T[n]), color=(scalarMap.to_rgba(n)), label=dataLabel)

        else:
            if labelSubscripts == True:
                if usetex == True:
                    ax.plot(data, color=(scalarMap.to_rgba(0)), label=(dataLabel % str(1)))
                else:
                    ax.plot(data, color=(scalarMap.to_rgba(0)), label=(dataLabel % str(1)))
            else:
                ax.plot(data, color=(scalarMap.to_rgba(0)), label=dataLabel)
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.xlim(xmin=0, xmax=(len(data) - 1))
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        numColx = np.size(data[0]) / 12 + 1
        if numColx > 3:
            numColx = 3
        plt.yticks(size=(10 + (numColx - 1) * 4))
        lgd = ax.legend(bbox_to_anchor=[1.05, 1], loc=2, ncol=(int(numColx)), frameon=False,
          prop=fontPP)
        for ii in range(np.size(figType)):
            plt.savefig((ResultsFolder + OptName + '_' + figName + '.' + figType[ii]), bbox_extra_artists=(
             lgd,),
              bbox_inches='tight')

        if Tikz:
            tikz_save(ResultsFolder + OptName + '_' + figName + '.tikz')
        plt.close()
        fail = 0
        return fail


    def DoubleConvPlot(figName, data, dataLabel, xLabel, yLabel, Color, ResultsFolder, OptName, figType=FileTypeRendered, figsizex=6, figsizey=3, width=0.5, xspacing=0.25, dpi=200, xtick=True, usetex=False, Tikz=False):
        plt.rc('text', usetex=usetex)
        Plot = plt.figure(figsize=(figsizex, figsizey), dpi=dpi)
        ax1 = Plot.add_subplot(111)
        ax1.plot((data[0]), (Color[0]), label=(dataLabel[0]))
        plt.xlabel(xLabel)
        plt.ylabel(yLabel[0])
        ax2 = ax1.twinx()
        ax2.plot((data[1]), (Color[1]), label=(dataLabel[1]))
        plt.ylabel(yLabel[1])
        handles1, labels1 = ax1.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        handles = handles1 + handles2
        labels = labels1 + labels2
        lgd = ax1.legend(handles, labels, bbox_to_anchor=[1.05, 1], loc=2, frameon=False,
          prop=fontPP)
        plt.xlim(xmin=0, xmax=(len(data[0]) - 1))
        ax1.spines['right'].set_visible(False)
        ax1.spines['top'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        ax1.yaxis.set_ticks_position('left')
        ax1.xaxis.set_ticks_position('bottom')
        ax1.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        plt.tight_layout()
        for ii in range(np.size(figType)):
            plt.savefig((ResultsFolder + OptName + '_' + figName + '.' + figType[ii]), bbox_extra_artists=(
             lgd,),
              bbox_inches='tight')

        if Tikz:
            tikz_save(ResultsFolder + OptName + '_' + figName + '.tikz')
        plt.close()
        fail = 0
        return fail


    def OptResultReport(optname, OptAlg, DesOptDir, diagrams=1, tables=0, lyx=0):
        DirRunFiles = DesOptDir + '/Results/' + optname + '/RunFiles/'
        ResultsFolder = DesOptDir + '/Results/' + optname + '/ResultReport/'
        file_OptSolData = open(DirRunFiles + optname + '_OptSol.pkl', 'rb')
        OptSolData = pickle.load(file_OptSolData)
        x0 = OptSolData['x0']
        xOpt = OptSolData['xOpt']
        xOptNorm = OptSolData['xOptNorm']
        xIter = OptSolData['xIter'].T
        xIterNorm = OptSolData['xIterNorm'].T
        fOpt = OptSolData['fOpt']
        fIter = OptSolData['fIter']
        fIterNorm = OptSolData['fIterNorm']
        gOpt = OptSolData['gOpt']
        gIter = OptSolData['gIter'].T
        gMaxIter = OptSolData['gMaxIter']
        fGradIter = OptSolData['fNablaIter'].T
        gGradIter = OptSolData['gNablaIter'].T
        fGradOpt = OptSolData['fNablaOpt']
        gGradOpt = OptSolData['gNablaOpt']
        OptName = OptSolData['OptName']
        OptModel = OptSolData['OptModel']
        OptTime = OptSolData['OptTime']
        today = OptSolData['today']
        computerName = OptSolData['computerName']
        operatingSystem = OptSolData['operatingSystem']
        architecture = OptSolData['architecture']
        nProcessors = OptSolData['nProcessors']
        userName = OptSolData['userName']
        Alg = OptSolData['Alg']
        DesVarNorm = OptSolData['DesVarNorm']
        KKTmax = OptSolData['KKTmax']
        lambda_c = OptSolData['lambda_c']
        nEval = OptSolData['nEval']
        nIter = OptSolData['nIter']
        SPg = OptSolData['SPg']
        gc = OptSolData['gc']
        x0norm = OptSolData['x0norm']
        xL = OptSolData['xL']
        xU = OptSolData['xU']
        ng = OptSolData['ng']
        nx = OptSolData['nx']
        nf = OptSolData['nf']
        Opt1Order = OptSolData['Opt1Order']
        hhmmss0 = OptSolData['hhmmss0']
        hhmmss1 = OptSolData['hhmmss1']
        if Alg in ('CONMIN', 'MMA', 'GCMMA', 'NLPQLP', 'SLSQP', 'FSQP', 'KSOPT'):
            xAxisLabel = 'Iteration'
            xAxisLabelR = 'Iteration'
        else:
            if Alg == 'NSGA2':
                xAxisLabel = 'Generation'
                xAxisLabelR = 'Generation'
            else:
                if nIter == nEval:
                    xAxisLabel = 'Evaluation'
                    xAxisLabelR = 'Evaluation'
                else:
                    xAxisLabel = 'Evaluation'
                    xAxisLabelR = 'Evaluation'
        if diagrams == 1:
            print('          Diagram generation process:          \n')
            progressbar(0, 82)
            if np.size(gOpt) > 0:
                data = [
                 fIterNorm, gMaxIter]
                dataLabel = ['$\\hat{\\mathsf{f}}$', '$\\mathsf{g}_\\mathrm{max}$']
                Color = ['b', 'g']
                yLabel = [
                 '$\\hat{\\mathsf{f}}$', '$\\mathsf{g}_\\mathrm{max}$']
                DoubleConvPlot('fgMaxIterNormRendered', data, dataLabel, xAxisLabel,
                  yLabel, Color, ResultsFolder, OptName, figType=FileTypeRendered,
                  figsizex=5.5,
                  usetex=True,
                  Tikz=TikzRendered)
                data = [fIterNorm, gMaxIter]
                dataLabel = ['\\$\\fn\\$', '$\\gmax\\$']
                Color = ['b', 'g']
                yLabel = [
                 '\\$\\fn\\$', '\\$\\gmax\\$']
                DoubleConvPlot('fgMaxIterNorm', data, dataLabel, xAxisLabelR, yLabel,
                  Color, ResultsFolder, OptName, figType=FileTypeRaw,
                  figsizex=5.5,
                  usetex=False,
                  Tikz=False)
                progressbar(6, 82)
                data = [
                 fIter, gMaxIter]
                dataLabel = ['$\\mathsf{f}$', '$\\mathsf{g}_\\mathrm{max}$']
                Color = ['b', 'g']
                yLabel = [
                 '$\\mathsf{f}$', '$\\mathsf{g}_\\mathrm{max}$']
                DoubleConvPlot('fgMaxIterRendered', data, dataLabel, xAxisLabel, yLabel,
                  Color, ResultsFolder, OptName, figType=FileTypeRendered,
                  figsizex=6,
                  usetex=True,
                  Tikz=TikzRendered)
                data = [fIter, gMaxIter]
                dataLabel = ['\\$\\f\\$', '$\\gmax\\$']
                Color = ['b', 'g']
                yLabel = [
                 '\\$\\f\\$', '\\$\\gmax\\$']
                DoubleConvPlot('fgMaxIter', data, dataLabel, xAxisLabelR, yLabel, Color,
                  ResultsFolder, OptName, figType=FileTypeRaw, figsizex=6,
                  usetex=False,
                  Tikz=False)
                progressbar(12, 82)
                fail = SingleConvPlot('gIterRendered', gIter, '$\\mathsf{g}_{%s}$', xAxisLabel,
                  '$\\mathsf{g}$', ResultsFolder, OptName,
                  figType=FileTypeRendered, figsizex=6,
                  figsizey=3,
                  width=0.5,
                  xspacing=0.25,
                  dpi=200,
                  xtick=True,
                  usetex=True,
                  Tikz=TikzRendered)
                fail = SingleConvPlot('gIter', gIter, '\\$\\g_{%s}$', xAxisLabelR, '\\$\\g\\$',
                  ResultsFolder, OptName, figType=FileTypeRaw,
                  figsizex=6,
                  figsizey=3,
                  width=0.5,
                  xspacing=0.25,
                  dpi=200,
                  xtick=True,
                  usetex=False,
                  Tikz=False)
                fail = BarPlot('gBarRendered', (gIter[0]), gOpt, '$g^0$', '$g^{*}$', 'Constraint',
                  '$g$', ResultsFolder, OptName, figType=FileTypeRendered,
                  Color0='#FAA43A',
                  ColorOpt='#5DA5DA',
                  figsizex=6,
                  figsizey=3,
                  width=0.5,
                  xspacing=0.25,
                  dpi=200,
                  usetex=True,
                  Tikz=TikzRendered)
                fail = BarPlot('gBar', (gIter[0]), gOpt, '\\$\\gin$', '\\$\\go$', 'Constraint',
                  '\\$\\g$', ResultsFolder, OptName, figType=FileTypeRaw,
                  Color0='#FAA43A',
                  ColorOpt='#5DA5DA',
                  figsizex=6,
                  figsizey=3,
                  width=0.5,
                  xspacing=0.25,
                  dpi=200,
                  usetex=False,
                  Tikz=False)
                progressbar(18, 82)
            else:
                fail = SingleConvPlot('fgMaxIterNormRendered', fIterNorm, '$\\hat{\\mathsf{f}}$',
                  xAxisLabel, '$\\hat{\\mathsf{f}}$',
                  ResultsFolder, OptName, figType=FileTypeRendered,
                  figsizex=6,
                  figsizey=3,
                  width=0.5,
                  xspacing=0.25,
                  dpi=200,
                  xtick=True,
                  usetex=True,
                  Tikz=TikzRendered,
                  labelSubscripts=False)
                fail = SingleConvPlot('fgMaxIterNorm', fIterNorm, '\\$\\fn\\$', xAxisLabelR,
                  '\\$\\fn\\$', ResultsFolder, OptName,
                  figType=FileTypeRaw, figsizex=6, figsizey=3,
                  width=0.5,
                  xspacing=0.25,
                  dpi=200,
                  xtick=True,
                  usetex=False,
                  labelSubscripts=False)
                fail = SingleConvPlot('fgMaxIterRendered', fIter, '$\\hat{\\mathsf{f}}$',
                  xAxisLabel, '$\\hat{\\mathsf{f}}$',
                  ResultsFolder, OptName, figType=FileTypeRendered,
                  figsizex=6,
                  figsizey=3,
                  width=0.5,
                  xspacing=0.25,
                  dpi=200,
                  xtick=True,
                  usetex=True,
                  Tikz=TikzRendered,
                  labelSubscripts=False)
                fail = SingleConvPlot('fgMaxIter', fIter, '\\$\\f\\$', xAxisLabelR, '\\$\\f\\$',
                  ResultsFolder, OptName, figType=FileTypeRaw,
                  figsizex=6,
                  figsizey=3,
                  width=0.5,
                  xspacing=0.25,
                  dpi=200,
                  xtick=True,
                  usetex=False,
                  labelSubscripts=False)
            progressbar(24, 82)
            fail = BarPlot('fBarRendered', (fIter[0]), fOpt, '$\\mathsf{f}^0$', '$\\mathsf{f}^{*}$',
              '', '$\\mathsf{f}$', ResultsFolder, OptName,
              figType=FileTypeRendered, Color0='#FAA43A', ColorOpt='#5DA5DA',
              figsizex=6,
              figsizey=3,
              width=0.5,
              xspacing=0.25,
              dpi=200,
              usetex=True,
              xtick=False,
              Tikz=TikzRendered)
            fail = BarPlot('fBar', (fIter[0]), fOpt, '\\$\\fin\\$', '\\$\\fo\\$', '', '\\$\\f\\$',
              ResultsFolder, OptName, figType=FileTypeRaw, Color0='#FAA43A',
              ColorOpt='#5DA5DA',
              figsizex=6,
              figsizey=3,
              width=0.5,
              xspacing=0.25,
              dpi=200,
              usetex=False,
              xtick=False)
            progressbar(26, 82)
            if len(fGradIter) is not 0:
                DataLabel = '$\\nabla_{\\mathsf{x}_{%s}} \\mathsf{f}$'
                fail = SingleConvPlot('fGradIterRendered', fGradIter, DataLabel, xAxisLabel,
                  '$\\nabla \\mathsf{f}$', ResultsFolder,
                  OptName, figsizey=3, width=0.5,
                  xspacing=0.25,
                  dpi=200,
                  xtick=True,
                  usetex=True,
                  Tikz=TikzRendered)
                fail = SingleConvPlot('fGradIter', fGradIter, '\\$\\d_{\\x_{%s}} \\f\\$',
                  xAxisLabelR, '\\$\\d \\f\\$',
                  ResultsFolder, OptName, figType=FileTypeRaw,
                  figsizex=6,
                  figsizey=3,
                  width=0.5,
                  xspacing=0.25,
                  dpi=200,
                  xtick=True,
                  usetex=False)
            progressbar(35, 82)
            fail = SingleConvPlot('xIterRendered', xIter, '$\\mathsf{x}_{%s}$', xAxisLabel,
              '$\\mathsf{x}$', ResultsFolder, OptName,
              figsizex=6, figsizey=3,
              width=0.5,
              xspacing=0.25,
              dpi=200,
              xtick=True,
              usetex=True,
              Tikz=TikzRendered)
            fail = SingleConvPlot('xIter', xIter, '\\$\\x_{%s}\\$', xAxisLabelR, '\\$\\x\\$',
              ResultsFolder, OptName, figType=FileTypeRaw,
              figsizex=6,
              figsizey=3,
              width=0.5,
              xspacing=0.25,
              dpi=200,
              xtick=True,
              usetex=False)
            progressbar(41, 82)
            if DesVarNorm in ('None', None, False):
                pass
            else:
                fail = SingleConvPlot('xIterNormRendered', xIterNorm, '$\\hat{\\mathsf{x}}_{%s}$',
                  xAxisLabel, '$\\hat{\\mathsf{x}}$',
                  ResultsFolder, OptName, figType=FileTypeRendered,
                  figsizex=6,
                  figsizey=3,
                  width=0.5,
                  xspacing=0.25,
                  dpi=200,
                  xtick=True,
                  usetex=True,
                  Tikz=TikzRendered)
                fail = SingleConvPlot('xIterNorm', xIterNorm, '\\$\\xn_{%s}\\$', xAxisLabelR,
                  '\\$\\xn\\$', ResultsFolder, OptName,
                  figType=FileTypeRaw, figsizex=6, figsizey=3,
                  width=0.5,
                  xspacing=0.25,
                  dpi=200,
                  xtick=True,
                  usetex=False)
            progressbar(49, 82)
            fail = BarPlot('xBarRendered', x0, xOpt, '$\\mathsf{x}^0$', '$\\mathsf{x}^{*}$',
              'Design variable', '$\\mathsf{x}$', ResultsFolder,
              OptName, figType=FileTypeRendered, Color0='#FAA43A',
              ColorOpt='#5DA5DA',
              figsizex=6,
              figsizey=3,
              width=0.5,
              xspacing=0.25,
              dpi=200,
              usetex=True,
              xtick=True,
              Tikz=TikzRendered)
            fail = BarPlot('xBar', x0, xOpt, '\\$\\xin$', '\\$\\xo$', 'Design variable',
              '\\$\\x$', ResultsFolder, OptName, figType=FileTypeRaw,
              Color0='#FAA43A',
              ColorOpt='#5DA5DA',
              figsizex=6,
              figsizey=3,
              width=0.5,
              xspacing=0.25,
              dpi=200,
              usetex=False,
              xtick=True)
            progressbar(52, 82)
            if DesVarNorm in ('None', None, False):
                pass
            else:
                fail = BarPlot('xBarNormRendered', x0norm, xOptNorm, '$\\mathsf{x}^0$',
                  '$\\mathsf{x}^{*}$', 'Design variable',
                  '$\\hat{x}$', ResultsFolder, OptName,
                  figType=FileTypeRendered, Color0='#FAA43A', ColorOpt='#5DA5DA',
                  figsizex=6,
                  figsizey=3,
                  width=0.5,
                  xspacing=0.25,
                  dpi=200,
                  usetex=True,
                  xtick=True,
                  Tikz=TikzRendered)
                fail = BarPlot('xBarNorm', x0norm, xOptNorm, '\\$\\xnin$', '\\$\\xno$',
                  'Design variable', '\\$\\xn$', ResultsFolder,
                  OptName, figType=FileTypeRaw, Color0='#FAA43A',
                  ColorOpt='#5DA5DA',
                  figsizex=6,
                  figsizey=3,
                  width=0.5,
                  xspacing=0.25,
                  dpi=200,
                  usetex=False,
                  xtick=True)
            progressbar(56, 82)
            plt.rc('text', usetex=True)
            try:
                plt.pcolor(gGradOpt.T)
                plt.colorbar()
            except:
                pass

            plt.xlabel('Design variable')
            plt.ylabel('Constraint')
            plt.xlim(xmin=0, xmax=nx)
            plt.ylim(ymin=0, ymax=ng)
            plt.grid(True, which='both')
            plt.tight_layout()
            for ii in range(np.size(FileTypeRendered)):
                plt.savefig(ResultsFolder + OptName + '_gGradOpt.' + FileTypeRendered[ii])

            if TikzRendered:
                pass
            plt.close()
            progressbar(63, 82)
            PlotFiles = [
             'gBar', 'fBar', 'fgMaxIterNorm', 'fgMaxIter', 'gIter',
             'fGradIter', 'xIter', 'xIterNorm', 'xBar', 'xBarNorm']
            mProc = [[]] * len(PlotFiles)
            if FigureSubfolders:
                for ii in range(len(FileTypeRendered)):
                    os.mkdir(ResultsFolder + os.sep + FileTypeRendered[ii])

                for ii in range(len(FileTypeRaw)):
                    try:
                        os.mkdir(ResultsFolder + os.sep + FileTypeRaw[ii])
                    except:
                        pass

            os.mkdir(ResultsFolder + os.sep + 'eps/')
            for ii in range(len(PlotFiles)):
                if InkscapeVersion not in ListBadInkscape:
                    mProc[ii] = Popen((InkscapeCall + ' -D -z --file=' + ResultsFolder + OptName + '_' + PlotFiles[ii] + '.pdf --export-pdf=' + ResultsFolder + OptName + '_' + PlotFiles[ii] + '.pdf --export-latex'),
                      shell=True).wait()
                else:
                    mProc[ii] = Popen((InkscapeCall + ' -D -z --file=' + ResultsFolder + OptName + '_' + PlotFiles[ii] + '.pdf --export-eps=' + ResultsFolder + 'eps/' + OptName + '_' + PlotFiles[ii] + '.eps --export-latex'),
                      shell=True).wait()
                if FigureSubfolders:
                    for iii in range(len(FileTypeRendered)):
                        try:
                            shutil.move(ResultsFolder + OptName + '_' + PlotFiles[ii] + 'Rendered.' + FileTypeRendered[iii], ResultsFolder + FileTypeRendered[iii])
                        except:
                            pass

                    for iii in range(len(FileTypeRaw)):
                        try:
                            shutil.move(ResultsFolder + OptName + '_' + PlotFiles[ii] + '.' + FileTypeRaw[iii], ResultsFolder + FileTypeRaw[iii])
                        except:
                            pass

            progressbar(82, 82)
            print('\n          Diagram generation finished:          \n')
        if tables == 1:
            os.mkdir(ResultsFolder + os.sep + 'tex/')
            tRR = open('' + ResultsFolder + 'tex/' + OptName + '_OptAlgOptionsTable.tex', 'w')
            optCrit = []
            optCrit.append('\\begin{table}[H] \n')
            optCrit.append('\\caption{Algorithm options} \n')
            optCrit.append('\\noindent \n')
            optCrit.append('\\begin{centering} \n')
            optCrit.append('\\begin{tabular}{cc} \n')
            optCrit.append('\\toprule \n')
            optCrit.append('Property & Value \\tabularnewline \n')
            optCrit.append('\\midrule \n')
            if Alg[:5] != 'PyGMO':
                for uu in OptAlg.options:
                    if str(uu) != 'defaults' and str(uu) != 'IFILE':
                        temp = [
                         '\\verb!', str(uu), '! & ',
                         str(OptAlg.options[uu][1]), ' \\tabularnewline \n']
                        optCrit = optCrit + temp

            else:
                optCrit.append('\\bottomrule \n')
                optCrit.append('\\end{tabular} \n')
                optCrit.append('\\par\\end{centering} \n')
                optCrit.append('\\end{table}')
                tRR.writelines(optCrit)
                tRR.close()
                os.system('tex2lyx ' + ResultsFolder + 'tex/' + OptName + '_OptAlgOptionsTable.tex')
                if DesVarNorm in ('None', None, False):
                    pass
                else:
                    tRR = open('' + ResultsFolder + 'tex/' + OptName + '_DesignVarNormTable.tex', 'w')
                    dvT = []
                    dvT.append('\\begin{longtable}{cccccc} \n')
                    dvT.append('\\caption{Details of normalized design variables $\\xn$}')
                    dvT.append(' \n')
                    dvT.append('\\tabularnewline \n')
                    dvT.append('\\midrule \n')
                    dvT.append('\\begin{minipage}{2.7cm} \\centering Normalized \\\\ design variable \\end{minipage} & Symbol & \\begin{minipage}{2cm} \\centering Start \\\\ value $\\xn^{0}$ \\end{minipage} & \\begin{minipage}{2cm} \\centering Lower \\\\ bound $\\xn^{L}$ \\end{minipage} &')
                    dvT.append('\\begin{minipage}{2cm} \\centering Upper \\\\ bound $\\xn^{U}$ \\end{minipage} & \\begin{minipage}{2cm} \\centering Optimal \\\\ value $\\xn^{*}$ \\end{minipage} \\tabularnewline')
                    dvT.append('\n \\midrule \n')
                    if nx == 1:
                        temp = [str(1), '&$\\xn_{1}$&', str(round(x0norm, 4)), '&',
                         str(0.0), '&', str(1.0), '&', str(round(xOptNorm, 4)),
                         '\\tabularnewline \n']
                        dvT = dvT + temp
                    else:
                        for ii in range(nx):
                            temp = [
                             str(ii + 1), '&$\\xn_{', str(ii + 1), '}$&',
                             str(round(x0norm[ii], 4)), '&', str(0.0), '&',
                             str(1.0), '&', str(round(xOptNorm[ii], 4)),
                             '\\tabularnewline \n']
                            dvT = dvT + temp

                    dvT.append('\\bottomrule \n')
                    dvT.append('\\end{longtable}')
                    tRR.writelines(dvT)
                    tRR.close()
                    os.system('tex2lyx ' + ResultsFolder + OptName + '_DesignVarNormTable.tex')
                tRR = open('' + ResultsFolder + 'tex/' + OptName + '_DesignVarTable.tex', 'w')
                dvT = []
                dvT.append('\\begin{longtable}{cccccc} \n')
                dvT.append('\\caption{Details of design variables $\\x$}')
                dvT.append(' \n')
                dvT.append('\\tabularnewline \n')
                dvT.append('\\midrule \n')
                dvT.append('\\begin{minipage}{2cm} \\centering Design \\\\ variable \\end{minipage} & Symbol & \\begin{minipage}{2cm} \\centering Start \\\\ value $\\x^{0}$ \\end{minipage} & \\begin{minipage}{2cm} \\centering Lower \\\\ bound $\\x^{L}$ \\end{minipage} &')
                dvT.append('\\begin{minipage}{2cm} \\centering Upper \\\\ bound $\\x^{U}$ \\end{minipage} & \\begin{minipage}{2cm} \\centering Optimal \\\\ value $\\x^{*}$ \\end{minipage} \\tabularnewline')
                dvT.append('\n \\midrule  \n')
                if nx == 1:
                    temp = [str(1), '&$\\x_{1}$&', str(round(x0, 4)), '&',
                     str(round(xL, 4)), '&', str(round(xU, 4)), '&',
                     str(round(xOpt, 4)), '\\tabularnewline \n']
                    dvT = dvT + temp
                else:
                    for ii in range(nx):
                        temp = [
                         str(ii + 1), '&$\\x_{', str(ii + 1), '}$&',
                         str(round(x0[ii], 4)), '&', str(round(xL[ii], 4)), '&',
                         str(round(xU[ii], 4)), '&', str(round(xOpt[ii], 4)),
                         '\\tabularnewline \n']
                        dvT = dvT + temp

                dvT.append('\\bottomrule \n')
                dvT.append('\\end{longtable}')
                tRR.writelines(dvT)
                tRR.close()
                os.system('tex2lyx ' + ResultsFolder + 'tex/' + OptName + '_DesignVarTable.tex')
                tRR = open('' + ResultsFolder + 'tex/' + OptName + '_SystemResponseTable.tex', 'w')
                srT = []
                srT.append('\\begin{longtable}{cccc} \n')
                srT.append('\\caption{System responses} \n')
                srT.append('\\tabularnewline \n')
                srT.append('\\midrule \n')
                srT.append('Response & Symbol & Start value  & Optimal value \\tabularnewline \n')
                srT.append('\\midrule \n')
                if Alg[:5] == 'PyGMO':
                    temp = [
                     'Objective function  & $\\f$ & ',
                     str(round(fIter[0], 4)), '&', str(round(fOpt[0], 4)),
                     '\\tabularnewline \n']
                else:
                    temp = [
                     'Objective function  & $\\f$ & ',
                     str(round(fIter[0], 4)), '&', str(round(fOpt[0], 4)),
                     '\\tabularnewline \n']
            srT = srT + temp
            if np.size(gc) > 0:
                for ii in range(ng):
                    temp = [
                     'Inequality constraint ', str(ii + 1),
                     '&$\\g_{', str(ii + 1), '}$&',
                     str(round(gIter[0][ii], 4)), '&',
                     str(round(gOpt[ii], 4)), '\\tabularnewline \n']
                    srT = srT + temp

            else:
                srT.append('\\bottomrule \n')
                srT.append('\\end{longtable}')
                tRR.writelines(srT)
                tRR.close()
                os.system('tex2lyx ' + ResultsFolder + 'tex/' + OptName + '_SystemResponseTable.tex')
                if np.size(gc) > 0:
                    tRR = open('' + ResultsFolder + 'tex/' + OptName + '_FirstOrderLagrangeTable.tex', 'w')
                    optCrit = []
                    optCrit.append('\\begin{longtable}{ccc}\n')
                    optCrit.append('\\caption{First-order optimality as well as non-zero Lagrangian multipliers} \n')
                    optCrit.append('\\tabularnewline \n')
                    optCrit.append('\\midrule \n')
                    optCrit.append('Property & Symbol & Value \\tabularnewline \n')
                    optCrit.append('\\midrule \n')
                    try:
                        temp = ['First-order optimality & $\\left\\Vert \\mathcal{\\nabla L}\\right\\Vert $ & ', str(round(Opt1Order, 4)), '\\tabularnewline \n']
                        optCrit = optCrit + temp
                        for uu in range(len(lambda_c)):
                            temp = ['Lagrangian multiplier of $\\g_{', str(uu + 1),
                             '}$ & $\\lambda_{\\g_{', str(uu + 1), '}}$ & ',
                             str(round(lambda_c[uu], 4)), '\\tabularnewline \n']
                            optCrit = optCrit + temp

                        optCrit.append('\\bottomrule \n')
                        optCrit.append('\\end{longtable}')
                        tRR.writelines(optCrit)
                        tRR.close()
                        os.system('tex2lyx ' + ResultsFolder + 'tex/' + OptName + '_FirstOrderLagrangeTable.tex')
                    except:
                        pass

                    if np.size(SPg) > 0:
                        tRR = open('' + ResultsFolder + 'tex/' + OptName + '_ShadowPricesTable.tex', 'w')
                        optCrit = []
                        optCrit.append('\\begin{longtable}{ccc} \n')
                        optCrit.append('\\caption{Shadow prices} \n')
                        optCrit.append('\\tabularnewline \n')
                        optCrit.append('\\midrule \n')
                        optCrit.append('Property & Symbol & Value \\tabularnewline \n')
                        optCrit.append('\\midrule \n')
                        for uu in range(len(SPg)):
                            temp = ['Shadow price of $g_{', str(uu + 1), '}$ & $S_{g_{',
                             str(uu + 1), '}}$ & ', str(round(SPg[uu], 4)),
                             '\\tabularnewline \n']
                            optCrit = optCrit + temp

                        optCrit.append('\\bottomrule \n')
                        optCrit.append('\\end{longtable}')
                        tRR.writelines(optCrit)
                        tRR.close()
                        os.system('tex2lyx ' + ResultsFolder + 'tex/' + OptName + '_ShadowPricesTable.tex')
                    templatePath = os.path.dirname(os.path.realpath(__file__)) + '/ResultReportFiles/'
                    shutil.copy(templatePath + '/DesOptPy.png', ResultsFolder + 'DesOptPy.png')
                    if InkscapeVersion == None:
                        FileName = [
                         '_ResultReportNoInkscape.lyx']
                elif InkscapeVersion in ListBadInkscape:
                    FileName = [
                     '_ResultReport_eps.lyx']
                else:
                    FileName = [
                     '_ResultReport.lyx']
            for ii in range(len(FileName)):
                fRR = open(templatePath + FileName[ii], 'r')
                contentRR = fRR.readlines()
                contentRR = [w.replace('XXXmodelname', OptModel) for w in contentRR]
                contentRR = [w.replace('XXXdate', today) for w in contentRR]
                contentRR = [w.replace('XXXcomputername', computerName) for w in contentRR]
                contentRR = [w.replace('XXXoperatingsystem', operatingSystem) for w in contentRR]
                contentRR = [w.replace('XXXarchitecture', architecture) for w in contentRR]
                contentRR = [w.replace('XXXnprocessors', nProcessors) for w in contentRR]
                contentRR = [w.replace('XXXuser', userName) for w in contentRR]
                contentRR = [w.replace('XXXmodelname', OptModel) for w in contentRR]
                contentRR = [w.replace('XXXnx', str(np.size(x0))) for w in contentRR]
                if np.size(gc) > 0:
                    contentRR = [w.replace('XXXnc', str(np.size(gc))) for w in contentRR]
                else:
                    contentRR = [w.replace('XXXnc', str(0)) for w in contentRR]
                contentRR = [w.replace('XXXalgorithmname', Alg) for w in contentRR]
                contentRR = [w.replace('XXXdesvarnorm', str(DesVarNorm)) for w in contentRR]
                contentRR = [w.replace('XXXoptions', 'Options') for w in contentRR]
                contentRR = [w.replace('XXXnit', str(nIter)) for w in contentRR]
                contentRR = [w.replace('XXXneval', str(nEval)) for w in contentRR]
                contentRR = [w.replace('XXXt0', hhmmss0) for w in contentRR]
                contentRR = [w.replace('XXXt1', hhmmss1) for w in contentRR]
                contentRR = [w.replace('XXXtopt', str(OptTime)) for w in contentRR]
                contentRR = [w.replace('AAA', OptName) for w in contentRR]
                fRR.close()
                fRR = open(ResultsFolder + OptName + FileName[ii], 'w')
                fRR.writelines(contentRR)
                fRR.close()

        if lyx == 1:
            for ii in range(len(FileName)):
                if InkscapeVersion in ListBadInkscape:
                    os.system(LyxCall + ' --export pdf ' + ResultsFolder + OptName + FileName[ii])
                else:
                    os.system(LyxCall + ' --export pdf2 ' + ResultsFolder + OptName + FileName[ii])
                if InkscapeVersion == None:
                    shutil.move(ResultsFolder + OptName + FileName[ii][:-3] + 'pdf', ResultsFolder + OptName + '_ResultReport.pdf')


    def progressbar(actTime, totTime):
        toolbar_width = 60
        percentage = float(actTime) / float(totTime)
        numOfChars = int(percentage * toolbar_width)
        Char = '='
        sys.stdout.write('\r[')
        sys.stdout.flush()
        for i in range(numOfChars):
            if i == toolbar_width / 2 - 1:
                sys.stdout.write('%03i' % int(percentage * 100) + '%')
            else:
                sys.stdout.write(Char)
                sys.stdout.flush()

        for i in range(numOfChars, toolbar_width):
            if i == toolbar_width / 2 - 1:
                sys.stdout.write('%03i' % int(percentage * 100) + '%')
            else:
                sys.stdout.write(' ')
                sys.stdout.flush()

        sys.stdout.write(']')
        sys.stdout.flush()


    def elapsed(starttime):
        time_now = time.time()
        print('time Elapsed:\t' + str(time_now - starttime))