# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hhempste/Documents/python/solidus/solidus/SolidusErrorLog.py
# Compiled at: 2017-05-09 17:00:04
import os
strApplicationDirectory = os.path.dirname(os.path.realpath(__file__)) + '/'
SOLIDUS_ERROR_LOG_FILE_NAME = 'SolidusError.log'
SOLIDUS_ERROR_LOG_FILE = strApplicationDirectory + SOLIDUS_ERROR_LOG_FILE_NAME

def openErrorLogFile(strModeIn):
    return open(SOLIDUS_ERROR_LOG_FILE, strModeIn)


def logError(strErrorTextIn, strFunctionNameIn):
    try:
        outFile = openErrorLogFile('a')
        outFile.write(strErrorTextIn + ' occurred in ' + strFunctionNameIn + '\n')
        outFile.close()
    except:
        pass


def logCodeMistakeError(strErrorTextIn, strFunctionNameIn):
    logError('CODE MISTAKE: ' + strErrorTextIn, strFunctionNameIn)