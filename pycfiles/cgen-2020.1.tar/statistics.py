# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: CGEA/lib/statistics.py
# Compiled at: 2016-04-29 13:00:50
import random, math, time
from copy import deepcopy
import numpy as np
from sklearn import mixture, preprocessing
from sklearn.externals import joblib
from statsmodels.sandbox.stats.multicomp import multipletests
from scipy.stats import hypergeom
from operator import itemgetter
from SimpleMapReduce import SimpleMapReduce
from errorHandling import printException
import itertools, multiprocessing as mp

def multiMap(mapFunc, inputs, numWorkers, chunksize, pool=None):
    if numWorkers > 1 and not pool:
        pool = mp.Pool(numWorkers)
    if numWorkers > 1:
        results = pool.map(mapFunc, inputs, chunksize=chunksize)
    else:
        results = map(mapFunc, inputs)
    if pool:
        pool.close()
        pool.join()
    return results


def scoreRankedLists(featureLists, rankedLists, status=None, numWorkers=mp.cpu_count(), pool=None):
    nameIndex = {}
    index = {}
    scoreData = multiMap(scoreRankedList(featureLists, rankedLists, status), rankedLists.keys(), numWorkers, chunksize=int(math.ceil(float(len(rankedLists.keys())) / numWorkers)), pool=pool)
    for count, data in enumerate(scoreData):
        name = data[0]
        index[count] = name
        nameIndex[name] = count

    scores = map(lambda x: [x[1]], scoreData)
    return [
     nameIndex, scores, index]


class scoreRankedList:

    def __init__(self, featureLists, rankedLists, status):
        self.featureLists = featureLists
        self.rankedLists = rankedLists
        self.status = status
        self.countLists = len(rankedLists.keys())

    def __call__(self, name):
        if self.status:
            self.status[2] += 1.0 / self.countLists * 3.3 / 10.0
        cmapList = self.rankedLists[name]
        return [
         name, generateScore(self.featureLists, cmapList)[0]]


class genPval:

    def __init__(self, weights):
        self.weights = weights

    def __call__(self, x):
        return sum(map(lambda y: pow(10, math.log(x[1][y] / self.weights[y], 10) + x[0]), range(0, len(self.weights))))


def generatePVals(backgroundModel, scores, setSizes=None, backgroundScores=None, scaler=None, alpha=0.05, FDR=None, numWorkers=mp.cpu_count(), pool=None):
    if not isinstance(backgroundModel, dict):
        if not FDR:
            FDR = calcFDR(backgroundModel, backgroundScores, alpha=alpha)
        if scaler:
            scores = scaler.transform(scores)
        pvals = map(genPval(backgroundModel.weights_), zip(*backgroundModel.score_samples(scores)))
        scores = map(itemgetter(0), scores)
    else:
        pvals = []
        FDRs = []
        for index, score in enumerate(scores):
            setSize = setSizes[index]
            if setSize not in backgroundModel:
                setSize = max(backgroundModel.keys())
            model = backgroundModel[setSize]['model']
            FDRs.append(backgroundModel[setSize]['FDR'])
            scaler = backgroundModel[setSize]['scaler']
            pvals.append(map(genPval(model.weights_), zip(*model.score_samples(scaler.transform(np.array([score]).reshape(1, -1)))))[0])

        FDR = np.mean(FDRs)
    adjpvals = multipletests(pvals, method='fdr_bh', alpha=FDR)[1]
    return [
     list(pvals), list(adjpvals), list(scores)]


def calcFDR(backgroundModel, backgroundScores, alpha=0.05):
    backgroundPvals = map(genPval(backgroundModel.weights_), zip(*backgroundModel.score_samples(backgroundScores)))
    FDR = sorted(backgroundPvals)[int(math.floor(len(backgroundPvals) * alpha))]
    return FDR


