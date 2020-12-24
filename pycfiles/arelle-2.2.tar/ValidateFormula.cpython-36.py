# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\ProgramData\lib\site-packages\arelle\ValidateFormula.py
# Compiled at: 2018-02-26 09:10:06
# Size of source mod 2**32: 90363 bytes
"""
Created on Dec 9, 2010

@author: Mark V Systems Limited
(c) Copyright 2010 Mark V Systems Limited, All rights reserved.
"""
import os, sys, time, logging
from collections import defaultdict
from threading import Timer
from arelle.ModelFormulaObject import ModelParameter, ModelInstance, ModelVariableSet, ModelFormula, ModelTuple, ModelVariable, ModelFactVariable, ModelVariableSetAssertion, ModelConsistencyAssertion, ModelExistenceAssertion, ModelValueAssertion, ModelAssertionSeverity, ModelPrecondition, ModelConceptName, Trace, Aspect, aspectModels, ModelAspectCover, ModelMessage
from arelle.ModelRenderingObject import ModelRuleDefinitionNode, ModelRelationshipDefinitionNode, ModelFilterDefinitionNode
from arelle.ModelObject import ModelObject
from arelle.ModelValue import qname, QName
from arelle import XbrlConst, XmlUtil, ModelXbrl, ModelDocument, XPathParser, XPathContext, FunctionXs, ValidateXbrlDimensions

class FormulaValidationException(Exception):

    def __init__(self):
        self.args = (
         self.__repr__(),)

    def __repr__(self):
        return _('Formula has validation error')


arcroleChecks = {XbrlConst.equalityDefinition: (None,
                                XbrlConst.qnEqualityDefinition,
                                'xbrlve:info'), 
 
 XbrlConst.assertionSet: (XbrlConst.qnAssertionSet,
                          (
                           XbrlConst.qnAssertion, XbrlConst.qnVariableSetAssertion),
                          'xbrlvalide:info'), 
 
 XbrlConst.assertionUnsatisfiedSeverity: (
                                          (
                                           XbrlConst.qnAssertion, XbrlConst.qnVariableSetAssertion),
                                          (
                                           XbrlConst.qnAssertionSeverityError, XbrlConst.qnAssertionSeverityWarning, XbrlConst.qnAssertionSeverityOk),
                                          'seve:assertionSeveritySourceError',
                                          'seve:assertionSeverityTargetError'), 
 
 XbrlConst.variableSet: (XbrlConst.qnVariableSet,
                         (
                          XbrlConst.qnVariableVariable, XbrlConst.qnParameter),
                         'xbrlve:info'), 
 
 XbrlConst.variableSetFilter: (XbrlConst.qnVariableSet,
                               XbrlConst.qnVariableFilter,
                               'xbrlve:info'), 
 
 XbrlConst.variableFilter: (XbrlConst.qnFactVariable,
                            XbrlConst.qnVariableFilter,
                            'xbrlve:info'), 
 
 XbrlConst.booleanFilter: (XbrlConst.qnVariableFilter,
                           XbrlConst.qnVariableFilter,
                           'xbrlbfe:info'), 
 
 XbrlConst.consistencyAssertionFormula: (XbrlConst.qnConsistencyAssertion,
                                         None,
                                         'xbrlca:info'), 
 
 XbrlConst.functionImplementation: (XbrlConst.qnCustomFunctionSignature,
                                    XbrlConst.qnCustomFunctionImplementation,
                                    'xbrlcfie:info'), 
 
 XbrlConst.tableBreakdown: (XbrlConst.qnTableTable,
                            XbrlConst.qnTableBreakdown,
                            'xbrlte:tableBreakdownSourceError',
                            'xbrlte:tableBreakdownTargetError'), 
 
 XbrlConst.tableBreakdownTree: (XbrlConst.qnTableBreakdown,
                                (
                                 XbrlConst.qnTableClosedDefinitionNode,
                                 XbrlConst.qnTableAspectNode),
                                'xbrlte:breakdownTreeSourceError',
                                'xbrlte:breakdownTreeTargetError'), 
 
 XbrlConst.tableDefinitionNodeSubtree: (XbrlConst.qnTableDefinitionNode,
                                        XbrlConst.qnTableDefinitionNode,
                                        'xbrlte:definitionNodeSubtreeSourceError',
                                        'xbrlte:definitionNodeSubtreeTargetError',
                                        (
                                         XbrlConst.qnTableConceptRelationshipNode,
                                         XbrlConst.qnTableDimensionRelationshipNode),
                                        None,
                                        'xbrlte:prohibitedDefinitionNodeSubtreeSourceError',
                                        None), 
 
 XbrlConst.tableFilter: (XbrlConst.qnTableTable,
                         XbrlConst.qnVariableFilter,
                         'xbrlte:tableFilterSourceError',
                         'xbrlte:tableFilterTargetError'), 
 
 XbrlConst.tableParameter: (XbrlConst.qnTableTable,
                            XbrlConst.qnParameter,
                            'xbrlte:tableParameterSourceError',
                            'xbrlte:tableParameterTargetError'), 
 
 XbrlConst.tableAspectNodeFilter: (XbrlConst.qnTableAspectNode,
                                   XbrlConst.qnVariableFilter,
                                   'xbrlte:aspectNodeFilterSourceError',
                                   'xbrlte:aspectNodeFilterTargetError'), 
 
 XbrlConst.tableBreakdownMMDD: (XbrlConst.qnTableTableMMDD,
                                XbrlConst.qnTableBreakdownMMDD,
                                'xbrlte:tableBreakdownSourceError',
                                'xbrlte:tableBreakdownTargetError'), 
 
 XbrlConst.tableBreakdownTreeMMDD: (XbrlConst.qnTableBreakdownMMDD,
                                    (
                                     XbrlConst.qnTableClosedDefinitionNodeMMDD,
                                     XbrlConst.qnTableAspectNodeMMDD),
                                    'xbrlte:breakdownTreeSourceError',
                                    'xbrlte:breakdownTreeTargetError'), 
 
 XbrlConst.tableDefinitionNodeSubtreeMMDD: (XbrlConst.qnTableDefinitionNodeMMDD,
                                            XbrlConst.qnTableDefinitionNodeMMDD,
                                            'xbrlte:definitionNodeSubtreeSourceError',
                                            'xbrlte:definitionNodeSubtreeTargetError',
                                            (
                                             XbrlConst.qnTableConceptRelationshipNodeMMDD,
                                             XbrlConst.qnTableDimensionRelationshipNodeMMDD),
                                            None,
                                            'xbrlte:prohibitedDefinitionNodeSubtreeSourceError',
                                            None), 
 
 XbrlConst.tableFilterMMDD: (XbrlConst.qnTableTableMMDD,
                             XbrlConst.qnVariableFilter,
                             'xbrlte:tableFilterSourceError',
                             'xbrlte:tableFilterTargetError'), 
 
 XbrlConst.tableParameterMMDD: (XbrlConst.qnTableTableMMDD,
                                XbrlConst.qnParameter,
                                'xbrlte:tableParameterSourceError',
                                'xbrlte:tableParameterTargetError'), 
 
 XbrlConst.tableAspectNodeFilterMMDD: (XbrlConst.qnTableAspectNodeMMDD,
                                       XbrlConst.qnVariableFilter,
                                       'xbrlte:aspectNodeFilterSourceError',
                                       'xbrlte:aspectNodeFilterTargetError'), 
 
 XbrlConst.tableBreakdown201305: (XbrlConst.qnTableTable201305,
                                  XbrlConst.qnTableBreakdown201305,
                                  'xbrlte:info'), 
 
 XbrlConst.tableBreakdownTree201305: (XbrlConst.qnTableBreakdown201305,
                                      (
                                       XbrlConst.qnTableClosedDefinitionNode201305,
                                       XbrlConst.qnTableAspectNode201305),
                                      'xbrlte:info'), 
 
 XbrlConst.tableDefinitionNodeSubtree201305: (XbrlConst.qnTableClosedDefinitionNode201305,
                                              XbrlConst.qnTableClosedDefinitionNode201305,
                                              'xbrlte:info'), 
 
 XbrlConst.tableFilter201305: (XbrlConst.qnTableTable201305,
                               XbrlConst.qnVariableFilter,
                               'xbrlte:info'), 
 
 XbrlConst.tableAspectNodeFilter201305: (XbrlConst.qnTableAspectNode201305,
                                         XbrlConst.qnVariableFilter,
                                         'xbrlte:info'), 
 
 XbrlConst.tableBreakdown201301: (XbrlConst.qnTableTable201301,
                                  (
                                   XbrlConst.qnTableClosedDefinitionNode201301,
                                   XbrlConst.qnTableFilterNode201301,
                                   XbrlConst.qnTableSelectionNode201301,
                                   XbrlConst.qnTableTupleNode201301),
                                  'xbrlte:info'), 
 
 XbrlConst.tableAxis2011: (XbrlConst.qnTableTable2011,
                           (
                            XbrlConst.qnTablePredefinedAxis2011,
                            XbrlConst.qnTableFilterAxis2011,
                            XbrlConst.qnTableSelectionAxis2011,
                            XbrlConst.qnTableTupleAxis2011),
                           'xbrlte:info'), 
 
 XbrlConst.tableFilter201301: (XbrlConst.qnTableTable201301,
                               XbrlConst.qnVariableFilter,
                               'xbrlte:info'), 
 
 XbrlConst.tableFilter2011: (XbrlConst.qnTableTable2011,
                             XbrlConst.qnVariableFilter,
                             'xbrlte:info'), 
 
 XbrlConst.tableDefinitionNodeSubtree201301: (XbrlConst.qnTableClosedDefinitionNode201301,
                                              XbrlConst.qnTableClosedDefinitionNode201301,
                                              'xbrlte:info'), 
 
 XbrlConst.tableAxisSubtree2011: (XbrlConst.qnTablePredefinedAxis2011,
                                  XbrlConst.qnTablePredefinedAxis2011,
                                  'xbrlte:info'), 
 
 XbrlConst.tableFilterNodeFilter2011: (XbrlConst.qnTableFilterNode201301,
                                       XbrlConst.qnVariableFilter,
                                       'xbrlte:info'), 
 
 XbrlConst.tableAxisFilter2011: (XbrlConst.qnTableFilterAxis2011,
                                 XbrlConst.qnVariableFilter,
                                 'xbrlte:info'), 
 
 XbrlConst.tableAxisFilter201205: (XbrlConst.qnTableFilterAxis2011,
                                   XbrlConst.qnVariableFilter,
                                   'xbrlte:info'), 
 
 XbrlConst.tableTupleContent201301: (
                                     (XbrlConst.qnTableTupleNode201301,
                                      XbrlConst.qnTableTupleAxis2011),
                                     (
                                      XbrlConst.qnTableRuleNode201301,
                                      XbrlConst.qnTableRuleAxis2011),
                                     'xbrlte:info')}

