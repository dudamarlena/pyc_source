# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/RenderingEvaluator.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 16837 bytes
__doc__ = '\nCreated on Jun 6, 2012\n\n@author: Mark V Systems Limited\n(c) Copyright 2012 Mark V Systems Limited, All rights reserved.\n'
from arelle import XPathContext, XbrlConst, XmlUtil
from arelle.ModelFormulaObject import aspectModels, aspectStr, Aspect
from arelle.ModelRenderingObject import CHILD_ROLLUP_FIRST, CHILD_ROLLUP_LAST, ModelDefinitionNode, ModelEuAxisCoord, ModelBreakdown, ModelClosedDefinitionNode, ModelRuleDefinitionNode, ModelFilterDefinitionNode, ModelDimensionRelationshipDefinitionNode
from arelle.ModelValue import QName

def init(modelXbrl):
    from arelle import ValidateXbrlDimensions, ValidateFormula, FormulaEvaluator, ModelDocument
    ValidateXbrlDimensions.loadDimensionDefaults(modelXbrl)
    hasXbrlTables = False
    for baseSetKey in modelXbrl.baseSets.keys():
        arcrole, ELR, linkqname, arcqname = baseSetKey
        if ELR and linkqname and arcqname and XbrlConst.isTableRenderingArcrole(arcrole):
            ValidateFormula.checkBaseSet(modelXbrl, arcrole, ELR, modelXbrl.relationshipSet(arcrole, ELR, linkqname, arcqname))
            if arcrole in (XbrlConst.tableBreakdown, XbrlConst.tableBreakdownMMDD, XbrlConst.tableBreakdown201305, XbrlConst.tableBreakdown201301, XbrlConst.tableAxis2011):
                hasXbrlTables = True

    if modelXbrl.modelDocument.type == ModelDocument.Type.INSTANCE:
        instance = None
    else:
        instance = ModelDocument.create(modelXbrl, ModelDocument.Type.INSTANCE, 'dummy.xml', ('http://www.xbrl.org/2003/xbrl-instance-2003-12-31.xsd', ))
    if hasXbrlTables:
        FormulaEvaluator.init()
        modelXbrl.rendrCntx = XPathContext.create(modelXbrl, instance)
        modelXbrl.profileStat(None)
        modelXbrl.parameters = modelXbrl.modelManager.formulaOptions.typedParameters(modelXbrl.prefixedNamespaces)
        ValidateFormula.validate(modelXbrl, xpathContext=modelXbrl.rendrCntx, parametersOnly=True, statusMsg=_('compiling rendering tables'))
        for msgArcrole in (XbrlConst.tableDefinitionNodeMessage201301, XbrlConst.tableDefinitionNodeSelectionMessage201301,
         XbrlConst.tableAxisMessage2011, XbrlConst.tableAxisSelectionMessage2011):
            for msgRel in modelXbrl.relationshipSet(msgArcrole).modelRelationships:
                ValidateFormula.checkMessageExpressions(modelXbrl, msgRel.toModelObject)

        for modelTable in modelXbrl.modelRenderingTables:
            modelTable.fromInstanceQnames = None
            modelTable.compile()
            hasNsWithAspectModel = modelTable.namespaceURI in (XbrlConst.euRend, XbrlConst.table2011, XbrlConst.table201301, XbrlConst.table201305)
            if modelTable.aspectModel not in ('non-dimensional', 'dimensional') and hasNsWithAspectModel:
                modelXbrl.error('xbrlte:unknownAspectModel', _('Table %(xlinkLabel)s, aspect model %(aspectModel)s not recognized'), modelObject=modelTable, xlinkLabel=modelTable.xlinkLabel, aspectModel=modelTable.aspectModel)
            else:
                modelTable.priorAspectAxisDisposition = {}
                oppositeAspectModel = (_DICT_SET({'dimensional', 'non-dimensional'}) - _DICT_SET({modelTable.aspectModel})).pop()
                if hasNsWithAspectModel:
                    uncoverableAspects = aspectModels[oppositeAspectModel] - aspectModels[modelTable.aspectModel]
                else:
                    uncoverableAspects = ()
                aspectsCovered = set()
                for tblAxisRel in modelXbrl.relationshipSet((XbrlConst.tableBreakdown, XbrlConst.tableBreakdownMMDD, XbrlConst.tableBreakdown201305, XbrlConst.tableBreakdown201301, XbrlConst.tableAxis2011)).fromModelObject(modelTable):
                    breakdownAspectsCovered = set()
                    hasCoveredAspect = checkBreakdownDefinitionNode(modelXbrl, modelTable, tblAxisRel, tblAxisRel.axisDisposition, uncoverableAspects, breakdownAspectsCovered)
                    aspectsCovered |= breakdownAspectsCovered
                    checkBreakdownLeafNodeAspects(modelXbrl, modelTable, tblAxisRel, set(), breakdownAspectsCovered)

                if Aspect.CONCEPT not in aspectsCovered and not hasNsWithAspectModel:
                    modelXbrl.error('xbrlte:tableMissingConceptAspect', _('Table %(xlinkLabel)s does not include the concept aspect as one of its participating aspects'), modelObject=modelTable, xlinkLabel=modelTable.xlinkLabel)
                del modelTable.priorAspectAxisDisposition
                parameterNames = {}
                for tblParamRel in modelXbrl.relationshipSet((XbrlConst.tableParameter, XbrlConst.tableParameterMMDD)).fromModelObject(modelTable):
                    parameterName = tblParamRel.variableQname
                    if parameterName in parameterNames:
                        modelXbrl.error('xbrlte:tableParameterNameClash ', _('Table %(xlinkLabel)s has parameter name clash for variable %(name)s'), modelObject=(
                         modelTable, tblParamRel, parameterNames[parameterName]), xlinkLabel=modelTable.xlinkLabel, name=parameterName)
                    else:
                        parameterNames[parameterName] = tblParamRel

        modelXbrl.profileStat(_('compileTables'))


