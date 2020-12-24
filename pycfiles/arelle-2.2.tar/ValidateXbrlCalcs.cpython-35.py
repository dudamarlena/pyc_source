# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/ValidateXbrlCalcs.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 30148 bytes
"""
Created on Oct 17, 2010

@author: Mark V Systems Limited
(c) Copyright 2010 Mark V Systems Limited, All rights reserved.
"""
from collections import defaultdict
from math import log10, isnan, isinf, fabs, trunc, fmod, floor, pow
import decimal
try:
    from regex import compile as re_compile
except ImportError:
    from re import compile as re_compile

import hashlib
from arelle import Locale, XbrlConst, XbrlUtil
from arelle.ModelObject import ObjectPropertyViewWrapper
from arelle.XmlValidate import UNVALIDATED, VALID
numberPattern = re_compile('[-+]?[0]*([1-9]?[0-9]*)([.])?(0*)([1-9]?[0-9]*)?([eE])?([-+]?[0-9]*)?')
ZERO = decimal.Decimal(0)
ONE = decimal.Decimal(1)
NaN = decimal.Decimal('NaN')
floatNaN = float('NaN')
floatINF = float('INF')

def validate(modelXbrl, inferDecimals=False, deDuplicate=False):
    ValidateXbrlCalcs(modelXbrl, inferDecimals, deDuplicate).validate()