def checkBaseSet(val, arcrole, ELR, relsSet):
    if arcrole in arcroleChecks:
        arcroleCheck = arcroleChecks[arcrole]
        notFromQname = notToQname = notFromErrCode = notToErrCode = None
        if len(arcroleCheck) == 3:
            fromQname, toQname, fromErrCode = arcroleCheck
            toErrCode = fromErrCode
        else:
            if len(arcroleCheck) == 4:
                fromQname, toQname, fromErrCode, toErrCode = arcroleCheck
            else:
                if len(arcroleCheck) == 8:
                    fromQname, toQname, fromErrCode, toErrCode, notFromQname, notToQname, notFromErrCode, notToErrCode = arcroleCheck
                else:
                    raise Exception('Invalid arcroleCheck ' + str(arcroleCheck))
        level = 'INFO' if fromErrCode.endswith(':info') else 'ERROR'
        for modelRel in relsSet.modelRelationships:
            fromMdlObj = modelRel.fromModelObject
            toMdlObj = modelRel.toModelObject
            if fromQname:
                if fromMdlObj is None or not val.modelXbrl.isInSubstitutionGroup(fromMdlObj.elementQname, fromQname) and fromMdlObj.elementQname.namespaceURI in val.modelXbrl.namespaceDocs:
                    val.modelXbrl.log(level, fromErrCode, (_('Relationship from %(xlinkFrom)s to %(xlinkTo)s should have an %(element)s source')),
                      modelObject=modelRel,
                      xlinkFrom=(modelRel.fromLabel),
                      xlinkTo=(modelRel.toLabel),
                      element=fromQname)
                else:
                    if notFromQname:
                        if val.modelXbrl.isInSubstitutionGroup(fromMdlObj.elementQname, notFromQname):
                            val.modelXbrl.log(level, notFromErrCode, (_('Relationship from %(xlinkFrom)s to %(xlinkTo)s should not have an %(element)s source')),
                              modelObject=modelRel,
                              xlinkFrom=(modelRel.fromLabel),
                              xlinkTo=(modelRel.toLabel),
                              element=fromQname)
                if toQname:
                    if toMdlObj is None or not val.modelXbrl.isInSubstitutionGroup(toMdlObj.elementQname, toQname) and toMdlObj.elementQname.namespaceURI in val.modelXbrl.namespaceDocs:
                        val.modelXbrl.log(level, toErrCode, (_('Relationship from %(xlinkFrom)s to %(xlinkTo)s should have an %(element)s target')),
                          modelObject=modelRel,
                          xlinkFrom=(modelRel.fromLabel),
                          xlinkTo=(modelRel.toLabel),
                          element=toQname)
                    elif notToQname and val.modelXbrl.isInSubstitutionGroup(fromMdlObj.elementQname, notToQname):
                        val.modelXbrl.log(level, notFromErrCode, (_('Relationship from %(xlinkFrom)s to %(xlinkTo)s should not have an %(element)s target')),
                          modelObject=modelRel,
                          xlinkFrom=(modelRel.fromLabel),
                          xlinkTo=(modelRel.toLabel),
                          element=fromQname)

    if arcrole == XbrlConst.functionImplementation:
        for relFrom, rels in relsSet.fromModelObjects().items():
            if len(rels) > 1:
                val.modelXbrl.error('xbrlcfie:tooManyCFIRelationships', (_('Function-implementation relationship from signature %(name)s has more than one implementation target')),
                  modelObject=([
                 relFrom] + rels),
                  name=(relFrom.name))

        for relTo, rels in relsSet.toModelObjects().items():
            if len(rels) > 1:
                val.modelXbrl.error('xbrlcfie:tooManyCFIRelationships', (_('Function implementation %(xlinkLabel)s must be the target of only one function-implementation relationship')),
                  modelObject=([
                 relTo] + rels),
                  xlinkLabel=(relTo.xlinkLabel))

    elif arcrole == XbrlConst.assertionUnsatisfiedSeverity:
        for relFrom, rels in relsSet.fromModelObjects().items():
            if len(rels) > 1:
                val.modelXbrl.error('seve:multipleSeveritiesForAssertionError', (_('Assertion-unsatisfied-severity relationship from %(xlinkLabel)s has more than one severity target')),
                  modelObject=([
                 relFrom] + rels),
                  xlinkLabel=(relFrom.xlinkLabel))

        for relTo, rels in relsSet.toModelObjects().items():
            if relTo.modelDocument.basename != 'severities.xml' or relTo.getparent().qname != XbrlConst.qnGenLink or relTo.getparent().getparent().qname != XbrlConst.qnLinkLinkbase:
                val.modelXbrl.error('seve:assertionSeverityTargetError', (_('Target of assertion-unsatisfied-severity relationship must be a severity element in the published severities linkbase.')),
                  modelObject=([
                 relTo] + rels))


def executeCallTest(val, name, callTuple, testTuple):
    if callTuple:
        XPathParser.initializeParser(val.modelXbrl.modelManager)
        try:
            val.modelXbrl.modelManager.showStatus(_('Executing call'))
            callExprStack = XPathParser.parse(val, callTuple[0], callTuple[1], name + ' call', Trace.CALL)
            xpathContext = XPathContext.create((val.modelXbrl), sourceElement=(callTuple[1]))
            result = xpathContext.evaluate(callExprStack)
            xpathContext.inScopeVars[qname('result', noPrefixIsNoNamespace=True)] = result
            val.modelXbrl.info('formula:trace', (_('%(name)s result %(result)s')),
              modelObject=(callTuple[1]),
              name=name,
              result=(str(result)))
            if testTuple:
                val.modelXbrl.modelManager.showStatus(_('Executing test'))
                testExprStack = XPathParser.parse(val, testTuple[0], testTuple[1], name + ' test', Trace.CALL)
                testResult = xpathContext.effectiveBooleanValue(None, xpathContext.evaluate(testExprStack))
                if testResult:
                    val.modelXbrl.info('cfcn:testPass', (_('Test %(name)s result %(result)s')),
                      modelObject=(testTuple[1]),
                      name=name,
                      result=(str(testResult)))
                else:
                    val.modelXbrl.error('cfcn:testFail', (_('Test %(name)s result %(result)s')),
                      modelObject=(testTuple[1]),
                      name=name,
                      result=(str(testResult)))
            xpathContext.close()
        except XPathContext.XPathException as err:
            val.modelXbrl.error((err.code), (_('%(name)s evaluation error: %(error)s \n%(errorSource)s')),
              modelObject=(callTuple[1]),
              name=name,
              error=(err.message),
              errorSource=(err.sourceErrorIndication))

        val.modelXbrl.modelManager.showStatus(_('ready'), 2000)


