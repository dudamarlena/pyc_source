# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/epscComp/setParameters.py
# Compiled at: 2009-05-29 13:49:10
from parameter import *
from scipy import *
import re, os, config

class SetParameters:
    """
    handling parameters for optimization

    Data member : betaFile => file path for particle phase parameters
                  mgFile => file path for matrix phase parameters
                  parDict => dictionary for the parameters
    """

    def __init__(self):
        self.betaFile = config.dirEpscCore + 'MATERIAL_1.sx'
        self.phase2File = config.dirEpscCore + 'MATERIAL_2.sx'
        self.parDict = {}

    def addPar(self, name, active, initialValue, comment=''):
        self.parDict[name] = Parameters(name=name, active=active, value=initialValue, comment=comment)

    def selectPars(self):
        self.parNames = []
        for (key, item) in self.parDict.iteritems():
            if item.active:
                self.parNames.append(key)

    def getParVals(self):
        parVals = []
        parOrder = []
        for parName in self.parNames:
            for i in range(8):
                for j in range(4):
                    if parName == config.voce[i][j]:
                        parOrder.append(i * 4 + j)

        print parOrder
        k = 0
        m = 0
        for k in range(len(parOrder) - 1):
            for m in range(len(parOrder) - k - 1):
                if parOrder[k] > parOrder[(k + m + 1)]:
                    temp = parOrder[k]
                    tempPar = self.parNames[k]
                    parOrder[k] = parOrder[(k + m + 1)]
                    self.parNames[k] = self.parNames[(k + m + 1)]
                    parOrder[k + m + 1] = temp
                    self.parNames[k + m + 1] = tempPar
                    m = 0

        for parName in self.parNames:
            parVals.append(self.parDict[parName].value)

        self.parVals = array(parVals)
        return self.parVals

    def setParVals(self, p):
        parNameList = []
        if len(self.parNames) != len(p):
            raise 'Invalid parameter assignment. Unequal array lengths!             len(self.parNames)=%s, len(p)=%s' % (len(self.parNames), len(p))
        elif type(p) != type(array([0])):
            raise 'parameters should be type array!'
        else:
            for i in range(len(p)):
                parName = self.parNames[i]
                self.parDict[parName].value = p[i]
                parNameList.append(parName)

            return parNameList

    def getPh1TemplateStr(self):
        fid = open(config.dirEpscCore + 'template_MATERIAL_Phase1_opt.sx', 'r')
        self.betaTemplateStr = fid.read()
        fid.close()

    def getPh2TemplateStr(self):
        fid = open(config.dirEpscCore + 'template_MATERIAL_Phase2_opt.sx', 'r')
        self.mgTemplateStr = fid.read()
        fid.close()

    def subBeta(self, vocePars):
        """vocePars= a list of voce pars in the correct order"""
        count = 0
        self.betaStr = self.betaTemplateStr
        for vocePar in vocePars:
            count = count + 1
            p = re.compile('\\$Voce_SS\\d{1,2}_' + `count`)
            (self.betaStr, num) = re.subn(p, `vocePar`, self.betaStr)
            print 'Voce parameter %s has been replaced for %s slip systems to %s' % (count, num, vocePar)

    def subMg(self, vocePars):
        """vocePars= a list of voce pars in the correct order"""
        count = 0
        self.mgStr = self.mgTemplateStr
        for vocePar in vocePars:
            count = count + 1
            p = re.compile('\\$Voce_SS\\d{1,2}_' + `count`)
            (self.mgStr, num) = re.subn(p, `vocePar`, self.mgStr)
            print 'Voce parameter %s has been replaced for %s slip systems to %s' % (count, num, vocePar)

    def subVoce(self):
        tempStr = self.betaTemplateStr
        for i in range(8):
            for j in range(4):
                tempStr = tempStr.replace('$Voce_SS' + str(i + 1) + '_' + str(j + 1), `(self.parDict[config.voce[i][j]].value)`)

        return tempStr

    def updateFiles(self):
        self.getPh1TemplateStr()
        result = self.subVoce()
        fid = open(self.betaFile, 'w')
        fid.write(result)
        fid.close()