class ValidateXbrlCalcs:

    def __init__(self, modelXbrl, inferDecimals=False, deDuplicate=False):
        self.modelXbrl = modelXbrl
        self.inferDecimals = inferDecimals
        self.deDuplicate = deDuplicate
        self.mapContext = {}
        self.mapUnit = {}
        self.sumFacts = defaultdict(list)
        self.sumConceptBindKeys = defaultdict(set)
        self.itemFacts = defaultdict(list)
        self.itemConceptBindKeys = defaultdict(set)
        self.duplicateKeyFacts = {}
        self.duplicatedFacts = set()
        self.consistentDupFacts = set()
        self.esAlFacts = defaultdict(list)
        self.esAlConceptBindKeys = defaultdict(set)
        self.conceptsInEssencesAlias = set()
        self.requiresElementFacts = defaultdict(list)
        self.conceptsInRequiresElement = set()

    def validate(self):
        if not self.modelXbrl.contexts and not self.modelXbrl.facts:
            return
        if not self.inferDecimals:
            self.modelXbrl.info('xbrl.5.2.5.2:inferringPrecision', 'Validating calculations inferring precision.')
        self.modelXbrl.profileActivity()
        uniqueContextHashes = {}
        for context in self.modelXbrl.contexts.values():
            h = context.contextDimAwareHash
            if h in uniqueContextHashes:
                if context.isEqualTo(uniqueContextHashes[h]):
                    self.mapContext[context] = uniqueContextHashes[h]
                else:
                    uniqueContextHashes[h] = context

        del uniqueContextHashes
        self.modelXbrl.profileActivity('... identify equal contexts', minTimeToShow=1.0)
        uniqueUnitHashes = {}
        for unit in self.modelXbrl.units.values():
            h = unit.hash
            if h in uniqueUnitHashes:
                if unit.isEqualTo(uniqueUnitHashes[h]):
                    self.mapUnit[unit] = uniqueUnitHashes[h]
                else:
                    uniqueUnitHashes[h] = unit

        self.modelXbrl.profileActivity('... identify equal units', minTimeToShow=1.0)
        for baseSetKey in self.modelXbrl.baseSets.keys():
            arcrole, ELR, linkqname, arcqname = baseSetKey
            if ELR and linkqname and arcqname and arcrole in (XbrlConst.essenceAlias, XbrlConst.requiresElement):
                conceptsSet = {XbrlConst.essenceAlias: self.conceptsInEssencesAlias, 
                 XbrlConst.requiresElement: self.conceptsInRequiresElement}[arcrole]
                for modelRel in self.modelXbrl.relationshipSet(arcrole, ELR, linkqname, arcqname).modelRelationships:
                    for concept in (modelRel.fromModelObject, modelRel.toModelObject):
                        if concept is not None and concept.qname is not None:
                            conceptsSet.add(concept)

        self.modelXbrl.profileActivity('... identify requires-element and esseance-aliased concepts', minTimeToShow=1.0)
        self.bindFacts(self.modelXbrl.facts, [self.modelXbrl.modelDocument.xmlRootElement])
        self.modelXbrl.profileActivity('... bind facts', minTimeToShow=1.0)
        for baseSetKey in self.modelXbrl.baseSets.keys():
            arcrole, ELR, linkqname, arcqname = baseSetKey
            if ELR and linkqname and arcqname and arcrole in (XbrlConst.summationItem, XbrlConst.essenceAlias, XbrlConst.requiresElement):
                relsSet = self.modelXbrl.relationshipSet(arcrole, ELR, linkqname, arcqname)
                if arcrole == XbrlConst.summationItem:
                    fromRelationships = relsSet.fromModelObjects()
                    for sumConcept, modelRels in fromRelationships.items():
                        sumBindingKeys = self.sumConceptBindKeys[sumConcept]
                        dupBindingKeys = set()
                        boundSumKeys = set()
                        for modelRel in modelRels:
                            itemConcept = modelRel.toModelObject
                            if itemConcept is not None and itemConcept.qname is not None:
                                itemBindingKeys = self.itemConceptBindKeys[itemConcept]
                                boundSumKeys |= sumBindingKeys & itemBindingKeys

                        boundSums = defaultdict(decimal.Decimal)
                        boundSummationItems = defaultdict(list)
                        for modelRel in modelRels:
                            weight = modelRel.weightDecimal
                            itemConcept = modelRel.toModelObject
                            if itemConcept is not None:
                                for itemBindKey in boundSumKeys:
                                    ancestor, contextHash, unit = itemBindKey
                                    factKey = (itemConcept, ancestor, contextHash, unit)
                                    if factKey in self.itemFacts:
                                        for fact in self.itemFacts[factKey]:
                                            if fact in self.duplicatedFacts:
                                                dupBindingKeys.add(itemBindKey)
                                            elif fact not in self.consistentDupFacts:
                                                roundedValue = roundFact(fact, self.inferDecimals)
                                                boundSums[itemBindKey] += roundedValue * weight
                                                boundSummationItems[itemBindKey].append(wrappedFactWithWeight(fact, weight, roundedValue))

                        for sumBindKey in boundSumKeys:
                            ancestor, contextHash, unit = sumBindKey
                            factKey = (sumConcept, ancestor, contextHash, unit)
                            if factKey in self.sumFacts:
                                sumFacts = self.sumFacts[factKey]
                                for fact in sumFacts:
                                    if fact in self.duplicatedFacts:
                                        dupBindingKeys.add(sumBindKey)
                                    elif sumBindKey not in dupBindingKeys and fact not in self.consistentDupFacts:
                                        roundedSum = roundFact(fact, self.inferDecimals)
                                        roundedItemsSum = roundFact(fact, self.inferDecimals, vDecimal=boundSums[sumBindKey])
                                        if roundedItemsSum != roundFact(fact, self.inferDecimals):
                                            d = inferredDecimals(fact)
                                            if isnan(d) or isinf(d):
                                                d = 4
                                            _boundSummationItems = boundSummationItems[sumBindKey]
                                            unreportedContribingItemQnames = []
                                            for modelRel in modelRels:
                                                itemConcept = modelRel.toModelObject
                                                if itemConcept is not None and (
                                                 itemConcept, ancestor, contextHash, unit) not in self.itemFacts:
                                                    unreportedContribingItemQnames.append(str(itemConcept.qname))

                                            self.modelXbrl.log('INCONSISTENCY', 'xbrl.5.2.5.2:calcInconsistency', _('Calculation inconsistent from %(concept)s in link role %(linkrole)s reported sum %(reportedSum)s computed sum %(computedSum)s context %(contextID)s unit %(unitID)s unreportedContributingItems %(unreportedContributors)s'), modelObject=wrappedSummationAndItems(fact, roundedSum, _boundSummationItems), concept=sumConcept.qname, linkrole=ELR, linkroleDefinition=self.modelXbrl.roleTypeDefinition(ELR), reportedSum=Locale.format_decimal(self.modelXbrl.locale, roundedSum, 1, max(d, 0)), computedSum=Locale.format_decimal(self.modelXbrl.locale, roundedItemsSum, 1, max(d, 0)), contextID=fact.context.id, unitID=fact.unit.id, unreportedContributors=', '.join(unreportedContribingItemQnames) or 'none')
                                            del unreportedContribingItemQnames[:]

                        boundSummationItems.clear()

                else:
                    if arcrole == XbrlConst.essenceAlias:
                        for modelRel in relsSet.modelRelationships:
                            essenceConcept = modelRel.fromModelObject
                            aliasConcept = modelRel.toModelObject
                            essenceBindingKeys = self.esAlConceptBindKeys[essenceConcept]
                            aliasBindingKeys = self.esAlConceptBindKeys[aliasConcept]
                            for esAlBindKey in essenceBindingKeys & aliasBindingKeys:
                                ancestor, contextHash = esAlBindKey
                                essenceFactsKey = (essenceConcept, ancestor, contextHash)
                                aliasFactsKey = (aliasConcept, ancestor, contextHash)
                                if essenceFactsKey in self.esAlFacts and aliasFactsKey in self.esAlFacts:
                                    for eF in self.esAlFacts[essenceFactsKey]:
                                        for aF in self.esAlFacts[aliasFactsKey]:
                                            essenceUnit = self.mapUnit.get(eF.unit, eF.unit)
                                            aliasUnit = self.mapUnit.get(aF.unit, aF.unit)
                                            if essenceUnit != aliasUnit:
                                                self.modelXbrl.log('INCONSISTENCY', 'xbrl.5.2.6.2.2:essenceAliasUnitsInconsistency', _('Essence-Alias inconsistent units from %(essenceConcept)s to %(aliasConcept)s in link role %(linkrole)s context %(contextID)s'), modelObject=(
                                                 modelRel, eF, aF), essenceConcept=essenceConcept.qname, aliasConcept=aliasConcept.qname, linkrole=ELR, linkroleDefinition=self.modelXbrl.roleTypeDefinition(ELR), contextID=eF.context.id)
                                            if not XbrlUtil.vEqual(eF, aF):
                                                self.modelXbrl.log('INCONSISTENCY', 'xbrl.5.2.6.2.2:essenceAliasUnitsInconsistency', _('Essence-Alias inconsistent value from %(essenceConcept)s to %(aliasConcept)s in link role %(linkrole)s context %(contextID)s'), modelObject=(
                                                 modelRel, eF, aF), essenceConcept=essenceConcept.qname, aliasConcept=aliasConcept.qname, linkrole=ELR, linkroleDefinition=self.modelXbrl.roleTypeDefinition(ELR), contextID=eF.context.id)

                    elif arcrole == XbrlConst.requiresElement:
                        for modelRel in relsSet.modelRelationships:
                            sourceConcept = modelRel.fromModelObject
                            requiredConcept = modelRel.toModelObject
                            if sourceConcept in self.requiresElementFacts and requiredConcept not in self.requiresElementFacts:
                                self.modelXbrl.log('INCONSISTENCY', 'xbrl.5.2.6.2.4:requiresElementInconsistency', _('Requires-Element %(requiringConcept)s missing required fact for %(requiredConcept)s in link role %(linkrole)s'), modelObject=sourceConcept, requiringConcept=sourceConcept.qname, requiredConcept=requiredConcept.qname, linkrole=ELR, linkroleDefinition=self.modelXbrl.roleTypeDefinition(ELR))

        self.modelXbrl.profileActivity('... find inconsistencies', minTimeToShow=1.0)
        self.modelXbrl.profileActivity()

    def bindFacts(self, facts, ancestors):
        for f in facts:
            concept = f.concept
            if concept is not None:
                if concept.isNumeric:
                    for ancestor in ancestors:
                        context = self.mapContext.get(f.context, f.context)
                        contextHash = context.contextNonDimAwareHash if context is not None else hash(None)
                        unit = self.mapUnit.get(f.unit, f.unit)
                        calcKey = (concept, ancestor, contextHash, unit)
                        if not f.isNil:
                            self.itemFacts[calcKey].append(f)
                            bindKey = (ancestor, contextHash, unit)
                            self.itemConceptBindKeys[concept].add(bindKey)

                    if not f.isNil:
                        self.sumFacts[calcKey].append(f)
                        self.sumConceptBindKeys[concept].add(bindKey)
                    if calcKey in self.duplicateKeyFacts:
                        fDup = self.duplicateKeyFacts[calcKey]
                        if self.deDuplicate:
                            if self.inferDecimals:
                                d = inferredDecimals(f)
                                dDup = inferredDecimals(fDup)
                                dMin = min((d, dDup))
                                pMin = None
                                hasAccuracy = not isnan(d) and not isnan(dDup)
                                fIsMorePrecise = d > dDup
                            else:
                                p = inferredPrecision(f)
                                pDup = inferredPrecision(fDup)
                                dMin = None
                                pMin = min((p, pDup))
                                hasAccuracy = p != 0
                                fIsMorePrecise = p > pDup
                            if hasAccuracy and roundValue(f.value, precision=pMin, decimals=dMin) == roundValue(fDup.value, precision=pMin, decimals=dMin):
                                if fIsMorePrecise:
                                    self.duplicateKeyFacts[calcKey] = f
                                    self.consistentDupFacts.add(fDup)
                                else:
                                    self.consistentDupFacts.add(f)
                            else:
                                self.duplicatedFacts.add(f)
                                self.duplicatedFacts.add(fDup)
                        else:
                            self.duplicatedFacts.add(f)
                            self.duplicatedFacts.add(fDup)
                    else:
                        self.duplicateKeyFacts[calcKey] = f
                else:
                    if concept.isTuple:
                        self.bindFacts(f.modelTupleFacts, ancestors + [f])
                    if concept in self.conceptsInEssencesAlias and not f.isNil:
                        ancestor = ancestors[(-1)]
                        context = self.mapContext.get(f.context, f.context)
                        contextHash = context.contextNonDimAwareHash if context is not None else hash(None)
                        esAlKey = (concept, ancestor, contextHash)
                        self.esAlFacts[esAlKey].append(f)
                        bindKey = (ancestor, contextHash)
                        self.esAlConceptBindKeys[concept].add(bindKey)
                    if concept in self.conceptsInRequiresElement:
                        self.requiresElementFacts[concept].append(f)