def validate(val, xpathContext=None, parametersOnly=False, statusMsg='', compileOnly=False):
    for e in ('xbrl.5.1.4.3:cycles', 'xbrlgene:violatedCyclesConstraint'):
        if e in val.modelXbrl.errors:
            val.modelXbrl.info('info', (_('Formula validation skipped due to %(error)s error')), modelObject=(val.modelXbrl),
              error=e)
            return

    val.modelXbrl.profileStat()
    formulaOptions = val.modelXbrl.modelManager.formulaOptions
    if XPathParser.initializeParser(val.modelXbrl.modelManager):
        val.modelXbrl.profileStat(_('initializeXPath2Grammar'))
    val.modelXbrl.modelManager.showStatus(statusMsg)
    val.modelXbrl.profileActivity()
    initialErrorCount = val.modelXbrl.logCount.get(logging._checkLevel('ERROR'), 0)
    parameterQnames = set()
    instanceQnames = set()
    parameterDependencies = {}
    instanceDependencies = defaultdict(set)
    dependencyResolvedParameters = set()
    orderedParameters = []
    orderedInstances = []
    for paramQname, modelParameter in val.modelXbrl.qnameParameters.items():
        if isinstance(modelParameter, ModelParameter):
            modelParameter.compile()
            parameterDependencies[paramQname] = modelParameter.variableRefs()
            parameterQnames.add(paramQname)
            if isinstance(modelParameter, ModelInstance):
                instanceQnames.add(paramQname)

    resolvedAParameter = True
    while resolvedAParameter:
        resolvedAParameter = False
        for paramQname in parameterQnames:
            if paramQname not in dependencyResolvedParameters and len(parameterDependencies[paramQname] - dependencyResolvedParameters) == 0:
                dependencyResolvedParameters.add(paramQname)
                orderedParameters.append(paramQname)
                resolvedAParameter = True

    for paramQname in parameterQnames:
        if paramQname not in dependencyResolvedParameters:
            circularOrUndefDependencies = parameterDependencies[paramQname] - dependencyResolvedParameters
            undefinedVars = circularOrUndefDependencies - parameterQnames
            paramsCircularDep = circularOrUndefDependencies - undefinedVars
            if len(undefinedVars) > 0:
                val.modelXbrl.error('xbrlve:unresolvedDependency', (_('Undefined dependencies in parameter %(name)s, to names %(dependencies)s')),
                  modelObject=(val.modelXbrl.qnameParameters[paramQname]),
                  name=paramQname,
                  dependencies=(', '.join(str(v) for v in undefinedVars)))
            if len(paramsCircularDep) > 0:
                val.modelXbrl.error('xbrlve:parameterCyclicDependencies', (_('Cyclic dependencies in parameter %(name)s, to names %(dependencies)s')),
                  modelObject=(val.modelXbrl.qnameParameters[paramQname]),
                  name=paramQname,
                  dependencies=(', '.join(str(d) for d in paramsCircularDep)))

    val.modelXbrl.profileActivity('... formula parameter checks', minTimeToShow=1.0)
    for custFnSig in val.modelXbrl.modelCustomFunctionSignatures.values():
        if custFnSig is not None:
            custFnQname = custFnSig.functionQname
            if custFnQname.namespaceURI == XbrlConst.xfi:
                val.modelXbrl.error('xbrlve:noProhibitedNamespaceForCustomFunction', (_('Custom function %(name)s has namespace reserved for functions in the function registry %(namespace)s')),
                  modelObject=custFnSig,
                  name=custFnQname,
                  namespace=(custFnQname.namespaceURI))
            _outputType = custFnSig.outputType
            if _outputType:
                if _outputType.namespaceURI == XbrlConst.xsd:
                    if not FunctionXs.isXsType(_outputType.localName):
                        val.modelXbrl.error('xbrlve:invalidDatatypeInCustomFunctionSignature', (_('Custom Function Signature %(name)s output type %(type)s is not valid')),
                          modelObject=custFnSig,
                          name=custFnQname,
                          type=_outputType)
            for _inputType in custFnSig.inputTypes:
                if _inputType and _inputType.namespaceURI == XbrlConst.xsd and not FunctionXs.isXsType(_inputType.localName):
                    val.modelXbrl.error('xbrlve:invalidDatatypeInCustomFunctionSignature', (_('Custom Function Signature %(name)s input type %(type)s is not valid')),
                      modelObject=custFnSig,
                      name=custFnQname,
                      type=_inputType)

            for modelRel in val.modelXbrl.relationshipSet(XbrlConst.functionImplementation).fromModelObject(custFnSig):
                custFnImpl = modelRel.toModelObject
                custFnSig.customFunctionImplementation = custFnImpl
                if len(custFnImpl.inputNames) != len(custFnSig.inputTypes):
                    val.modelXbrl.error('xbrlcfie:inputMismatch', (_('Custom function %(name)s signature has %(parameterCountSignature)s parameters but implementation has %(parameterCountImplementation)s, must be matching')),
                      modelObject=custFnSig,
                      name=custFnQname,
                      parameterCountSignature=(len(custFnSig.inputTypes)),
                      parameterCountImplementation=(len(custFnImpl.inputNames)))

    for custFnImpl in val.modelXbrl.modelCustomFunctionImplementations:
        if not val.modelXbrl.relationshipSet(XbrlConst.functionImplementation).toModelObject(custFnImpl):
            val.modelXbrl.error('xbrlcfie:missingCFIRelationship', (_('Custom function implementation %(xlinkLabel)s has no relationship from any custom function signature')),
              modelObject=custFnSig,
              xlinkLabel=(custFnImpl.xlinkLabel))
        custFnImpl.compile()

    val.modelXbrl.profileActivity('... custom function checks and compilation', minTimeToShow=1.0)
    if xpathContext is None:
        xpathContext = XPathContext.create(val.modelXbrl)
    xpathContext.parameterQnames = parameterQnames
    for paramQname in orderedParameters:
        modelParameter = val.modelXbrl.qnameParameters[paramQname]
        if not isinstance(modelParameter, ModelInstance):
            asType = modelParameter.asType
            if asType:
                if asType.namespaceURI == XbrlConst.xsd:
                    if not FunctionXs.isXsType(asType.localName):
                        val.modelXbrl.error('xbrlve:parameterTypeMismatch', (_('Parameter %(name)s type %(type)s is not valid')),
                          modelObject=modelParameter,
                          name=paramQname,
                          type=asType)
            asLocalName = asType.localName if asType else 'string'
            try:
                if val.parameters:
                    if paramQname in val.parameters:
                        paramDataType, paramValue = val.parameters[paramQname]
                        if isinstance(paramDataType, str):
                            if paramDataType.startswith('xs:'):
                                typeLocalName = paramDataType[3:]
                            else:
                                if ':' in paramDataType:
                                    paramDataType = qname(paramDataType, val.modelXbrl.prefixedNamespaces)
                                    typeLocalName = paramDataType.localName
                        else:
                            if isinstance(paramDataType, QName):
                                typeLocalName = paramDataType.localName
                            else:
                                typeLocalName = 'string'
                        value = FunctionXs.call(xpathContext, None, typeLocalName, [paramValue])
                        result = FunctionXs.call(xpathContext, None, asLocalName, [value])
                        if formulaOptions.traceParameterInputValue:
                            val.modelXbrl.info('formula:trace', (_('Parameter %(name)s input value %(input)s')),
                              modelObject=modelParameter,
                              name=paramQname,
                              input=result)
                        xpathContext.inScopeVars[paramQname] = result
                    else:
                        if modelParameter.isRequired:
                            val.modelXbrl.error('xbrlve:missingParameterValue', (_('Parameter %(name)s is required but not input')),
                              modelObject=modelParameter,
                              name=paramQname)
                        else:
                            modelParameter.selectProg or val.modelXbrl.error('xbrlve:missingParameterValue', (_('Parameter %(name)s does not have a select attribute')),
                              modelObject=modelParameter,
                              name=paramQname)
                else:
                    result = modelParameter.evaluate(xpathContext, asType)
                    if formulaOptions.traceParameterExpressionResult:
                        val.modelXbrl.info('formula:trace', (_('Parameter %(name)s select result %(result)s')),
                          modelObject=modelParameter,
                          name=paramQname,
                          result=result)
                    xpathContext.inScopeVars[paramQname] = result
            except XPathContext.XPathException as err:
                val.modelXbrl.error(('xbrlve:parameterTypeMismatch' if err.code == 'err:FORG0001' else err.code), (_('Parameter \n%(name)s \nException: \n%(error)s')),
                  modelObject=modelParameter,
                  name=paramQname,
                  error=(err.message),
                  messageCodes=('xbrlve:parameterTypeMismatch', 'err:FORG0001'))

    val.modelXbrl.profileActivity('... parameter checks and select evaluation', minTimeToShow=1.0)
    val.modelXbrl.profileStat(_('parametersProcessing'))
    val.modelXbrl.modelFormulaEqualityDefinitions = {}
    for modelRel in val.modelXbrl.relationshipSet(XbrlConst.equalityDefinition).modelRelationships:
        typedDomainElt = modelRel.fromModelObject
        modelEqualityDefinition = modelRel.toModelObject
        if typedDomainElt in val.modelXbrl.modelFormulaEqualityDefinitions:
            val.modelXbrl.error('xbrlve:multipleTypedDimensionEqualityDefinitions', (_('Multiple typed domain definitions from %(typedDomain)s to %(equalityDefinition1)s and %(equalityDefinition2)s')),
              modelObject=(modelRel.arcElement),
              typedDomain=(typedDomainElt.qname),
              equalityDefinition1=(modelEqualityDefinition.xlinkLabel),
              equalityDefinition2=(val.modelXbrl.modelFormulaEqualityDefinitions[typedDomainElt].xlinkLabel))
        else:
            modelEqualityDefinition.compile()
            val.modelXbrl.modelFormulaEqualityDefinitions[typedDomainElt] = modelEqualityDefinition

    if parametersOnly:
        return
    for modelVariableSet in val.modelXbrl.modelVariableSets:
        modelVariableSet.compile()

    val.modelXbrl.profileStat(_('formulaCompilation'))
    produceOutputXbrlInstance = False
    instanceProducingVariableSets = defaultdict(list)
    for modelVariableSet in val.modelXbrl.modelVariableSets:
        varSetInstanceDependencies = set()
        if isinstance(modelVariableSet, ModelFormula):
            instanceQname = None
            for modelRel in val.modelXbrl.relationshipSet(XbrlConst.formulaInstance).fromModelObject(modelVariableSet):
                instance = modelRel.toModelObject
                if isinstance(instance, ModelInstance):
                    if instanceQname is None:
                        instanceQname = instance.instanceQname
                        modelVariableSet.fromInstanceQnames = {instanceQname}
                    else:
                        val.modelXbrl.info('arelle:multipleOutputInstances', (_('Multiple output instances for formula %(xlinkLabel)s, to names %(instanceTo)s, %(instanceTo2)s')),
                          modelObject=modelVariableSet,
                          xlinkLabel=(modelVariableSet.xlinkLabel),
                          instanceTo=instanceQname,
                          instanceTo2=(instance.instanceQname))

            if instanceQname is None:
                instanceQname = XbrlConst.qnStandardOutputInstance
                instanceQnames.add(instanceQname)
                modelVariableSet.fromInstanceQnames = None
            modelVariableSet.outputInstanceQname = instanceQname
            if getattr(val, 'validateSBRNL', False):
                val.modelXbrl.error('SBR.NL.2.3.9.03', (_('Formula:formula %(xlinkLabel)s is not allowed')),
                  modelObject=modelVariableSet,
                  xlinkLabel=(modelVariableSet.xlinkLabel))
        else:
            instanceQname = None
            modelVariableSet.countSatisfied = 0
            modelVariableSet.countNotSatisfied = 0
            checkValidationMessages(val, modelVariableSet)
        instanceProducingVariableSets[instanceQname].append(modelVariableSet)
        modelVariableSet.outputInstanceQname = instanceQname
        if modelVariableSet.aspectModel not in ('non-dimensional', 'dimensional'):
            val.modelXbrl.error('xbrlve:unknownAspectModel', (_('Variable set %(xlinkLabel)s, aspect model %(aspectModel)s not recognized')),
              modelObject=modelVariableSet,
              xlinkLabel=(modelVariableSet.xlinkLabel),
              aspectModel=(modelVariableSet.aspectModel))
        modelVariableSet.hasConsistencyAssertion = False
        nameVariables = {}
        qnameRels = {}
        definedNamesSet = set()
        for modelRel in val.modelXbrl.relationshipSet(XbrlConst.variableSet).fromModelObject(modelVariableSet):
            varqname = modelRel.variableQname
            if varqname:
                qnameRels[varqname] = modelRel
                toVariable = modelRel.toModelObject
                if varqname not in definedNamesSet:
                    definedNamesSet.add(varqname)
                if varqname not in nameVariables:
                    nameVariables[varqname] = toVariable
                else:
                    if nameVariables[varqname] != toVariable:
                        val.modelXbrl.error('xbrlve:duplicateVariableNames', (_('Multiple variables named %(xlinkLabel)s in variable set %(name)s')),
                          modelObject=toVariable,
                          xlinkLabel=(modelVariableSet.xlinkLabel),
                          name=varqname)
                fromInstanceQnames = None
                for instRel in val.modelXbrl.relationshipSet(XbrlConst.instanceVariable).toModelObject(toVariable):
                    fromInstance = instRel.fromModelObject
                    if isinstance(fromInstance, ModelInstance):
                        fromInstanceQname = fromInstance.instanceQname
                        varSetInstanceDependencies.add(fromInstanceQname)
                        instanceDependencies[instanceQname].add(fromInstanceQname)
                        if fromInstanceQnames is None:
                            fromInstanceQnames = set()
                        fromInstanceQnames.add(fromInstanceQname)

                if fromInstanceQnames is None:
                    varSetInstanceDependencies.add(XbrlConst.qnStandardInputInstance)
                    if instanceQname:
                        instanceDependencies[instanceQname].add(XbrlConst.qnStandardInputInstance)
                toVariable.fromInstanceQnames = fromInstanceQnames
            else:
                val.modelXbrl.error('xbrlve:variableNameResolutionFailure', (_('Variables name %(name)s cannot be determined on arc from %(xlinkLabel)s')),
                  modelObject=modelRel,
                  xlinkLabel=(modelVariableSet.xlinkLabel),
                  name=(modelRel.variablename))

        checkVariablesScopeVisibleQnames(val, nameVariables, definedNamesSet, modelVariableSet)
        definedNamesSet |= parameterQnames
        variableDependencies = {}
        for modelRel in val.modelXbrl.relationshipSet(XbrlConst.variableSet).fromModelObject(modelVariableSet):
            variable = modelRel.toModelObject
            if isinstance(variable, (ModelParameter, ModelVariable)):
                varqname = modelRel.variableQname
                depVars = variable.variableRefs()
                variableDependencies[varqname] = depVars
                if len(depVars) > 0:
                    if formulaOptions.traceVariablesDependencies:
                        val.modelXbrl.info('formula:trace', (_('Variable set %(xlinkLabel)s, variable %(name)s, dependences %(dependencies)s')),
                          modelObject=modelVariableSet,
                          xlinkLabel=(modelVariableSet.xlinkLabel),
                          name=varqname,
                          dependencies=depVars)
                definedNamesSet.add(varqname)
                if isinstance(variable, ModelFactVariable):
                    variable.hasNoVariableDependencies = len(depVars - parameterQnames) == 0
                    for depVar in XPathParser.variableReferencesSet(variable.fallbackValueProg, variable):
                        if depVar in qnameRels and isinstance(qnameRels[depVar].toModelObject, ModelVariable):
                            val.modelXbrl.error('xbrlve:fallbackValueVariableReferenceNotAllowed', (_("Variable set %(xlinkLabel)s fallbackValue '%(fallbackValue)s' cannot refer to variable %(dependency)s")),
                              modelObject=variable,
                              xlinkLabel=(modelVariableSet.xlinkLabel),
                              fallbackValue=(variable.fallbackValue),
                              dependency=depVar)

                    checkFilterAspectModel(val, modelVariableSet, variable.filterRelationships, xpathContext)

        orderedNameSet = set()
        orderedNameList = []
        orderedAVariable = True
        while orderedAVariable:
            orderedAVariable = False
            for varqname, depVars in variableDependencies.items():
                if varqname not in orderedNameSet:
                    if len(depVars - parameterQnames - orderedNameSet) == 0:
                        orderedNameList.append(varqname)
                        orderedNameSet.add(varqname)
                        orderedAVariable = True
                    if varqname in instanceQnames:
                        varSetInstanceDependencies.add(varqname)
                        instanceDependencies[instanceQname].add(varqname)
                    elif isinstance(nameVariables.get(varqname), ModelInstance):
                        instqname = nameVariables[varqname].instanceQname
                        varSetInstanceDependencies.add(instqname)
                        instanceDependencies[instanceQname].add(instqname)

        for varqname, depVars in variableDependencies.items():
            if varqname not in orderedNameSet:
                circularOrUndefVars = depVars - parameterQnames - orderedNameSet
                undefinedVars = circularOrUndefVars - definedNamesSet
                varsCircularDep = circularOrUndefVars - undefinedVars
                if len(undefinedVars) > 0:
                    val.modelXbrl.error('xbrlve:unresolvedDependency', (_('Undefined variable dependencies in variable set %(xlinkLabel)s, from variable %(nameFrom)s to %(nameTo)s')),
                      modelObject=modelVariableSet,
                      xlinkLabel=(modelVariableSet.xlinkLabel),
                      nameFrom=varqname,
                      nameTo=undefinedVars)
                if len(varsCircularDep) > 0:
                    val.modelXbrl.error('xbrlve:cyclicDependencies', (_('Cyclic dependencies in variable set %(xlinkLabel)s, from variable %(nameFrom)s to %(nameTo)s')),
                      modelObject=modelVariableSet,
                      xlinkLabel=(modelVariableSet.xlinkLabel),
                      nameFrom=varqname,
                      nameTo=varsCircularDep)

        for varSetDepVarQname in modelVariableSet.variableRefs():
            if varSetDepVarQname not in definedNamesSet:
                if varSetDepVarQname not in parameterQnames:
                    val.modelXbrl.error('xbrlve:unresolvedDependency', (_('Undefined variable dependency in variable set %(xlinkLabel)s, %(name)s')),
                      modelObject=modelVariableSet,
                      xlinkLabel=(modelVariableSet.xlinkLabel),
                      name=varSetDepVarQname)
                if varSetDepVarQname in instanceQnames:
                    varSetInstanceDependencies.add(varSetDepVarQname)
                    instanceDependencies[instanceQname].add(varSetDepVarQname)
                elif isinstance(nameVariables.get(varSetDepVarQname), ModelInstance):
                    instqname = nameVariables[varSetDepVarQname].instanceQname
                    varSetInstanceDependencies.add(instqname)
                    instanceDependencies[instanceQname].add(instqname)

        if formulaOptions.traceVariablesOrder:
            val.modelXbrl.info('formula:trace', (_('Variable set %(xlinkLabel)s, variables order: %(dependencies)s')),
              modelObject=modelVariableSet,
              xlinkLabel=(modelVariableSet.xlinkLabel),
              dependencies=orderedNameList)
        if formulaOptions.traceVariablesDependencies:
            if len(varSetInstanceDependencies) > 0:
                if varSetInstanceDependencies != {XbrlConst.qnStandardInputInstance}:
                    val.modelXbrl.info('formula:trace', (_('Variable set %(xlinkLabel)s, instance dependences %(dependencies)s')),
                      modelObject=modelVariableSet,
                      xlinkLabel=(modelVariableSet.xlinkLabel),
                      dependencies=varSetInstanceDependencies)
        modelVariableSet.orderedVariableRelationships = []
        for varqname in orderedNameList:
            if varqname in qnameRels:
                modelVariableSet.orderedVariableRelationships.append(qnameRels[varqname])

        orderedNameSet.clear()
        del orderedNameList[:]
        if isinstance(modelVariableSet, ModelExistenceAssertion):
            for depVar in XPathParser.variableReferencesSet(modelVariableSet.testProg, modelVariableSet):
                if depVar in qnameRels and isinstance(qnameRels[depVar].toModelObject, ModelVariable):
                    val.modelXbrl.error('xbrleae:variableReferenceNotAllowed', (_('Existence Assertion %(xlinkLabel)s, cannot refer to variable %(name)s')),
                      modelObject=modelVariableSet,
                      xlinkLabel=(modelVariableSet.xlinkLabel),
                      name=depVar)

        checkValidationMessageVariables(val, modelVariableSet, qnameRels, xpathContext.parameterQnames)
        if isinstance(modelVariableSet, ModelFormula):
            for consisAsserRel in val.modelXbrl.relationshipSet(XbrlConst.consistencyAssertionFormula).toModelObject(modelVariableSet):
                consisAsser = consisAsserRel.fromModelObject
                if isinstance(consisAsser, ModelConsistencyAssertion):
                    checkValidationMessages(val, consisAsser)
                    checkValidationMessageVariables(val, consisAsser, qnameRels, xpathContext.parameterQnames)

        modelVariableSet.preconditions = []
        for modelRel in val.modelXbrl.relationshipSet(XbrlConst.variableSetPrecondition).fromModelObject(modelVariableSet):
            precondition = modelRel.toModelObject
            if isinstance(precondition, ModelPrecondition):
                modelVariableSet.preconditions.append(precondition)

        for modelRel in val.modelXbrl.relationshipSet(XbrlConst.variableSetFilter).fromModelObject(modelVariableSet):
            varSetFilter = modelRel.toModelObject
            if modelRel.isCovered:
                val.modelXbrl.warning('arelle:variableSetFilterCovered', (_('Variable set %(xlinkLabel)s, filter %(filterLabel)s, cannot be covered')),
                  modelObject=varSetFilter,
                  xlinkLabel=(modelVariableSet.xlinkLabel),
                  filterLabel=(varSetFilter.xlinkLabel))
                modelRel._isCovered = False
            for depVar in varSetFilter.variableRefs():
                if depVar in qnameRels and isinstance(qnameRels[depVar].toModelObject, ModelVariable):
                    val.modelXbrl.error('xbrlve:factVariableReferenceNotAllowed', (_('Variable set %(xlinkLabel)s, filter %(filterLabel)s, cannot refer to variable %(name)s')),
                      modelObject=varSetFilter,
                      xlinkLabel=(modelVariableSet.xlinkLabel),
                      filterLabel=(varSetFilter.xlinkLabel),
                      name=depVar)

        if isinstance(modelVariableSet, ModelFormula):
            checkFormulaRules(val, modelVariableSet, nameVariables)
        nameVariables.clear()
        qnameRels.clear()
        definedNamesSet.clear()
        variableDependencies.clear()
        varSetInstanceDependencies.clear()

    val.modelXbrl.profileActivity('... assertion and formula checks and compilation', minTimeToShow=1.0)
    for modelTable in val.modelXbrl.modelRenderingTables:
        modelTable.fromInstanceQnames = None
        if modelTable.aspectModel not in ('non-dimensional', 'dimensional'):
            val.modelXbrl.error('xbrlte:unknownAspectModel', (_('Table %(xlinkLabel)s, aspect model %(aspectModel)s not recognized')),
              modelObject=modelTable,
              xlinkLabel=(modelTable.xlinkLabel),
              aspectModel=(modelTable.aspectModel))
        modelTable.compile()
        checkTableRules(val, xpathContext, modelTable)

    val.modelXbrl.profileActivity('... rendering tables and axes checks and compilation', minTimeToShow=1.0)
    orderedInstancesSet = set()
    stdInpInst = {XbrlConst.qnStandardInputInstance}
    orderedInstancesList = []
    orderedAnInstance = True
    while orderedAnInstance:
        orderedAnInstance = False
        for instqname, depInsts in instanceDependencies.items():
            if instqname and instqname not in orderedInstancesSet and len(depInsts - stdInpInst - orderedInstancesSet) == 0:
                orderedInstancesList.append(instqname)
                orderedInstancesSet.add(instqname)
                orderedAnInstance = True

    for independentInstance in _DICT_SET(instanceProducingVariableSets.keys()) - _DICT_SET(orderedInstancesList):
        orderedInstancesList.append(independentInstance)
        orderedInstancesSet.add(independentInstance)

    if None not in orderedInstancesList:
        orderedInstancesList.append(None)
    for instqname, depInsts in instanceDependencies.items():
        if instqname not in orderedInstancesSet:
            missingDependentInstances = depInsts - stdInpInst
            if val.parameters:
                missingDependentInstances -= _DICT_SET(val.parameters.keys())
            if instqname:
                if missingDependentInstances:
                    val.modelXbrl.error('xbrlvarinste:instanceVariableRecursionCycle', (_('Cyclic dependencies of instance %(name)s produced by a formula, with variables consuming instances %(dependencies)s')),
                      modelObject=(val.modelXbrl),
                      name=instqname,
                      dependencies=missingDependentInstances)
                else:
                    if instqname == XbrlConst.qnStandardOutputInstance:
                        orderedInstancesSet.add(instqname)
                        orderedInstancesList.append(instqname)
            elif instqname in depInsts:
                val.modelXbrl.error('xbrlvarinste:instanceVariableRecursionCycle', (_('Cyclic dependencies of instance %(name)s produced by its own variables')),
                  modelObject=(val.modelXbrl),
                  name=instqname)

    if formulaOptions.traceVariablesOrder:
        if len(orderedInstancesList) > 1:
            val.modelXbrl.info('formula:trace', (_('Variable instances processing order: %(dependencies)s')),
              modelObject=(val.modelXbrl),
              dependencies=orderedInstancesList)
    for modelRel in val.modelXbrl.relationshipSet(XbrlConst.consistencyAssertionFormula).modelRelationships:
        if isinstance(modelRel.fromModelObject, ModelConsistencyAssertion):
            if isinstance(modelRel.toModelObject, ModelFormula):
                consisAsser = modelRel.fromModelObject
                consisAsser.countSatisfied = 0
                consisAsser.countNotSatisfied = 0
                if consisAsser.hasProportionalAcceptanceRadius:
                    if consisAsser.hasAbsoluteAcceptanceRadius:
                        val.modelXbrl.error('xbrlcae:acceptanceRadiusConflict', (_('Consistency assertion %(xlinkLabel)s has both absolute and proportional acceptance radii')),
                          modelObject=consisAsser,
                          xlinkLabel=(consisAsser.xlinkLabel))
            consisAsser.orderedVariableRelationships = []
            for consisParamRel in val.modelXbrl.relationshipSet(XbrlConst.consistencyAssertionParameter).fromModelObject(consisAsser):
                if isinstance(consisParamRel.toModelObject, ModelVariable):
                    val.modelXbrl.error('xbrlcae:variablesNotAllowed', (_('Consistency assertion %(xlinkLabel)s has relationship to a %(elementTo)s %(xlinkLabelTo)s')),
                      modelObject=consisAsser,
                      xlinkLabel=(consisAsser.xlinkLabel),
                      elementTo=(consisParamRel.toModelObject.localName),
                      xlinkLabelTo=(consisParamRel.toModelObject.xlinkLabel))
                elif isinstance(consisParamRel.toModelObject, ModelParameter):
                    consisAsser.orderedVariableRelationships.append(consisParamRel)

            consisAsser.compile()
            modelRel.toModelObject.hasConsistencyAssertion = True

    val.modelXbrl.profileActivity('... consistency assertion setup', minTimeToShow=1.0)
    xpathContext.defaultDimensionAspects = set(val.modelXbrl.qnameDimensionDefaults.keys())
    xpathContext.dimensionsAspectUniverse = xpathContext.defaultDimensionAspects
    for cntx in val.modelXbrl.contexts.values():
        xpathContext.dimensionsAspectUniverse |= _DICT_SET(cntx.qnameDims.keys())

    for instanceQname in instanceQnames:
        if instanceQname not in (XbrlConst.qnStandardInputInstance, XbrlConst.qnStandardOutputInstance) and val.parameters and instanceQname in val.parameters:
            for namedInstance in val.parameters[instanceQname][1]:
                ValidateXbrlDimensions.loadDimensionDefaults(namedInstance)
                xpathContext.defaultDimensionAspects |= _DICT_SET(namedInstance.qnameDimensionDefaults.keys())
                xpathContext.dimensionsAspectUniverse |= _DICT_SET(namedInstance.qnameDimensionDefaults.keys())
                for cntx in namedInstance.contexts.values():
                    xpathContext.dimensionsAspectUniverse |= _DICT_SET(cntx.qnameDims.keys())

    for instanceQname, modelVariableSets in instanceProducingVariableSets.items():
        for modelVariableSet in modelVariableSets:
            for varScopeRel in val.modelXbrl.relationshipSet(XbrlConst.variablesScope).toModelObject(modelVariableSet):
                if isinstance(varScopeRel.fromModelObject, ModelVariableSet):
                    sourceVariableSet = varScopeRel.fromModelObject
                    if sourceVariableSet.outputInstanceQname != instanceQname:
                        val.modelXbrl.error('xbrlvarscopee:differentInstances', (_('Variable set %(xlinkLabel1)s in instance %(instance1)s has variables scope relationship to varaible set %(xlinkLabel2)s in instance %(instance2)s')),
                          modelObject=modelVariableSet,
                          xlinkLabel1=(sourceVariableSet.xlinkLabel),
                          instance1=(sourceVariableSet.outputInstanceQname),
                          xlinkLabel2=(modelVariableSet.xlinkLabel),
                          instance2=(modelVariableSet.outputInstanceQname))
                    if sourceVariableSet.aspectModel != modelVariableSet.aspectModel:
                        val.modelXbrl.error('xbrlvarscopee:conflictingAspectModels', (_('Variable set %(xlinkLabel1)s aspectModel (%(aspectModel1)s) differs from varaible set %(xlinkLabel2)s aspectModel (%(aspectModel2)s)')),
                          modelObject=modelVariableSet,
                          xlinkLabel1=(sourceVariableSet.xlinkLabel),
                          aspectModel1=(sourceVariableSet.aspectModel),
                          xlinkLabel2=(modelVariableSet.xlinkLabel),
                          aspectModel2=(modelVariableSet.aspectModel))

    val.modelXbrl.profileActivity('... instances scopes and setup', minTimeToShow=1.0)
    val.modelXbrl.profileStat(_('formulaValidation'))
    if initialErrorCount < val.modelXbrl.logCount.get(logging._checkLevel('ERROR'), 0) or compileOnly or getattr(val, 'validateFormulaCompileOnly', False):
        return
    if instanceQnames:
        val.modelXbrl.modelManager.showStatus(_('initializing formula output instances'))
        schemaRefs = [val.modelXbrl.modelDocument.relativeUri(referencedDoc.uri) for referencedDoc in val.modelXbrl.modelDocument.referencesDocument.keys() if referencedDoc.type == ModelDocument.Type.SCHEMA]
    outputXbrlInstance = None
    for instanceQname in instanceQnames:
        if instanceQname == XbrlConst.qnStandardInputInstance:
            pass
        else:
            if val.parameters:
                if instanceQname in val.parameters:
                    namedInstance = val.parameters[instanceQname][1]
                else:
                    uri = val.modelXbrl.modelDocument.filepath[:-4] + '-output-XBRL-instance'
                    if instanceQname != XbrlConst.qnStandardOutputInstance:
                        uri = uri + '-' + instanceQname.localName
                    uri = uri + '.xml'
                    namedInstance = ModelXbrl.create((val.modelXbrl.modelManager), newDocumentType=(ModelDocument.Type.INSTANCE),
                      url=uri,
                      schemaRefs=schemaRefs,
                      isEntry=True)
                    ValidateXbrlDimensions.loadDimensionDefaults(namedInstance)
                xpathContext.inScopeVars[instanceQname] = namedInstance
                if instanceQname == XbrlConst.qnStandardOutputInstance:
                    outputXbrlInstance = namedInstance

    val.modelXbrl.profileActivity('... output instances setup', minTimeToShow=1.0)
    val.modelXbrl.profileStat(_('formulaInstancesSetup'))
    timeFormulasStarted = time.time()
    val.modelXbrl.modelManager.showStatus(_('running formulae'))
    runIDs = (formulaOptions.runIDs or '').replace('|', ' ').split()
    if runIDs:
        val.modelXbrl.info('formula:trace', (_('Formua/assertion IDs restriction: %(ids)s')),
          modelXbrl=(val.modelXbrl),
          ids=(', '.join(runIDs)))
    try:
        if hasattr(val, 'maxFormulaRunTime'):
            if val.maxFormulaRunTime > 0:
                maxFormulaRunTimeTimer = Timer(val.maxFormulaRunTime * 60.0, xpathContext.runTimeExceededCallback)
                maxFormulaRunTimeTimer.start()
        else:
            maxFormulaRunTimeTimer = None
        from arelle.FormulaEvaluator import init as formulaEvaluatorInit, evaluate
        formulaEvaluatorInit()
        val.modelXbrl.profileActivity('... evaluations', minTimeToShow=1.0)
        for instanceQname in orderedInstancesList:
            for modelVariableSet in instanceProducingVariableSets[instanceQname]:
                if val.modelXbrl.relationshipSet(XbrlConst.variablesScope).toModelObject(modelVariableSet) or not runIDs or modelVariableSet.id in runIDs or modelVariableSet.hasConsistencyAssertion and any(modelRel.fromModelObject.id in runIDs for modelRel in val.modelXbrl.relationshipSet(XbrlConst.consistencyAssertionFormula).toModelObject(modelVariableSet) if isinstance(modelRel.fromModelObject, ModelConsistencyAssertion)):
                    try:
                        varSetId = modelVariableSet.id or modelVariableSet.xlinkLabel
                        val.modelXbrl.profileActivity(('... evaluating ' + varSetId), minTimeToShow=10.0)
                        val.modelXbrl.modelManager.showStatus(_('evaluating {0}').format(varSetId))
                        val.modelXbrl.profileActivity(('... evaluating ' + varSetId), minTimeToShow=1.0)
                        evaluate(xpathContext, modelVariableSet)
                        val.modelXbrl.profileStat(modelVariableSet.localName + '_' + varSetId)
                    except XPathContext.XPathException as err:
                        val.modelXbrl.error((err.code), (_('Variable set \n%(variableSet)s \nException: \n%(error)s')),
                          modelObject=modelVariableSet,
                          variableSet=(str(modelVariableSet)),
                          error=(err.message))

        if maxFormulaRunTimeTimer:
            maxFormulaRunTimeTimer.cancel()
    except XPathContext.RunTimeExceededException:
        val.modelXbrl.info('formula:maxRunTime', (_('Formula execution ended after %(mins)s minutes')),
          modelObject=(val.modelXbrl),
          mins=(val.maxFormulaRunTime))

    asserTests = {}
    for exisValAsser in val.modelXbrl.modelVariableSets:
        if isinstance(exisValAsser, ModelVariableSetAssertion) and (not runIDs or exisValAsser.id in runIDs):
            asserTests[exisValAsser.id] = (
             exisValAsser.countSatisfied, exisValAsser.countNotSatisfied)
            if formulaOptions.traceAssertionResultCounts:
                val.modelXbrl.info('formula:trace', (_('%(assertionType)s Assertion %(id)s evaluations : %(satisfiedCount)s satisfied, %(notSatisfiedCount)s not satisfied')),
                  modelObject=exisValAsser,
                  assertionType=('Existence' if isinstance(exisValAsser, ModelExistenceAssertion) else 'Value'),
                  id=(exisValAsser.id),
                  satisfiedCount=(exisValAsser.countSatisfied),
                  notSatisfiedCount=(exisValAsser.countNotSatisfied))

    for modelRel in val.modelXbrl.relationshipSet(XbrlConst.consistencyAssertionFormula).modelRelationships:
        if isinstance(modelRel.fromModelObject, ModelConsistencyAssertion) and isinstance(modelRel.toModelObject, ModelFormula) and (not runIDs or modelRel.fromModelObject.id in runIDs):
            consisAsser = modelRel.fromModelObject
            asserTests[consisAsser.id] = (consisAsser.countSatisfied, consisAsser.countNotSatisfied)
            if formulaOptions.traceAssertionResultCounts:
                val.modelXbrl.info('formula:trace', (_('Consistency Assertion %(id)s evaluations : %(satisfiedCount)s satisfied, %(notSatisfiedCount)s not satisfied')),
                  modelObject=consisAsser,
                  id=(consisAsser.id),
                  satisfiedCount=(consisAsser.countSatisfied),
                  notSatisfiedCount=(consisAsser.countNotSatisfied))

    if asserTests:
        val.modelXbrl.log(None, 'asrtNoLog', None, assertionResults=asserTests)
    if outputXbrlInstance:
        if val.modelXbrl.formulaOutputInstance:
            val.modelXbrl.formulaOutputInstance.close()
        val.modelXbrl.formulaOutputInstance = outputXbrlInstance
    val.modelXbrl.modelManager.showStatus(_('formulae finished'), 2000)
    instanceProducingVariableSets.clear()
    parameterQnames.clear()
    instanceQnames.clear()
    parameterDependencies.clear()
    instanceDependencies.clear()
    dependencyResolvedParameters.clear()
    orderedInstancesSet.clear()
    del orderedParameters
    del orderedInstances
    del orderedInstancesList
    xpathContext.close()
    val.modelXbrl.profileStat(_('formulaExecutionTotal'), time.time() - timeFormulasStarted)