backgroundModelScoringMethods = {'query': lambda x, y, z, w, s, nw, p: generateBackgroundScores(x, y, z, status=s, numWorkers=nw, pool=p), 
   'randomSubset': lambda x, y, z, w, s, nw, p: reduce(lambda a, b: a + b, map(lambda placeholder: generateBackgroundScores(random.sample(x, w), sorted(y, key=lambda k: random.random()), int(math.ceil(math.sqrt(z))), numWorkers=nw, pool=p), range(0, int(math.ceil(math.sqrt(z))))))}
n_components = {'query': 3, 'randomSubset': 2}

def generateBackgroundModel(featureLists, rankedList, numPermutations=1000, sizeOfSubset=None, method='query', status=None, numWorkers=mp.cpu_count(), pool=None):
    scores = backgroundModelScoringMethods[method](featureLists, rankedList, numPermutations, sizeOfSubset, status, numWorkers, pool)
    scaler = preprocessing.StandardScaler().fit(scores)
    scores = scaler.transform(scores)
    model = mixture.GMM(n_components=n_components[method], covariance_type='diag', min_covar=0.001, tol=1e-05, n_iter=10000, n_init=200)
    model.fit(scores)
    return [
     model, list(scores), scaler]


def generateBackgroundScores(featureLists, rankedList, numPermutations, status=None, numWorkers=mp.cpu_count(), pool=None):
    generateBackgroundScoreFunction = generateBackgroundScore(featureLists, rankedList, numPermutations, status)
    scores = multiMap(generateBackgroundScoreFunction, range(numPermutations), numWorkers, chunksize=int(math.ceil(float(numPermutations) / numWorkers)), pool=pool)
    return scores


class generateBackgroundScore:

    def __init__(self, featureLists, rankedList, numPermutations, status):
        self.featureLists = featureLists
        self.rankedList = rankedList
        self.numPermutations = numPermutations
        self.status = status

    def __call__(self, runNumber):
        if self.status:
            self.status[2] += 1.0 / self.numPermutations * 3.0 / 10.0
        if isinstance(self.rankedList, dict):
            unrankedList = sorted(self.rankedList[random.choice(self.rankedList.keys())], key=lambda k: random.random())
        elif isinstance(self.rankedList, list):
            unrankedList = sorted(self.rankedList, key=lambda k: random.random())
        else:
            unrankedList = sorted(self.rankedList, key=lambda k: random.random())
        return [
         generateScore(self.featureLists, unrankedList)[0]]


def generateScore(featureLists, rankedList):
    if not isinstance(featureLists[0], list):
        featureLists = [featureLists]
    unrankedSet = set(rankedList)
    lenRankedList = len(rankedList)
    peakValues = []
    peakValueIndices = []
    hitPositions = []
    for featureList in featureLists:
        featureSet = set(featureList)
        featureSet = set.intersection(featureSet, unrankedSet)
        numHits = len(featureSet)
        if numHits > 0:
            numMisses = lenRankedList - numHits
            hits = map(lambda x: int(x in featureSet), rankedList)
            hitPositions.append(deepcopy(hits))
            hits = np.cumsum(hits)
            hits = map(lambda x: float(x) / numHits, hits)
            misses = np.cumsum(map(lambda x: int(x not in featureSet), rankedList))
            misses = map(lambda x: float(x) / numMisses, misses)
            difference = map(lambda x: abs(hits[x] - misses[x]), range(lenRankedList))
            peakValue = max(difference)
            peakIndex = difference.index(peakValue)
            peakValueIndices.append(peakIndex)
            peakValues.append(hits[peakIndex] - misses[peakIndex])

    if len(peakValues) == 1:
        score = peakValues[0]
        peakValueIndices = peakValueIndices[0]
        hitPositions = hitPositions[0]
    elif len(featureLists) == 2:
        score = (peakValues[0] - peakValues[1]) / 2
    else:
        raise ValueError
    return [score, peakValueIndices, hitPositions]


