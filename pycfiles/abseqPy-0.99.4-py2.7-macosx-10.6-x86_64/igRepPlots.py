# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/abseqPy/IgRepReporting/igRepPlots.py
# Compiled at: 2019-04-23 02:08:32
"""
    Short description: Quality Control Analysis of Immunoglobulin Repertoire NGS (Paired-End MiSeq)    
    Author: Monther Alhamdoosh    
    Python Version: 2.7
    Changes log: check git commits. 
"""
import os, gzip, numpy as np, math, numpy, random, itertools, scipy.stats, multiprocessing
from collections import Counter, defaultdict
from os.path import exists
from Bio import SeqIO
from numpy import Inf, mean, isnan
import abseqPy.IgRepertoire.igRepUtils
from abseqPy.IgRepAuxiliary.seqUtils import maxlen, WeightedPopulation
from abseqPy.IgMultiRepertoire.PlotManager import PlotManager
from abseqPy.logger import printto, LEVEL
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt, matplotlib.colors as mcolors
from matplotlib import cm

def plotSeqLenDistClasses(seqFile, sampleName, outputFile, fileFormat='fasta', maxLen=Inf, stream=None):
    if eitherExists(outputFile):
        printto(stream, '\tFile found ... ' + os.path.basename(outputFile), LEVEL.WARN)
        return
    else:
        printto(stream, '\tThe sequence length distribution of each gene family is being calculated ...')
        ighvDist = {}
        ighvSizes = {}
        with abseqPy.IgRepertoire.igRepUtils.safeOpen(seqFile) as (fp):
            for rec in SeqIO.parse(fp, fileFormat):
                if len(rec) <= maxLen:
                    if len(rec.id.split('|')) > 1:
                        ighvID = rec.id.split('|')[1]
                    else:
                        ighvID = rec.id
                    id = ighvID.split('-')[0].split('/')[0]
                    if ighvDist.get(id, None) is None:
                        ighvDist[id] = 0
                        ighvSizes[id] = []
                    ighvSizes[id].append(len(rec))
                    ighvDist[id] += 1

        if sum(ighvDist.values()):
            plotDist(ighvDist, sampleName, outputFile)
            classes = sorted(ighvDist, key=ighvDist.get, reverse=True)
            outputFile, ext = os.path.splitext(outputFile)
            outputFile += '_box' + ext
            if PlotManager.pythonPlotOn():
                fig, ax = plt.subplots()
                ax.boxplot(map(lambda x: ighvSizes[x], classes))
                ind = np.arange(1, len(classes) + 1)
                ax.set_xticks(ind)
                ax.set_xticklabels(classes, rotation=45)
                ax.set_title('Sequence Lengths in ' + sampleName)
                fig.savefig(outputFile.replace('.csv', '.png'), dpi=300)
                plt.close()
            writeCSV(outputFile, 'x,y\n', '{},{}\n', [ (klass, val) for klass in classes for val in ighvSizes[klass] ])
            for k in classes:
                printto(stream, (k, ighvDist[k], min(ighvSizes[k]), max(ighvSizes[k])), LEVEL.INFO)

        return