def checkBreakdownDefinitionNode(modelXbrl, modelTable, tblAxisRel, tblAxisDisposition, uncoverableAspects, aspectsCovered):
    definitionNode = tblAxisRel.toModelObject
    hasCoveredAspect = False
    if isinstance(definitionNode, (ModelDefinitionNode, ModelEuAxisCoord)):
        for aspect in definitionNode.aspectsCovered():
            aspectsCovered.add(aspect)
            if aspect in uncoverableAspects or isinstance(aspect, QName) and modelTable.aspectModel == 'non-dimensional':
                modelXbrl.error('xbrlte:axisAspectModelMismatch', _('%(definitionNode)s %(xlinkLabel)s, aspect model %(aspectModel)s, aspect %(aspect)s not allowed'), modelObject=modelTable, definitionNode=definitionNode.localName, xlinkLabel=definitionNode.xlinkLabel, aspectModel=modelTable.aspectModel, aspect=str(aspect) if isinstance(aspect, QName) else Aspect.label[aspect])
            hasCoveredAspect = True
            if aspect in modelTable.priorAspectAxisDisposition:
                otherAxisDisposition, otherDefinitionNode = modelTable.priorAspectAxisDisposition[aspect]
                if tblAxisDisposition != otherAxisDisposition and aspect != Aspect.DIMENSIONS:
                    modelXbrl.error('xbrlte:aspectClashBetweenBreakdowns', _('%(definitionNode)s %(xlinkLabel)s, aspect %(aspect)s defined on axes of disposition %(axisDisposition)s and %(axisDisposition2)s'), modelObject=(
                     modelTable, definitionNode, otherDefinitionNode), definitionNode=definitionNode.localName, xlinkLabel=definitionNode.xlinkLabel, axisDisposition=tblAxisDisposition, axisDisposition2=otherAxisDisposition, aspect=str(aspect) if isinstance(aspect, QName) else Aspect.label[aspect])
            else:
                modelTable.priorAspectAxisDisposition[aspect] = (
                 tblAxisDisposition, definitionNode)

        ruleSetChildren = XmlUtil.children(definitionNode, definitionNode.namespaceURI, 'ruleSet')
        if definitionNode.isMerged:
            if ruleSetChildren:
                modelXbrl.error('xbrlte:mergedRuleNodeWithTaggedRuleSet', _('Merged %(definitionNode)s %(xlinkLabel)s has tagged rule set(s)'), modelObject=[
                 modelTable, definitionNode] + ruleSetChildren, definitionNode=definitionNode.localName, xlinkLabel=definitionNode.xlinkLabel)
            labelRels = modelXbrl.relationshipSet(XbrlConst.elementLabel).fromModelObject(definitionNode)
            if labelRels:
                modelXbrl.error('xbrlte:invalidUseOfLabel', _('Merged %(definitionNode)s %(xlinkLabel)s has label(s)'), modelObject=[
                 modelTable, definitionNode] + [r.toModelObject for r in labelRels], definitionNode=definitionNode.localName, xlinkLabel=definitionNode.xlinkLabel)
            if not definitionNode.isAbstract:
                modelXbrl.error('xbrlte:nonAbstractMergedRuleNode', _('Merged %(definitionNode)s %(xlinkLabel)s is not abstract'), modelObject=(
                 modelTable, definitionNode), definitionNode=definitionNode.localName, xlinkLabel=definitionNode.xlinkLabel)
    if isinstance(definitionNode, ModelRuleDefinitionNode):
        tagConstraintSets = {}
        otherConstraintSet = None
        for ruleSet in XmlUtil.children(definitionNode, definitionNode.namespaceURI, 'ruleSet'):
            tag = ruleSet.tagName
            if tag is not None:
                for aspect in ruleSet.aspectsCovered():
                    if aspect != Aspect.DIMENSIONS:
                        modelTable.aspectsInTaggedConstraintSets.add(aspect)

            if tag in tagConstraintSets:
                modelXbrl.error('xbrlte:duplicateTag', _('%(definitionNode)s %(xlinkLabel)s duplicate rule set tags %(tag)s'), modelObject=(
                 modelTable, definitionNode, tagConstraintSets[tag], ruleSet), definitionNode=definitionNode.localName, xlinkLabel=definitionNode.xlinkLabel, tag=tag)
            else:
                tagConstraintSets[tag] = ruleSet

        for tag, constraintSet in definitionNode.constraintSets.items():
            if otherConstraintSet is None:
                otherConstraintSet = constraintSet
            elif otherConstraintSet.aspectsCovered() != constraintSet.aspectsCovered():
                modelXbrl.error('xbrlte:constraintSetAspectMismatch', _('%(definitionNode)s %(xlinkLabel)s constraint set mismatches between %(tag1)s and %(tag2)s in constraints %(aspects)s'), modelObject=(
                 modelTable, definitionNode, otherConstraintSet, constraintSet), definitionNode=definitionNode.localName, xlinkLabel=definitionNode.xlinkLabel, tag1=getattr(otherConstraintSet, 'tagName', '(no tag)'), tag2=getattr(constraintSet, 'tagName', '(no tag)'), aspects=', '.join(aspectStr(aspect) for aspect in otherConstraintSet.aspectsCovered() ^ constraintSet.aspectsCovered() if aspect != Aspect.DIMENSIONS))

    if isinstance(definitionNode, ModelDimensionRelationshipDefinitionNode):
        hasCoveredAspect = True
        if modelTable.aspectModel == 'non-dimensional':
            modelXbrl.error('xbrlte:axisAspectModelMismatch', _("DimensionRelationship axis %(xlinkLabel)s can't be used in non-dimensional aspect model"), modelObject=(
             modelTable, definitionNode), xlinkLabel=definitionNode.xlinkLabel)
    definitionNodeHasChild = False
    for axisSubtreeRel in modelXbrl.relationshipSet((XbrlConst.tableBreakdownTree, XbrlConst.tableBreakdownTreeMMDD, XbrlConst.tableBreakdownTree201305, XbrlConst.tableDefinitionNodeSubtree, XbrlConst.tableDefinitionNodeSubtreeMMDD, XbrlConst.tableDefinitionNodeSubtree201305, XbrlConst.tableDefinitionNodeSubtree201301, XbrlConst.tableAxisSubtree2011)).fromModelObject(definitionNode):
        if checkBreakdownDefinitionNode(modelXbrl, modelTable, axisSubtreeRel, tblAxisDisposition, uncoverableAspects, aspectsCovered):
            hasCoveredAspect = True
        definitionNodeHasChild = True

    if isinstance(definitionNode, ModelFilterDefinitionNode):
        for aspect in definitionNode.aspectsCovered():
            if isinstance(aspect, QName):
                concept = modelXbrl.qnameConcepts.get(aspect)
                if concept is None or not concept.isDimensionItem:
                    modelXbrl.error('xbrlte:invalidDimensionQNameOnAspectNode', _('Aspect node %(xlinkLabel)s dimensional aspect %(dimension)s is not a dimension'), modelObject=(
                     modelTable, definitionNode), xlinkLabel=definitionNode.xlinkLabel, dimension=aspect)

    if not definitionNodeHasChild:
        if definitionNode.namespaceURI in ('http://www.eurofiling.info/2010/rendering',
                                           'http://xbrl.org/2011/table') and not hasCoveredAspect:
            modelXbrl.error('xbrlte:aspectValueNotDefinedByOrdinate', _('%(definitionNode)s %(xlinkLabel)s does not define an aspect'), modelObject=(
             modelTable, definitionNode), xlinkLabel=definitionNode.xlinkLabel, definitionNode=definitionNode.localName)
        if isinstance(definitionNode, ModelClosedDefinitionNode) and definitionNode.isAbstract:
            modelXbrl.error('xbrlte:abstractRuleNodeNoChildren', _('Abstract %(definitionNode)s %(xlinkLabel)s has no children'), modelObject=(
             modelTable, definitionNode), xlinkLabel=definitionNode.xlinkLabel, definitionNode=definitionNode.localName)
    return hasCoveredAspect


