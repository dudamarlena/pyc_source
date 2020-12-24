# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wehrle/opt/FuzzAnPy2/FuzzAnPy/FuzzPlot.py
# Compiled at: 2019-08-20 20:05:53
# Size of source mod 2**32: 13953 bytes
"""
Created on Wed Nov 13 16:20:34 2013

@author: wehrle

TODO FuzzFnContourPlot:interpolate as here http://blog.enthought.com/general/visualizing-uncertainty/
TODO FuzzFnContourPlot: add colorbar()
"""
from __future__ import absolute_import, division, print_function
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import rcParams
import numpy as np
DefaultColor = (0, 0.4823529411764706, 0.8941176470588236)
DefaultEdgeColor = (0, 0.4823529411764706, 0.8941176470588236)
pgf_with_pdflatex = {'pgf.texsystem':'pdflatex',  'pgf.preamble':[
  '\\usepackage[utf8x]{inputenc}',
  '\\usepackage[T1]{fontenc}',
  '\\usepackage{cmbright}']}

def FuzzFnContourPlot(rFuzz, x=[], xlabel='Dependent parameter', ylabel='Value of uncertain function', Cfuz=DefaultColor, fontsize=12, font='tex gyre pagella', pdpi=100, xlimits=[], ylimits=[], xsize=7, ysize=5, outline=True, fill=True, nYTicks=5, nXTicks=5, xAxisRot=True, frame=True):
    plt.rcParams['font.family'] = font
    nalpha = np.size(rFuzz, 1)
    if len(x) == 0:
        x = np.linspace(0, np.size(rFuzz))
    fig1 = plt.figure(figsize=(xsize, ysize), dpi=pdpi)
    ax1 = fig1.add_subplot(1, 1, 1)
    if fill:
        for ii in reversed(range(np.size(rFuzz, 1) - 1)):
            ax1.fill_between(x, (rFuzz[:, ii + 1, 1]), (rFuzz[:, ii, 1]), facecolor=Cfuz, alpha=(1.0 / nalpha * (nalpha - ii - 1) * 0.9),
              linewidth=0,
              edgecolor=DefaultEdgeColor)
            ax1.fill_between(x, (rFuzz[:, ii + 1, 0]), (rFuzz[:, ii, 0]), facecolor=Cfuz, alpha=(1.0 / nalpha * (nalpha - ii - 1) * 0.9),
              linewidth=0,
              edgecolor=DefaultEdgeColor)

        ax1.fill_between(x, (rFuzz[:, 0, 1]), (rFuzz[:, 0, 0]), facecolor=Cfuz, alpha=1.0,
          linewidth=0)
    if outline:
        ax1.plot(x, (rFuzz[:, :, 0]), x, (rFuzz[:, :, 1]), color=Cfuz, linewidth=1.0)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if ylimits != []:
        plt.ylim(ylimits[0], ylimits[1])
    if xlimits != []:
        plt.xlim(xlimits[0], xlimits[1])
    if not frame:
        ax1.spines['right'].set_visible(False)
        ax1.spines['top'].set_visible(False)
        ax1.get_xaxis().tick_bottom()
        ax1.get_yaxis().tick_left()
    if xlimits != []:
        if xlimits != []:
            plt.yticks(np.linspace(ylimits[0], ylimits[1], nYTicks))
    xloc = plt.MaxNLocator(nXTicks)
    ax1.xaxis.set_major_locator(xloc)
    if xAxisRot:
        plt.setp((ax1.get_xticklabels()), rotation='vertical')
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    return (
     plt, ax1)


def FuzzFnContourPlot1(rFuzz, x=[], xlabel='$\\tilde{x}$', ylabel='$\\tilde{y}}$', pdpi=100, Cfuz=DefaultColor, fontsize=18, xlimits=[], ylimits=[], xsize=7, ysize=5):
    rcParams.update({'figure.autolayout': True})
    rcParams.update(pgf_with_pdflatex)
    nalpha = np.size(rFuzz, 1)
    if len(x) == 0:
        x = np.linspace(0, np.size(rFuzz))
    fig1 = plt.figure(figsize=(xsize, ysize), dpi=pdpi)
    ax1 = fig1.add_subplot(1, 1, 1)
    for ii in reversed(range(np.size(rFuzz, 1) - 1)):
        ax1.fill_between(x, (rFuzz[:, ii + 1, 1]), (rFuzz[:, ii, 1]), facecolor=Cfuz, alpha=(1.0 / nalpha * (nalpha - ii - 1) * 0.9),
          linewidth=0,
          edgecolor=DefaultEdgeColor)
        ax1.fill_between(x, (rFuzz[:, ii + 1, 0]), (rFuzz[:, ii, 0]), facecolor=Cfuz, alpha=(1.0 / nalpha * (nalpha - ii - 1) * 0.9),
          linewidth=0,
          edgecolor=DefaultEdgeColor)

    ax1.fill_between(x, (rFuzz[:, 0, 1]), (rFuzz[:, 0, 0]), facecolor=Cfuz, alpha=1.0,
      linewidth=0.0)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if ylimits != []:
        plt.ylim(ylimits[0], ylimits[1])
    font = {'size': fontsize}
    (plt.rc)(*('font', ), **font)
    rcParams.update({'figure.autolayout': True})
    return plt


