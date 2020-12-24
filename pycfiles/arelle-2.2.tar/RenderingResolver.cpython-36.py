# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\ProgramData\lib\site-packages\arelle\RenderingResolver.py
# Compiled at: 2018-02-26 09:10:06
# Size of source mod 2**32: 44977 bytes
"""
Created on Sep 13, 2011

@author: Mark V Systems Limited
(c) Copyright 2011 Mark V Systems Limited, All rights reserved.
"""
import os, io, sys, json
from collections import defaultdict
from arelle import XbrlConst
from arelle.ModelObject import ModelObject
from arelle.ModelDtsObject import ModelResource
from arelle.ModelValue import QName
from arelle.ModelFormulaObject import Aspect
from arelle.ModelRenderingObject import ModelEuTable, ModelTable, ModelBreakdown, ModelEuAxisCoord, ModelDefinitionNode, ModelClosedDefinitionNode, ModelRuleDefinitionNode, ModelRelationshipDefinitionNode, ModelSelectionDefinitionNode, ModelFilterDefinitionNode, ModelConceptRelationshipDefinitionNode, ModelDimensionRelationshipDefinitionNode, ModelCompositionDefinitionNode, ModelTupleDefinitionNode, StructuralNode, ROLLUP_NOT_ANALYZED, CHILDREN_BUT_NO_ROLLUP, CHILD_ROLLUP_FIRST, CHILD_ROLLUP_LAST, OPEN_ASPECT_ENTRY_SURROGATE
from arelle.PrototypeInstanceObject import FactPrototype
from arelle.XPathContext import XPathException
RENDER_UNITS_PER_CHAR = 16

class ResolutionException(Exception):

    def __init__(self, code, message, **kwargs):
        self.kwargs = kwargs
        self.code = code
        self.message = message
        self.args = (self.__repr__(),)

    def __repr__(self):
        return _('[{0}] exception {1}').format(self.code, self.message % self.kwargs)


def resolveAxesStructure(view, viewTblELR):
    if isinstance(viewTblELR, (ModelEuTable, ModelTable)):
        table = viewTblELR
        for rel in view.modelXbrl.relationshipSet((XbrlConst.tableBreakdown, XbrlConst.tableBreakdownMMDD, XbrlConst.tableBreakdown201305, XbrlConst.tableBreakdown201301, XbrlConst.tableAxis2011)).fromModelObject(table):
            view.axisSubtreeRelSet = view.modelXbrl.relationshipSet((XbrlConst.tableBreakdownTree, XbrlConst.tableBreakdownTreeMMDD, XbrlConst.tableBreakdownTree201305, XbrlConst.tableDefinitionNodeSubtree, XbrlConst.tableDefinitionNodeSubtreeMMDD, XbrlConst.tableDefinitionNodeSubtree201305, XbrlConst.tableDefinitionNodeSubtree201301, XbrlConst.tableAxisSubtree2011), rel.linkrole)
            return resolveTableAxesStructure(view, table, view.modelXbrl.relationshipSet((XbrlConst.tableBreakdown, XbrlConst.tableBreakdownMMDD, XbrlConst.tableBreakdown201305, XbrlConst.tableBreakdown201301, XbrlConst.tableAxis2011), rel.linkrole))

        return (None, None, None, None)
    else:
        tblAxisRelSet = view.modelXbrl.relationshipSet(XbrlConst.euTableAxis, viewTblELR)
        if len(tblAxisRelSet.modelRelationships) > 0:
            view.axisSubtreeRelSet = view.modelXbrl.relationshipSet(XbrlConst.euAxisMember, viewTblELR)
        else:
            tblAxisRelSet = view.modelXbrl.relationshipSet((XbrlConst.tableBreakdown, XbrlConst.tableBreakdownMMDD, XbrlConst.tableBreakdown201305, XbrlConst.tableBreakdown201301, XbrlConst.tableAxis2011), viewTblELR)
            view.axisSubtreeRelSet = view.modelXbrl.relationshipSet((XbrlConst.tableBreakdownTree, XbrlConst.tableBreakdownTreeMMDD, XbrlConst.tableBreakdownTree201305, XbrlConst.tableDefinitionNodeSubtree, XbrlConst.tableDefinitionNodeSubtreeMMDD, XbrlConst.tableDefinitionNodeSubtree201305, XbrlConst.tableDefinitionNodeSubtree201301, XbrlConst.tableAxisSubtree2011), viewTblELR)
        if tblAxisRelSet is None or len(tblAxisRelSet.modelRelationships) == 0:
            view.modelXbrl.modelManager.addToLog(_('no table relationships for {0}').format(viewTblELR))
            return (None, None, None, None)
        modelRoleTypes = view.modelXbrl.roleTypes.get(viewTblELR)
        if modelRoleTypes is not None:
            if len(modelRoleTypes) > 0:
                view.roledefinition = modelRoleTypes[0].definition
                if view.roledefinition is None or view.roledefinition == '':
                    view.roledefinition = os.path.basename(viewTblELR)
        try:
            for table in tblAxisRelSet.rootConcepts:
                return resolveTableAxesStructure(view, table, tblAxisRelSet)

        except ResolutionException as ex:
            (view.modelXbrl.error)(ex.code, ex.message, exc_info=True, **ex.kwargs)

        return (None, None, None, None)