def checkVariablesScopeVisibleQnames(val, nameVariables, definedNamesSet, modelVariableSet):
    for visibleVarSetRel in val.modelXbrl.relationshipSet(XbrlConst.variablesScope).toModelObject(modelVariableSet):
        varqname = visibleVarSetRel.variableQname
        if varqname:
            if varqname not in nameVariables:
                nameVariables[varqname] = visibleVarSetRel.fromModelObject
            if varqname not in definedNamesSet:
                definedNamesSet.add(varqname)
        visibleVarSet = visibleVarSetRel.fromModelObject
        for modelRel in val.modelXbrl.relationshipSet(XbrlConst.variableSet).fromModelObject(visibleVarSet):
            varqname = modelRel.variableQname
            if varqname:
                if varqname not in nameVariables:
                    nameVariables[varqname] = modelRel.toModelObject
                if varqname not in definedNamesSet:
                    definedNamesSet.add(varqname)

        checkVariablesScopeVisibleQnames(val, nameVariables, definedNamesSet, visibleVarSet)


def checkFilterAspectModel(val, variableSet, filterRelationships, xpathContext, uncoverableAspects=None):
    result = set()
    if uncoverableAspects is None:
        oppositeAspectModel = (_DICT_SET({'dimensional', 'non-dimensional'}) - _DICT_SET({variableSet.aspectModel})).pop()
        try:
            uncoverableAspects = aspectModels[oppositeAspectModel] - aspectModels[variableSet.aspectModel]
        except KeyError:
            return result

    acfAspectsCovering = {}
    for varFilterRel in filterRelationships:
        _filter = varFilterRel.toModelObject
        isAllAspectCoverFilter = False
        if isinstance(_filter, ModelAspectCover):
            for aspect in _filter.aspectsCovered(None, xpathContext):
                if aspect in acfAspectsCovering:
                    otherFilterCover, otherFilterLabel = acfAspectsCovering[aspect]
                    if otherFilterCover != varFilterRel.isCovered:
                        val.modelXbrl.error('xbrlacfe:inconsistentAspectCoverFilters', (_('Variable set %(xlinkLabel)s, aspect cover filter %(filterLabel)s, aspect %(aspect)s, conflicts with %(filterLabel2)s with inconsistent cover attribute')),
                          modelObject=variableSet,
                          xlinkLabel=(variableSet.xlinkLabel),
                          filterLabel=(_filter.xlinkLabel),
                          aspect=(str(aspect) if isinstance(aspect, QName) else Aspect.label[aspect]),
                          filterLabel2=otherFilterLabel)
                else:
                    acfAspectsCovering[aspect] = (
                     varFilterRel.isCovered, _filter.xlinkLabel)

            isAllAspectCoverFilter = _filter.isAll
        try:
            aspectsCovered = _filter.aspectsCovered(None)
            if not isAllAspectCoverFilter:
                if any(isinstance(aspect, QName) for aspect in aspectsCovered) and Aspect.DIMENSIONS in uncoverableAspects or aspectsCovered & uncoverableAspects:
                    val.modelXbrl.error('xbrlve:filterAspectModelMismatch', (_('Variable set %(xlinkLabel)s, aspect model %(aspectModel)s filter %(filterName)s %(filterLabel)s can cover aspect not in aspect model')),
                      modelObject=variableSet,
                      xlinkLabel=(variableSet.xlinkLabel),
                      aspectModel=(variableSet.aspectModel),
                      filterName=(_filter.localName),
                      filterLabel=(_filter.xlinkLabel))
            result |= aspectsCovered
        except Exception:
            pass

        if hasattr(_filter, 'filterRelationships'):
            result |= checkFilterAspectModel(val, variableSet, _filter.filterRelationships, xpathContext, uncoverableAspects)

    return result