def plotSeqLenDist(counts, sampleName, outputFile, fileFormat='fasta', maxLen=Inf, histtype='bar', dna=True, autoscale=None, maxbins=20, seqName='', normed=False, removeOutliers=False, stream=None):
    if eitherExists(outputFile):
        printto(stream, '\tSequence length distribution file found ... ' + os.path.basename(outputFile), LEVEL.WARN)
        return
    else:
        printto(stream, '\tThe sequence length distribution is being calculated for ' + sampleName)
        if isinstance(counts, str):
            with abseqPy.IgRepertoire.igRepUtils.safeOpen(counts) as (fp):
                sizes = [ len(rec) for rec in SeqIO.parse(fp, fileFormat) if len(rec) <= maxLen ]
            if len(sizes) == 0:
                return
            count = Counter(sizes)
            sizes = count.keys()
            weights = count.values()
        else:
            if isinstance(counts, list):
                sizes = map(lambda x: int(x) if not isnan(x) else 0, counts)
                weights = [1] * len(sizes)
            elif isinstance(counts, Counter):
                sizes = counts.keys()
                weights = map(lambda x: counts[x], sizes)
            try:
                if len(sizes) == 0:
                    printto(stream, 'No length to calculate, skipping ...', LEVEL.INFO)
                    return
            except NameError:
                printto(stream, 'No length to calculate, skipping ...', LEVEL.INFO)
                return

        if removeOutliers:
            sizes, weights = excludeOutliers(sizes, weights)
        bins = max(sizes) - min(sizes)
        if bins > maxbins:
            bins = bins / 2
        if maxbins == -1:
            bins = 40
        if bins == 0:
            bins = 1
        fig, ax = plt.subplots(figsize=(8, 5))
        if histtype in ('bar', 'step', 'stepfilled'):
            histcals, bins, patches = ax.hist(sizes, bins=bins, range=autoscale, density=normed, weights=weights, histtype=histtype)
            writeCSV(outputFile, 'length,count\n', '{},{}\n', [ (k, v) for k, v in zip(sizes, weights) ])
            if normed:
                mu, sigma = weightedAvgAndStd(sizes, weights)
                if sigma != 0:
                    y = scipy.stats.norm.pdf(bins, mu, sigma)
                    ax.plot(bins, y, 'r--')
        else:
            if all([ x == 1 for x in weights ]):
                tmp = Counter(sizes)
                sizes = tmp.keys()
                weights = map(lambda x: tmp[x], sizes)
            if normed:
                weights = [ x / sum(weights) for x in weights ]
            histcals = None
            ax.plot(sizes, weights)
        title = '{:,} Sequences {} in {} \nLengths {:d} to {:d}'
        ax.set_title(title.format(sum(weights), 'of ' + seqName if seqName != '' else '', sampleName, min(sizes), max(sizes)))
        if dna:
            ax.set_xlabel('Sequence Length (bp)')
        else:
            ax.set_xlabel('Sequence Length (aa)')
        if autoscale:
            ax.set_xticks(np.arange(autoscale[0], autoscale[1] + 1, 5))
        if not normed:
            ax.set_ylabel('Count')
        else:
            ax.set_ylabel('Proportion')
        fig.savefig(outputFile.replace('.csv', '.png'), dpi=300)
        plt.close()
        return histcals


def plotSeqDuplication(frequencies, labels, filename, title='', grouped=False, stream=None):
    if eitherExists(filename):
        printto(stream, '\tFile found ... ' + os.path.basename(filename), LEVEL.WARN)
        return
    if PlotManager.pythonPlotOn():
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.grid()
        ax.set_xlabel('Duplication Level')
        ax.set_ylabel('Proportion of Duplicated Sequences')
        if not grouped:
            ax.set_title(title + ('\nTotal is {:,}').format(int(sum(frequencies[0]))))
        else:
            ax.set_title(title + ('\nTotal is {:,}').format(sum(map(lambda x: sum(x), frequencies))))
    csvData = []
    for freqs, l in zip(frequencies, labels):
        total = sum(freqs)
        freqs.sort()
        freqs = np.array(freqs)
        ticks = np.linspace(10, 10000, 100).tolist()
        y = []
        for x in ticks:
            y.append(sum(1.0 * freqs[(freqs >= x)]) / total)

        ticks = map(lambda x: (x - 10) * 10 / 9990 + 10, ticks)
        less10Ticks = []
        less10Y = []
        for i in range(1, 10):
            less10Ticks.append(i)
            less10Y.append(sum(freqs == i) * 1.0 / total)

        y = less10Y + y
        ticks = less10Ticks + ticks
        csvData.extend([ (i, j, l) for i, j in zip(ticks, y) ])
        if PlotManager.pythonPlotOn():
            ax.plot(ticks, y, label=l)

    xticks = range(1, 10, 2) + [10] + range(11, 21, 2)
    xlabels = range(1, 10, 2) + ['>=10']
    xlabels += map(lambda x: '>' + str(int(x) - int(x) % 100) if x > 100 else '>=' + str(int(x)), np.linspace(10, 10000, (len(xticks) - len(xlabels)) * 2).tolist()[1::2])
    writeCSV(filename, 'x,y,region\n', '{},{},{}\n', csvData, metadata=str(xticks).strip('[]') + '\n' + str(xlabels).strip('[]') + '\n')
    if PlotManager.pythonPlotOn():
        ax.set_xticks(xticks)
        ax.set_xticklabels(xlabels, rotation=45)
        ax.legend()
        ax.legend(loc='upper left')
        plt.subplots_adjust(bottom=0.2)
        fig.savefig(filename.replace('.csv', '.png'), dpi=300)
        plt.close()