def resolveTableAxesStructure(view, table, tblAxisRelSet):
    view.dataCols = 0
    view.dataRows = 0
    view.dataFirstCol = 0
    view.dataFirstRow = 0
    view.colHdrNonStdRoles = []
    view.colHdrDocRow = False
    view.colHdrCodeRow = False
    view.colHdrRows = 0
    view.rowHdrNonStdRoles = []
    view.rowHdrCols = 0
    view.rowHdrColWidth = [0]
    view.rowNonAbstractHdrSpanMin = [0]
    view.rowHdrDocCol = False
    view.rowHdrCodeCol = False
    view.zAxisRows = 0
    view.aspectModel = table.aspectModel
    view.zmostOrdCntx = None
    view.modelTable = table
    view.topRollup = {'x':ROLLUP_NOT_ANALYZED,  'y':ROLLUP_NOT_ANALYZED}
    view.aspectEntryObjectId = 0
    view.modelTable = table
    view.rendrCntx = table.renderingXPathContext
    xTopStructuralNode = yTopStructuralNode = zTopStructuralNode = None
    tblAxisRels = tblAxisRelSet.fromModelObject(table)
    facts = view.modelXbrl.factsInInstance
    if facts:
        facts = table.filteredFacts(view.rendrCntx, view.modelXbrl.factsInInstance)
    view.breakdownNodes = defaultdict(list)
    for tblAxisRel in tblAxisRels:
        definitionNode = tblAxisRel.toModelObject
        addBreakdownNode(view, tblAxisRel.axisDisposition, definitionNode)

    for disposition in ('z', 'x', 'y'):
        for i, tblAxisRel in enumerate(tblAxisRels):
            definitionNode = tblAxisRel.toModelObject
            if tblAxisRel.axisDisposition == disposition:
                if isinstance(definitionNode, (ModelEuAxisCoord, ModelBreakdown, ModelDefinitionNode)):
                    if disposition == 'x' and xTopStructuralNode is None:
                        xTopStructuralNode = StructuralNode(None, definitionNode, definitionNode, (view.zmostOrdCntx), tableNode=table, rendrCntx=(view.rendrCntx))
                        xTopStructuralNode.hasOpenNode = False
                        if isinstance(definitionNode, (ModelBreakdown, ModelClosedDefinitionNode)):
                            if definitionNode.parentChildOrder is not None:
                                view.xAxisChildrenFirst.set(definitionNode.parentChildOrder == 'children-first')
                                view.xTopRollup = CHILD_ROLLUP_LAST if definitionNode.parentChildOrder == 'children-first' else CHILD_ROLLUP_FIRST
                        expandDefinition(view, xTopStructuralNode, definitionNode, definitionNode, 1, disposition, facts, i, tblAxisRels)
                        view.dataCols = xTopStructuralNode.leafNodeCount
                        break
            if disposition == 'y':
                if yTopStructuralNode is None:
                    yTopStructuralNode = StructuralNode(None, definitionNode, definitionNode, (view.zmostOrdCntx), tableNode=table, rendrCntx=(view.rendrCntx))
                    yTopStructuralNode.hasOpenNode = False
                    if isinstance(definitionNode, (ModelBreakdown, ModelClosedDefinitionNode)):
                        if definitionNode.parentChildOrder is not None:
                            view.yAxisChildrenFirst.set(definitionNode.parentChildOrder == 'children-first')
                            view.yTopRollup = CHILD_ROLLUP_LAST if definitionNode.parentChildOrder == 'children-first' else CHILD_ROLLUP_FIRST
                    expandDefinition(view, yTopStructuralNode, definitionNode, definitionNode, 1, disposition, facts, i, tblAxisRels)
                    view.dataRows = yTopStructuralNode.leafNodeCount
                    break
                else:
                    if disposition == 'z':
                        if zTopStructuralNode is None:
                            zTopStructuralNode = StructuralNode(None, definitionNode, definitionNode, tableNode=table, rendrCntx=(view.rendrCntx))
                            zTopStructuralNode._choiceStructuralNodes = []
                            zTopStructuralNode.hasOpenNode = False
                            expandDefinition(view, zTopStructuralNode, definitionNode, definitionNode, 1, disposition, facts, i, tblAxisRels)
                            break

    view.colHdrTopRow = view.zAxisRows + 1
    for i in range(view.rowHdrCols):
        if view.rowNonAbstractHdrSpanMin[i]:
            lastRowMinWidth = view.rowNonAbstractHdrSpanMin[i] - sum(view.rowHdrColWidth[i] for j in range(i, view.rowHdrCols - 1))
            if lastRowMinWidth > view.rowHdrColWidth[(view.rowHdrCols - 1)]:
                view.rowHdrColWidth[view.rowHdrCols - 1] = lastRowMinWidth

    view.rowHdrWrapLength = 200 + sum(view.rowHdrColWidth[:view.rowHdrCols + 1])
    view.dataFirstRow = view.colHdrTopRow + view.colHdrRows + len(view.colHdrNonStdRoles)
    view.dataFirstCol = 1 + view.rowHdrCols + len(view.rowHdrNonStdRoles)
    for hdrNonStdRoles in (view.colHdrNonStdRoles, view.rowHdrNonStdRoles):
        iCodeRole = -1
        for i, hdrNonStdRole in enumerate(hdrNonStdRoles):
            if 'code' in os.path.basename(hdrNonStdRole).lower():
                iCodeRole = i
                break

        if iCodeRole >= 0 and len(hdrNonStdRoles) > 1 and iCodeRole < len(hdrNonStdRoles) - 1:
            del hdrNonStdRoles[iCodeRole]
            hdrNonStdRoles.append(hdrNonStdRole)

    if view.topRollup['x']:
        view.xAxisChildrenFirst.set(view.topRollup['x'] == CHILD_ROLLUP_LAST)
    if view.topRollup['y']:
        view.yAxisChildrenFirst.set(view.topRollup['y'] == CHILD_ROLLUP_LAST)
    return (tblAxisRelSet, xTopStructuralNode, yTopStructuralNode, zTopStructuralNode)