def FuzzFn3dPlot(rFuzz, x=[], pdpi=100, Cfuz=DefaultColor, xsize=7, ysize=5):
    rcParams.update({'figure.autolayout': True})
    rcParams.update(pgf_with_pdflatex)
    fig = plt.figure(figsize=(xsize, ysize), dpi=pdpi)
    ax = fig.gca(projection='3d')
    mu = np.linspace(1, 0, np.size(rFuzz, 1))
    for ii in reversed(range(np.size(rFuzz, 1))):
        ax.plot(x, rFuzz[:, ii, 1], mu[ii])
        ax.plot(x, rFuzz[:, ii, 0], mu[ii])

    return plt


def FuzzPlot(rFuzz, xlabel='Value', pdpi=100, Cfuz=DefaultColor, fill=True, fontsize=18, xsize=5, ysize=4, xlimits=[], lang='EN', TextRender=True, AxisNameLong=True, frame=False, nYTicks=2, nXTicks=4, xAxisRot=True):
    rcParams.update({'figure.autolayout': True})
    rcParams.update(pgf_with_pdflatex)
    if not TextRender:
        rcParams.update({'svg.fonttype': 'none'})
    trans = 0.5
    fig = plt.figure(figsize=(xsize, ysize), dpi=pdpi)
    ax = fig.add_subplot(1, 1, 1)
    mu = np.linspace(1, 0, np.size(rFuzz, 0))
    xplot = np.concatenate((np.flipud(rFuzz[:, 0]), rFuzz[:, 1]), axis=0)
    muplot = np.concatenate((np.flipud(mu), mu), axis=0)
    if fill:
        ax.fill_between((rFuzz[:, 0]), mu, facecolor=Cfuz, alpha=trans, linewidth=0.0)
        ax.fill_between([rFuzz[(0, 1)], rFuzz[(0, 0)]], [1, 1], facecolor=Cfuz, alpha=trans,
          linewidth=0.0)
        ax.fill_between((rFuzz[:, 1]), mu, facecolor=Cfuz, alpha=trans, linewidth=0.0)
    ax.plot(xplot, muplot, 'b-')
    plt.ylim(0, 1.1)
    if xlimits != []:
        plt.xlim(xlimits[0], xlimits[1])
    plt.xlabel(xlabel)
    plt.yticks(np.arange(0, 1 + (nYTicks - 1), 1 / (nYTicks - 1)))
    xloc = plt.MaxNLocator(nXTicks)
    ax.xaxis.set_major_locator(xloc)
    if not frame:
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
    if xAxisRot:
        plt.setp((ax.get_xticklabels()), rotation='vertical')
    if AxisNameLong:
        if lang == 'EN':
            if TextRender:
                plt.ylabel('Membership $\\mu$')
        elif not TextRender:
            plt.ylabel('Membership \\$\\mu\\$')
    else:
        if lang == 'DE':
            if TextRender:
                plt.ylabel('Zugehörigkeit $\\mu$')
            else:
                if not TextRender:
                    plt.ylabel('Zugeh\\"origkeit \\$\\mu\\$')
        else:
            if TextRender:
                h = plt.ylabel('$\\mu$')
            else:
                if not TextRender:
                    h = plt.ylabel('\\$\\mu\\$')
                h.set_rotation(0)
        rcParams.update({'font.size': fontsize})
        plt.tight_layout()
        return plt


def PlotShadowPrice(SP):
    import matplotlib.pyplot as plt
    import numpy as np
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for c, z in zip(['g', 'y'], [2, 1]):
        xs = np.arange(6)
        ys = np.random.rand(6)
        ax.bar(xs, ys, zs=z, zdir='y', color=c, alpha=0.8)

    ax.set_xlabel('Structural response')
    ax.set_ylabel('Uncertain parameter')
    ax.set_zlabel('Reduction of uncertainty in structural response due to 10%                   reduction of uncertainty in uncertain parameter')
    return plt


def PlotShadowUncertainties(ShadowUncertainty, xnames=[], ynames=[], xsize=10, ysize=10, pdpi=100):
    data = ShadowUncertainty.T
    plt.figure(figsize=(xsize, ysize), dpi=pdpi)
    plt.pcolor(data, cmap='rainbow')
    plt.colorbar()
    if xnames == []:
        xnames = [[]] * data.shape[1]
        for ii in range(data.shape[1]):
            xnames[ii] = '\\$r_' + str(ii + 1) + '\\$'

    if ynames == []:
        ynames = [[]] * data.shape[0]
        for ii in range(data.shape[0]):
            ynames[ii] = '\\$p_' + str(ii + 1) + '\\$'

    plt.xticks(np.arange(0.5, data.shape[1] + 0.5), xnames)
    plt.yticks(np.arange(0.5, data.shape[0] + 0.5), ynames)
    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            plt.text((x + 0.5), (y + 0.5), ('%.4f' % data[(y, x)]), horizontalalignment='center',
              verticalalignment='center')

    plt.xlabel('Structural response')
    plt.ylabel('Uncertain parameter')
    print('new')
    return plt