def roundFact(fact, inferDecimals=False, vDecimal=None):
    if vDecimal is None:
        vStr = fact.value
        try:
            vDecimal = decimal.Decimal(vStr)
            vFloatFact = float(vStr)
        except (decimal.InvalidOperation, ValueError):
            vDecimal = NaN
            vFloatFact = floatNaN

    else:
        if vDecimal.is_nan():
            return vDecimal
        vStr = None
        try:
            vFloatFact = float(fact.value)
        except ValueError:
            vFloatFact = floatNaN

        dStr = fact.decimals
        pStr = fact.precision
        if dStr == 'INF' or pStr == 'INF':
            vRounded = vDecimal
        else:
            if inferDecimals:
                if pStr:
                    p = int(pStr)
                    if p == 0:
                        vRounded = NaN
                    else:
                        if vDecimal == 0:
                            vRounded = ZERO
                        else:
                            vAbs = fabs(vFloatFact)
                            d = p - int(floor(log10(vAbs))) - 1
                            vRounded = decimalRound(vDecimal, d, decimal.ROUND_HALF_EVEN)
                else:
                    if dStr:
                        d = int(dStr)
                        vRounded = decimalRound(vDecimal, d, decimal.ROUND_HALF_EVEN)
                    else:
                        vRounded = vDecimal
            else:
                if dStr:
                    match = numberPattern.match(vStr if vStr else str(vDecimal))
                    if match:
                        nonZeroInt, period, zeroDec, nonZeroDec, e, exp = match.groups()
                        p = (len(nonZeroInt) if nonZeroInt and len(nonZeroInt) > 0 else -len(zeroDec)) + (int(exp) if exp and len(exp) > 0 else 0) + int(dStr)
                    else:
                        p = 0
                else:
                    if pStr:
                        p = int(pStr)
                    else:
                        p = None
                    if p == 0:
                        vRounded = NaN
                    else:
                        if vDecimal == 0:
                            vRounded = vDecimal
                        else:
                            if p is not None:
                                vAbs = vDecimal.copy_abs()
                                log = vAbs.log10()
                                d = p - int(log) - (1 if vAbs >= 1 else 0)
                                vRounded = decimalRound(vDecimal, d, decimal.ROUND_HALF_UP)
                            else:
                                vRounded = vDecimal
        return vRounded