def sortkey(obj):
    if isinstance(obj, ModelObject):
        return obj.objectIndex
    else:
        return obj


def addBreakdownNode(view, disposition, node):
    if isinstance(node, ModelBreakdown):
        axisBreakdowns = view.breakdownNodes[disposition]
        if node not in axisBreakdowns:
            axisBreakdowns.append(node)


def childContainsOpenNodes(childStructuralNode):
    if isinstance(childStructuralNode.definitionNode, ModelFilterDefinitionNode):
        if childStructuralNode.isLabeled or any([node.isEntryPrototype(default=False) for node in childStructuralNode.childStructuralNodes]):
            return True
    for node in childStructuralNode.childStructuralNodes:
        if childContainsOpenNodes(node):
            return True

    return False


def expandDefinition(view, structuralNode, breakdownNode, definitionNode, depth, axisDisposition, facts, i=None, tblAxisRels=None, processOpenDefinitionNode=True):
    subtreeRelationships = view.axisSubtreeRelSet.fromModelObject(definitionNode)

    def checkLabelWidth(structuralNode, checkBoundFact=False):
        if axisDisposition == 'y':
            label = structuralNode.header(lang=(view.lang), returnGenLabel=(not checkBoundFact),
              returnMsgFormatString=(not checkBoundFact))
            if label:
                widestWordLen = max(len(w) * RENDER_UNITS_PER_CHAR for w in label.split())
                while structuralNode.depth >= len(view.rowHdrColWidth):
                    view.rowHdrColWidth.append(0)

                if definitionNode.isAbstract or not subtreeRelationships:
                    if widestWordLen > view.rowHdrColWidth[structuralNode.depth]:
                        view.rowHdrColWidth[structuralNode.depth] = widestWordLen
                elif widestWordLen > view.rowNonAbstractHdrSpanMin[structuralNode.depth]:
                    view.rowNonAbstractHdrSpanMin[structuralNode.depth] = widestWordLen

    if axisDisposition == 'z':
        if structuralNode.aspects is None:
            structuralNode.aspects = view.zOrdinateChoices.get(definitionNode, None)
    if structuralNode and isinstance(definitionNode, (ModelBreakdown, ModelEuAxisCoord, ModelDefinitionNode)):
        try:
            try:
                ordCardinality, ordDepth = definitionNode.cardinalityAndDepth(structuralNode, handleXPathException=False)
            except XPathException as ex:
                if isinstance(definitionNode, ModelConceptRelationshipDefinitionNode):
                    view.modelXbrl.error('xbrlte:expressionNotCastableToRequiredType', (_('Relationship node %(xlinkLabel)s expression not castable to required type (%(xpathError)s)')),
                      modelObject=(
                     view.modelTable, definitionNode),
                      xlinkLabel=(definitionNode.xlinkLabel),
                      axis=(definitionNode.localName),
                      xpathError=(str(ex)))
                    return

            if not definitionNode.isAbstract and isinstance(definitionNode, ModelClosedDefinitionNode) and ordCardinality == 0:
                view.modelXbrl.error('xbrlte:closedDefinitionNodeZeroCardinality', (_('Closed definition node %(xlinkLabel)s does not contribute at least one structural node')),
                  modelObject=(
                 view.modelTable, definitionNode),
                  xlinkLabel=(definitionNode.xlinkLabel),
                  axis=(definitionNode.localName))
            nestedDepth = depth + ordDepth
            cartesianProductNestedArgs = [
             view, nestedDepth, axisDisposition, facts, tblAxisRels, i]
            if axisDisposition == 'z':
                if depth == 1:
                    view.zAxisRows += 1
            else:
                if axisDisposition == 'x':
                    if ordDepth:
                        if nestedDepth - 1 > view.colHdrRows:
                            view.colHdrRows = nestedDepth - 1
                    hdrNonStdRoles = view.colHdrNonStdRoles
                else:
                    if axisDisposition == 'y':
                        if ordDepth:
                            if nestedDepth - 1 > view.rowHdrCols:
                                view.rowHdrCols = nestedDepth - 1
                                for j in range(1 + ordDepth):
                                    view.rowHdrColWidth.append(RENDER_UNITS_PER_CHAR)
                                    view.rowNonAbstractHdrSpanMin.append(0)

                            checkLabelWidth(structuralNode, checkBoundFact=False)
                        hdrNonStdRoles = view.rowHdrNonStdRoles
            if axisDisposition in ('x', 'y'):
                hdrNonStdPosition = -1
                for rel in view.modelXbrl.relationshipSet(XbrlConst.elementLabel).fromModelObject(definitionNode):
                    if isinstance(rel.toModelObject, ModelResource):
                        if rel.toModelObject.role != XbrlConst.genStandardLabel:
                            labelLang = rel.toModelObject.xmlLang
                            labelRole = rel.toModelObject.role
                            if labelLang == view.lang or labelLang.startswith(view.lang) or view.lang.startswith(labelLang) or 'code' in labelRole:
                                labelRole = rel.toModelObject.role
                                if labelRole in hdrNonStdRoles:
                                    hdrNonStdPosition = hdrNonStdRoles.index(labelRole)
                                else:
                                    hdrNonStdRoles.insert(hdrNonStdPosition + 1, labelRole)

            isCartesianProductExpanded = False
            if not isinstance(definitionNode, ModelFilterDefinitionNode):
                isCartesianProductExpanded = True
                for axisSubtreeRel in subtreeRelationships:
                    childDefinitionNode = axisSubtreeRel.toModelObject
                    if childDefinitionNode.isRollUp:
                        structuralNode.rollUpStructuralNode = StructuralNode(structuralNode, breakdownNode, childDefinitionNode)
                        if not structuralNode.childStructuralNodes:
                            structuralNode.subtreeRollUp = CHILD_ROLLUP_FIRST
                        else:
                            structuralNode.subtreeRollUp = CHILD_ROLLUP_LAST
                        if not view.topRollup.get(axisDisposition):
                            view.topRollup[axisDisposition] = structuralNode.subtreeRollUp
                    else:
                        if isinstance(definitionNode, (ModelBreakdown, ModelCompositionDefinitionNode)):
                            if isinstance(childDefinitionNode, ModelRelationshipDefinitionNode):
                                childStructuralNode = structuralNode
                    childStructuralNode = StructuralNode(structuralNode, breakdownNode, childDefinitionNode)
                    if axisDisposition != 'z':
                        structuralNode.childStructuralNodes.append(childStructuralNode)
                    if axisDisposition != 'z':
                        expandDefinition(view, childStructuralNode, breakdownNode, childDefinitionNode, depth + ordDepth, axisDisposition, facts, i, tblAxisRels)
                        if not childContainsOpenNodes(childStructuralNode):
                            cartesianProductExpander(childStructuralNode, *cartesianProductNestedArgs)
                    else:
                        childStructuralNode.indent = depth - 1
                        if structuralNode.choiceStructuralNodes is not None:
                            structuralNode.choiceStructuralNodes.append(childStructuralNode)
                        expandDefinition(view, childStructuralNode, breakdownNode, childDefinitionNode, depth + 1, axisDisposition, facts)

            if processOpenDefinitionNode:
                if isinstance(definitionNode, ModelRelationshipDefinitionNode):
                    structuralNode.isLabeled = False
                    selfStructuralNodes = {} if definitionNode.axis.endswith('-or-self') else None
                    for rel in definitionNode.relationships(structuralNode):
                        if not isinstance(rel, list):
                            relChildStructuralNode = addRelationship(breakdownNode, definitionNode, rel, structuralNode, cartesianProductNestedArgs, selfStructuralNodes)
                        else:
                            addRelationships(breakdownNode, definitionNode, rel, relChildStructuralNode, cartesianProductNestedArgs)

                    if axisDisposition == 'z':
                        if structuralNode.choiceStructuralNodes:
                            if structuralNode.choiceStructuralNodes[0].definitionNode == definitionNode:
                                del structuralNode.choiceStructuralNodes[0]

                        def flattenChildNodesToChoices(childStructuralNodes, indent):
                            while childStructuralNodes:
                                choiceStructuralNode = childStructuralNodes.pop(0)
                                choiceStructuralNode.indent = indent
                                structuralNode.choiceStructuralNodes.append(choiceStructuralNode)
                                flattenChildNodesToChoices(choiceStructuralNode.childStructuralNodes, indent + 1)

                        if structuralNode.childStructuralNodes:
                            flattenChildNodesToChoices(structuralNode.childStructuralNodes, 0)
                    if isinstance(definitionNode, ModelConceptRelationshipDefinitionNode):
                        if definitionNode._sourceQname != XbrlConst.qnXfiRoot:
                            if definitionNode._sourceQname not in view.modelXbrl.qnameConcepts:
                                view.modelXbrl.error('xbrlte:invalidConceptRelationshipSource', (_('Concept relationship rule node %(xlinkLabel)s source %(source)s does not refer to an existing concept.')),
                                  modelObject=definitionNode,
                                  xlinkLabel=(definitionNode.xlinkLabel),
                                  source=(definitionNode._sourceQname))
                    else:
                        if isinstance(definitionNode, ModelDimensionRelationshipDefinitionNode):
                            dim = view.modelXbrl.qnameConcepts.get(definitionNode._dimensionQname)
                            if dim is None or not dim.isExplicitDimension:
                                view.modelXbrl.error('xbrlte:invalidExplicitDimensionQName', (_('Dimension relationship rule node %(xlinkLabel)s dimension %(dimension)s does not refer to an existing explicit dimension.')),
                                  modelObject=definitionNode,
                                  xlinkLabel=(definitionNode.xlinkLabel),
                                  dimension=(definitionNode._dimensionQname))
                            domMbr = view.modelXbrl.qnameConcepts.get(definitionNode._sourceQname)
                            if domMbr is None or not domMbr.isDomainMember:
                                view.modelXbrl.error('xbrlte:invalidDimensionRelationshipSource', (_('Dimension relationship rule node %(xlinkLabel)s source %(source)s does not refer to an existing domain member.')),
                                  modelObject=definitionNode,
                                  xlinkLabel=(definitionNode.xlinkLabel),
                                  source=(definitionNode._sourceQname))
                    if definitionNode._axis in ('child', 'child-or-self', 'parent',
                                                'parent-or-self', 'sibling', 'sibling-or-self'):
                        if not isinstance(definitionNode._generations, _NUM_TYPES) or definitionNode._generations > 1:
                            view.modelXbrl.error('xbrlte:relationshipNodeTooManyGenerations ', (_('Relationship rule node %(xlinkLabel)s formulaAxis %(axis)s implies a single generation tree walk but generations %(generations)s is greater than one.')),
                              modelObject=definitionNode,
                              xlinkLabel=(definitionNode.xlinkLabel),
                              axis=(definitionNode._axis),
                              generations=(definitionNode._generations))
                else:
                    if isinstance(definitionNode, ModelSelectionDefinitionNode):
                        structuralNode.setHasOpenNode()
                        structuralNode.isLabeled = False
                        isCartesianProductExpanded = True
                        varQn = definitionNode.variableQname
                        if varQn:
                            selections = sorted((structuralNode.evaluate(definitionNode, definitionNode.evaluate) or []), key=(lambda obj: sortkey(obj)))
                            if isinstance(selections, (list, set, tuple)):
                                if len(selections) > 1:
                                    for selection in selections:
                                        childStructuralNode = StructuralNode(structuralNode, breakdownNode, definitionNode, contextItemFact=selection)
                                        childStructuralNode.variables[varQn] = selection
                                        childStructuralNode.indent = 0
                                        if axisDisposition == 'z':
                                            structuralNode.choiceStructuralNodes.append(childStructuralNode)
                                            childStructuralNode.zSelection = True
                                        else:
                                            structuralNode.childStructuralNodes.append(childStructuralNode)
                                            expandDefinition(view, childStructuralNode, breakdownNode, definitionNode, depth, axisDisposition, facts, processOpenDefinitionNode=False)
                                            cartesianProductExpander(childStructuralNode, *cartesianProductNestedArgs)

                            structuralNode.variables[varQn] = selections
                    else:
                        if isinstance(definitionNode, ModelFilterDefinitionNode):
                            structuralNode.setHasOpenNode()
                            structuralNode.isLabeled = False
                            isCartesianProductExpanded = True
                            structuralNode.abstract = True
                            filteredFactsPartitions = structuralNode.evaluate(definitionNode, (definitionNode.filteredFactsPartitions),
                              evalArgs=(
                             facts,))
                            if structuralNode._rendrCntx.formulaOptions.traceVariableFilterWinnowing:
                                view.modelXbrl.info('table:trace', (_('Filter node %(xlinkLabel)s facts partitions: %(factsPartitions)s')),
                                  modelObject=definitionNode,
                                  xlinkLabel=(definitionNode.xlinkLabel),
                                  factsPartitions=(str(filteredFactsPartitions)))
                            if axisDisposition != 'z':
                                childList = structuralNode.childStructuralNodes
                                if structuralNode.isEntryPrototype(default=True):
                                    for i in range(getattr(view, 'openBreakdownLines', 0 if filteredFactsPartitions else 1)):
                                        view.aspectEntryObjectId += 1
                                        filteredFactsPartitions.append([FactPrototype(view, {'aspectEntryObjectId': OPEN_ASPECT_ENTRY_SURROGATE + str(view.aspectEntryObjectId)})])
                                        if structuralNode.isEntryPrototype(default=False):
                                            break

                            else:
                                childList = structuralNode.choiceStructuralNodes
                            for factsPartition in filteredFactsPartitions:
                                childStructuralNode = StructuralNode(structuralNode, breakdownNode, definitionNode, contextItemFact=(factsPartition[0]))
                                childStructuralNode.factsPartition = factsPartition
                                childStructuralNode.indent = 0
                                childStructuralNode.depth -= 1
                                childList.append(childStructuralNode)
                                checkLabelWidth(childStructuralNode, checkBoundFact=True)
                                cartesianProductNestedArgs[3] = factsPartition
                                if subtreeRelationships:
                                    for axisSubtreeRel in subtreeRelationships:
                                        child2DefinitionNode = axisSubtreeRel.toModelObject
                                        child2StructuralNode = StructuralNode(childStructuralNode, breakdownNode, child2DefinitionNode)
                                        childStructuralNode.childStructuralNodes.append(child2StructuralNode)
                                        expandDefinition(view, child2StructuralNode, breakdownNode, child2DefinitionNode, depth + ordDepth, axisDisposition, factsPartition)
                                        cartesianProductExpander(child2StructuralNode, *cartesianProductNestedArgs)

                                else:
                                    cartesianProductExpander(childStructuralNode, *cartesianProductNestedArgs)

                            childList.sort(key=(lambda childStructuralNode: childStructuralNode.header(lang=(view.lang), returnGenLabel=False,
                              returnMsgFormatString=False) or ''))
                        else:
                            if isinstance(definitionNode, ModelTupleDefinitionNode):
                                structuralNode.abstract = True
                                matchingTupleFacts = structuralNode.evaluate(definitionNode, (definitionNode.filteredFacts),
                                  evalArgs=(
                                 facts,))
                                for tupleFact in matchingTupleFacts:
                                    childStructuralNode = StructuralNode(structuralNode, breakdownNode, definitionNode, contextItemFact=tupleFact)
                                    childStructuralNode.indent = 0
                                    structuralNode.childStructuralNodes.append(childStructuralNode)
                                    expandDefinition(view, childStructuralNode, breakdownNode, definitionNode, depth, axisDisposition, [tupleFact])

                                if structuralNode.childStructuralNodes:
                                    if any(sOC.header(lang=(view.lang)) for sOC in structuralNode.childStructuralNodes):
                                        structuralNode.childStructuralNodes.sort(key=(lambda childStructuralNode: childStructuralNode.header(lang=(view.lang)) or ''))
                            else:
                                if isinstance(definitionNode, ModelRuleDefinitionNode):
                                    for constraintSet in definitionNode.constraintSets.values():
                                        _aspectsCovered = constraintSet.aspectsCovered()
                                        for aspect in _aspectsCovered:
                                            if constraintSet.aspectValueDependsOnVars(aspect) or aspect == Aspect.CONCEPT:
                                                conceptQname = definitionNode.aspectValue(view.rendrCntx, Aspect.CONCEPT)
                                                concept = view.modelXbrl.qnameConcepts.get(conceptQname)
                                                if concept is None or not concept.isItem or concept.isDimensionItem or concept.isHypercubeItem:
                                                    view.modelXbrl.error('xbrlte:invalidQNameAspectValue', (_('Rule node %(xlinkLabel)s specifies concept %(concept)s does not refer to an existing primary item concept.')),
                                                      modelObject=definitionNode,
                                                      xlinkLabel=(definitionNode.xlinkLabel),
                                                      concept=conceptQname)
                                            elif isinstance(aspect, QName):
                                                memQname = definitionNode.aspectValue(view.rendrCntx, aspect)
                                                mem = view.modelXbrl.qnameConcepts.get(memQname)
                                            if isinstance(memQname, QName):
                                                if mem is None or not mem.isDomainMember:
                                                    if memQname != XbrlConst.qnFormulaDimensionSAV:
                                                        view.modelXbrl.error('xbrlte:invalidQNameAspectValue', (_('Rule node %(xlinkLabel)s specifies domain member %(concept)s does not refer to an existing domain member concept.')),
                                                          modelObject=definitionNode,
                                                          xlinkLabel=(definitionNode.xlinkLabel),
                                                          concept=memQname)

                                    if not definitionNode.constraintSets:
                                        view.modelXbrl.error('xbrlte:incompleteAspectRule', (_('Rule node %(xlinkLabel)s does not specify an aspect value.')),
                                          modelObject=definitionNode,
                                          xlinkLabel=(definitionNode.xlinkLabel))
                        if axisDisposition == 'z':
                            if structuralNode.choiceStructuralNodes:
                                choiceNodeIndex = view.zOrdinateChoices.get(definitionNode, 0)
                                if isinstance(choiceNodeIndex, dict):
                                    structuralNode.aspects = choiceNodeIndex
                                    structuralNode.choiceNodeIndex = -1
                                else:
                                    if choiceNodeIndex < len(structuralNode.choiceStructuralNodes):
                                        structuralNode.choiceNodeIndex = choiceNodeIndex
                                    else:
                                        structuralNode.choiceNodeIndex = 0
                            view.zmostOrdCntx = structuralNode
                        if not isCartesianProductExpanded or axisDisposition == 'z' and structuralNode.choiceStructuralNodes is not None:
                            cartesianProductExpander(structuralNode, *cartesianProductNestedArgs)
                    if not structuralNode.childStructuralNodes:
                        subOrdContext = StructuralNode(structuralNode, breakdownNode, definitionNode)
        except ResolutionException as ex:
            if sys.version[0] >= '3':
                raise ex.with_traceback(ex.__traceback__)
            else:
                raise ex
        except Exception as ex:
            e = ResolutionException('arelle:resolutionException', (_('Exception in resolution of definition node %(node)s: %(error)s')),
              modelObject=definitionNode,
              node=(definitionNode.qname),
              error=(str(ex)))
            if sys.version[0] >= '3':
                raise e.with_traceback(ex.__traceback__)
            else:
                raise e