def PDF_TEX(FileName, NewName=[]):
    if NewName == []:
        NewName = FileName[0:-4] + '.pdf'
    import os
    os.system('inkscape -D -z --file=' + FileName + ' --export-pdf=' + NewName[0:-4] + '.pdf --export-latex')
    input1 = open(NewName[0:-4] + '.pdf_tex', 'r')
    clean = input1.read().replace('−', '-')
    input1.close()
    output = open(NewName[0:-4] + '.pdf_tex', 'w')
    output.write(clean)
    input1.close()


def IntPlot(data, labels=[], Units=[], show=False, xPlot=5, color=DefaultColor, delta=0.5, plotBuffer=0.1, xAxisRot=True, xlabel='Uncertain value', font='tex gyre pagella'):
    nP = np.shape(data)[0]
    if np.shape(np.shape(data))[0] == 1:
        data = data.reshape(nP, 1)
        interval = False
    else:
        if np.shape(np.shape(data))[0] == 3:
            interval = True
        else:
            interval = True
    yPlot = nP * 0.25
    thick = nP ** 0.1 * 0.3
    plt.rcParams['font.family'] = font
    plt.rcParams['figure.figsize'] = (xPlot, yPlot)
    if not labels:
        if np.shape(data)[0] == 1:
            labels = [
             'Parameter']
        else:
            for ii in range(np.shape(data)[0]):
                labels.append('Parameter ' + str(ii + 1))

    else:
        yplaces = [0.5 + i for i in reversed(range(nP))]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_yticks(yplaces)
        ax.set_yticklabels(labels, horizontalalignment='left')
        ax.set_ylim((0, nP))
        for ii, val in enumerate(data):
            if interval:
                print(val)
                start = val[(0, 0)]
                end = val[(0, 1)]
                pos = yplaces[ii]
                ax.add_patch(patches.Rectangle((start, pos - delta / 2.0), (end - start), thick,
                  color=color))

        pmin = np.min(data)
        pmax = np.max(data)
        ax.plot((pmin * (1 - plotBuffer), pmax * (1 + plotBuffer)), (0, 0), 'w', alpha=0.0)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.yaxis.set_ticks_position('none')
        ax.xaxis.set_ticks_position('bottom')
        plt.grid(False)
        nlmax = 0
        for ilabel in labels:
            nl = len(ilabel)
            if nl > nlmax:
                nlmax = nl

        yax = ax.get_yaxis()
        yax.set_tick_params(direction='out', pad=(nlmax * 5))
        if not Units:
            ax.set_xlabel(xlabel)
        else:
            ax.set_xlabel(xlabel + ' [' + Units + ']')
    if xAxisRot:
        plt.setp((ax.get_xticklabels()), rotation='vertical')
    plt.xlim(np.min(data) - (np.max(data) - np.min(data)) / 5, np.max(data) + (np.max(data) - np.min(data)) / 5)
    return (plt, ax)


if __name__ == '__main__':
    print('Test of interval plotting:')
    data = np.array([[300, 900],
     [
      350, 850],
     [
      400, 800],
     [
      450, 750],
     [
      500, 700],
     [
      550, 650],
     [
      599, 601],
     [
      300, 900],
     [
      350, 850],
     [
      400, 800],
     [
      450, 750],
     [
      500, 700],
     [
      550, 650],
     [
      599, 601],
     [
      300, 900],
     [
      350, 850],
     [
      400, 800],
     [
      450, 750],
     [
      500, 700],
     [
      550, 650],
     [
      350, 850],
     [
      400, 800],
     [
      450, 750],
     [
      500, 700],
     [
      550, 650],
     [
      599, 601],
     [
      300, 900],
     [
      350, 850],
     [
      400, 800],
     [
      450, 750],
     [
      500, 700],
     [
      550, 650],
     [
      599, 601],
     [
      300, 900],
     [
      350, 850],
     [
      400, 800],
     [
      450, 750],
     [
      500, 700],
     [
      550, 650]])
    labels = []
    for ii in range(len(data)):
        labels.append('Stiffness ' + str(ii + 1))

    ax = IntPlot(data, labels=labels, Units='N/mm')
    data = np.array([[300, 900],
     [
      400, 800],
     [
      450, 750],
     [
      500, 700],
     [
      550, 650],
     [
      599, 601],
     [
      300, 900]])
    labels = []
    for ii in range(len(data)):
        labels.append('Stiffness ' + str(ii + 1))

    ax = IntPlot(data, labels=labels, Units='N/mm')
    data = np.array([[300, 900],
     [
      400, 800]])
    labels = []
    for ii in range(len(data)):
        labels.append('Stiffness ' + str(ii + 1))

    ax = IntPlot(data, labels=labels, Units='N/mm')