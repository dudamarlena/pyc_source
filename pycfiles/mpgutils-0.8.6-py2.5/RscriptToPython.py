# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/mpgutils/RUtils/RscriptToPython.py
# Compiled at: 2009-08-18 16:54:35
"""usage: %prog [options] <input file>

Load an R library, and pass in options from the command line to that library

This is an adapter that should be used by python clients to R code.

"""
import sys, optparse, mpgutils.utils, os, subprocess

def callRscript(lstLibraries, methodName, dctArguments, captureOutput=False, bVerbose=True):
    strCall = generateCall(lstLibraries, methodName, dctArguments)
    if bVerbose:
        print 'Calling:  ' + strCall
    if captureOutput:
        output = subprocess.Popen(strCall, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        return output
    else:
        subprocess.Popen(strCall, shell=True).wait()


def generateCall(lstLibraries, methodName, dctArguments):
    strCommand = 'Rscript'
    for library in lstLibraries:
        libCommand = "-e 'library(" + library + ")'"
        strCommand = strCommand + ' ' + libCommand

    methodCommand = "-e '" + methodName + '('
    argNames = dctArguments.keys()
    argValues = dctArguments.values()
    for i in range(len(argNames)):
        methodCommand = methodCommand + argNames[i] + '='
        value = encodeValue(argValues[i])
        methodCommand = methodCommand + value
        if i != len(argNames) - 1:
            methodCommand = methodCommand + ','

    methodCommand = methodCommand + ")'"
    strCommand = strCommand + ' ' + methodCommand
    return strCommand


def encodeValue(value):
    if value == None:
        return 'NULL'
    if isinstance(value, bool):
        if value == True:
            return 'T'
        if value == False:
            return 'F'
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return str(value)
    if isinstance(value, str):
        return '"' + value + '"'
    return value