def decimalRound(x, d, rounding):
    if x.is_normal():
        if -28 <= d <= 28:
            if d >= 0:
                return x.quantize(ONE.scaleb(-d), rounding)
            return x.scaleb(d).quantize(ONE, rounding).scaleb(-d)
        return x


def inferredPrecision(fact):
    vStr = fact.value
    dStr = fact.decimals
    pStr = fact.precision
    if dStr == 'INF' or pStr == 'INF':
        return floatINF
    try:
        vFloat = float(vStr)
        if dStr:
            match = numberPattern.match(vStr if vStr else str(vFloat))
            if match:
                nonZeroInt, period, zeroDec, nonZeroDec, e, exp = match.groups()
                p = (len(nonZeroInt) if nonZeroInt else -len(zeroDec) if nonZeroDec else 0) + (int(exp) if exp else 0) + int(dStr)
                if p < 0:
                    p = 0
            else:
                p = 0
        else:
            return int(pStr)
    except ValueError:
        return floatNaN

    if p == 0:
        return 0
    else:
        if vFloat == 0:
            return 0
        return p


def inferredDecimals(fact):
    vStr = fact.value
    dStr = fact.decimals
    pStr = fact.precision
    if dStr == 'INF' or pStr == 'INF':
        return floatINF
    try:
        if pStr:
            p = int(pStr)
            if p == 0:
                return floatNaN
            else:
                vFloat = float(vStr)
                if vFloat == 0:
                    return floatINF
                vAbs = fabs(vFloat)
                return p - int(floor(log10(vAbs))) - 1
        elif dStr:
            return int(dStr)
    except ValueError:
        pass

    return floatNaN


