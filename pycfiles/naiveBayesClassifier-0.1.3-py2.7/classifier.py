# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/naiveBayesClassifier/classifier.py
# Compiled at: 2014-05-12 12:53:33
from __future__ import division
import operator
from functools import reduce
from ExceptionNotSeen import NotSeen

class Classifier(object):
    """docstring for Classifier"""

    def __init__(self, trainedData, tokenizer):
        super(Classifier, self).__init__()
        self.data = trainedData
        self.tokenizer = tokenizer
        self.defaultProb = 1e-09

    def classify(self, text):
        documentCount = self.data.getDocCount()
        classes = self.data.getClasses()
        tokens = self.tokenizer.tokenize(text)
        probsOfClasses = {}
        for className in classes:
            tokensProbs = [ self.getTokenProb(token, className) for token in tokens ]
            try:
                tokenSetProb = reduce(lambda a, b: a * b, (i for i in tokensProbs if i))
            except:
                tokenSetProb = 0

            probsOfClasses[className] = tokenSetProb / self.getPrior(className)

        return sorted(probsOfClasses.items(), key=operator.itemgetter(1), reverse=True)

    def getPrior(self, className):
        return self.data.getClassDocCount(className) / self.data.getDocCount()

    def getTokenProb(self, token, className):
        classDocumentCount = self.data.getClassDocCount(className)
        try:
            tokenFrequency = self.data.getFrequency(token, className)
        except NotSeen as e:
            return

        if tokenFrequency is None:
            return self.defaultProb
        else:
            probablity = tokenFrequency / classDocumentCount
            return probablity