def dedup(population, n, k=5):
    """
    given a population and a sample size, randomly select n sequences and get the number of unique sequences from them.
    This experiment is repeated k times and a list of length k is returned
    :param population: collection of sequences
    :param n: sample size to randomly pick sequences from
    :param k: number of times to repeat the deduplication experiment
    :return: tuple (a, b) where
            a == n
            b is a list of length k, each element is the number of deduplicated sequences after randomly picking n
            from population (i.e. the number will be <= n)
    """
    hs = [ len(set(random.sample(population, n))) for _ in range(k) ]
    return (
     n, hs)


def plotSeqRarefaction(seqs, labels, filename, weights=None, title='', threads=2, stream=None):
    """
    In ecology, rarefaction is a technique to assess species richness from the results
    of sampling. Rarefaction allows the calculation of species richness for a given
    number of individual samples, based on the construction of so-called rarefaction curves.
    This curve is a plot of the number of species as a function of the number of samples.
    Source: https://en.wikipedia.org/wiki/Rarefaction_(ecology )

    :param seqs: list of lists
                ith nested list should consist of sequences that correspond to ith element of label
    :param labels: list of strings
                ith item describes the region of the ith list in seqs parameter
    :param filename: output filename
    :param weights: list
                sequence weights
    :param title: string
                plot title
    :param threads: int
    :param stream: output stream
    :return: None
    """
    if eitherExists(filename):
        printto(stream, '\tFile found ... ' + os.path.basename(filename), LEVEL.WARN)
        return
    else:
        if PlotManager.pythonPlotOn():
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.grid()
            ax.set_xlabel('Sample size')
            ax.set_ylabel('Number of Deduplicated Sequences')
            ax.set_title(title)
        csvData = []
        for setSeqs, l, w in zip(seqs, labels, weights):
            if w is not None:
                total = sum(w)
            else:
                total = len(setSeqs)
            ticks = []
            S = 10
            while S < total:
                ticks.append(S)
                S = int(S * 1.5)

            ticks.append(total)
            pool = multiprocessing.Pool(processes=threads)
            population = WeightedPopulation(setSeqs, w)
            result = [ pool.apply_async(dedup, args=(population, t)) for t in ticks ]
            pt = sorted([ p.get() for p in result ], key=lambda tup: tup[0])
            pool.close()
            pool.join()
            csvData.extend([ (x, y, l) for x, ys in pt for y in ys ])
            if PlotManager.pythonPlotOn():
                ax.plot([ d[0] for d in pt ], [ mean(d[1]) * 1.0 for d in pt ], label=l)

        xticks = np.linspace(0, total, 15).astype(int)
        xticks = map(lambda x: x - x % 1000 if x > 1000 else x, xticks[:-1])
        xticks.append(total)
        writeCSV(filename, 'x,y,region\n', '{},{},{}\n', csvData, zip=True, metadata=str(xticks).strip('[]') + '\n')
        if PlotManager.pythonPlotOn():
            ax.legend(loc='upper left')
            ax.set_xticks(xticks)
            ax.set_xticklabels(xticks, rotation=90)
            plt.subplots_adjust(bottom=0.21)
            fig.savefig(filename.replace('.csv', '.png'), dpi=300)
            plt.close()
        return