def checkFormulaRules(val, formula, nameVariables):
    if not (formula.hasRule(Aspect.CONCEPT) or formula.source(Aspect.CONCEPT)):
        if XmlUtil.hasDescendant(formula, XbrlConst.formula, 'concept'):
            val.modelXbrl.error('xbrlfe:incompleteConceptRule', (_('Formula %(xlinkLabel)s concept rule does not have a nearest source and does not have a child element')),
              modelObject=formula,
              xlinkLabel=(formula.xlinkLabel))
        else:
            val.modelXbrl.error('xbrlfe:missingConceptRule', (_('Formula %(xlinkLabel)s omits a rule for the concept aspect')),
              modelObject=formula,
              xlinkLabel=(formula.xlinkLabel))
    if not isinstance(formula, ModelTuple):
        if not (formula.hasRule(Aspect.SCHEME) or formula.source(Aspect.SCHEME)) or not (formula.hasRule(Aspect.VALUE) or formula.source(Aspect.VALUE)):
            if XmlUtil.hasDescendant(formula, XbrlConst.formula, 'entityIdentifier'):
                val.modelXbrl.error('xbrlfe:incompleteEntityIdentifierRule', (_('Formula %(xlinkLabel)s entity identifier rule does not have a nearest source and does not have either a @scheme or a @value attribute')),
                  modelObject=formula,
                  xlinkLabel=(formula.xlinkLabel))
            else:
                val.modelXbrl.error('xbrlfe:missingEntityIdentifierRule', (_('Formula %(xlinkLabel)s omits a rule for the entity identifier aspect')),
                  modelObject=formula,
                  xlinkLabel=(formula.xlinkLabel))
            if not (formula.hasRule(Aspect.PERIOD_TYPE) or formula.source(Aspect.PERIOD_TYPE)):
                if XmlUtil.hasDescendant(formula, XbrlConst.formula, 'period'):
                    val.modelXbrl.error('xbrlfe:incompletePeriodRule', (_('Formula %(xlinkLabel)s period rule does not have a nearest source and does not have a child element')),
                      modelObject=formula,
                      xlinkLabel=(formula.xlinkLabel))
                else:
                    val.modelXbrl.error('xbrlfe:missingPeriodRule', (_('Formula %(xlinkLabel)s omits a rule for the period aspect')),
                      modelObject=formula,
                      xlinkLabel=(formula.xlinkLabel))
            concept = val.modelXbrl.qnameConcepts.get(formula.evaluateRule(None, Aspect.CONCEPT))
            if concept is None:
                sourceFactVar = nameVariables.get(formula.source(Aspect.CONCEPT))
                if isinstance(sourceFactVar, ModelFactVariable):
                    for varFilterRels in (formula.groupFilterRelationships, sourceFactVar.filterRelationships):
                        for varFilterRel in varFilterRels:
                            _filter = varFilterRel.toModelObject
                            if isinstance(_filter, ModelConceptName):
                                for conceptQname in _filter.conceptQnames:
                                    concept = val.modelXbrl.qnameConcepts.get(conceptQname)
                                    if concept is not None and concept.isNumeric:
                                        break

            if concept is not None:
                if concept.isNumeric:
                    if formula.hasRule(Aspect.MULTIPLY_BY) or formula.hasRule(Aspect.DIVIDE_BY) or formula.source(Aspect.UNIT) or XmlUtil.hasDescendant(formula, XbrlConst.formula, 'unit'):
                        val.modelXbrl.error('xbrlfe:missingSAVForUnitRule', (_('Formula %(xlinkLabel)s unit rule does not have a source and does not have a child element')),
                          modelObject=formula,
                          xlinkLabel=(formula.xlinkLabel))
                    else:
                        val.modelXbrl.error('xbrlfe:missingUnitRule', (_('Formula %(xlinkLabel)s omits a rule for the unit aspect')),
                          modelObject=formula,
                          xlinkLabel=(formula.xlinkLabel))
                else:
                    if formula.hasRule(Aspect.MULTIPLY_BY) or formula.hasRule(Aspect.DIVIDE_BY) or formula.source((Aspect.UNIT), acceptFormulaSource=False):
                        val.modelXbrl.error('xbrlfe:conflictingAspectRules', (_('Formula %(xlinkLabel)s has a rule for the unit aspect of a non-numeric concept %(concept)s')),
                          modelObject=formula,
                          xlinkLabel=(formula.xlinkLabel),
                          concept=(concept.qname))
                    aspectPeriodType = formula.evaluateRule(None, Aspect.PERIOD_TYPE)
                    if concept.periodType == 'duration' and aspectPeriodType == 'instant' or concept.periodType == 'instant' and aspectPeriodType in ('duration',
                                                                                                                                                      'forever'):
                        val.modelXbrl.error('xbrlfe:conflictingAspectRules', (_('Formula %(xlinkLabel)s has a rule for the %(aspectPeriodType)s period aspect of a %(conceptPeriodType)s concept %(concept)s')),
                          modelObject=formula,
                          xlinkLabel=(formula.xlinkLabel),
                          concept=(concept.qname),
                          aspectPeriodType=aspectPeriodType,
                          conceptPeriodType=(concept.periodType))
        else:
            for eltName, dim, badUsageErr, missingSavErr in (('explicitDimension', 'explicit', 'xbrlfe:badUsageOfExplicitDimensionRule', 'xbrlfe:missingSAVForExplicitDimensionRule'),
                                                             ('typedDimension', 'typed', 'xbrlfe:badUsageOfTypedDimensionRule', 'xbrlfe:missingSAVForTypedDimensionRule')):
                for dimElt in XmlUtil.descendants(formula, XbrlConst.formula, eltName):
                    dimQname = qname(dimElt, dimElt.get('dimension'))
                    dimConcept = val.modelXbrl.qnameConcepts.get(dimQname)
                    if dimQname:
                        if dimConcept is None or (not dimConcept.isExplicitDimension if dim == 'explicit' else not dimConcept.isTypedDimension):
                            val.modelXbrl.error(badUsageErr, (_('Formula %(xlinkLabel)s dimension attribute %(dimension)s on the %(dimensionType)s dimension rule contains a QName that does not identify an (dimensionType)s dimension.')),
                              modelObject=formula,
                              xlinkLabel=(formula.xlinkLabel),
                              dimensionType=dim,
                              dimension=dimQname,
                              messageCodes=('xbrlfe:badUsageOfExplicitDimensionRule',
                                            'xbrlfe:badUsageOfTypedDimensionRule'))
                        else:
                            if not XmlUtil.hasChild(dimElt, XbrlConst.formula, '*'):
                                if not formula.source(Aspect.DIMENSIONS, dimElt):
                                    val.modelXbrl.error(missingSavErr, (_('Formula %(xlinkLabel)s %(dimension)s dimension rule does not have any child elements and does not have a SAV for the %(dimensionType)s dimension that is identified by its dimension attribute.')),
                                      modelObject=formula,
                                      xlinkLabel=(formula.xlinkLabel),
                                      dimensionType=dim,
                                      dimension=dimQname,
                                      messageCodes=('xbrlfe:missingSAVForExplicitDimensionRule',
                                                    'xbrlfe:missingSAVForTypedDimensionRule'))

            if formula.aspectModel == 'non-dimensional':
                unexpectedElts = XmlUtil.descendants(formula, XbrlConst.formula, ('explicitDimension',
                                                                                  'typedDimension'))
                if unexpectedElts:
                    val.modelXbrl.error('xbrlfe:unrecognisedAspectRule', (_('Formula %(xlinkLabel)s aspect model, %(aspectModel)s, includes an rule for aspect not defined in this aspect model: %(undefinedAspects)s')),
                      modelObject=formula,
                      xlinkLabel=(formula.xlinkLabel),
                      aspectModel=(formula.aspectModel),
                      undefinedAspects=(', '.join([elt.localName for elt in unexpectedElts])))
    for sourceElt in [formula] + XmlUtil.descendants(formula, XbrlConst.formula, '*', 'source', '*'):
        if sourceElt.get('source') is not None:
            qnSource = qname(sourceElt, (sourceElt.get('source')), noPrefixIsNoNamespace=True)
            if qnSource == XbrlConst.qnFormulaUncovered:
                if formula.implicitFiltering != 'true':
                    val.modelXbrl.error('xbrlfe:illegalUseOfUncoveredQName', (_('Formula %(xlinkLabel)s, not implicit filtering element has formulaUncovered source: %(name)s')),
                      modelObject=formula,
                      xlinkLabel=(formula.xlinkLabel),
                      name=(sourceElt.localName))
            else:
                if qnSource not in nameVariables:
                    val.modelXbrl.error('xbrlfe:nonexistentSourceVariable', (_('Variable set %(xlinkLabel)s, source %(name)s is not in the variable set')),
                      modelObject=formula,
                      xlinkLabel=(formula.xlinkLabel),
                      name=qnSource)
                else:
                    factVariable = nameVariables.get(qnSource)
            if isinstance(factVariable, ModelVariableSet):
                pass
            else:
                if not isinstance(factVariable, ModelFactVariable):
                    val.modelXbrl.error('xbrlfe:nonexistentSourceVariable', (_('Variable set %(xlinkLabel)s, source %(name)s not a factVariable but is a %(element)s')),
                      modelObject=formula,
                      xlinkLabel=(formula.xlinkLabel),
                      name=qnSource,
                      element=(factVariable.localName))
                else:
                    if factVariable.fallbackValue is not None:
                        val.modelXbrl.error('xbrlfe:bindEmptySourceVariable', (_('Formula %(xlinkLabel)s: source %(name)s is a fact variable that has a fallback value')),
                          modelObject=formula,
                          xlinkLabel=(formula.xlinkLabel),
                          name=qnSource)
                    elif sourceElt.localName == 'formula':
                        if factVariable.bindAsSequence == 'true':
                            val.modelXbrl.error('xbrlfe:defaultAspectValueConflicts', (_('Formula %(xlinkLabel)s: formula source %(name)s is a fact variable that binds as a sequence')),
                              modelObject=formula,
                              xlinkLabel=(formula.xlinkLabel),
                              name=qnSource)