def roundValue(value, precision=None, decimals=None, scale=None):
    try:
        vDecimal = decimal.Decimal(value)
        if scale:
            iScale = int(scale)
            vDecimal = vDecimal.scaleb(iScale)
        if precision is not None:
            vFloat = float(value)
            if scale:
                vFloat = pow(vFloat, iScale)
    except (decimal.InvalidOperation, ValueError):
        return NaN

    if precision is not None:
        if not isinstance(precision, (int, float)):
            if precision == 'INF':
                precision = floatINF
            else:
                try:
                    precision = int(precision)
                except ValueError:
                    precision = floatNaN

            if isinf(precision):
                vRounded = vDecimal
        else:
            if precision == 0 or isnan(precision):
                vRounded = NaN
            else:
                if vFloat == 0:
                    vRounded = ZERO
                else:
                    vAbs = fabs(vFloat)
                    log = log10(vAbs)
                    d = precision - int(log) - (1 if vAbs >= 1 else 0)
                    vRounded = decimalRound(vDecimal, d, decimal.ROUND_HALF_UP)
    elif decimals is not None:
        pass
    if not isinstance(decimals, (int, float)):
        if decimals == 'INF':
            decimals = floatINF
        else:
            try:
                decimals = int(decimals)
            except ValueError:
                decimals = floatNaN

        if isinf(decimals):
            vRounded = vDecimal
        else:
            if isnan(decimals):
                vRounded = NaN
            else:
                vRounded = decimalRound(vDecimal, decimals, decimal.ROUND_HALF_EVEN)
    else:
        vRounded = vDecimal
    return vRounded