def plotSeqRecapture(seqs, labels, filename, weights=None, title='', stream=None):
    """
    Perform non-redundant capture-recapture analysis and plot the percent recapture
    Assumption 1: the population is assumed to be "closed".
    Assumption 2:  The chance for each individual in the population to be caught
    are equal and constant for both the initial marking period and the recapture period.
    Assumption 3:  Sufficient time must be allowed between the initial marking period
     and the recapture period
    Assumption 4: Animals do not lose their marks.

    :param seqs: list of lists
                ith nested list should consist of sequences that correspond to ith element of label
    :param labels: list of strings
                ith item describes the region of the ith list in seqs parameter
    :param filename: output filename
    :param weights: list
                sequence weights
    :param title: string
                plot title
    :param stream: output stream
    :return: None
    """
    if eitherExists(filename):
        printto(stream, '\tFile found ... ' + os.path.basename(filename), LEVEL.WARN)
        return
    else:
        if PlotManager.pythonPlotOn():
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.grid()
            ax.set_xlabel('Sample size')
            ax.set_ylabel('Percent Recapture')
            ax.set_title(title)
        for setSeqs, l, w in zip(seqs, labels, weights):
            if w is not None:
                total = sum(w)
            else:
                total = len(setSeqs)
            ticks = []
            S = 10
            while S < total:
                ticks.append(S)
                S = int(S * 1.5)

            ticks.append(total)
            pt = []
            population = WeightedPopulation(setSeqs, w)
            for j in ticks:
                hs = []
                for k in range(5):
                    s1 = set(random.sample(population, j))
                    s2 = set(random.sample(population, j))
                    inter = s2.intersection(s1)
                    hs.append(len(inter) * 100.0 / len(s2))

                pt.append((j, mean(hs)))

            if PlotManager.pythonPlotOn():
                ax.plot([ d[0] for d in pt ], [ d[1] for d in pt ], label=l)

        xticks = np.linspace(0, total, 15).astype(int)
        xticks = map(lambda x: x - x % 1000 if x > 1000 else x, xticks[:-1])
        xticks.append(total)
        if PlotManager.pythonPlotOn():
            ax.legend(loc='upper left')
            ax.set_xticks(xticks)
            ax.set_xticklabels(xticks, rotation=90)
            plt.subplots_adjust(bottom=0.21)
            fig.savefig(filename.replace('.csv', '.png'), dpi=300)
            plt.close()
        return


def recapture(population, n, k=5):
    """
    given a population, conducts recapture analysis for sample size = n.
    This experiment is repeated k times, and a list of length k is returned with percent recapture rate.
    :param population: collection of sequences
    :param n: sample size to randomly pick
    :param k: repeat recapture experiment k times
    :return: tuple of (a, b) where
            a == n
            b is a list of length k and each value is the percentage of recapture
    """
    hs = []
    for _ in range(k):
        s1 = set(np.random.choice(population, n))
        s2 = set(np.random.choice(population, n))
        intersection = s2.intersection(s1)
        hs.append(len(intersection) * 100.0 / len(s2))

    return (
     n, hs)


def plotSeqRecaptureNew(seqs, labels, filename, title='', threads=2, stream=None):
    """
    Perform non-redundant capture-recapture analysis and plot the percent recapture.
    Uses sampling without replacement and gives equal properties to all clones.

    Assumption 1: the population is assumed to be "closed".
    Assumption 2:  The chance for each individual in the population to be caught
    are equal and constant for both the initial marking period and the recapture period.
    Assumption 3:  Sufficient time must be allowed between the initial marking period
     and the recapture period
    Assumption 4: Animals do not lose their marks.

    :param seqs: list of lists
                ith nested list should consist of sequences that correspond to ith element of label
    :param labels: list of strings
                ith item describes the region of the ith list in seqs parameter
    :param filename: output filename
    :param title: string
                plot title
    :param threads: int
    :param stream: output stream
    :return: None
    """
    if eitherExists(filename):
        printto(stream, '\tFile found ... ' + os.path.basename(filename), LEVEL.WARN)
        return
    if PlotManager.pythonPlotOn():
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.grid()
        ax.set_xlabel('Sample size')
        ax.set_ylabel('Percent Recapture')
        ax.set_title(title)
    csvData = []
    for setSeqs, l in zip(seqs, labels):
        total = 35000
        ticks = np.linspace(100, total, 50).astype(int)
        pool = multiprocessing.Pool(processes=threads)
        result = [ pool.apply_async(recapture, args=(setSeqs, t)) for t in ticks ]
        pt = sorted([ p.get() for p in result ], key=lambda tup: tup[0])
        pool.close()
        pool.join()
        csvData.extend([ (x, y, l) for x, ys in pt for y in ys ])
        if PlotManager.pythonPlotOn():
            ax.plot([ d[0] for d in pt ], [ mean(d[1]) for d in pt ], label=l)

    xticks = np.linspace(0, total, 15).astype(int)
    xticks = map(lambda x: x - x % 1000 if x > 1000 else x, xticks)
    writeCSV(filename, 'x,y,region\n', '{},{},{}\n', csvData, zip=True, metadata=str(xticks).strip('[]') + '\n')
    if PlotManager.pythonPlotOn():
        ax.legend(loc='upper left')
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks, rotation=90)
        plt.subplots_adjust(bottom=0.21)
        fig.savefig(filename.replace('.csv', '.png'), dpi=300)
        plt.close()