def checkTableRules(val, xpathContext, table):
    checkFilterAspectModel(val, table, table.filterRelationships, xpathContext)
    checkDefinitionNodeRules(val, table, table, (XbrlConst.tableBreakdown, XbrlConst.tableBreakdownMMDD, XbrlConst.tableBreakdown201305, XbrlConst.tableAxis2011), xpathContext)


def checkDefinitionNodeRules(val, table, parent, arcrole, xpathContext):
    for rel in val.modelXbrl.relationshipSet(arcrole).fromModelObject(parent):
        axis = rel.toModelObject
        if axis is not None:
            if isinstance(axis, ModelFilterDefinitionNode):
                checkFilterAspectModel(val, table, axis.filterRelationships, xpathContext)
            else:
                if isinstance(axis, ModelRuleDefinitionNode):
                    rulesByAspect = defaultdict(set)
                    for elt in XmlUtil.descendants(axis, XbrlConst.formula, '*'):
                        try:
                            if elt.localName in ('concept', 'entityIdentifier', 'period',
                                                 'unit'):
                                rulesByAspect[elt.localName].add(elt)
                            else:
                                if elt.localName in ('explicitDimension', 'typedDimension'):
                                    rulesByAspect[(elt.localName, elt.xAttributes['dimension'].xValue)].add(elt)
                                else:
                                    if elt.localName == 'occFragments':
                                        rulesByAspect[(elt.localName, elt.xAttributes['occ'].xValue)].add(elt)
                            if elt.localName == ('concept', 'member') and not any(c.localName in ('qname',
                                                                                                  'qnameExpression') for c in XmlUtil.children(elt, XbrlConst.formula, '*')) or elt.localName == 'explicitDimension' and (not XmlUtil.children(elt, XbrlConst.formula, 'member') or not val.modelXbrl.qnameConcepts.get(elt.xAttributes['dimension'].xValue).isDimensionItem) or elt.localName == 'typedDimension' and not any(c.localName in ('xpath',
                                                                                                                                                                                                                                                                                                                                                                                                                                               'value') for c in XmlUtil.children(elt, XbrlConst.formula, '*')) or elt.localName == 'instant' and not elt.get('value') or elt.localName == 'duration' and not (elt.get('start') or elt.get('end')) or elt.localName == 'entityIdentifier' and not (elt.get('scheme') and elt.get('value')) or elt.localName == 'unit' and not any(c.localName in ('multiplyBy',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  'divideBy') for c in XmlUtil.children(elt, XbrlConst.formula, '*')) or elt.localName in ('multiplyBy',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           'divideBy') and not elt.get('measure'):
                                raise FormulaValidationException
                        except (FormulaValidationException, KeyError, AttributeError):
                            val.modelXbrl.error('xbrlte:incompleteAspectRule', (_('RuleAxis %(xlinkLabel)s includes an incomplete rule aspect: %(incompleteAspect)s')),
                              modelObject=axis,
                              xlinkLabel=(axis.xlinkLabel),
                              incompleteAspect=(elt.qname))

                        if elt.localName == 'occFragments' and XmlUtil.children(elt, XbrlConst.xbrldi, '*'):
                            val.modelXbrl.error('xbrlfe:badSubsequentOCCValue', (_('Formula %(label)s OCC element in rule aspect %(occ)s covers a dimensional aspect')),
                              modelObject=axis,
                              label=(axis.xlinkLabel),
                              occ=(elt.qname))

                    for aspect, rules in rulesByAspect.items():
                        if len(rules) > 1:
                            val.modelXbrl.error('xbrlte:multipleValuesForAspect', (_('RuleAxis %(xlinkLabel)s has %(count)s rules for aspect: %(multipleAspect)s')),
                              modelObject=axis,
                              xlinkLabel=(axis.xlinkLabel),
                              count=(len(rules)),
                              multipleAspect=aspect)

                    del rulesByAspect
                    if table.aspectModel == 'non-dimensional':
                        unexpectedElts = XmlUtil.descendants(axis, XbrlConst.formula, ('explicitDimension',
                                                                                       'typedDimension'))
                        if unexpectedElts:
                            val.modelXbrl.error('xbrlte:axisAspectModelMismatch', (_('RuleAxis %(xlinkLabel)s aspect model, %(aspectModel)s, includes an rule for aspect not defined in this aspect model: %(undefinedAspects)s')),
                              modelObject=axis,
                              xlinkLabel=(axis.xlinkLabel),
                              aspectModel=(table.aspectModel),
                              undefinedAspects=(', '.join([elt.localName for elt in unexpectedElts])))
                    for sourceElt in [axis] + XmlUtil.descendants(axis, XbrlConst.formula, '*', 'source', '*'):
                        if sourceElt.get('source') is not None:
                            qnSource = qname(sourceElt, (sourceElt.get('source')), noPrefixIsNoNamespace=True)
                            val.modelXbrl.info('table:info', (_('RuleAxis rule %(xlinkLabel)s contains a @source attribute %(qnSource)s which is not applicable to table rule axes.')),
                              modelObject=axis,
                              xlinkLabel=(axis.xlinkLabel),
                              qnSource=qnSource)

                    for childElt in XmlUtil.children(axis, '*', '*'):
                        if childElt.namespaceURI not in (XbrlConst.formula, axis.namespaceURI):
                            val.modelXbrl.error('xbrlte:unrecognisedAspectRule', (_('RuleAxis %(xlinkLabel)s aspect model includes an unrecognized rule aspect: %(unrecognizedAspect)s')),
                              modelObject=axis,
                              xlinkLabel=(axis.xlinkLabel),
                              unrecognizedAspect=(childElt.qname))

                else:
                    if isinstance(axis, ModelRelationshipDefinitionNode):
                        for qnameAttr in ('relationshipSourceQname', 'arcQname', 'linkQname',
                                          'dimensionQname'):
                            eltQname = axis.get(qnameAttr)
                            if eltQname and eltQname not in val.modelXbrl.qnameConcepts:
                                val.modelXbrl.info('table:info', (_('%(axis)s rule %(xlinkLabel)s contains a %(qnameAttr)s QName %(qname)s which is not in the DTS.')),
                                  modelObject=axis,
                                  axis=(axis.localName.title()),
                                  xlinkLabel=(axis.xlinkLabel),
                                  qnameAttr=qnameAttr,
                                  qname=eltQname)

                checkDefinitionNodeRules(val, table, axis, (XbrlConst.tableBreakdownTree, XbrlConst.tableBreakdownTreeMMDD, XbrlConst.tableBreakdownTree201305, XbrlConst.tableDefinitionNodeSubtree201301, XbrlConst.tableAxisSubtree2011), xpathContext)


