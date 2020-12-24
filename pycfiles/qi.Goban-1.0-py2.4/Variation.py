# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/Goban/lib/Variation.py
# Compiled at: 2008-04-06 04:02:05
import copy

class VariationList(dict):
    __module__ = __name__

    def __init__(self):
        dict.__init__(self)
        self.variationTree = dict()

    def addVariation(self, varId, movesAndAnnotations, branchMove=0, parentId=None):
        self[varId] = movesAndAnnotations
        self.variationTree[varId] = dict()
        if parentId is not None:
            pDict = self.variationTree[parentId]
            if not pDict.has_key(branchMove):
                pDict[branchMove] = list()
            pDict[branchMove].append(varId)
            self.variationTree[parentId] = pDict
            self.variationTree[varId][branchMove] = [parentId]
        return

    def chapterizeVariationNames(self):
        newVarNames = dict()
        newVarNames[0] = '0'
        self.chapterizeVariation(0, newVarNames)
        for key in self.keys():
            self[newVarNames[key]] = self[key]
            del self[key]

        for key in self.variationTree.keys():
            newMoveDict = dict()
            for move in self.variationTree[key]:
                newMoveDict[move] = [ newVarNames[childVar] for childVar in self.variationTree[key][move] ]

            self.variationTree[newVarNames[key]] = newMoveDict
            del self.variationTree[key]

    def chapterizeVariation(self, key, newVarNames):
        parentName = newVarNames[key]
        childVariations = list()
        for move in self.variationTree[key].keys():
            childVarsAtMove = self.variationTree[key][move]
            for child in childVarsAtMove:
                childVariations.append(child)

        childVariations = [ item for item in childVariations if item > key ]
        childVariations.sort()
        for i in range(0, len(childVariations)):
            newVarNames[childVariations[i]] = parentName + '.' + str(i + 1)
            self.chapterizeVariation(childVariations[i], newVarNames)

    def hasVariations(self, varid, moveNo):
        if self.variationTree[varid].has_key(moveNo):
            return self.variationTree[varid][moveNo]
        return

    def getMove(self, varid, moveNo):
        return self[varid][0][moveNo]

    def getAnnotation(self, varid, moveNo):
        if self[varid][1].has_key(moveNo):
            return self[varid][1][moveNo]