def plotVenn(sets, filename, title='', stream=None):
    if eitherExists(filename):
        printto(stream, 'File found ... ' + os.path.basename(filename), LEVEL.WARN)
        return
    fig, ax = plt.subplots()
    if len(sets) == 2:
        from matplotlib_venn import venn2
        venn2(sets.values(), sets.keys())
    elif len(sets) == 3:
        from matplotlib_venn import venn3
        venn3(sets.values(), sets.keys())
    else:
        printto(stream, 'Venn diagram cannot be generated for more than 3 restriction enzymes', LEVEL.ERR)
        return
    ax.set_title(title)
    fig.savefig(filename, dpi=300)
    plt.close()


def plotDist(ighvDistfam, sampleName, filename, title='', proportion=True, rotateLabels=True, vertical=True, sortValues=True, top=15, maintainx=False, stream=None):
    if eitherExists(filename):
        printto(stream, 'File found ... ' + os.path.basename(filename), LEVEL.WARN)
        return
    if sortValues:
        classes = sorted(ighvDistfam, key=ighvDistfam.get, reverse=True)
    else:
        if not maintainx:
            classes = ighvDistfam.keys()
            classes.sort()
        else:
            classes = ighvDistfam.keys()
        allClasses = classes[:]
        if len(classes) > top:
            classes = classes[:top]
        if not vertical:
            classes = classes[::-1]
            allClasses = allClasses[::-1]
        total = sum(ighvDistfam.values()) * 1.0
        if total == 0:
            printto(stream, ('Will not calculate {} because there is no distribution.').format(os.path.basename(filename.rstrip(os.sep))), LEVEL.WARN)
            return
        stats = map(lambda x: ighvDistfam[x] / total * 100, classes)
        if len(stats) < 1:
            return
        ind = np.arange(len(classes))
        fig, ax = plt.subplots(figsize=(8, 5) if vertical else (5, 8))
        ax.grid()
        if len(classes) > 10:
            width = 0.4
        else:
            width = 0.6
        if proportion:
            topvalFormat = '{:.2f}'
        else:
            topvalFormat = '{:,}'
        if vertical:
            writeCSV(filename, 'x,y,raw\n', '{},{},{}\n', [ (x, y, ighvDistfam[x]) for x, y in zip(allClasses, map(lambda i: ighvDistfam[i] / total * 100, allClasses))
                                                          ], metadata='vert,total=' + str(total) + '\n')
            rects = ax.bar(ind, stats, width)
            ax.set_xticks(ind + width / 2)
            ax.set_ylim(top=max(stats) * 1.1)
            if rotateLabels:
                ax.set_xticklabels(classes, rotation=45)
            else:
                ax.set_xticklabels(classes)
            ax.set_ylabel('Proportion (%)')
            for rect in rects:
                height = rect.get_height()
                if not proportion:
                    ax.text(rect.get_x() + rect.get_width() / 2.0, 1.05 * height, topvalFormat.format(int(np.round(height * total / 100))), ha='center', va='bottom', size=10, color='red')
                else:
                    ax.text(rect.get_x() + rect.get_width() / 2.0, 1.05 * height, topvalFormat.format(height), ha='center', va='bottom', size=10, color='red')

        else:
            writeCSV(filename, 'x,y,raw\n', '{},{},{}\n', [ (x, y, ighvDistfam[y]) for x, y in zip(map(lambda i: ighvDistfam[i] / total * 100, allClasses), allClasses)
                                                          ], metadata='hori,total=' + str(total) + '\n')
            rects = ax.barh(ind, stats, width)
            ax.set_yticks(ind + width / 2)
            ax.set_xlim(right=max(stats) * 1.1)
            if rotateLabels:
                ax.set_yticklabels(classes, rotation=45)
            else:
                ax.set_yticklabels(classes)
            ax.set_xlabel('Proportion (%)')
            for rect in rects:
                width = rect.get_width()
                if not proportion:
                    ax.text(0.8 + width, rect.get_y() + rect.get_height() / 2.0, topvalFormat.format(int(np.round(width * total / 100))), ha='center', va='bottom', size=10, color='red')
                else:
                    ax.text(0.8 + width, rect.get_y() + rect.get_height() / 2.0, topvalFormat.format(width), ha='center', va='bottom', size=10, color='red')

    if title == '':
        title = 'IGV Abundance in Sample ' + sampleName
    title += ('\nTotal is {:,}').format(int(total))
    ax.set_title(title)
    plt.tight_layout()
    if PlotManager.pythonPlotOn():
        fig.savefig(filename.replace('.csv', '.png'), dpi=300)
    plt.close()


