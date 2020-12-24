# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\minixsv\xsvalErrorHandler.py
# Compiled at: 2008-08-08 10:44:52
import string, os
IGNORE_WARNINGS = 0
PRINT_WARNINGS = 1
STOP_ON_WARNINGS = 2

class ErrorHandler:
    __module__ = __name__

    def __init__(self, errorLimit, warningProc, verbose):
        self.errorLimit = errorLimit
        self.warningProc = warningProc
        self.verbose = verbose
        self.errorList = []
        self.noOfErrors = 0
        self.warningList = []
        self.infoDict = {}

    def hasErrors(self):
        return self.errorList != []

    def addError(self, errstr, element=None, endTag=0):
        filePath = ''
        lineNo = 0
        if element:
            filePath = element.getFilePath()
            if endTag:
                lineNo = element.getEndLineNumber()
            else:
                lineNo = element.getStartLineNumber()
        self.errorList.append((filePath, lineNo, 'ERROR', '%s' % errstr))
        self.noOfErrors += 1
        if self.noOfErrors == self.errorLimit:
            self._raiseXsvalException('\nError Limit reached!!')

    def addWarning(self, warnstr, element=None):
        filePath = ''
        lineNo = 0
        if element:
            filePath = element.getFilePath()
            lineNo = element.getStartLineNumber()
        self.warningList.append((filePath, lineNo, 'WARNING', warnstr))

    def addInfo(self, infostr, element=None):
        self.infoDict.setdefault('INFO: %s' % infostr, 1)

    def raiseError(self, errstr, element=None):
        self.addError(errstr, element)
        self._raiseXsvalException()

    def flushOutput(self):
        if self.infoDict != {}:
            print string.join(self.infoDict.keys(), '\n')
            self.infoList = []
        if self.warningProc == PRINT_WARNINGS and self.warningList != []:
            print self._assembleOutputList(self.warningList, sorted=1)
            self.warningList = []
        elif self.warningProc == STOP_ON_WARNINGS:
            self.errorList.extend(self.warningList)
        if self.errorList != []:
            self._raiseXsvalException()

    def _raiseXsvalException(self, additionalInfo=''):
        output = self._assembleOutputList(self.errorList) + additionalInfo
        self.errorList = self.warningList = []
        raise XsvalError(output)

    def _assembleOutputList(self, outputList, sorted=0):
        if sorted:
            outputList.sort()
        outputStrList = []
        for outElement in outputList:
            outputStrList.append(self._assembleOutString(outElement))

        return string.join(outputStrList, '\n')

    def _assembleOutString(self, listElement):
        fileStr = ''
        lineStr = ''
        if listElement[0] != '':
            if self.verbose:
                fileStr = '%s: ' % listElement[0]
            else:
                fileStr = '%s: ' % os.path.basename(listElement[0])
        if listElement[1] != 0:
            lineStr = 'line %d: ' % listElement[1]
        return '%s: %s%s%s' % (listElement[2], fileStr, lineStr, listElement[3])


class XsvalError(StandardError):
    __module__ = __name__