def compoundSetGSEA(rankedDrugs, mixmdls, compoundSets, alpha=0.05, numWorkers=mp.cpu_count(), pool=None):
    scores = []
    peakPositions = []
    hitPositionLists = []
    setSizes = []
    scoreData = multiMap(scoreCompoundSet(compoundSets, rankedDrugs), range(len(compoundSets)), min(numWorkers, len(compoundSets)), chunksize=int(math.ceil(float(len(compoundSets)) / numWorkers)), pool=pool)
    scores, peakPositions, hitPositionLists, setSizes = zip(*scoreData)
    pvals, adjpvals, scores = generatePVals(mixmdls, scores, setSizes=setSizes, alpha=alpha)
    output = []
    for index, (compoundName, _) in enumerate(compoundSets):
        output.append({'Name': compoundName, 'P-Value': pvals[index], 
           'Adjusted P-Value': adjpvals[index], 
           'Score': scores[index], 
           'Peak Position': peakPositions[index], 
           'Hit Positions': hitPositionLists[index]})

    return output


class scoreCompoundSet:

    def __init__(self, compoundSets, rankedDrugs):
        self.compoundSets = compoundSets
        self.rankedDrugs = rankedDrugs

    def __call__(self, index):
        compoundName, compoundSet = self.compoundSets[index]
        score, peakPosition, hitPositions = generateScore(compoundSet, self.rankedDrugs)
        hitPositions = map(itemgetter(0), filter(lambda x: x[1], enumerate(hitPositions)))
        hitPositions = (';').join(map(lambda x: self.rankedDrugs[x] + ':' + str(x), hitPositions))
        setSize = len(compoundSet)
        return [
         score, peakPosition, hitPositions, setSize]


def compoundSetHypergeometricEnrichment(querySet, compoundSets, universeSize, numWorkers, pool=None):
    compoundSetPvals = multiMap(setHypergeometricEnrichmentClass(querySet, universeSize), compoundSets, min(numWorkers, len(compoundSets)), chunksize=int(math.ceil(float(len(compoundSets)) / numWorkers)), pool=pool)
    compoundSetAdjPvals = multipletests(compoundSetPvals, method='fdr_bh', alpha=0.05)[1]
    return zip(*[compoundSetPvals, compoundSetAdjPvals])


class setHypergeometricEnrichmentClass:

    def __init__(self, querySet, universeSize):
        self.querySet, self.universeSize = querySet, universeSize

    def __call__(self, popB):
        return setHypergeometricEnrichmentScore(self.querySet, popB, self.universeSize)


def setHypergeometricEnrichmentScore(popA, popB, popSize):
    if not (isinstance(popA, set) and isinstance(popB, set)):
        print 'inputs should be sets in compoundSetHypergeometricEnrichment'
        return False
    popASize = len(popA)
    popBSize = len(popB)
    popAB = set.intersection(popA, popB)
    popABSize = len(popAB)
    if not len(set.union(popA, popB)) + popABSize == popASize + popBSize:
        print 'popA: ' + str(popA)
        print 'popB: ' + str(popB)
        print 'popAB: ' + str(popAB)
        print 'something is rotten in the state of setHypergeometricEnrichment function.'
    return hypergeom.sf(*[popABSize - 1, popSize, popASize, popBSize])


def makeMixmdl(featureList, filepath, maxSetSize=50, numIterations=100, alpha=0.05, setSizes=None):
    models = {}
    if not setSizes:
        setSizes = set(range(1, maxSetSize + 1))
    for i in setSizes:
        print 'Iteration#' + str(i)
        model, scores, scaler = generateBackgroundModel(featureList, featureList, numPermutations=numIterations, sizeOfSubset=i, method='randomSubset')
        models[i] = {'model': model, 'scaler': scaler, 
           'FDR': calcFDR(model, scores, alpha=alpha)}
        print np.histogram(scores)
        print 'Background weights:' + str(model.weights_)
        print 'Background means:' + str(map(itemgetter(0), model.means_))
        print 'Background covars:' + str(map(itemgetter(0), model.covars_))

    joblib.dump(models, filepath)