def generateStatsHeatmap(data, sampleName, xyCol, axlabels, filename, stream=None):
    if eitherExists(filename):
        printto(stream, ('File {} found, skipping generation ... ').format(os.path.basename(filename)), LEVEL.WARN)
        return
    x = data[xyCol[0]].tolist()
    y = data[xyCol[1]].tolist()
    total = len(x)
    BINS = 10
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=BINS)
    heatmap = heatmap / np.sum(heatmap) * 100
    exportMatrix(heatmap.transpose(), centrizeBins(xedges), centrizeBins(yedges), filename, metadata='total=' + str(total))
    extent = [xedges[0], xedges[(-1)], yedges[0], yedges[(-1)]]
    title = 'Alignment Quality of Sample ' + sampleName
    title += ('\nTotal is {:,}').format(int(total))
    plotHeatmap(heatmap.transpose()[::-1], extent, xedges, yedges, filename, axlabels, title)


def centrizeBins(bins):
    return bins[:-1] + np.diff(bins) / 2


def exportMatrix(matrix, xlabel, ylabel, filename, sep='\t', metadata=None):
    assert len(xlabel) == matrix.shape[1]
    assert len(ylabel) == matrix.shape[0]
    with open(filename, 'w') as (fp):
        if metadata:
            fp.write(str(metadata) + '\n')
        fp.write(sep.join(map(str, xlabel)) + '\n')
        [ fp.write(str(ylabel[i]) + sep + sep.join(map(str, row)) + '\n') for i, row in enumerate(matrix) ]


def plotHeatmap(hm, extent, xticks, yticks, filename, axlabels=None, title=None):
    if PlotManager.pythonPlotOn():
        fig, ax = plt.subplots()
        cax = ax.imshow(hm, cmap='jet', interpolation='nearest', extent=extent)
        if axlabels is not None:
            ax.set_xlabel(axlabels[0])
            ax.set_ylabel(axlabels[1])
        ax.set_title(title)
        ax.set_xticks(np.array(xticks).astype(int))
        ax.set_yticks(np.array(yticks).astype(int))
        ax.tick_params(axis='both', which='major', labelsize=8)
        cbar = fig.colorbar(cax, ticks=np.linspace(np.min(hm), np.max(hm), 5), orientation='horizontal')
        forceAspect(ax, aspect=1)
        fig.savefig(filename, dpi=300)
        plt.close()
    return


def plotHeatmapFromDF(df, filename, title=None, stream=None):
    fig, ax = plt.subplots()
    cax = ax.pcolor(df, cmap=cm.Blues)
    fig = plt.gcf()
    fig.set_size_inches(11, 13)
    ax.set_frame_on(False)
    ax.set_yticks(np.arange(df.shape[0]) + 0.5, minor=False)
    ax.set_xticks(np.arange(df.shape[1]) + 0.5, minor=False)
    ax.set_yticks(np.arange(df.shape[0] + 1), minor=True)
    ax.set_xticks(np.arange(df.shape[1] + 1), minor=True)
    ax.set_xlim([0, df.shape[1]])
    ax.set_ylim([0, df.shape[0]])
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    if len(df) > 20:
        ax.set_xticklabels(df.columns, minor=False, fontsize='small')
        ax.set_yticklabels(df.index, minor=False, fontsize='small')
    else:
        ax.set_xticklabels(df.columns, minor=False)
        ax.set_yticklabels(df.index, minor=False)
    plt.xticks(rotation=90)
    ax.grid(True, which='minor')
    ax = plt.gca()
    for t in ax.xaxis.get_major_ticks():
        t.tick1On = False
        t.tick2On = False

    for t in ax.yaxis.get_major_ticks():
        t.tick1On = False
        t.tick2On = False

    cbar = fig.colorbar(cax, ticks=np.linspace(df.min().min(), df.max().max(), 5), label='Jaccard index', orientation='horizontal')
    fig.savefig(filename, dpi=300)
    plt.close()


