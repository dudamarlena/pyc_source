# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/FunctionCustom.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 5912 bytes
"""
Created on Apr 21, 2011

@author: Mark V Systems Limited
(c) Copyright 2011 Mark V Systems Limited, All rights reserved.
"""
import xml.dom, math, re
from arelle.ModelValue import qname
from arelle import XPathContext, XbrlUtil
from arelle.ModelInstanceObject import ModelDimensionValue
from arelle.PythonUtil import flattenSequence
from decimal import Decimal

class fnFunctionNotAvailable(Exception):

    def __init__(self):
        self.args = ('custom function not available', )

    def __repr__(self):
        return self.args[0]


def call(xc, p, qname, contextItem, args):
    try:
        cfSig = xc.modelXbrl.modelCustomFunctionSignatures[(qname, len(args))]
        if cfSig is not None and cfSig.customFunctionImplementation is not None:
            return callCfi(xc, p, qname, cfSig, contextItem, args)
        else:
            if qname in xc.customFunctions:
                return xc.customFunctions[qname](xc, p, contextItem, args)
            if qname not in customFunctions:
                raise fnFunctionNotAvailable
            return customFunctions[qname](xc, p, contextItem, args)
    except (fnFunctionNotAvailable, KeyError):
        raise XPathContext.FunctionNotAvailable('custom function:{0}'.format(str(qname)))


def callCfi(xc, p, qname, cfSig, contextItem, args):
    if len(args) != len(cfSig.inputTypes):
        raise XPathContext.FunctionNumArgs()
    cfi = cfSig.customFunctionImplementation
    overriddenInScopeVars = {}
    traceSource = xc.formulaOptions.traceSource(xc.traceType)
    traceEvaluation = xc.formulaOptions.traceEvaluation(xc.traceType)
    inputNames = cfi.inputNames
    for i, argName in enumerate(inputNames):
        if argName in xc.inScopeVars:
            overriddenInScopeVars[argName] = xc.inScopeVars[argName]
        xc.inScopeVars[argName] = args[i]

    if traceEvaluation:
        xc.modelXbrl.info('formula:trace', _('%(cfi)s(%(arguments)s)'), modelObject=cfi, cfi=qname, arguments=', '.join('{}={}'.format(argName, args[i]) for i, argName in enumerate(inputNames)))
    for i, step in enumerate(cfi.stepExpressions):
        stepQname, stepExpression = step
        stepProg = cfi.stepProgs[i]
        if traceSource:
            xc.modelXbrl.info('formula:trace', _('%(cfi)s step %(step)s \nExpression: \n%(expression)s'), modelObject=cfi, cfi=qname, step=stepQname, expression=stepExpression)
        result = xc.evaluate(stepProg)
        if traceEvaluation:
            xc.modelXbrl.info('formula:trace', _('%(cfi)s step %(step)s \nResult: \n%(expression)s'), modelObject=cfi, cfi=qname, step=stepQname, expression=result)
        if stepQname in xc.inScopeVars:
            overriddenInScopeVars[stepQname] = xc.inScopeVars[stepQname]
        xc.inScopeVars[stepQname] = result

    if traceSource:
        xc.modelXbrl.info('formula:trace', _('%(cfi)s output \nExpression: \n%(expression)s'), modelObject=cfi, cfi=qname, expression=cfi.outputExpression)
    result = xc.evaluateAtomicValue(cfi.outputProg, cfSig.outputType)
    if traceEvaluation:
        xc.modelXbrl.info('formula:trace', _('%(cfi)s output \nResult: \n%(expression)s'), modelObject=cfi, cfi=qname, expression=result)
    for step in cfi.stepExpressions:
        stepQname = step[0]
        if stepQname in overriddenInScopeVars:
            xc.inScopeVars[stepQname] = overriddenInScopeVars[stepQname]

    for i, argName in enumerate(inputNames):
        if argName in overriddenInScopeVars:
            xc.inScopeVars[argName] = overriddenInScopeVars[argName]
        else:
            del xc.inScopeVars[argName]

    if result is None:
        raise XPathContext.FunctionArgType('output', cfSig.outputType, result)
    return result


def my_fn_PDxEV(xc, p, contextItem, args):
    if len(args) != 2:
        raise XPathContext.FunctionNumArgs()
    PDseq = flattenSequence(args[0])
    EVseq = flattenSequence(args[1])
    dimQname = qname('{http://www.example.com/wgt-avg}ExposuresDimension')
    PDxEV = []
    for pd in PDseq:
        if pd.context is not None:
            pdDim = pd.context.dimValue(dimQname)
            for ev in EVseq:
                if ev.context is not None:
                    evDim = ev.context.dimValue(dimQname)
                    if pdDim is not None and isinstance(pdDim, ModelDimensionValue):
                        dimEqual = pdDim.isEqualTo(evDim, equalMode=XbrlUtil.S_EQUAL2)
                else:
                    if evDim is not None and isinstance(evDim, ModelDimensionValue):
                        dimEqual = evDim.isEqualTo(pdDim, equalMode=XbrlUtil.S_EQUAL2)
                    else:
                        dimEqual = pdDim == evDim
                if dimEqual:
                    pdX = pd.xValue
                    evX = ev.xValue
                    if isinstance(pdX, Decimal) and isinstance(evX, float):
                        pdX = float(pdX)
                    else:
                        if isinstance(evX, Decimal) and isinstance(pdX, float):
                            pdX = float(evX)
                        PDxEV.append(pdX * evX)
                        break

    return PDxEV


customFunctions = {qname('{http://www.example.com/wgt-avg/function}my-fn:PDxEV'): my_fn_PDxEV}