def checkValidationMessages(val, modelVariableSet):
    for msgRelationship in (XbrlConst.assertionSatisfiedMessage, XbrlConst.assertionUnsatisfiedMessage):
        for modelRel in val.modelXbrl.relationshipSet(msgRelationship).fromModelObject(modelVariableSet):
            checkMessageExpressions(val, modelRel.toModelObject)


def checkMessageExpressions(val, message):
    if isinstance(message, ModelMessage) and not hasattr(message, 'expressions'):
        formatString = []
        expressions = []
        bracketNesting = 0
        skipTo = None
        expressionIndex = 0
        expression = None
        lastC = None
        for c in message.text:
            if skipTo:
                if c == skipTo:
                    skipTo = None
                if expression is not None and c in ("'", '"'):
                    skipTo = c
            elif lastC == c:
                if c in ('{', '}'):
                    lastC = None
            else:
                if lastC == '{':
                    bracketNesting += 1
                    expression = []
                    lastC = None
                elif c == '}' and expression is not None:
                    expressions.append(''.join(expression).strip())
                    expression = None
                    formatString.append('0[{0}]'.format(expressionIndex))
                    expressionIndex += 1
                    lastC = c
                else:
                    if lastC == '}':
                        bracketNesting -= 1
                        lastC = None
                    else:
                        lastC = c
            if expression is not None:
                expression.append(c)
            else:
                formatString.append(c)

        if lastC == '}':
            bracketNesting -= 1
        if bracketNesting:
            val.modelXbrl.error(('xbrlmsge:missingLeftCurlyBracketInMessage' if bracketNesting < 0 else 'xbrlmsge:missingRightCurlyBracketInMessage'), (_('Message %(xlinkLabel)s: unbalanced %(character)s character(s) in: %(text)s')),
              modelObject=message,
              xlinkLabel=(message.xlinkLabel),
              character=('{' if bracketNesting < 0 else '}'),
              text=(message.text),
              messageCodes=('xbrlmsge:missingLeftCurlyBracketInMessage', 'xbrlmsge:missingRightCurlyBracketInMessage'))
        else:
            message.expressions = expressions
            message.formatString = ''.join(formatString)
        if not message.xmlLang:
            val.modelXbrl.error('xbrlmsge:xbrlmsge:missingMessageLanguage', (_('Message %(xlinkLabel)s is missing an effective value for xml:lang: %(text)s.')),
              modelObject=message,
              xlinkLabel=(message.xlinkLabel),
              text=(message.text))


