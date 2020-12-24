# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/ModelRelationshipSet.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 20587 bytes
__doc__ = '\nCreated on Oct 5, 2010\n\n@author: Mark V Systems Limited\n(c) Copyright 2010 Mark V Systems Limited, All rights reserved.\n'
from collections import defaultdict
from arelle import ModelDtsObject, XbrlConst, XmlUtil, ModelValue
from arelle.ModelObject import ModelObject
from arelle.ModelDtsObject import ModelResource
from arelle.PrototypeDtsObject import LocPrototype, PrototypeObject
from arelle.XbrlConst import consecutiveArcrole
import os, sys
USING_EQUIVALENCE_KEY = sys.intern(_STR_8BIT('using_equivalence_key'))

def create(modelXbrl, arcrole, linkrole=None, linkqname=None, arcqname=None, includeProhibits=False):
    return ModelRelationshipSet(modelXbrl, arcrole, linkrole, linkqname, arcqname, includeProhibits)


def ineffectiveArcs(baseSetModelLinks, arcrole, arcqname=None):
    hashEquivalentRels = defaultdict(list)
    for modelLink in baseSetModelLinks:
        for linkChild in modelLink:
            if isinstance(linkChild, (ModelObject, PrototypeObject)) and linkChild.get('{http://www.w3.org/1999/xlink}type') == 'arc' and arcrole == linkChild.get('{http://www.w3.org/1999/xlink}arcrole') and (arcqname is None or arcqname == linkChild):
                fromLabel = linkChild.get('{http://www.w3.org/1999/xlink}from')
                toLabel = linkChild.get('{http://www.w3.org/1999/xlink}to')
                for fromResource in modelLink.labeledResources[fromLabel]:
                    for toResource in modelLink.labeledResources[toLabel]:
                        modelRel = ModelDtsObject.ModelRelationship(modelLink.modelDocument, linkChild, fromResource.dereference(), toResource.dereference())
                        hashEquivalentRels[modelRel.equivalenceHash].append(modelRel)

    ineffectives = []
    keyEquivalentRels = defaultdict(list)
    for hashEquivRelList in hashEquivalentRels.values():
        if len(hashEquivRelList) == 1:
            if hashEquivRelList[0].prohibitedUseSortKey == 2:
                ineffective = hashEquivRelList[0]
                ineffective.ineffectivity = _('prohibited arc (priority {0}) has no other arc to prohibit').format(ineffective.priority)
                ineffectives.append(ineffective)
        else:
            for modelRel in hashEquivRelList:
                keyEquivalentRels[modelRel.equivalenceKey].append(modelRel)

            for keyEquivRelList in keyEquivalentRels.values():
                equivalentRels = [(modelRel.priority, modelRel.prohibitedUseSortKey, i) for i, modelRel in enumerate(keyEquivRelList)]
                priorRel = None
                for rel in sorted(equivalentRels):
                    if rel[1] == 2:
                        if priorRel is None:
                            ineffective = keyEquivRelList[rel[2]]
                            ineffective.ineffectivity = _('prohibited arc (priority {0}) has no other arc to prohibit').format(ineffective.priority)
                            ineffectives.append(ineffective)
                        elif priorRel[1] == 2:
                            ineffective = keyEquivRelList[priorRel[2]]
                            effective = keyEquivRelList[rel[2]]
                            ineffective.ineffectivity = _('prohibited arc (priority {0}, {1} - {2}) has an equivalent prohibited arc (priority {3}, {4} - {5})\n').format(ineffective.priority, ineffective.modelDocument.basename, ineffective.sourceline, effective.priority, effective.modelDocument.basename, effective.sourceline)
                            ineffectives.append(ineffective)
                    elif priorRel is not None and priorRel[1] != 2:
                        ineffective = keyEquivRelList[priorRel[2]]
                        effective = keyEquivRelList[rel[2]]
                        ineffective.ineffectivity = _('arc (priority {0}, {1} - {2}) is ineffective due to equivalent arc (priority {3}, {4} - {5})\n').format(ineffective.priority, ineffective.modelDocument.basename, ineffective.sourceline, effective.priority, effective.modelDocument.basename, effective.sourceline)
                        ineffectives.append(ineffective)
                    priorRel = rel

            keyEquivalentRels.clear()

    return ineffectives