def cmap_discretize(cmap, N):
    """Return a discrete colormap from the continuous colormap cmap.

        cmap: colormap instance, eg. cm.jet. 
        N: number of colors.

    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
        imshow(x, cmap=djet)
    """
    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)
    colors_i = np.concatenate((np.linspace(0, 1.0, N), (0.0, 0.0, 0.0, 0.0)))
    colors_rgba = cmap(colors_i)
    indices = np.linspace(0, 1.0, N + 1)
    cdict = {}
    for ki, key in enumerate(('red', 'green', 'blue')):
        cdict[key] = [ (indices[i], colors_rgba[(i - 1, ki)], colors_rgba[(i, ki)]) for i in range(N + 1) ]

    return mcolors.LinearSegmentedColormap(cmap.name + '_%d' % N, cdict, 1024)


def forceAspect(ax, aspect=1):
    im = ax.get_images()
    extent = im[0].get_extent()
    ax.set_aspect(abs((extent[1] - extent[0]) / (extent[3] - extent[2])) / aspect)


def excludeOutliers(values, weights, m=4.0):
    values = np.array(values)
    weights = np.array(weights)
    avg, std = weightedAvgAndStd(values, weights)
    sel = abs(values - avg) <= m * std
    return (values[sel].tolist(), weights[sel].tolist())


def weightedAvgAndStd(values, weights):
    """
    Return the weighted average and standard deviation.

    values, weights -- Numpy ndarrays with the same shape.
    """
    average = np.average(values, weights=weights)
    variance = np.average((values - average) ** 2, weights=weights)
    return (average, math.sqrt(variance))


AA = [
 'GAST', 'CVILPFYMW', 'NQH', 'DE', 'KR']
AA_colours = numpy.concatenate((
 cm.Oranges((1 + numpy.arange(len(AA[0]), dtype=float)) / (len(AA[0]) + 1)),
 cm.Greens((1 + numpy.arange(len(AA[1]), dtype=float)) / (len(AA[1]) + 1)),
 cm.Purples((1 + numpy.arange(len(AA[2]), dtype=float)) / (len(AA[2]) + 1)),
 cm.Reds((1 + numpy.arange(len(AA[3]), dtype=float)) / (len(AA[3]) + 1)),
 cm.Blues((1 + numpy.arange(len(AA[4]), dtype=float)) / (len(AA[4]) + 1))))
AA = ('').join(AA)