def checkValidationMessageVariables(val, modelVariableSet, varNames, paramNames):
    if isinstance(modelVariableSet, ModelConsistencyAssertion):
        varSetVars = (
         qname(XbrlConst.ca, 'aspect-matched-facts'),
         qname(XbrlConst.ca, 'acceptance-radius'),
         qname(XbrlConst.ca, 'absolute-acceptance-radius-expression'),
         qname(XbrlConst.ca, 'proportional-acceptance-radius-expression'))
    else:
        if isinstance(modelVariableSet, ModelExistenceAssertion):
            varSetVars = (
             XbrlConst.qnEaTestExpression,)
        else:
            if isinstance(modelVariableSet, ModelValueAssertion):
                varSetVars = (
                 XbrlConst.qnVaTestExpression,)
    for msgRelationship in (XbrlConst.assertionSatisfiedMessage, XbrlConst.assertionUnsatisfiedMessage):
        for modelRel in val.modelXbrl.relationshipSet(msgRelationship).fromModelObject(modelVariableSet):
            message = modelRel.toModelObject
            message.compile()
            for msgVarQname in message.variableRefs():
                if msgVarQname not in varNames and msgVarQname not in varSetVars and msgVarQname not in paramNames:
                    val.modelXbrl.error('err:XPST0008', (_('Undefined variable dependency in message %(xlinkLabel)s, %(name)s')),
                      modelObject=message,
                      xlinkLabel=(message.xlinkLabel),
                      name=msgVarQname)
                else:
                    if msgVarQname in varNames and isinstance(modelVariableSet, ModelExistenceAssertion) and isinstance(varNames[msgVarQname].toModelObject, ModelVariable):
                        val.modelXbrl.error('err:XPST0008', (_('Existence Assertion depends on evaluation variable in message %(xlinkLabel)s, %(name)s')),
                          modelObject=message,
                          xlinkLabel=(message.xlinkLabel),
                          name=msgVarQname)