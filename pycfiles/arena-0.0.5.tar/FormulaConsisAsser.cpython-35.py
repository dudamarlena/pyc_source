# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/FormulaConsisAsser.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 7033 bytes
__doc__ = '\nCreated on Jan 9, 2011\n\n@author: Mark V Systems Limited\n(c) Copyright 2011 Mark V Systems Limited, All rights reserved.\n'
from arelle import XbrlConst
from arelle.XbrlUtil import xEqual, S_EQUAL2
from arelle.ValidateXbrlCalcs import inferredPrecision, roundValue
from math import fabs

def evaluate(xpCtx, varSet, derivedFact):
    for consisAsserRel in xpCtx.modelXbrl.relationshipSet(XbrlConst.consistencyAssertionFormula).toModelObject(varSet):
        consisAsser = consisAsserRel.fromModelObject
        hasProportionalAcceptanceRadius = consisAsser.hasProportionalAcceptanceRadius
        hasAbsoluteAcceptanceRadius = consisAsser.hasAbsoluteAcceptanceRadius
        if derivedFact is None:
            pass
        else:
            isNumeric = derivedFact.isNumeric
            if isNumeric and not derivedFact.isNil:
                pass
            derivedFactInferredPrecision = inferredPrecision(derivedFact)
            if derivedFactInferredPrecision == 0 and not hasProportionalAcceptanceRadius and not hasAbsoluteAcceptanceRadius:
                if xpCtx.formulaOptions.traceVariableSetExpressionResult:
                    xpCtx.modelXbrl.info('formula:trace', _('Consistency assertion %(id)s formula %(xlinkLabel)s fact %(derivedFact)s has zero precision and no radius is defined, skipping consistency assertion'), modelObject=consisAsser, id=consisAsser.id, xlinkLabel=varSet.xlinkLabel, derivedFact=derivedFact)
                continue
                aspectMatchedInputFacts = []
                isStrict = consisAsser.isStrict
                for inputFact in xpCtx.modelXbrl.facts:
                    if not inputFact.isNil and inputFact.qname == derivedFact.qname and inputFact.context.isEqualTo(derivedFact.context, dimensionalAspectModel=varSet.aspectModel == 'dimensional') and (not isNumeric or inputFact.unit.isEqualTo(derivedFact.unit)):
                        aspectMatchedInputFacts.append(inputFact)

        if len(aspectMatchedInputFacts) == 0:
            if isStrict:
                if derivedFact.isNil:
                    isSatisfied = True
                else:
                    isSatisfied = False
        else:
            if xpCtx.formulaOptions.traceVariableSetExpressionResult:
                xpCtx.modelXbrl.info('formula:trace', _('Consistency assertion %(id)s formula %(xlinkLabel)s no input facts matched to %(derivedFact)s, skipping consistency assertion'), modelObject=consisAsser, id=consisAsser.id, xlinkLabel=varSet.xlinkLabel, derivedFact=derivedFact)
                continue
            else:
                if derivedFact.isNil:
                    isSatisfied = False
                else:
                    isSatisfied = True
            paramQnamesAdded = []
            for paramRel in consisAsser.orderedVariableRelationships:
                paramQname = paramRel.variableQname
                paramVar = paramRel.toModelObject
                paramValue = xpCtx.inScopeVars.get(paramVar.parameterQname)
                paramAlreadyInVars = paramQname in xpCtx.inScopeVars
                if not paramAlreadyInVars:
                    paramQnamesAdded.append(paramQname)
                    xpCtx.inScopeVars[paramQname] = paramValue

            acceptance = None
            for fact in aspectMatchedInputFacts:
                if isSatisfied != True:
                    break
                if fact.isNil:
                    if not derivedFact.isNil:
                        isSatisfied = False
                else:
                    if isNumeric:
                        factInferredPrecision = inferredPrecision(fact)
                        if factInferredPrecision == 0 and not hasProportionalAcceptanceRadius and not hasAbsoluteAcceptanceRadius and xpCtx.formulaOptions.traceVariableSetExpressionResult:
                            xpCtx.modelXbrl.info('formula:trace', _('Consistency assertion %(id)s formula %(xlinkLabel)s input fact matched to %(derivedFact)s has zero precision and no radius, skipping consistency assertion'), modelObject=consisAsser, id=consisAsser.id, xlinkLabel=varSet.xlinkLabel, derivedFact=derivedFact)
                            isSatisfied = None
                            break
                        if hasProportionalAcceptanceRadius or hasAbsoluteAcceptanceRadius:
                            acceptance = consisAsser.evalRadius(xpCtx, derivedFact.vEqValue)
                            if acceptance is not None:
                                if hasProportionalAcceptanceRadius:
                                    acceptance *= derivedFact.vEqValue
                                isSatisfied = fabs(derivedFact.vEqValue - fact.vEqValue) <= fabs(acceptance)
                            else:
                                isSatisfied = None
                        else:
                            p = min(derivedFactInferredPrecision, factInferredPrecision)
                            if p == 0 or roundValue(derivedFact.value, precision=p) != roundValue(fact.value, precision=p):
                                isSatisfied = False
                    elif not xEqual(fact, derivedFact, equalMode=S_EQUAL2):
                        isSatisfied = False

            if isSatisfied is not None:
                if xpCtx.formulaOptions.traceVariableSetExpressionResult:
                    xpCtx.modelXbrl.info('formula:trace', _('Consistency assertion %(id)s result %(result)s'), modelObject=consisAsser, id=consisAsser.id, result=isSatisfied)
                message = consisAsser.message(isSatisfied)
                if message is not None:
                    xpCtx.inScopeVars[XbrlConst.qnCaAspectMatchedFacts] = aspectMatchedInputFacts
                    xpCtx.inScopeVars[XbrlConst.qnCaAcceptanceRadius] = acceptance
                    xpCtx.inScopeVars[XbrlConst.qnCaAbsoluteAcceptanceRadiusExpression] = consisAsser.get('absoluteAcceptanceRadius')
                    xpCtx.inScopeVars[XbrlConst.qnCaProportionalAcceptanceRadiusExpression] = consisAsser.get('proportionalAcceptanceRadius')
                    xpCtx.modelXbrl.info('message:' + consisAsser.id, message.evaluate(xpCtx), modelObject=message, messageCodes='message:{variableSetID|xlinkLabel}')
                    xpCtx.inScopeVars.pop(XbrlConst.qnCaAspectMatchedFacts)
                    xpCtx.inScopeVars.pop(XbrlConst.qnCaAcceptanceRadius)
                    xpCtx.inScopeVars.pop(XbrlConst.qnCaAbsoluteAcceptanceRadiusExpression)
                    xpCtx.inScopeVars.pop(XbrlConst.qnCaProportionalAcceptanceRadiusExpression)
                if isSatisfied:
                    consisAsser.countSatisfied += 1
                else:
                    consisAsser.countNotSatisfied += 1
                for paramQname in paramQnamesAdded:
                    xpCtx.inScopeVars.pop(paramQname)