# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/accountingModules/structures.py
# Compiled at: 2012-04-02 10:34:53
import numpy

class Cac_details:

    def __init__(self):
        self.PI = ''
        self.startDate = ''
        self.expiryDate = ''
        self.allocatedCoreHours = 0
        self.jobsList = []

    def setPI(self, PI):
        self.PI = PI

    def setStartDate(self, startDate):
        self.startDate = startDate

    def setExpiryDate(self, expiryDate):
        self.expiryDate = expiryDate

    def setAllocatedHours(self, allocatedCoreHours):
        self.allocatedCoreHours = allocatedCoreHours

    def addJob(self, jobTuple):
        self.jobsList.append(jobTuple)

    def getNumJobs(self):
        return len(self.jobsList)

    def getUsedCoreHours(self):
        theSum = 0
        for i in range(len(self.jobsList)):
            theSum += self.jobsList[i][1]

        return theSum

    def getUsedNodes(self):
        theSum = 0
        try:
            for i in range(len(self.jobsList)):
                theSum += self.jobsList[i][2]

            return theSum
        except:
            return 0

    def getMedian(self):
        theMedian = 0
        tempList = []
        try:
            for i in range(len(self.jobsList)):
                tempList.append(self.jobsList[i][2])

            return numpy.median(tempList)
        except:
            return 0