def cartesianProductExpander(childStructuralNode, view, depth, axisDisposition, facts, tblAxisRels, i):
    if i is not None:
        for j, tblRel in enumerate(tblAxisRels[i + 1:]):
            tblObj = tblRel.toModelObject
            if isinstance(tblObj, (ModelEuAxisCoord, ModelDefinitionNode)):
                if axisDisposition == tblRel.axisDisposition:
                    if axisDisposition == 'z':
                        subOrdTblCntx = StructuralNode(childStructuralNode, tblObj, tblObj)
                        subOrdTblCntx._choiceStructuralNodes = []
                        subOrdTblCntx.indent = 0
                        depth = 0
                        childStructuralNode.childStructuralNodes.append(subOrdTblCntx)
                    else:
                        subOrdTblCntx = childStructuralNode
                    if isinstance(childStructuralNode.definitionNode, ModelClosedDefinitionNode):
                        matchingFacts = childStructuralNode.evaluate((childStructuralNode.definitionNode), (childStructuralNode.definitionNode.filteredFacts),
                          evalArgs=(
                         facts,))
                    else:
                        matchingFacts = facts
                    subOrdTblCntx.abstract = True
                    expandDefinition(view, subOrdTblCntx, tblObj, tblObj, depth, axisDisposition, matchingFacts, j + i + 1, tblAxisRels)
                    break