def baseSetArcroles(modelXbrl):
    return sorted(set((XbrlConst.baseSetArcroleLabel(b[0]), b[0]) for b in modelXbrl.baseSets.keys()))


def labelroles(modelXbrl, includeConceptName=False):
    return sorted(set((XbrlConst.labelroleLabel(r), r) for r in modelXbrl.labelroles | ({XbrlConst.conceptNameLabelRole} if includeConceptName else set()) if r is not None))


def baseSetRelationship(arcElement):
    modelXbrl = arcElement.modelXbrl
    arcrole = arcElement.get('{http://www.w3.org/1999/xlink}arcrole')
    ELR = arcElement.getparent().get('{http://www.w3.org/1999/xlink}role')
    for rel in modelXbrl.relationshipSet(arcrole, ELR).modelRelationships:
        if rel.arcElement == arcElement:
            return rel


class ModelRelationshipSet:
    __slots__ = ('isChanged', 'modelXbrl', 'arcrole', 'linkrole', 'linkqname', 'arcqname',
                 'modelRelationshipsFrom', 'modelRelationshipsTo', 'modelConceptRoots',
                 'modellinkRoleUris', 'modelRelationships', '_testHintedLabelLinkrole')

    def __init__(self, modelXbrl, arcrole, linkrole=None, linkqname=None, arcqname=None, includeProhibits=False):
        self.isChanged = False
        self.modelXbrl = modelXbrl
        self.arcrole = arcrole
        self.linkrole = linkrole
        self.linkqname = linkqname
        self.arcqname = arcqname
        relationshipSetKey = (
         arcrole, linkrole, linkqname, arcqname, includeProhibits)
        if not isinstance(arcrole, (tuple, frozenset)):
            modelLinks = self.modelXbrl.baseSets.get((arcrole, linkrole, linkqname, arcqname), [])
        else:
            modelLinks = []
            for ar in arcrole:
                modelLinks.extend(self.modelXbrl.baseSets.get((ar, linkrole, linkqname, arcqname), []))

        relationships = {}
        isDimensionRel = self.arcrole == 'XBRL-dimensions'
        isFormulaRel = self.arcrole == 'XBRL-formulae'
        isTableRenderingRel = self.arcrole == 'Table-rendering'
        isFootnoteRel = self.arcrole == 'XBRL-footnotes'
        if not isinstance(arcrole, (tuple, frozenset)):
            arcrole = (
             arcrole,)
        for modelLink in modelLinks:
            arcs = []
            linkEltQname = modelLink.qname
            for linkChild in modelLink:
                linkChildArcrole = linkChild.get('{http://www.w3.org/1999/xlink}arcrole')
                if linkChild.get('{http://www.w3.org/1999/xlink}type') == 'arc' and linkChildArcrole:
                    if isFootnoteRel:
                        arcs.append(linkChild)
                    else:
                        if isDimensionRel:
                            if XbrlConst.isDimensionArcrole(linkChildArcrole):
                                arcs.append(linkChild)
                        else:
                            if isFormulaRel:
                                if XbrlConst.isFormulaArcrole(linkChildArcrole):
                                    arcs.append(linkChild)
                            else:
                                if isTableRenderingRel:
                                    if XbrlConst.isTableRenderingArcrole(linkChildArcrole):
                                        arcs.append(linkChild)
                                elif linkChildArcrole in arcrole and (arcqname is None or arcqname == linkChild.qname) and (linkqname is None or linkqname == linkEltQname):
                                    arcs.append(linkChild)

            for arcElement in arcs:
                fromLabel = arcElement.get('{http://www.w3.org/1999/xlink}from')
                toLabel = arcElement.get('{http://www.w3.org/1999/xlink}to')
                for fromResource in modelLink.labeledResources[fromLabel]:
                    for toResource in modelLink.labeledResources[toLabel]:
                        if isinstance(fromResource, (ModelResource, LocPrototype)) and isinstance(toResource, (ModelResource, LocPrototype)):
                            modelRel = ModelDtsObject.ModelRelationship(modelLink.modelDocument, arcElement, fromResource.dereference(), toResource.dereference())
                            modelRelEquivalenceHash = modelRel.equivalenceHash
                            if modelRelEquivalenceHash not in relationships:
                                relationships[modelRelEquivalenceHash] = modelRel
                            else:
                                otherRel = relationships[modelRelEquivalenceHash]
                                if otherRel is not USING_EQUIVALENCE_KEY:
                                    if modelRel.isIdenticalTo(otherRel):
                                        pass
                                    else:
                                        relationships[otherRel.equivalenceKey] = otherRel
                                        relationships[modelRelEquivalenceHash] = USING_EQUIVALENCE_KEY
                                modelRelEquivalenceKey = modelRel.equivalenceKey
                                if modelRelEquivalenceKey not in relationships or modelRel.priorityOver(relationships[modelRelEquivalenceKey]):
                                    relationships[modelRelEquivalenceKey] = modelRel

        self.modelRelationshipsFrom = None
        self.modelRelationshipsTo = None
        self.modelConceptRoots = None
        self.modellinkRoleUris = None
        orderRels = defaultdict(list)
        for modelRel in relationships.values():
            if modelRel is not USING_EQUIVALENCE_KEY and (includeProhibits or not modelRel.isProhibited):
                orderRels[modelRel.order].append(modelRel)

        self.modelRelationships = [modelRel for order in sorted(orderRels.keys()) for modelRel in orderRels[order]]
        modelXbrl.relationshipSets[relationshipSetKey] = self

    def clear(self):
        self.modelXbrl = None
        del self.modelRelationships[:]
        if self.modelRelationshipsTo is not None:
            self.modelRelationshipsTo.clear()
        if self.modelRelationshipsFrom is not None:
            self.modelRelationshipsFrom.clear()
        if self.modelConceptRoots is not None:
            del self.modelConceptRoots[:]
        self.linkqname = self.arcqname = None

    def __bool__(self):
        return len(self.modelRelationships) > 0

    @property
    def linkRoleUris(self):
        if self.modellinkRoleUris is None:
            self.modellinkRoleUris = set(modelRel.linkrole for modelRel in self.modelRelationships)
        return self.modellinkRoleUris

    def loadModelRelationshipsFrom(self):
        if self.modelRelationshipsFrom is None:
            self.modelRelationshipsFrom = defaultdict(list)
            for modelRel in self.modelRelationships:
                fromModelObject = modelRel.fromModelObject
                if fromModelObject is not None:
                    self.modelRelationshipsFrom[fromModelObject].append(modelRel)

    def loadModelRelationshipsTo(self):
        if self.modelRelationshipsTo is None:
            self.modelRelationshipsTo = defaultdict(list)
            for modelRel in self.modelRelationships:
                toModelObject = modelRel.toModelObject
                if toModelObject is not None:
                    self.modelRelationshipsTo[toModelObject].append(modelRel)

    def fromModelObjects(self):
        self.loadModelRelationshipsFrom()
        return self.modelRelationshipsFrom

    def fromModelObject(self, modelFrom):
        if self.modelRelationshipsFrom is None:
            self.loadModelRelationshipsFrom()
        return self.modelRelationshipsFrom.get(modelFrom, [])

    def toModelObjects(self):
        self.loadModelRelationshipsTo()
        return self.modelRelationshipsTo

    def toModelObject(self, modelTo):
        if self.modelRelationshipsTo is None:
            self.loadModelRelationshipsTo()
        return self.modelRelationshipsTo.get(modelTo, [])

    def fromToModelObjects(self, modelFrom, modelTo, checkBothDirections=False):
        self.loadModelRelationshipsFrom()
        rels = [rel for rel in self.fromModelObject(modelFrom) if rel.toModelObject is modelTo]
        if checkBothDirections:
            rels += [rel for rel in self.fromModelObject(modelTo) if rel.toModelObject is modelFrom]
        return rels

    @property
    def rootConcepts(self):
        if self.modelConceptRoots is None:
            self.loadModelRelationshipsFrom()
            self.loadModelRelationshipsTo()
            self.modelConceptRoots = [modelRelFrom for modelRelFrom in self.modelRelationshipsFrom.keys() if modelRelFrom not in self.modelRelationshipsTo]
        return self.modelConceptRoots

    def isRelated(self, modelFrom, axis, modelTo=None, visited=None, isDRS=False):
        if isinstance(modelFrom, ModelValue.QName):
            modelFrom = self.modelXbrl.qnameConcepts.get(modelFrom)
        if isinstance(modelTo, ModelValue.QName):
            modelTo = self.modelXbrl.qnameConcepts.get(modelTo)
            if modelTo is None:
                pass
            return False
        if axis.endswith('self') and (modelTo is None or modelFrom == modelTo):
            return True
        isDescendantAxis = 'descendant' in axis
        if axis.startswith('ancestral-'):
            if self.isRelated(modelFrom, axis[10:], modelTo):
                return True
            if visited is None:
                visited = set()
            if modelFrom in visited:
                return False
            visited.add(modelFrom)
            isRel = any(self.isRelated(modelRel.fromModelObject, axis, modelTo, visited) for modelRel in self.toModelObject(modelFrom))
            visited.discard(modelFrom)
            return isRel
        if axis.startswith('sibling'):
            axis = axis[7:]
            return any(self.isRelated(modelRel.fromModelObject, axis, modelTo) for modelRel in self.toModelObject(modelFrom))
        for modelRel in self.fromModelObject(modelFrom):
            toConcept = modelRel.toModelObject
            if modelTo is None or modelTo == toConcept:
                return True
            if isDescendantAxis:
                if visited is None:
                    visited = set()
                if toConcept not in visited:
                    visited.add(toConcept)
                    if isDRS:
                        if self.modelXbrl.relationshipSet(consecutiveArcrole[modelRel.arcrole], modelRel.consecutiveLinkrole, self.linkqname, self.arcqname).isRelated(toConcept, axis, modelTo, visited, isDRS):
                            return True
                    elif self.isRelated(toConcept, axis, modelTo, visited, isDRS):
                        return True
                    visited.discard(toConcept)

        return False

    def label(self, modelFrom, role, lang, returnMultiple=False, returnText=True, linkroleHint=None):
        shorterLangInLabel = longerLangInLabel = None
        shorterLangLabels = longerLangLabels = None
        langLabels = []
        wildRole = role == '*'
        labels = self.fromModelObject(modelFrom)
        if linkroleHint:
            try:
                testHintedLinkrole = self._testHintedLabelLinkrole
            except AttributeError:
                self._testHintedLabelLinkrole = testHintedLinkrole = len(self.linkRoleUris) > 1

            if testHintedLinkrole:
                labelsHintedLink = []
                labelsDefaultLink = []
                labelsOtherLinks = []
                for modelLabelRel in labels:
                    label = modelLabelRel.toModelObject
                    if wildRole or role == label.role:
                        linkrole = modelLabelRel.linkrole
                        if linkrole == linkroleHint:
                            labelsHintedLink.append(modelLabelRel)
                        else:
                            if linkrole == XbrlConst.defaultLinkRole:
                                labelsDefaultLink.append(modelLabelRel)
                            else:
                                labelsOtherLinks.append(modelLabelRel)

                labels = labelsHintedLink or labelsDefaultLink or labelsOtherLinks
        if len(labels) > 1:
            labels.sort(key=lambda rel: rel.priority, reverse=True)
        for modelLabelRel in labels:
            label = modelLabelRel.toModelObject
            if wildRole or role == label.role:
                labelLang = label.xmlLang
                text = label.textValue if returnText else label
                if lang is None or len(lang) == 0 or lang == labelLang:
                    langLabels.append(text)
                    if not returnMultiple:
                        break
                else:
                    if labelLang.startswith(lang):
                        if not longerLangInLabel or len(longerLangInLabel) > len(labelLang):
                            longerLangInLabel = labelLang
                            longerLangLabels = [text]
                        else:
                            longerLangLabels.append(text)
                    elif lang.startswith(labelLang):
                        if not shorterLangInLabel or len(shorterLangInLabel) < len(labelLang):
                            shorterLangInLabel = labelLang
                            shorterLangLabels = [text]
                        else:
                            shorterLangLabels.append(text)

        if langLabels:
            if returnMultiple:
                return langLabels
            return langLabels[0]
        if shorterLangLabels:
            if returnMultiple:
                return shorterLangLabels
            return shorterLangLabels[0]
        if longerLangLabels:
            if returnMultiple:
                return longerLangLabels
            return longerLangLabels[0]