def barLogo(counts, title, filename, removeOutliers=False, scaled=False, stream=None):
    """

    :param counts:
    :param title:
    :param filename:
    :param removeOutliers:
    :param scaled: boolean
                proportion over max number of amino acid. If False, then proportion is set to be over the sum
                of current position's number of amino acids. For example, position 23 might have N-2 total amino acid
                counts ( i.e. sum(counts[22].values()) == N-2) because there are 2 sequences that don't have length
                >= 23. If scaled was set to False, the proportion calculated for position 23 is x / N-2 rather than
                x / N
    :param stream:
    :return:
    """
    if eitherExists(filename):
        printto(stream, 'File found ... ' + os.path.basename(filename), LEVEL.WARN)
        return
    totals = np.array([ sum(ct.values()) for ct in counts ])
    if removeOutliers:
        sel = totals > 0.01 * max(totals)
        counts = [ counts[i] for i in range(len(counts)) if sel[i] ]
    if scaled:
        barFractions = [ [ ct.get(aa, 0) / float(max(totals)) for aa in AA ] for ct in counts ]
    else:
        barFractions = [ [ ct.get(aa, 0) / float(sum(ct.values())) for aa in AA ] for ct in counts
                       ]
    byAA = [ [] for aa in AA ]
    byAABase = [ [] for aa in AA ]
    for bf in barFractions:
        s = 0.0
        for i, aa in enumerate(AA):
            byAA[i].append(bf[i])
            byAABase[i].append(s)
            s += bf[i]

    if PlotManager.pythonPlotOn():
        fig, ax = plt.subplots(figsize=(8, 5))
        for i, aa in enumerate(AA):
            ax.bar(numpy.arange(len(barFractions)) + 0.05, byAA[i], width=0.9, bottom=byAABase[i], color=AA_colours[i], label=AA[i], lw=0)

        ax.set_title(title, fontsize=20)
        ax.set_ylim(0, 1)
        ax.set_xticks(numpy.arange(len(counts)) + 0.5)
        ax.set_xticklabels([ ct.most_common(1)[0][0] for ct in counts ])
        ax.tick_params(axis='both', which='major', labelsize=14)
        ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1), fontsize='x-small')
        fig.savefig(filename, dpi=300)
        plt.close()


def generateCumulativeLogo(seqs, weights, region, filename, stream=None):
    if eitherExists(filename):
        printto(stream, '\t' + region + ' Cumulative Logo was found ', LEVEL.WARN)
    else:
        m = min(30, maxlen(seqs))
        aaCounts = []
        for x in range(m):
            cnt = defaultdict(int)
            for i in range(len(seqs)):
                seq = seqs[i].upper()
                if x < len(seq):
                    cnt[seq[x]] += weights[i]

            aaCounts.append(Counter(cnt))

        barLogo(aaCounts, ('{} ({:,})').format(region.upper(), sum(weights)), filename.replace('.csv', '.png'), removeOutliers=region != 'cdr3', stream=stream)
        barLogo(aaCounts, ('{} ({:,})').format(region.upper(), sum(weights)), filename.replace('.csv', '_scaled.png'), scaled=True, stream=stream)
        rawCountsFileName, _ = os.path.splitext(filename)
        rawCountsFileName += '_raw.csv'
        allAAs = ('').join(set(itertools.chain.from_iterable(count.keys() for count in aaCounts))).upper()
        total = max(sum(count.values()) for count in aaCounts)
        with open(rawCountsFileName, 'w') as (fp):
            positions = range(1, len(aaCounts) + 1)
            fp.write('AminoAcid/Position,' + (',').join(map(str, positions)) + '\n')
            for aa in sorted(allAAs):
                aaBuffer = ''
                for counter in aaCounts:
                    aaBuffer += ',' + ('{:.3}').format(float(counter.get(aa, 0)) / total)

                fp.write(('{}{}\n').format(aa, aaBuffer))

        plotFileName, _ = os.path.splitext(filename)
        plotFileName += '.csv'
        writeCSV(plotFileName, 'position,aa,count\n', '{},{},{}\n', vals=[ (p, aa, counts) for p, cnt in enumerate(aaCounts) for aa, counts in cnt.items() ])


def writeCSV(filename, header, template, vals, zip=False, metadata=''):
    """
    Writes to file - filename using provided header and template format
    :param filename: filename to save csv
    :param header: first row of csv - header row
    :param template: for each line, format the values according to template
    :param vals: list of (list or) tuples to unpack into template placeholder
    :param zip: True if file should be zipped, false otherwise [default=False]
    :param metadata: Prints metadata before csv header. [default=""]
    :return: None. Outputs a CSV file
    """
    assert '.csv' in filename
    if exists(filename) or exists(filename + '.gz'):
        return
    if zip:
        f = gzip.open(filename + ('' if '.gz' in filename else '.gz'), 'wb')
    else:
        f = open(filename, 'w')
    f.write(metadata)
    f.write(header + ('\n' if '\n' not in header else ''))
    for arg in vals:
        f.write(template.format(*arg))

    f.close()


def eitherExists(filename, originalExt='.png', exts=('.csv', '.csv.gz')):
    if exists(filename):
        return True
    if PlotManager.pythonPlotOn():
        return False
    for ex in exts:
        if exists(filename.replace(originalExt, ex)):
            return True

    return False