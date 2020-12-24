# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: CGEA/lib/featureBasedCGEA.py
# Compiled at: 2016-04-20 16:30:38
from file import read_JSON, read_file, write_csv, prettyPrint
import random, math, time, os, json, multiprocessing as mp
from copy import deepcopy
import numpy as np, os
from sklearn import mixture, preprocessing
from sklearn.externals import joblib
from statsmodels.sandbox.stats.multicomp import multipletests
from operator import itemgetter
from statistics import generateBackgroundModel, generateScore, generatePVals, compoundSetGSEA, scoreRankedLists, makeMixmdl
from CGEAdata import CGEAdata
from featureListProcessing import formatGeneLists

def featureBasedCGEA(upgenes, downgenes, saveAs, outputDir, sortDir, data, status, alpha=0.05, numWorkers=mp.cpu_count(), pool=None, verbose=True, numPermutations=1000):
    status[1] = 'Started'
    status[2] = 0.01
    curTime = time.time()
    data = CGEAdata(data=data)
    status[1] = 'Loading cmap data'
    if verbose:
        print status[1]
    cmap = data.get('cmap')
    status[1] = 'Loaded cmap data'
    if verbose:
        print status[1]
    status[2] = 0.03
    geneLists = formatGeneLists([upgenes, downgenes])
    status[1] = 'Generating Null Model'
    if verbose:
        print status[1]
    curTime = time.time()
    backgroundModel, backgroundScores, scaler = generateBackgroundModel(geneLists, cmap, status=status, numWorkers=numWorkers, numPermutations=numPermutations)
    status[1] = 'Generated Null Model'
    if verbose:
        print status[1]
    status[2] = 0.33
    curTime = time.time()
    status[1] = 'Scoring Compounds'
    if verbose:
        print status[1]
    drugIndex, scores, index = scoreRankedLists(geneLists, cmap, status=status, numWorkers=numWorkers, pool=pool)
    curTime = time.time()
    pvals, adjpvals, scores = generatePVals(backgroundModel, scores, backgroundScores=backgroundScores, scaler=scaler, alpha=alpha, numWorkers=numWorkers, pool=pool)
    status[1] = 'Compounds Scored and Annotated'
    if verbose:
        print status[1]
    status[2] = 0.66
    curTime = time.time()
    drugAnnotations = {}
    for drug in drugIndex.keys():
        index = drugIndex[drug]
        drugAnnotations[drug] = {'Name': drug, 'Score': scores[index], 
           'P-Value': pvals[index], 
           'Adjusted P-Value': adjpvals[index]}

    status[1] = 'Performing Gene Enrichment'
    if verbose:
        print status[1]
    rankedAnnotatedDrugs, compoundSetResults = geneEnrichment(drugAnnotations, data, status=status, numWorkers=numWorkers, pool=pool)
    results = {'Annotated Compounds': rankedAnnotatedDrugs, 'Combined Enrichment Results': compoundSetResults}
    status[1] = 'Performed Gene Enrichment'
    if verbose:
        print status[1]
    status[2] = 0.99
    curTime = time.time()
    return results


typos = {'X6.bromoindirubin.3..oxime': '6-bromoindirubin-3-oxime', 'alpha.estradiol': 'alpha-estradiol'}
mySort = {'up': lambda x: x.sort(key=itemgetter('Score')), 
   'down': lambda x: sort(key=itemgetter('Score'), reverse=True), 
   'abs': lambda x: x.sort(key=lambda y: abs(y['Score']))}

def geneEnrichment(drugAnnotations, data, sortDir='up', status=None, numWorkers=mp.cpu_count(), pool=None):
    curTime = time.time()
    cmapDrugMetaData = data.get('cmapDrugMetaData')
    for drugData in cmapDrugMetaData:
        if drugData['name'] in drugAnnotations:
            drugAnnotations[drugData['name']].update(drugData)
            del drugAnnotations[drugData['name']]['name']
        elif drugData['Rname'] in drugAnnotations:
            drugAnnotations[drugData['Rname']].update(drugData)
            del drugAnnotations[drugData['Rname']]['name']
        elif drugData['name'] in typos:
            drugAnnotations[typos[drugData['name']]].update(drugData)
            del drugAnnotations[typos[drugData['name']]]['name']
        elif drugData['Rname'] in typos:
            drugAnnotations[typos[drugData['Rname']]].update(drugData)
            del drugAnnotations[typos[drugData['Rname']]]['name']
        else:
            print 'Missing from annotations: ' + drugData['name'] + '/' + drugData['Rname']

    del cmapDrugMetaData
    rankedAnnotatedDrugs = drugAnnotations.values()
    mySort[sortDir](rankedAnnotatedDrugs)
    sizeThreshold = 5
    targetEnrSeedPAdj = 0.1
    minCompoundSetSizeThreshold = 5
    unifiedCompoundLevelSets = data.get('unifiedCompoundLevelSets')
    mixmdls = data.getModel('mixmdl')
    if not mixmdls:
        print 'Gene Enrichment Mixture Models are not loaded. Computing Compound Set Mixmdls.'
        setSizes = reduce(lambda x, y: set.union(x, set(map(len, y.values()))), unifiedCompoundLevelSets.values(), set())
        makeMixmdl(data.get('cmap').keys(), data.getPath('mixmdl'), setSizes=setSizes, numIterations=1000)
        mixmdls = data.getModel('mixmdl')
    status[2] += 0.03
    enrichmentData = data.getEnrichmentData()
    rankedDrugs = map(itemgetter('Name'), rankedAnnotatedDrugs)
    compoundSetResults = {}
    numSets = len(unifiedCompoundLevelSets.keys() + enrichmentData.keys())
    for setType, compoundSets in unifiedCompoundLevelSets.items() + enrichmentData.items():
        compoundSets = filter(lambda x: len(x[1]) > minCompoundSetSizeThreshold, compoundSets.items())
        if len(compoundSets) > 0:
            compoundSetResults[setType] = compoundSetGSEA(rankedDrugs, mixmdls, compoundSets, numWorkers=numWorkers, pool=pool)
        status[2] += 1.0 / numSets * 3.0 / 10.0

    summaryResults = reduce(lambda x, y: x + map(lambda z: dict(zip(['Compound Set'] + z.keys(), [y[0]] + z.values())), y[1]), compoundSetResults.items(), [])
    mySort[sortDir](summaryResults)
    return [rankedAnnotatedDrugs, summaryResults]