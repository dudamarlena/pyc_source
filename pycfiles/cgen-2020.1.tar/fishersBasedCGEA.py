# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/max/Desktop/workspace/CGEA-Packages/CGEA/CGEA/lib/fishersBasedCGEA.py
# Compiled at: 2016-04-13 15:06:37
from CGEAdata import CGEAdata
import multiprocessing as mp
from file import read_JSON, write_JSON, read_file
import os, time
from copy import deepcopy
from operator import itemgetter
from statistics import compoundSetHypergeometricEnrichment
import itertools, re
from drugListProcessing import drugListProcessing
from CGEA import __file__ as package_path
package_path = os.path.dirname(package_path)

def fishersBasedCGEA(drugList, outputDir, sortDir, data, status, alpha=0.05, numWorkers=mp.cpu_count(), verbose=True):
    status[1] = 'Started'
    status[2] = 0.01
    curTime = time.time()
    data = CGEAdata(data=data)
    status[1] = 'Loading cmap data'
    if verbose:
        print status[1]
    cmap = data.get('cmapDrugMetaDataWithOffsides')
    dlp = drugListProcessing(cmap)
    print 'Loaded cmap data - took ' + str(time.time() - curTime) + ' seconds'
    status[1] = 'Loaded cmap data'
    if verbose:
        print status[1]
    status[2] = 0.03
    drugList = list(itertools.chain(*map(lambda x: re.findall("[\\w']+", x), read_file(drugList))))
    hitNames = set(map(lambda x: x[0].lower(), filter(lambda x: x[1], dlp.inCMAP(drugList))))
    cmapNames = set(map(lambda x: x['Name'].lower(), cmap))
    annotatedCompounds = dlp.annotateCMAP(hitNames)
    compoundSetResults = {}
    minCompoundSetSizeThreshold = 5
    compoundListsFilepath = package_path + '/data/CompoundLists_SizeThreshold-' + str(minCompoundSetSizeThreshold) + '.json'
    if not os.path.isfile(compoundListsFilepath):
        startTime = time.time()
        unifiedCompoundLevelSets = data.get('unifiedCompoundLevelSets')
        enrichmentData = data.getEnrichmentData()
        compoundLists = unifiedCompoundLevelSets.items() + enrichmentData.items()
        compoundListsNames = map(itemgetter(0), compoundLists)
        compoundLists = list(itertools.chain(*map(lambda x: map(lambda y: (x[0],
         y[0],
         map(lambda z: z.lower(), filter(lambda z: dlp.inCMAP(z), y[1]))), x[1].items()), compoundLists)))
        compoundLists = filter(lambda x: len(x[2]) > minCompoundSetSizeThreshold, compoundLists)
        write_JSON(compoundListsFilepath, compoundLists)
    else:
        startTime = time.time()
        compoundLists = read_JSON(compoundListsFilepath)
    compoundSets = map(lambda x: set(x[2]), compoundLists)
    compoundSetScores = compoundSetHypergeometricEnrichment(hitNames, compoundSets, len(cmapNames), numWorkers)
    summaryResults = map(lambda x: {'Compound Set': x[1][0], 'Name': x[1][1], 
       'P-Value': compoundSetScores[x[0]][0], 
       'Adjusted P-Value': compoundSetScores[x[0]][1], 
       'Overlap Set': set.intersection(hitNames, compoundSets[x[0]])}, enumerate(compoundLists))
    for x in range(len(summaryResults)):
        if len(summaryResults[x]['Overlap Set']) == 0:
            summaryResults[x]['Overlap Set'] = 'NA'
        else:
            summaryResults[x]['Overlap Set'] = (';').join(sorted(summaryResults[x]['Overlap Set']))

    results = {'Annotated Compounds': annotatedCompounds, 'Combined Enrichment Results': summaryResults}
    return results