def insignificantDigits(value, precision=None, decimals=None, scale=None):
    try:
        vDecimal = decimal.Decimal(value)
        if scale:
            iScale = int(scale)
            vDecimal = vDecimal.scaleb(iScale)
        if precision is not None:
            vFloat = float(value)
            if scale:
                vFloat = pow(vFloat, iScale)
    except (decimal.InvalidOperation, ValueError):
        return

    if precision is not None:
        if not isinstance(precision, (int, float)):
            if precision == 'INF':
                return
                try:
                    precision = int(precision)
                except ValueError:
                    return

                if isinf(precision) or precision == 0 or isnan(precision) or vFloat == 0:
                    return
                vAbs = fabs(vFloat)
                log = log10(vAbs)
                decimals = precision - int(log) - (1 if vAbs >= 1 else 0)
    elif decimals is not None:
        if not isinstance(decimals, (int, float)):
            pass
    if decimals == 'INF':
        return
        try:
            decimals = int(decimals)
        except ValueError:
            return

        if isinf(decimals) or isnan(decimals):
            return
    else:
        return
    if vDecimal.is_normal():
        if -28 <= decimals <= 28:
            if decimals > 0:
                divisor = ONE.scaleb(-decimals)
            else:
                divisor = ONE.scaleb(-decimals).quantize(ONE, decimal.ROUND_HALF_UP)
            insignificantDigits = abs(vDecimal) % divisor
            if insignificantDigits:
                pass
            return (
             vDecimal // divisor * divisor,
             insignificantDigits)


def wrappedFactWithWeight(fact, weight, roundedValue):
    return ObjectPropertyViewWrapper(fact, (('weight', weight), ('roundedValue', roundedValue)))


def wrappedSummationAndItems(fact, roundedSum, boundSummationItems):
    """ ARELLE-281, replace: faster python-based hash (replace with hashlib for fewer collisions)
    itemValuesHash = hash( tuple(( hash(b.modelObject.qname), hash(b.extraProperties[1][1]) )
                                 # sort by qname so we don't care about reordering of summation terms
                                 for b in sorted(boundSummationItems,
                                                       key=lambda b: b.modelObject.qname)) )
    sumValueHash = hash( (hash(fact.qname), hash(roundedSum)) )
    """
    sha256 = hashlib.sha256()
    for b in sorted(boundSummationItems, key=lambda b: b.modelObject.qname):
        sha256.update(b.modelObject.qname.namespaceURI.encode('utf-8', 'replace'))
        sha256.update(b.modelObject.qname.localName.encode('utf-8', 'replace'))
        sha256.update(str(b.extraProperties[1][1]).encode('utf-8', 'replace'))

    itemValuesHash = sha256.hexdigest()
    sha256 = hashlib.sha256()
    sha256.update(fact.qname.namespaceURI.encode('utf-8', 'replace'))
    sha256.update(fact.qname.localName.encode('utf-8', 'replace'))
    sha256.update(str(roundedSum).encode('utf-8', 'replace'))
    sumValueHash = sha256.hexdigest()
    return [
     ObjectPropertyViewWrapper(fact, (
      (
       'sumValueHash', sumValueHash),
      (
       'itemValuesHash', itemValuesHash),
      (
       'roundedSum', roundedSum)))] + boundSummationItems