def checkBreakdownLeafNodeAspects(modelXbrl, modelTable, tblAxisRel, parentAspectsCovered, breakdownAspects):
    definitionNode = tblAxisRel.toModelObject
    aspectsCovered = parentAspectsCovered.copy()
    if isinstance(definitionNode, (ModelDefinitionNode, ModelEuAxisCoord)):
        for aspect in definitionNode.aspectsCovered():
            aspectsCovered.add(aspect)

        definitionNodeHasChild = False
        for axisSubtreeRel in modelXbrl.relationshipSet((XbrlConst.tableBreakdownTree, XbrlConst.tableBreakdownTreeMMDD, XbrlConst.tableBreakdownTree201305, XbrlConst.tableDefinitionNodeSubtree, XbrlConst.tableDefinitionNodeSubtreeMMDD, XbrlConst.tableDefinitionNodeSubtree201305, XbrlConst.tableDefinitionNodeSubtree201301, XbrlConst.tableAxisSubtree2011)).fromModelObject(definitionNode):
            checkBreakdownLeafNodeAspects(modelXbrl, modelTable, axisSubtreeRel, aspectsCovered, breakdownAspects)
            definitionNodeHasChild = True

        if not definitionNode.isAbstract and not isinstance(definitionNode, ModelBreakdown):
            missingAspects = set(aspect for aspect in breakdownAspects if aspect not in aspectsCovered and aspect != Aspect.DIMENSIONS and not isinstance(aspect, QName))
            if missingAspects:
                modelXbrl.error('xbrlte:missingAspectValue', _('%(definitionNode)s %(xlinkLabel)s does not define an aspect for %(aspect)s'), modelObject=(
                 modelTable, definitionNode), xlinkLabel=definitionNode.xlinkLabel, definitionNode=definitionNode.localName, aspect=', '.join(aspectStr(aspect) for aspect in missingAspects))