def addRelationship(breakdownNode, relDefinitionNode, rel, structuralNode, cartesianProductNestedArgs, selfStructuralNodes=None):
    variableQname = relDefinitionNode.variableQname
    conceptQname = relDefinitionNode.conceptQname
    coveredAspect = relDefinitionNode.coveredAspect(structuralNode)
    if not coveredAspect:
        return
    else:
        if selfStructuralNodes is not None:
            fromConceptQname = rel.fromModelObject.qname
            if fromConceptQname in selfStructuralNodes:
                childStructuralNode = selfStructuralNodes[fromConceptQname]
            else:
                childStructuralNode = StructuralNode(structuralNode, breakdownNode, relDefinitionNode)
                structuralNode.childStructuralNodes.append(childStructuralNode)
                selfStructuralNodes[fromConceptQname] = childStructuralNode
                if variableQname:
                    childStructuralNode.variables[variableQname] = []
                if conceptQname:
                    childStructuralNode.variables[conceptQname] = fromConceptQname
                childStructuralNode.aspects[coveredAspect] = fromConceptQname
            relChildStructuralNode = StructuralNode(childStructuralNode, breakdownNode, relDefinitionNode)
            childStructuralNode.childStructuralNodes.append(relChildStructuralNode)
        else:
            relChildStructuralNode = StructuralNode(structuralNode, breakdownNode, relDefinitionNode)
            structuralNode.childStructuralNodes.append(relChildStructuralNode)
        preferredLabel = rel.preferredLabel
        if preferredLabel == XbrlConst.periodStartLabel:
            relChildStructuralNode.tagSelector = 'table.periodStart'
        else:
            if preferredLabel == XbrlConst.periodStartLabel:
                relChildStructuralNode.tagSelector = 'table.periodEnd'
        if variableQname:
            relChildStructuralNode.variables[variableQname] = rel
        toConceptQname = rel.toModelObject.qname
        if conceptQname:
            relChildStructuralNode.variables[conceptQname] = toConceptQname
        relChildStructuralNode.aspects[coveredAspect] = toConceptQname
        cartesianProductExpander(relChildStructuralNode, *cartesianProductNestedArgs)
        return relChildStructuralNode


def addRelationships(breakdownNode, relDefinitionNode, rels, structuralNode, cartesianProductNestedArgs):
    childStructuralNode = None
    for rel in rels:
        if not isinstance(rel, list):
            childStructuralNode = addRelationship(breakdownNode, relDefinitionNode, rel, structuralNode, cartesianProductNestedArgs)
        else:
            if childStructuralNode is None:
                childStructuralNode = StructuralNode(structuralNode, breakdownNode, relDefinitionNode)
                structuralNode.childStructuralNodes.append(childStructuralNode)
                addRelationships(breakdownNode, relDefinitionNode, rel, childStructuralNode, cartesianProductNestedArgs)
            else:
                addRelationships(breakdownNode, relDefinitionNode, rel, childStructuralNode, cartesianProductNestedArgs)