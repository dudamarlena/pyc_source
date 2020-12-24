# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/ValidateFiling.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 167937 bytes
"""
Created on Oct 17, 2010

@author: Mark V Systems Limited
(c) Copyright 2010 Mark V Systems Limited, All rights reserved.

Deprecated Nov 15, 2015.  Use plugin/validate/EFM/Filing.py
"""
import xml.dom, xml.parsers, os, re, collections, datetime
from decimal import Decimal
from collections import defaultdict
from arelle import ModelDocument, ModelValue, ValidateXbrl, ModelRelationshipSet, XmlUtil, XbrlConst, UrlUtil, ValidateFilingDimensions, ValidateFilingDTS, ValidateFilingText
from arelle.ValidateXbrlCalcs import insignificantDigits
from arelle.XmlValidate import UNVALIDATED, VALID
from arelle.ModelObject import ModelObject
from arelle.ModelInstanceObject import ModelFact
from arelle.ModelDtsObject import ModelConcept
from arelle.PluginManager import pluginClassMethods
from arelle.UrlUtil import isHttpUrl
datePattern = None
linkroleDefinitionStatementSheet = None

class ValidateFiling(ValidateXbrl.ValidateXbrl):

    def __init__(self, modelXbrl):
        global GFMcontextDatePattern
        global datePattern
        global efmCIKpattern
        global htmlFileNamePattern
        global instanceFileNamePattern
        global linkroleDefinitionStatementSheet
        global signOrCurrencyPattern
        super(ValidateFiling, self).__init__(modelXbrl)
        if datePattern is None:
            datePattern = re.compile('([12][0-9]{3})-([01][0-9])-([0-3][0-9])')
            GFMcontextDatePattern = re.compile('^[12][0-9]{3}-[01][0-9]-[0-3][0-9]$')
            signOrCurrencyPattern = re.compile('^(-)[0-9]+|[^eE](-)[0-9]+|(\\()[0-9].*(\\))|([$€£\x00a5])')
            instanceFileNamePattern = re.compile('^(\\w+)-([12][0-9]{3}[01][0-9][0-3][0-9]).xml$')
            htmlFileNamePattern = re.compile('([a-zA-Z0-9][._a-zA-Z0-9-]*)\\.htm$')
            linkroleDefinitionStatementSheet = re.compile('[^-]+-\\s+Statement\\s+-\\s+.*', re.IGNORECASE)
            efmCIKpattern = re.compile('^[0-9]{10}$')

    def validate(self, modelXbrl, parameters=None):
        if not hasattr(modelXbrl.modelDocument, 'xmlDocument'):
            return
        self._isStandardUri = {}
        modelXbrl.modelManager.disclosureSystem.loadStandardTaxonomiesDict()
        if modelXbrl.modelManager.disclosureSystem.SBRNL:
            for pluginXbrlMethod in pluginClassMethods('Validate.SBRNL.Start'):
                pluginXbrlMethod(self, modelXbrl)

            self.qnSbrLinkroleorder = ModelValue.qname('http://www.nltaxonomie.nl/5.0/basis/sbr/xbrl/xbrl-syntax-extension', 'linkroleOrder')
            self.typedDomainQnames = set()
            self.typedDomainElements = set()
            for modelConcept in modelXbrl.qnameConcepts.values():
                if modelConcept.isTypedDimension:
                    typedDomainElement = modelConcept.typedDomainElement
                    if isinstance(typedDomainElement, ModelConcept):
                        self.typedDomainQnames.add(typedDomainElement.qname)
                        self.typedDomainElements.add(typedDomainElement)

        super(ValidateFiling, self).validate(modelXbrl, parameters)
        xbrlInstDoc = modelXbrl.modelDocument.xmlDocument.getroot()
        disclosureSystem = self.disclosureSystem
        disclosureSystemVersion = disclosureSystem.version
        modelXbrl.modelManager.showStatus(_('validating {0}').format(disclosureSystem.name))
        self.modelXbrl.profileActivity()
        conceptsUsed = {}
        labelsRelationshipSet = modelXbrl.relationshipSet(XbrlConst.conceptLabel)
        if self.validateSBRNL:
            genLabelsRelationshipSet = modelXbrl.relationshipSet(XbrlConst.elementLabel)
        presentationRelationshipSet = modelXbrl.relationshipSet(XbrlConst.parentChild)
        referencesRelationshipSetWithProhibits = modelXbrl.relationshipSet(XbrlConst.conceptReference, includeProhibits=True)
        self.modelXbrl.profileActivity('... cache lbl, pre, ref relationships', minTimeToShow=1.0)
        validateInlineXbrlGFM = modelXbrl.modelDocument.type == ModelDocument.Type.INLINEXBRL and self.validateGFM
        validateEFMpragmatic = disclosureSystem.names and 'efm-pragmatic' in disclosureSystem.names
        self.validateLoggingSemantic = validateLoggingSemantic = modelXbrl.isLoggingEffectiveFor(level='WARNING-SEMANTIC') or modelXbrl.isLoggingEffectiveFor(level='ERROR-SEMANTIC')
        if self.validateEFM:
            for pluginXbrlMethod in pluginClassMethods('Validate.EFM.Start'):
                pluginXbrlMethod(self)

        self.fileNameBasePart = None
        self.fileNameDate = None
        self.entityRegistrantName = None
        self.requiredContext = None
        self.standardNamespaceConflicts = defaultdict(set)
        self.exhibitType = None
        if modelXbrl.modelDocument.type == ModelDocument.Type.INSTANCE or modelXbrl.modelDocument.type == ModelDocument.Type.INLINEXBRL:
            instanceName = modelXbrl.modelDocument.basename
            paramFilerIdentifier = None
            paramFilerIdentifiers = None
            paramFilerNames = None
            submissionType = None
            if self.validateEFM and self.parameters:
                p = self.parameters.get(ModelValue.qname('CIK', noPrefixIsNoNamespace=True))
                if p and len(p) == 2 and p[1] not in ('null', 'None'):
                    paramFilerIdentifier = p[1]
                p = self.parameters.get(ModelValue.qname('cikList', noPrefixIsNoNamespace=True))
                if p and len(p) == 2:
                    paramFilerIdentifiers = p[1].split(',')
                p = self.parameters.get(ModelValue.qname('cikNameList', noPrefixIsNoNamespace=True))
                if p and len(p) == 2:
                    paramFilerNames = p[1].split('|Edgar|')
                    if paramFilerIdentifiers and len(paramFilerIdentifiers) != len(paramFilerNames):
                        self.modelXbrl.error(('EFM.6.05.24.parameters', 'GFM.3.02.02'), _('parameters for cikList and cikNameList different list entry counts: %(cikList)s, %(cikNameList)s'), modelXbrl=modelXbrl, cikList=paramFilerIdentifiers, cikNameList=paramFilerNames)
                p = self.parameters.get(ModelValue.qname('submissionType', noPrefixIsNoNamespace=True))
                if p and len(p) == 2:
                    submissionType = p[1]
                p = self.parameters.get(ModelValue.qname('exhibitType', noPrefixIsNoNamespace=True))
                if p and len(p) == 2:
                    self.exhibitType = p[1]
            m = instanceFileNamePattern.match(instanceName)
            if modelXbrl.modelDocument.type == ModelDocument.Type.INLINEXBRL and any(name.startswith('efm') for name in disclosureSystem.names):
                m = htmlFileNamePattern.match(instanceName)
                if m:
                    self.fileNameBasePart = None
                    self.fileNameDatePart = None
                else:
                    modelXbrl.error(self.EFM60303, _('Invalid inline xbrl document in {base}.htm": %(filename)s'), modelObject=modelXbrl.modelDocument, filename=instanceName, messageCodes=('EFM.6.03.03', ))
        elif m:
            self.fileNameBasePart = m.group(1)
            self.fileNameDatePart = m.group(2)
            if not self.fileNameBasePart:
                modelXbrl.error((self.EFM60303, 'GFM.1.01.01'), _('Invalid instance document base name part (ticker or mnemonic name) in "{base}-{yyyymmdd}.xml": %(filename)s'), modelObject=modelXbrl.modelDocument, filename=modelXbrl.modelDocument.basename, messageCodes=('EFM.6.03.03',
                                                                                                                                                                                                                                                                                'EFM.6.23.01',
                                                                                                                                                                                                                                                                                'GFM.1.01.01'))
            else:
                try:
                    self.fileNameDate = datetime.datetime.strptime(self.fileNameDatePart, '%Y%m%d').date()
                except ValueError:
                    modelXbrl.error((self.EFM60303, 'GFM.1.01.01'), _('Invalid instance document base name part (date) in "{base}-{yyyymmdd}.xml": %(filename)s'), modelObject=modelXbrl.modelDocument, filename=modelXbrl.modelDocument.basename, messageCodes=('EFM.6.03.03',
                                                                                                                                                                                                                                                                 'EFM.6.23.01',
                                                                                                                                                                                                                                                                 'GFM.1.01.01'))

        else:
            modelXbrl.error((self.EFM60303, 'GFM.1.01.01'), _('Invalid instance document name, must match "{base}-{yyyymmdd}.xml": %(filename)s'), modelObject=modelXbrl.modelDocument, filename=modelXbrl.modelDocument.basename, messageCodes=('EFM.6.03.03',
                                                                                                                                                                                                                                                 'EFM.6.23.01',
                                                                                                                                                                                                                                                 'GFM.1.01.01'))
        entityIdentifierValue = None
        entityIdentifierValueElt = None
        if disclosureSystem.identifierValueName:
            for entityIdentifierElt in xbrlInstDoc.iterdescendants('{http://www.xbrl.org/2003/instance}identifier'):
                if isinstance(entityIdentifierElt, ModelObject):
                    schemeAttr = entityIdentifierElt.get('scheme')
                    entityIdentifier = XmlUtil.text(entityIdentifierElt)
                    if not disclosureSystem.identifierSchemePattern.match(schemeAttr):
                        try:
                            contextId = entityIdentifierElt.getparent().getparent().id
                        except AttributeError:
                            contextId = 'not available'

                        modelXbrl.error(('EFM.6.05.01', 'GFM.1.02.01'), _('Invalid entity identifier scheme %(scheme)s in context %(context)s for identifier %(identifier)s'), modelObject=entityIdentifierElt, scheme=schemeAttr, context=contextId, identifier=entityIdentifier)
                    if not disclosureSystem.identifierValuePattern.match(entityIdentifier):
                        modelXbrl.error(('EFM.6.05.02', 'GFM.1.02.02'), _('Invalid entity identifier %(entityIdentifierName)s: %(entityIdentifer)s'), modelObject=entityIdentifierElt, entityIdentifierName=disclosureSystem.identifierValueName, entityIdentifer=entityIdentifier)
                    if not entityIdentifierValue:
                        entityIdentifierValue = entityIdentifier
                        entityIdentifierValueElt = entityIdentifierElt
                        if self.validateEFM and not efmCIKpattern.match(entityIdentifierValue):
                            self.modelXbrl.error('EFM.6.05.23.cikValue', _('EntityIdentifier %(entityIdentifer)s must be 10 digits.'), modelObject=entityIdentifierElt, entityIdentifer=entityIdentifierValue)
                    elif entityIdentifier != entityIdentifierValue:
                        modelXbrl.error(('EFM.6.05.03', 'GFM.1.02.03'), _('Multiple %(entityIdentifierName)ss: %(entityIdentifer)s, %(entityIdentifer2)s'), modelObject=(
                         entityIdentifierElt, entityIdentifierValueElt), entityIdentifierName=disclosureSystem.identifierValueName, entityIdentifer=entityIdentifierValue, entityIdentifer2=entityIdentifier, filerIdentifier=','.join(paramFilerIdentifiers or []))

            self.modelXbrl.profileActivity('... filer identifier checks', minTimeToShow=1.0)
        contexts = modelXbrl.contexts.values()
        contextIDs = set()
        uniqueContextHashes = {}
        contextsWithDisallowedOCEs = []
        contextsWithDisallowedOCEcontent = []
        for context in contexts:
            contextID = context.id
            contextIDs.add(contextID)
            h = context.contextDimAwareHash
            if h in uniqueContextHashes:
                if context.isEqualTo(uniqueContextHashes[h]):
                    modelXbrl.error(('EFM.6.05.07', 'GFM.1.02.07'), _('Context ID %(context)s is equivalent to context ID %(context2)s'), modelObject=(
                     context, uniqueContextHashes[h]), context=contextID, context2=uniqueContextHashes[h].id)
            else:
                uniqueContextHashes[h] = context
            if self.validateGFM:
                for dateElt in XmlUtil.children(context, XbrlConst.xbrli, ('startDate',
                                                                           'endDate',
                                                                           'instant')):
                    dateText = XmlUtil.text(dateElt)
                    if not GFMcontextDatePattern.match(dateText):
                        modelXbrl.error('GFM.1.02.25', _('Context id %(context)s %(elementName)s invalid content %(value)s'), modelObject=dateElt, context=contextID, elementName=dateElt.prefixedName, value=dateText)

            hasSegment = XmlUtil.hasChild(context, XbrlConst.xbrli, 'segment')
            hasScenario = XmlUtil.hasChild(context, XbrlConst.xbrli, 'scenario')
            notAllowed = None
            if disclosureSystem.contextElement == 'segment' and hasScenario:
                notAllowed = _('Scenario')
            else:
                if disclosureSystem.contextElement == 'scenario' and hasSegment:
                    notAllowed = _('Segment')
                else:
                    if disclosureSystem.contextElement == 'either' and hasSegment and hasScenario:
                        notAllowed = _('Both segment and scenario')
                    elif disclosureSystem.contextElement == 'none' and (hasSegment or hasScenario):
                        notAllowed = _('Neither segment nor scenario')
            if notAllowed:
                if validateEFMpragmatic:
                    contextsWithDisallowedOCEs.append(context)
                else:
                    modelXbrl.error(('EFM.6.05.04', 'GFM.1.02.04', 'SBR.NL.2.3.5.06'), _('%(elementName)s element not allowed in context Id: %(context)s'), modelObject=context, elementName=notAllowed, context=contextID, count=1)
                for contextName in {'segment': ('{http://www.xbrl.org/2003/instance}segment', ), 
                 'scenario': ('{http://www.xbrl.org/2003/instance}scenario', ), 
                 'either': ('{http://www.xbrl.org/2003/instance}segment', '{http://www.xbrl.org/2003/instance}scenario'), 
                 'both': ('{http://www.xbrl.org/2003/instance}segment', '{http://www.xbrl.org/2003/instance}scenario'), 
                 'none': [], None: []}[disclosureSystem.contextElement]:
                    for segScenElt in context.iterdescendants(contextName):
                        if isinstance(segScenElt, ModelObject):
                            childTags = ', '.join([child.prefixedName for child in segScenElt.iterchildren() if isinstance(child, ModelObject) and child.tag != '{http://xbrl.org/2006/xbrldi}explicitMember'])
                            if len(childTags) > 0:
                                if validateEFMpragmatic:
                                    contextsWithDisallowedOCEcontent.append(context)
                                else:
                                    modelXbrl.error(('EFM.6.05.05', 'GFM.1.02.05'), _('%(elementName)s of context Id %(context)s has disallowed content: %(content)s'), modelObject=context, context=contextID, content=childTags, elementName=contextName.partition('}')[2].title())

                if context.isForeverPeriod:
                    self.modelXbrl.error('EFM.6.05.38', _('Context %(contextID)s has a forever period.'), modelObject=context, contextID=contextID)

        if validateEFMpragmatic:
            if contextsWithDisallowedOCEs:
                modelXbrl.error(('EFM.6.05.04', 'GFM.1.02.04'), _('%(count)s contexts contain disallowed %(elementName)s: %(context)s'), modelObject=contextsWithDisallowedOCEs, elementName=notAllowed, count=len(contextsWithDisallowedOCEs), context=', '.join(c.id for c in contextsWithDisallowedOCEs))
            if contextsWithDisallowedOCEcontent:
                modelXbrl.error(('EFM.6.05.05', 'GFM.1.02.05'), _('%(count)s contexts contain disallowed %(elementName)s content: %(context)s'), modelObject=contextsWithDisallowedOCEcontent, elementName=disclosureSystem.contextElement, count=len(contextsWithDisallowedOCEcontent), context=', '.join(c.id for c in contextsWithDisallowedOCEcontent))
            del uniqueContextHashes
            del contextsWithDisallowedOCEs
            del contextsWithDisallowedOCEcontent
            self.modelXbrl.profileActivity('... filer context checks', minTimeToShow=1.0)
            amendmentDescription = None
            amendmentDescriptionFact = None
            amendmentFlag = None
            amendmentFlagFact = None
            documentPeriodEndDate = None
            documentPeriodEndDateFact = None
            documentType = None
            documentTypeFact = None
            deiItems = {}
            deiFacts = {}
            commonSharesItemsByStockClass = defaultdict(list)
            commonSharesClassMembers = None
            hasDefinedStockAxis = False
            hasCommonSharesOutstandingDimensionedFactWithDefaultStockClass = False
            commonSharesClassUndefinedMembers = None
            commonStockMeasurementDatetime = None
            deiCheckLocalNames = {
             'EntityRegistrantName',
             'EntityCommonStockSharesOutstanding',
             'EntityCurrentReportingStatus',
             'EntityVoluntaryFilers',
             disclosureSystem.deiCurrentFiscalYearEndDateElement,
             'EntityFilerCategory',
             'EntityWellKnownSeasonedIssuer',
             'EntityPublicFloat',
             disclosureSystem.deiDocumentFiscalYearFocusElement,
             'DocumentFiscalPeriodFocus',
             'EntityReportingCurrencyISOCode'}
            for f in modelXbrl.facts:
                factContextID = f.contextID
                contextIDs.discard(factContextID)
                context = f.context
                factInDeiNamespace = None
                factQname = f.qname
                if factQname:
                    factElementName = factQname.localName
                    if disclosureSystem.deiNamespacePattern is not None:
                        factInDeiNamespace = disclosureSystem.deiNamespacePattern.match(factQname.namespaceURI)
                    if context is not None:
                        pass
                    if not context.hasSegment and not context.hasScenario:
                        if factInDeiNamespace:
                            pass
                value = f.value
                if factElementName == disclosureSystem.deiAmendmentFlagElement:
                    amendmentFlag = value
                    amendmentFlagFact = f
                else:
                    if factElementName == 'AmendmentDescription':
                        amendmentDescription = value
                        amendmentDescriptionFact = f
                    else:
                        if factElementName == disclosureSystem.deiDocumentPeriodEndDateElement:
                            documentPeriodEndDate = value
                            documentPeriodEndDateFact = f
                            commonStockMeasurementDatetime = context.endDatetime
                        else:
                            if factElementName == 'DocumentType':
                                documentType = value
                                documentTypeFact = f
                            else:
                                if factElementName == disclosureSystem.deiFilerIdentifierElement:
                                    deiItems[factElementName] = value
                                    deiFilerIdentifierFact = f
                                else:
                                    if factElementName == disclosureSystem.deiFilerNameElement:
                                        deiItems[factElementName] = value
                                        deiFilerNameFact = f
                                    else:
                                        if factElementName in deiCheckLocalNames:
                                            deiItems[factElementName] = value
                                            deiFacts[factElementName] = f
                                            if self.requiredContext is None and context.isStartEndPeriod and context.startDatetime is not None and context.endDatetime is not None:
                                                self.requiredContext = context
                                        else:
                                            isEntityCommonStockSharesOutstanding = factElementName == 'EntityCommonStockSharesOutstanding'
                                            hasClassOfStockMember = False
                                            for dimValue in context.qnameDims.values():
                                                if dimValue.isExplicit:
                                                    dimConcept = dimValue.dimension
                                                    memConcept = dimValue.member
                                                    for dConcept in (dimConcept, memConcept):
                                                        if dConcept is not None:
                                                            conceptsUsed[dConcept] = False

                                                    if isEntityCommonStockSharesOutstanding and dimConcept is not None and dimConcept.name == 'StatementClassOfStockAxis':
                                                        commonSharesItemsByStockClass[memConcept.qname].append(f)
                                                        if commonSharesClassMembers is None:
                                                            commonSharesClassMembers = set()
                                                        commonSharesClassMembers.add(memConcept.qname)
                                                        hasClassOfStockMember = True

                                        if isEntityCommonStockSharesOutstanding and not hasClassOfStockMember:
                                            hasCommonSharesOutstandingDimensionedFactWithDefaultStockClass = True
                                        if self.validateEFM:
                                            for pluginXbrlMethod in pluginClassMethods('Validate.EFM.Fact'):
                                                pluginXbrlMethod(self, f)

                                        concept = f.concept
                                        if concept is None:
                                            modelXbrl.error(('EFM.6.04.03', 'GFM.2.01.01'), _('Fact %(fact)s of context %(contextID)s has an XBRL error'), modelObject=f, fact=f.qname, contextID=factContextID)
                                        else:
                                            conceptsUsed[concept] = False
                                            if concept.isNumeric and f.precision:
                                                modelXbrl.error(('EFM.6.05.17', 'GFM.1.02.16'), _("Numeric fact %(fact)s of context %(contextID)s has a precision attribute '%(precision)s'"), modelObject=f, fact=f.qname, contextID=factContextID, precision=f.precision)
                                            if self.validateEFM and concept.type is not None and concept.type.isDomainItemType:
                                                modelXbrl.error('EFM.6.05.25', _('Domain item %(fact)s in context %(contextID)s may not appear as a fact'), modelObject=f, fact=f.qname, contextID=factContextID)
                                        if validateInlineXbrlGFM and (f.localName == 'nonFraction' or f.localName == 'fraction'):
                                            syms = signOrCurrencyPattern.findall(f.text)
                                            if syms:
                                                modelXbrl.error(('EFM.N/A', 'GFM.1.10.18'), 'ix-numeric Fact %(fact)s of context %(contextID)s has a sign or currency symbol "%(value)s" in "%(text)s"', modelObject=f, fact=f.qname, contextID=factContextID, value=''.join(s for t in syms for s in t), text=f.text)

            self.entityRegistrantName = deiItems.get('EntityRegistrantName')
            if not (entityIdentifierValue == '0000000000' and self.validateEFM and documentType == 'L SDR'):
                pass
            if disclosureSystem.deiFilerIdentifierElement in deiItems:
                value = deiItems[disclosureSystem.deiFilerIdentifierElement]
                if entityIdentifierValue != value:
                    self.modelXbrl.error(('EFM.6.05.23', 'GFM.3.02.02'), _('dei:%(elementName)s %(value)s must match the context entity identifier %(entityIdentifier)s'), modelObject=deiFilerIdentifierFact, elementName=disclosureSystem.deiFilerIdentifierElement, value=value, entityIdentifier=entityIdentifierValue)
                if paramFilerIdentifiers:
                    pass
                if value not in paramFilerIdentifiers:
                    self.modelXbrl.error(('EFM.6.05.23.submissionIdentifier', 'GFM.3.02.02'), _('dei:%(elementName)s %(value)s must match submission: %(filerIdentifier)s'), modelObject=deiFilerIdentifierFact, elementName=disclosureSystem.deiFilerIdentifierElement, value=value, filerIdentifier=','.join(paramFilerIdentifiers))
        elif paramFilerIdentifier and value != paramFilerIdentifier:
            self.modelXbrl.error(('EFM.6.05.23.submissionIdentifier', 'GFM.3.02.02'), _('dei:%(elementName)s %(value)s must match submission: %(filerIdentifier)s'), modelObject=deiFilerIdentifierFact, elementName=disclosureSystem.deiFilerIdentifierElement, value=value, filerIdentifier=paramFilerIdentifier)
        if disclosureSystem.deiFilerNameElement in deiItems:
            value = deiItems[disclosureSystem.deiFilerNameElement]
            if paramFilerIdentifiers and paramFilerNames and entityIdentifierValue in paramFilerIdentifiers:
                prefix = paramFilerNames[paramFilerIdentifiers.index(entityIdentifierValue)]
                if not value.lower().startswith(prefix.lower()):
                    self.modelXbrl.error(('EFM.6.05.24', 'GFM.3.02.02'), _('dei:%(elementName)s %(prefix)s should be a case-insensitive prefix of: %(value)s'), modelObject=deiFilerNameFact, elementName=disclosureSystem.deiFilerNameElement, prefix=prefix, value=value)
                self.modelXbrl.profileActivity('... filer fact checks', minTimeToShow=1.0)
                if len(contextIDs) > 0:
                    for undefinedFact in modelXbrl.undefinedFacts:
                        contextIDs.discard(undefinedFact.get('contextRef'))

                    if len(contextIDs) > 0:
                        modelXbrl.error(('EFM.6.05.08', 'GFM.1.02.08'), _('The instance document contained a context(s) %(contextIDs)s that was(are) not used in any fact.'), modelXbrl=modelXbrl, contextIDs=', '.join(str(c) for c in contextIDs))
                    if disclosureSystem.GFM or disclosureSystemVersion[0] >= 27 or documentType in {'40-F', '10-KT/A', 'N-CSRS/A', '20-F', '10-Q/A', '10', '10-Q', '10-KT', 'N-Q/A', '10-QT/A', 'N-CSRS', '10-QT', '10/A', '10-K/A', 'N-Q', '20-F/A', 'N-CSR', 'N-CSR/A', '10-K', '40-F/A'}:
                        durationCntxStartDatetimes = defaultdict(set)
                        for cntx in contexts:
                            if cntx.isStartEndPeriod and cntx.startDatetime is not None:
                                durationCntxStartDatetimes[cntx.startDatetime].add(cntx)

                        probStartEndCntxsByEnd = defaultdict(set)
                        startEndCntxsByEnd = defaultdict(set)
                        probInstantCntxsByEnd = defaultdict(set)
                        probCntxs = set()
                        for cntx in contexts:
                            end = cntx.endDatetime
                            if end is not None:
                                if cntx.isStartEndPeriod:
                                    thisStart = cntx.startDatetime
                                    for otherStart, otherCntxs in durationCntxStartDatetimes.items():
                                        duration = end - otherStart
                                        if duration > datetime.timedelta(0) and duration <= datetime.timedelta(1):
                                            if disclosureSystemVersion[0] < 27:
                                                probCntxs |= otherCntxs - {cntx}
                                            elif thisStart is not None and end - thisStart > datetime.timedelta(1):
                                                for otherCntx in otherCntxs:
                                                    if otherCntx is not cntx and otherCntx.endDatetime != end and otherStart != cntx.startDatetime:
                                                        probCntxs.add(otherCntx)

                                    if probCntxs:
                                        probStartEndCntxsByEnd[end] |= probCntxs
                                        startEndCntxsByEnd[end] |= {cntx}
                                        probCntxs.clear()
                                    if self.validateEFM and cntx.isInstantPeriod:
                                        for otherStart, otherCntxs in durationCntxStartDatetimes.items():
                                            duration = end - otherStart
                                            if duration > datetime.timedelta(0) and duration <= datetime.timedelta(1):
                                                probCntxs |= otherCntxs

                                        if probCntxs:
                                            probInstantCntxsByEnd[end] |= probCntxs | {cntx}
                                            probCntxs.clear()

                        del probCntxs
                        for end, probCntxs in probStartEndCntxsByEnd.items():
                            endCntxs = startEndCntxsByEnd[end]
                            modelXbrl.error(('EFM.6.05.09', 'GFM.1.2.9'), _('Context endDate %(endDate)s, and startDate(s) have a duration of one day, for end context(s): %(endContexts)s and start context(s): %(startContexts)s; that is inconsistent with document type %(documentType)s.'), modelObject=probCntxs, endDate=XmlUtil.dateunionValue(end, subtractOneDay=True), endContexts=', '.join(sorted(c.id for c in endCntxs)), startContexts=', '.join(sorted(c.id for c in probCntxs)), documentType=documentType)

                        if disclosureSystemVersion[0] < 27:
                            for end, probCntxs in probInstantCntxsByEnd.items():
                                modelXbrl.error('EFM.6.05.10', _('Context instant date %(endDate)s startDate has a duration of one day,with end (instant) of context(s): %(contexts)s; that is inconsistent with document type %(documentType)s.'), modelObject=probCntxs, endDate=XmlUtil.dateunionValue(end, subtractOneDay=True), contexts=', '.join(sorted(c.id for c in probCntxs)), documentType=documentType)

                        del probStartEndCntxsByEnd
                        del startEndCntxsByEnd
                        del probInstantCntxsByEnd
                        del durationCntxStartDatetimes
                        self.modelXbrl.profileActivity('... filer instant-duration checks', minTimeToShow=1.0)
                    foundRequiredContext = False
                    for c in contexts:
                        if c.isStartEndPeriod:
                            if not c.hasSegment:
                                foundRequiredContext = True
                                break

                    if not foundRequiredContext:
                        modelXbrl.error(('EFM.6.05.19', 'GFM.1.02.18'), _('Required context (no segment) not found for document type %(documentType)s.'), modelObject=documentTypeFact, documentType=documentType)
                    uniqueUnitHashes = {}
                    for unit in self.modelXbrl.units.values():
                        h = unit.hash
                        if h in uniqueUnitHashes:
                            if unit.isEqualTo(uniqueUnitHashes[h]):
                                modelXbrl.error(('EFM.6.05.11', 'GFM.1.02.10'), _('Units %(unitID)s and %(unitID2)s are equivalent.'), modelObject=(
                                 unit, uniqueUnitHashes[h]), unitID=unit.id, unitID2=uniqueUnitHashes[h].id)
                        else:
                            uniqueUnitHashes[h] = unit
                        if self.validateEFM:
                            for measureElt in unit.iterdescendants(tag='{http://www.xbrl.org/2003/instance}measure'):
                                if isinstance(measureElt.xValue, ModelValue.QName) and len(measureElt.xValue.localName) > 65:
                                    l = len(measureElt.xValue.localName.encode('utf-8'))
                                    if l > 200:
                                        modelXbrl.error('EFM.6.05.36', _('Unit has a measure  with localName length (%(length)s) over 200 bytes long in utf-8, %(measure)s.'), modelObject=measureElt, unitID=unit.id, measure=measureElt.xValue.localName, length=l)

                    del uniqueUnitHashes
                    self.modelXbrl.profileActivity('... filer unit checks', minTimeToShow=1.0)
                    requiredFactLang = disclosureSystem.defaultXmlLang
                    factsForLang = {}
                    factForConceptContextUnitLangHash = {}
                    keysNotDefaultLang = {}
                    iF1 = 1
                    for f1 in modelXbrl.facts:
                        if not f1.isNil:
                            langTestKey = '{0},{1},{2}'.format(f1.qname, f1.contextID, f1.unitID)
                            factsForLang.setdefault(langTestKey, []).append(f1)
                            lang = f1.xmlLang
                            if lang and lang != requiredFactLang:
                                keysNotDefaultLang[langTestKey] = f1
                            if f1.isNumeric and f1.decimals and f1.decimals != 'INF' and not f1.isNil and getattr(f1, 'xValid', 0) == 4:
                                try:
                                    insignificance = insignificantDigits(f1.xValue, decimals=f1.decimals)
                                    if insignificance:
                                        modelXbrl.error(('EFM.6.05.37', 'GFM.1.02.26'), _('Fact %(fact)s of context %(contextID)s decimals %(decimals)s value %(value)s has nonzero digits in insignificant portion %(insignificantDigits)s.'), modelObject=f1, fact=f1.qname, contextID=f1.contextID, decimals=f1.decimals, value=f1.xValue, truncatedDigits=insignificance[0], insignificantDigits=insignificance[1])
                                except (ValueError, TypeError):
                                    modelXbrl.error(('EFM.6.05.37', 'GFM.1.02.26'), _('Fact %(fact)s of context %(contextID)s decimals %(decimals)s value %(value)s causes Value Error exception.'), modelObject=f1, fact=f1.qname, contextID=f1.contextID, decimals=f1.decimals, value=f1.value)

                                h = f1.conceptContextUnitLangHash
                                if h in factForConceptContextUnitLangHash:
                                    f2 = factForConceptContextUnitLangHash[h]
                                    if f1.qname == f2.qname and f1.contextID == f2.contextID and f1.unitID == f2.unitID and f1.xmlLang == f2.xmlLang:
                                        modelXbrl.error(('EFM.6.05.12', 'GFM.1.02.11'), 'Facts %(fact)s of context %(contextID)s and %(contextID2)s are equivalent.', modelObject=(
                                         f1, f2), fact=f1.qname, contextID=f1.contextID, contextID2=f2.contextID)
                                else:
                                    factForConceptContextUnitLangHash[h] = f1
                                iF1 += 1

                    del factForConceptContextUnitLangHash
                    self.modelXbrl.profileActivity('... filer fact checks', minTimeToShow=1.0)
                    for keyNotDefaultLang, factNotDefaultLang in keysNotDefaultLang.items():
                        anyDefaultLangFact = False
                        for fact in factsForLang[keyNotDefaultLang]:
                            if fact.xmlLang == requiredFactLang:
                                anyDefaultLangFact = True
                                break

                        if not anyDefaultLangFact:
                            self.modelXbrl.error(('EFM.6.05.14', 'GFM.1.02.13'), _("Fact %(fact)s of context %(contextID)s has text of xml:lang '%(lang)s' without corresponding %(lang2)s text"), modelObject=factNotDefaultLang, fact=factNotDefaultLang.qname, contextID=factNotDefaultLang.contextID, lang=factNotDefaultLang.xmlLang, lang2=requiredFactLang)

                    if not labelsRelationshipSet:
                        self.modelXbrl.error(('EFM.6.10.01.missingLabelLinkbase', 'GFM.1.05.01'), _('A label linkbase is required but was not found'), modelXbrl=modelXbrl)
        else:
            if disclosureSystem.defaultXmlLang:
                for concept in conceptsUsed.keys():
                    self.checkConceptLabels(modelXbrl, labelsRelationshipSet, disclosureSystem, concept)

            if self.validateEFMorGFM:
                ValidateFilingText.validateTextBlockFacts(modelXbrl)
                if amendmentFlag is None:
                    modelXbrl.log('WARNING' if validateEFMpragmatic else 'ERROR', ('EFM.6.05.20.missingAmendmentFlag',
                                                                                   'GFM.3.02.01'), _('%(elementName)s is not found in the default context'), modelXbrl=modelXbrl, elementName=disclosureSystem.deiAmendmentFlagElement)
        if not documentPeriodEndDate:
            modelXbrl.error(('EFM.6.05.20.missingDocumentPeriodEndDate', 'GFM.3.02.01'), _('%(elementName)s is required and was not found in the default context'), modelXbrl=modelXbrl, elementName=disclosureSystem.deiDocumentPeriodEndDateElement)
        else:
            dateMatch = datePattern.match(documentPeriodEndDate)
            if not dateMatch or dateMatch.lastindex != 3:
                modelXbrl.error(('EFM.6.05.20', 'GFM.3.02.01'), _("%(elementName)s is in the default context is incorrect '%(date)s'"), modelXbrl=modelXbrl, elementName=disclosureSystem.deiDocumentPeriodEndDateElement, date=documentPeriodEndDate)
            self.modelXbrl.profileActivity('... filer label and text checks', minTimeToShow=1.0)
            if self.validateEFM:
                if amendmentFlag == 'true' and amendmentDescription is None:
                    modelXbrl.log('WARNING' if validateEFMpragmatic else 'ERROR', 'EFM.6.05.20.missingAmendmentDescription', _('AmendmentFlag is true in context %(contextID)s so AmendmentDescription is also required'), modelObject=amendmentFlagFact, contextID=amendmentFlagFact.contextID if amendmentFlagFact is not None else 'unknown')
                if amendmentDescription is not None and amendmentFlag != 'true':
                    modelXbrl.log('WARNING' if validateEFMpragmatic else 'ERROR', 'EFM.6.05.20.extraneous', _('AmendmentDescription can not be provided when AmendmentFlag is not true in context %(contextID)s'), modelObject=amendmentDescriptionFact, contextID=amendmentDescriptionFact.contextID)
                if documentType is None:
                    modelXbrl.error('EFM.6.05.20.missingDocumentType', _('DocumentType is required and was not found in the default context'), modelXbrl=modelXbrl)
            if documentType not in {'485BPOS', 'F-3', 'POS462B', 'F-10/A', 'S-1MEF', 'S-4MEF', 'N-1A', '10-QT/A', '20FR12B', '40FR12B/A', 'S-3DPOS', '8-K15D5', '8-K12G3', '10-QT', '10-K/A', 'F-1/A', '8-K12B/A', 'F-3MEF', '20-F', 'L SDR', 'K SDR', 'S-B', 'S-3ASR', '10-Q/A', '40FR12G', '6-K', 'F-1', 'F-3ASR', 'F-3D', '40FR12B', '497', 'F-4 POS', '10-Q', '8-K/A', 'F-4EF', '40FR12G/A', 'S-3MEF', '40-F/A', '10-12B/A', 'N-CSRS/A', 'N-1A/A', 'SD/A', 'F-9 POS', '10-12G/A', 'F-9/A', 'F-4', '8-K15D5/A', '8-K12B', 'SP 15D2/A', 'S-4/A', 'F-6', 'F-3/A', '6-K/A', '20FR12G/A', '20-F/A', 'POSASR', '10-K', '20FR12B/A', 'F-9EF', 'S-4', 'S-4EF', 'S-11MEF', 'F-10', 'S-20', 'S-11', 'Other', 'F-9', 'S-1', 'S-11/A', '40-F', '8-K12G3/A', 'F-4MEF', 'N-Q', '10-12G', 'SD', 'POS AM', 'S-BMEF', 'N-CSRS', 'F-3DPOS', 'N-CSR/A', 'F-10EF', 'F-4/A', 'S-3/A', 'SP 15D2', '10-KT', 'POS EX', 'S-1/A', '10-12B', '10-KT/A', '20FR12G', 'S-4 POS', 'S-3', 'N-CSR', 'N-Q/A', '8-K', 'F-10POS', 'S-3D', 'POS462C', 'F-1MEF'}:
                modelXbrl.error('EFM.6.05.20.documentTypeValue', _("DocumentType '%(documentType)s' of context %(contextID)s was not recognized"), modelObject=documentTypeFact, contextID=documentTypeFact.contextID, documentType=documentType)
            elif submissionType:
                expectedDocumentTypes = {'10-12B': ('10-12B', 'Other'), 
                 '10-12B/A': ('10-12B/A', 'Other'), 
                 '10-12G': ('10-12G', 'Other'), 
                 '10-12G/A': ('10-12G/A', 'Other'), 
                 '10-K': ('10-K', ), 
                 '10-K/A': ('10-K', '10-K/A'), 
                 '10-KT': ('10-K', '10-KT', 'Other'), 
                 '10-KT/A': ('10-K', '10-KT', '10-KT/A', 'Other'), 
                 '10-Q': ('10-Q', ), 
                 '10-Q/A': ('10-Q', '10-Q/A'), 
                 '10-QT': ('10-Q', '10-QT', 'Other'), 
                 '10-QT/A': ('10-Q', '10-QT', '10-QT/A', 'Other'), 
                 '20-F': ('20-F', ), 
                 '20-F/A': ('20-F', '20-F/A'), 
                 '20FR12B': ('20FR12B', 'Other'), 
                 '20FR12B/A': ('20FR12B/A', 'Other'), 
                 '20FR12G': ('20FR12G', 'Other'), 
                 '20FR12G/A': ('20FR12G/A', 'Other'), 
                 '40-F': ('40-F', ), 
                 '40-F/A': ('40-F', '40-F/A'), 
                 '40FR12B': ('40FR12B', 'Other'), 
                 '40FR12B/A': ('40FR12B/A', 'Other'), 
                 '40FR12G': ('40FR12G', 'Other'), 
                 '40FR12G/A': ('40FR12G/A', 'Other'), 
                 '485BPOS': ('485BPOS', ), 
                 '497': ('497', 'Other'), 
                 '6-K': ('6-K', ), 
                 '6-K/A': ('6-K', '6-K/A'), 
                 '8-K': ('8-K', ), 
                 '8-K/A': ('8-K', '8-K/A'), 
                 '8-K12B': ('8-K12B', 'Other'), 
                 '8-K12B/A': ('8-K12B/A', 'Other'), 
                 '8-K12G3': ('8-K12G3', 'Other'), 
                 '8-K12G3/A': ('8-K12G3/A', 'Other'), 
                 '8-K15D5': ('8-K15D5', 'Other'), 
                 '8-K15D5/A': ('8-K15D5/A', 'Other'), 
                 'F-1': ('F-1', ), 
                 'F-1/A': ('F-1', 'F-1/A'), 
                 'F-10': ('F-10', ), 
                 'F-10/A': ('F-10', 'F-10/A'), 
                 'F-10EF': ('F-10EF', 'Other'), 
                 'F-10POS': ('F-10POS', 'Other'), 
                 'F-1MEF': ('F-1MEF', ), 
                 'F-3': ('F-3', ), 
                 'F-3/A': ('F-3', 'F-3/A'), 
                 'F-3ASR': ('F-3', 'F-3ASR'), 
                 'F-3D': ('F-3', 'F-3D'), 
                 'F-3DPOS': ('F-3', 'F-3DPOS'), 
                 'F-3MEF': ('F-3MEF', ), 
                 'F-4': ('F-4', ), 
                 'F-4 POS': ('F-4', 'F-4 POS'), 
                 'F-4/A': ('F-4', 'F-4/A'), 
                 'F-4EF': ('F-4', 'F-4EF'), 
                 'F-4MEF': ('F-4MEF', ), 
                 'F-9': ('F-9', ), 
                 'F-9 POS': ('F-9', 'F-9 POS'), 
                 'F-9/A': ('F-9', 'F-9/A'), 
                 'F-9EF': ('F-9', 'F-9EF'), 
                 'N-1A': ('N-1A', ), 
                 'N-1A/A': ('N-1A/A', 'Other'), 
                 'N-CSR': ('N-CSR', ), 
                 'N-CSR/A': ('N-CSR/A', ), 
                 'N-CSRS': ('N-CSRS', ), 
                 'N-CSRS/A': ('N-CSRS/A', ), 
                 'N-Q': ('N-Q', ), 
                 'N-Q/A': ('N-Q/A', ), 
                 'POS AM': ('F-1', 'F-3', 'F-4', 'F-6', 'Other', 'POS AM', 'S-1', 'S-11', 'S-20', 'S-3', 'S-4',
 'S-B'), 
                 
                 'POS EX': ('F-3', 'F-4', 'Other', 'POS EX', 'S-1', 'S-3', 'S-4'), 
                 
                 'POS462B': ('F-1MEF', 'F-3MEF', 'F-4MEF', 'Other', 'POS462B', 'POS462C', 'S-11MEF', 'S-1MEF',
 'S-3MEF', 'S-BMEF'), 
                 
                 'POSASR': ('F-3', 'Other', 'POSASR', 'S-3'), 
                 'S-1': ('S-1', ), 
                 'S-1/A': ('S-1', 'S-1/A'), 
                 'S-11': ('S-11', ), 
                 'S-11/A': ('S-11/A', ), 
                 'S-11MEF': ('S-11MEF', ), 
                 'S-1MEF': ('S-1MEF', ), 
                 'S-3': ('S-3', ), 
                 'S-3/A': ('S-3', 'S-3/A'), 
                 'S-3ASR': ('S-3', 'S-3ASR'), 
                 'S-3D': ('S-3', 'S-3D'), 
                 'S-3DPOS': ('S-3', 'S-3DPOS'), 
                 'S-3MEF': ('S-3MEF', ), 
                 'S-4': ('S-4', ), 
                 'S-4 POS': ('S-4', 'S-4 POS'), 
                 'S-4/A': ('S-4', 'S-4/A'), 
                 'S-4EF': ('S-4', 'S-4EF'), 
                 'S-4MEF': ('S-4MEF', ), 
                 'SD': ('SD', ), 
                 'SD/A': ('SD/A', ), 
                 'SP 15D2': ('SP 15D2', ), 
                 'SP 15D2/A': ('SP 15D2/A', ), 
                 'SDR': ('K SDR', 'L SDR'), 
                 'SDR/A': ('K SDR', 'L SDR'), 
                 'SDR-A': ('K SDR', 'L SDR'), 
                 'SDR/W ': ('K SDR', 'L SDR')}.get(submissionType)
                if expectedDocumentTypes and documentType not in expectedDocumentTypes:
                    modelXbrl.error('EFM.6.05.20.submissionDocumentType' if self.exhibitType != 'EX-2.01' else 'EFM.6.23.03', _("DocumentType '%(documentType)s' of context %(contextID)s inapplicable to submission form %(submissionType)s"), modelObject=documentTypeFact, contextID=documentTypeFact.contextID, documentType=documentType, submissionType=submissionType, messageCodes=('EFM.6.05.20.submissionDocumentType',
                                                                                                                                                                                                                                                                                                                                                                                            'EFM.6.23.03'))
            if self.exhibitType and documentType is not None:
                if (documentType in ('SD', 'SD/A')) != (self.exhibitType == 'EX-2.01'):
                    modelXbrl.error({'EX-100': 'EFM.6.23.04', 
                     'EX-101': 'EFM.6.23.04', 
                     'EX-99.K SDR.INS': 'EFM.6.23.04', 
                     'EX-99.L SDR.INS': 'EFM.6.23.04', 
                     'EX-2.01': 'EFM.6.23.05'}.get(self.exhibitType, 'EX-101'), _('The value for dei:DocumentType, %(documentType)s, is not allowed for %(exhibitType)s attachments.'), modelObject=documentTypeFact, contextID=documentTypeFact.contextID, documentType=documentType, exhibitType=self.exhibitType, messageCodes=('EFM.6.23.04',
                                                                                                                                                                                                                                                                                                                                   'EFM.6.23.04',
                                                                                                                                                                                                                                                                                                                                   'EFM.6.23.05'))
            elif (documentType == 'K SDR') != (val.exhibitType in ('EX-99.K SDR', 'EX-99.K SDR.INS')) or (documentType == 'L SDR') != (val.exhibitType in ('EX-99.L SDR',
                                                                                                                                                           'EX-99.L SDR.INS')):
                modelXbrl.error('EFM.6.05.20.exhibitDocumentType', _("The value for dei:DocumentType, '%(documentType)s' is not allowed for %(exhibitType)s attachments."), modelObject=documentTypeFact, contextID=documentTypeFact.contextID, documentType=documentType, exhibitType=val.exhibitType)
        for doctypesRequired, deiItemsRequired in ((('10-K', '10-KT', '10-Q', '10-QT', '20-F', '40-F', '10-K/A', '10-KT/A', '10-Q/A', '10-QT/A', '20-F/A', '40-F/A', '6-K', 'NCSR', 'N-CSR', 'N-CSRS', 'N-Q', '6-K/A', 'NCSR/A', 'N-CSR/A', 'N-CSRS/A', 'N-Q/A', '10', 'S-1', 'S-3', 'S-4', 'S-11', 'POS AM', '10/A', 'S-1/A', 'S-3/A', 'S-4/A', 'S-11/A', '8-K', 'F-1', 'F-3', 'F-10', '497', '485BPOS', '8-K/A', 'F-1/A', 'F-3/A', 'F-10/A', 'K SDR', 'L SDR', 'Other'), ('EntityRegistrantName', 'EntityCentralIndexKey')),
                                                   (('10-K', '10-KT', '20-F', '40-F', '10-K/A', '10-KT/A', '20-F/A', '40-F/A'), ('EntityCurrentReportingStatus',)),
                                                   (('10-K', '10-KT', '10-K/A', '10-KT/A'), ('EntityVoluntaryFilers', 'EntityPublicFloat')),
                                                   (('10-K', '10-KT', '10-Q', '10-QT', '20-F', '40-F', '10-K/A', '10-KT/A', '10-Q/A', '10-QT/A', '20-F/A', '40-F/A', '6-K', 'NCSR', 'N-CSR', 'N-CSRS', 'N-Q', '6-K/A', 'NCSR/A', 'N-CSR/A', 'N-CSRS/A', 'N-Q/A', 'K SDR', 'L SDR'), ('CurrentFiscalYearEndDate', 'DocumentFiscalYearFocus', 'DocumentFiscalPeriodFocus')),
                                                   (('10-K', '10-KT', '10-Q', '10-QT', '20-F', '10-K/A', '10-KT/A', '10-Q/A', '10-QT/A', '20-F/A', '10', 'S-1', 'S-3', 'S-4', 'S-11', 'POS AM', '10/A', 'S-1/A', 'S-3/A', 'S-4/A', 'S-11/A', 'K SDR', 'L SDR'), ('EntityFilerCategory',)),
                                                   (('10-K', '10-KT', '20-F', '10-K/A', '10-KT/A', '20-F/A'), ('EntityWellKnownSeasonedIssuer',)),
                                                   (('SD', 'SD/A'), ('EntityReportingCurrencyISOCode',))):
            if documentType in doctypesRequired:
                for deiItem in deiItemsRequired:
                    if deiItem not in deiItems or not deiItems[deiItem]:
                        modelXbrl.log('WARNING' if validateEFMpragmatic and deiItem in {'EntityFilerCategory', 'EntityCurrentReportingStatus', 'CurrentFiscalYearEndDate', 'EntityWellKnownSeasonedIssuer', 'DocumentFiscalYearFocus', 'DocumentFiscalPeriodFocus', 'EntityPublicFloat', 'EntityVoluntaryFilers'} else 'ERROR', 'EFM.6.05.21.{0}'.format(deiItem) if validateEFMpragmatic and deiItem in {'EntityFilerCategory', 'EntityRegistrantName', 'EntityCentralIndexKey', 'EntityCurrentReportingStatus', 'CurrentFiscalYearEndDate', 'EntityWellKnownSeasonedIssuer', 'DocumentFiscalYearFocus', 'DocumentFiscalPeriodFocus', 'EntityPublicFloat', 'EntityVoluntaryFilers'} else 'EFM.6.23.36' if deiItem == 'EntityReportingCurrencyISOCode' else 'EFM.6.05.21', _("dei:%(elementName)s is required for DocumentType '%(documentType)s' of context %(contextID)s"), modelObject=documentTypeFact, contextID=documentTypeFact.contextID, documentType=documentType, elementName=deiItem, messageCodes=('EFM.6.05.21.CurrentFiscalYearEndDate',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                'EFM.6.05.21.DocumentFiscalPeriodFocus',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                'EFM.6.05.21.DocumentFiscalYearFocus',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                'EFM.6.05.21.EntityRegistrantName',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                'EFM.6.05.21.EntityCentralIndexKey',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                'EFM.6.05.21.EntityCurrentReportingStatus',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                'EFM.6.05.21.EntityFilerCategory',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                'EFM.6.05.21.EntityPublicFloat',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                'EFM.6.05.21.EntityVoluntaryFilers',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                'EFM.6.05.21.EntityWellKnownSeasonedIssuer',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                'EFM.6.23.36',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                'EFM.6.05.21'))

        if documentType in {'40-F', '10-KT/A', '20-F', '10-Q/A', '10-Q', '10-KT', '10-QT/A', '10-QT', '10-K/A', '20-F/A', '10-K', '40-F/A'}:
            defaultContextSharesOutstandingValue = deiItems.get('EntityCommonStockSharesOutstanding')
            errLevel = 'WARNING' if validateEFMpragmatic else 'ERROR'
            if commonSharesClassMembers:
                if defaultContextSharesOutstandingValue:
                    modelXbrl.log(errLevel, 'EFM.6.05.26', _("dei:EntityCommonStockSharesOutstanding is required for DocumentType '%(documentType)s' but not in the default context because there are multiple classes of common shares"), modelObject=documentTypeFact, contextID=documentTypeFact.contextID, documentType=documentType)
                elif len(commonSharesClassMembers) == 1:
                    modelXbrl.log(errLevel, 'EFM.6.05.26', _("dei:EntityCommonStockSharesOutstanding is required for DocumentType '%(documentType)s' but but a default-context because only one class of stock"), modelObject=documentTypeFact, documentType=documentType)
                for mem, facts in commonSharesItemsByStockClass.items():
                    if len(facts) != 1:
                        modelXbrl.log(errLevel, 'EFM.6.05.26', _("dei:EntityCommonStockSharesOutstanding is required for DocumentType '%(documentType)s' but only one per stock class %(stockClass)s"), modelObject=documentTypeFact, documentType=documentType, stockClass=mem)

            else:
                if hasCommonSharesOutstandingDimensionedFactWithDefaultStockClass and not defaultContextSharesOutstandingValue:
                    modelXbrl.log(errLevel, 'EFM.6.05.26', _("dei:EntityCommonStockSharesOutstanding is required for DocumentType '%(documentType)s' but missing for a non-default-context fact"), modelObject=documentTypeFact, documentType=documentType)
                elif not defaultContextSharesOutstandingValue:
                    modelXbrl.log(errLevel, 'EFM.6.05.26', _("dei:EntityCommonStockSharesOutstanding is required for DocumentType '%(documentType)s' in the default context because there are not multiple classes of common shares"), modelObject=documentTypeFact, documentType=documentType)
            if documentType in ('SD', 'SD/A'):
                self.modelXbrl.profileActivity('... filer required facts checks (other than SD)', minTimeToShow=1.0)
                rxdNs = None
                rxdDoc = None
                hasRxdPre = hasRxdDef = False
                for rxdLoc in disclosureSystem.familyHrefs['RXD']:
                    rxdUri = rxdLoc.href
                    if rxdUri in modelXbrl.urlDocs:
                        if rxdUri.endswith('.xsd') and rxdLoc.elements == '1':
                            if rxdNs is None:
                                rxdDoc = modelXbrl.urlDocs[rxdUri]
                                rxdNs = rxdDoc.targetNamespace
                            else:
                                modelXbrl.error('EFM.6.23.10', _('The DTS of must use only one version of the RXD schema'), modelObject=(
                                 rxdDoc, modelXbrl.urlDocs[rxdUri]), instance=instanceName)
                        else:
                            if '/rxd-pre-' in rxdUri:
                                hasRxdPre = True
                            elif '/rxd-def-' in rxdUri:
                                hasRxdDef = True

                if not hasRxdPre:
                    modelXbrl.error('EFM.6.23.08', _('The DTS must use a standard presentation linkbase from Family RXD in edgartaxonomies.xml.'), modelObject=modelXbrl, instance=instanceName)
                if not hasRxdDef:
                    modelXbrl.error('EFM.6.23.09', _('The DTS must use a standard definition linkbase from Family RXD in edgartaxonomies.xml.'), modelObject=modelXbrl, instance=instanceName)
                countryNs = None
                deiNS = None
                for url, doc in modelXbrl.urlDocs.items():
                    if doc.type == ModelDocument.Type.SCHEMA:
                        if url.startswith('http://xbrl.sec.gov/country/'):
                            if countryNs is None:
                                countryNs = doc.targetNamespace
                            else:
                                modelXbrl.error('EFM.6.23.11', _('The DTS must use must use only one version of the COUNTRY schema.'), modelObject=(doc for url, doc in modelXbrl.urlDocs.items() if url.startswith('http://xbrl.sec.gov/country/')), instance=instanceName)
                            if disclosureSystem.deiNamespacePattern.match(doc.targetNamespace):
                                deiNS = doc.targetNamespace

                if rxdNs:
                    qn = ModelValue.qname(rxdNs, 'AmendmentNumber')
                    if amendmentFlag == 'true' and (qn not in modelXbrl.factsByQname or not any(f.context is not None and not f.context.hasSegment for f in modelXbrl.factsByQname[qn])):
                        modelXbrl.error('EFM.6.23.06', _('The value for dei:DocumentType, %(documentType)s, requires a value for rxd:AmendmentNumber in the Required Context.'), modelObject=modelXbrl, documentType=documentType)
                else:
                    modelXbrl.error('EFM.6.23.07', _('The DTS must use a standard schema from Family RXD in edgartaxonomies.xml.'), modelObject=modelXbrl, instance=instanceName)

                class Rxd:

                    def __init__(self):
                        for name in ('CountryAxis', 'GovernmentAxis', 'PaymentTypeAxis',
                                     'ProjectAxis', 'PmtAxis', 'AllGovernmentsMember',
                                     'AllProjectsMember', 'BusinessSegmentAxis',
                                     'EntityDomain', 'A', 'Cm', 'Co', 'Cu', 'D',
                                     'Gv', 'E', 'K', 'Km', 'P', 'Payments', 'Pr',
                                     'Sm'):
                            setattr(self, name, ModelValue.qname(rxdNs, 'rxd:' + name))

                rxd = Rxd()
                f1 = deiFacts.get(disclosureSystem.deiCurrentFiscalYearEndDateElement)
                if f1 is not None and documentPeriodEndDateFact is not None and f1.xValid >= VALID and documentPeriodEndDateFact.xValid >= VALID:
                    d = ModelValue.dateunionDate(documentPeriodEndDateFact.xValue)
                    if f1.xValue.month != d.month or f1.xValue.day != d.day:
                        modelXbrl.error('EFM.6.23.26', _('The dei:CurrentFiscalYearEndDate, %(fyEndDate)s does not match the dei:DocumentReportingPeriod %(reportingPeriod)s'), modelObject=(
                         f1, documentPeriodEndDateFact), fyEndDate=f1.value, reportingPeriod=documentPeriodEndDateFact.value)
                    if documentPeriodEndDateFact is not None and documentPeriodEndDateFact.xValid >= VALID and not any(f2.xValue == documentPeriodEndDateFact.xValue for f2 in modelXbrl.factsByQname[rxd.D] if f2.xValid >= VALID):
                        modelXbrl.error('EFM.6.23.27', _('The dei:DocumentPeriodEndDate %(reportingPeriod)s has no corresponding rxd:D fact.'), modelObject=documentPeriodEndDateFact, reportingPeriod=documentPeriodEndDateFact.value)
                    for url, doc in modelXbrl.urlDocs.items():
                        if url not in disclosureSystem.standardTaxonomiesDict and doc.type == ModelDocument.Type.SCHEMA:
                            for concept in XmlUtil.children(doc.xmlRootElement, XbrlConst.xsd, 'element'):
                                name = concept.name
                                if not concept.isAbstract and not concept.isTextBlock:
                                    modelXbrl.error('EFM.6.23.12', _('Extension concept %(concept)s is non-abstract and not a Text Block.'), modelObject=concept, schemaName=doc.basename, name=concept.name, concept=concept.qname)
                                elif name.endswith('Table') or name.endswith('Axis') or name.endswith('Domain'):
                                    modelXbrl.error('EFM.6.23.13', _('Extension concept %(concept)s is not allowed in an extension schema.'), modelObject=concept, schemaName=doc.basename, name=concept.name, concept=concept.qname)

                    self.modelXbrl.profileActivity('... SD checks 6-13, 26-27', minTimeToShow=1.0)
                    dimDefRelSet = modelXbrl.relationshipSet(XbrlConst.dimensionDefault)
                    dimDomRelSet = modelXbrl.relationshipSet(XbrlConst.dimensionDomain)
                    hypDimRelSet = modelXbrl.relationshipSet(XbrlConst.hypercubeDimension)
                    hasHypRelSet = modelXbrl.relationshipSet(XbrlConst.all)
                    for rel in dimDomRelSet.modelRelationships:
                        if isinstance(rel.fromModelObject, ModelConcept) and isinstance(rel.toModelObject, ModelConcept) and not dimDefRelSet.isRelated(rel.fromModelObject, 'child', rel.toModelObject):
                            modelXbrl.error('EFM.6.23.14', _('The target of the dimension-domain relationship in role %(linkrole)s from %(source)s to %(target)s must be the default member of %(source)s.'), modelObject=(
                             rel, rel.fromModelObject, rel.toModelObject), linkbaseName=rel.modelDocument.basename, linkrole=rel.linkrole, source=rel.fromModelObject.qname, target=rel.toModelObject.qname)

                    domMemRelSet = modelXbrl.relationshipSet(XbrlConst.domainMember)
                    memDim = {}

                    def checkMemMultDims(memRel, dimRel, elt, ELR, visited):
                        if elt not in visited:
                            visited.add(elt)
                            for rel in domMemRelSet.toModelObject(elt):
                                if rel.consecutiveLinkrole == ELR and isinstance(rel.fromModelObject, ModelConcept):
                                    checkMemMultDims(memRel, None, rel.fromModelObject, rel.linkrole, visited)

                            for rel in dimDomRelSet.toModelObject(elt):
                                if rel.consecutiveLinkrole == ELR:
                                    dim = rel.fromModelObject
                                    mem = memRel.toModelObject
                                    if isinstance(dim, ModelConcept) and isinstance(mem, ModelConcept):
                                        if dim.qname == rxd.PaymentTypeAxis and not mem.modelDocument.targetNamespace.startswith('http://xbrl.sec.gov/rxd/'):
                                            modelXbrl.error('EFM.6.23.17', _('The member %(member)s in dimension rxd:PaymentTypeAxis in linkrole %(linkrole)s must be a QName with namespace that begins with "http://xbrl.sec.gov/rxd/". '), modelObject=(
                                             rel, memRel, dim, mem), member=mem.qname, linkrole=rel.linkrole)
                                        if dim.qname == rxd.CountryAxis and not mem.modelDocument.targetNamespace.startswith('http://xbrl.sec.gov/country/'):
                                            modelXbrl.error('EFM.6.23.18', _('The member %(member)s in dimension rxd:CountryAxis in linkrole %(linkrole)s must be a QName with namespace that begins with "http://xbrl.sec.gov/country//". '), modelObject=(
                                             rel, memRel, dim, mem), member=mem.qname, linkrole=rel.linkrole)
                                        checkMemMultDims(memRel, rel, rel.fromModelObject, rel.linkrole, visited)

                            for rel in hypDimRelSet.toModelObject(elt):
                                if rel.consecutiveLinkrole == ELR and isinstance(rel.fromModelObject, ModelConcept):
                                    checkMemMultDims(memRel, dimRel, rel.fromModelObject, rel.linkrole, visited)

                            for rel in hasHypRelSet.toModelObject(elt):
                                if rel.consecutiveLinkrole == ELR and isinstance(rel.fromModelObject, ModelConcept):
                                    linkrole = rel.linkrole
                                    mem = memRel.toModelObject
                                    if (mem, linkrole) not in memDim:
                                        memDim[(mem, linkrole)] = (
                                         dimRel, memRel)
                                    else:
                                        otherDimRel, otherMemRel = memDim[(mem, linkrole)]
                                        modelXbrl.error('EFM.6.23.16', _('The member %(member)s has two dimensions, %(dimension1)s in linkrole %(linkrole1)s and  %(dimension2)s in linkrole %(linkrole2)s. '), modelObject=(
                                         dimRel, otherDimRel, memRel, otherMemRel, dimRel.fromModelObject, otherDimRel.fromModelObject), member=mem.qname, dimension1=dimRel.fromModelObject.qname, linkrole1=linkrole, dimension2=otherDimRel.fromModelObject.qname, linkrole2=otherDimRel.linkrole)

                            visited.discard(elt)

                    for rel in domMemRelSet.modelRelationships:
                        if isinstance(rel.fromModelObject, ModelConcept) and isinstance(rel.toModelObject, ModelConcept):
                            for rel2 in modelXbrl.relationshipSet(XbrlConst.domainMember, rel.consecutiveLinkrole).fromModelObject(rel.toModelObject):
                                if rel2.fromModelObject is not None and rel2.toModelObject is not None:
                                    modelXbrl.error('EFM.6.23.15', _('The domain-member relationship in %(linkrole)s from %(source)s to %(target)s is consecutive with domain-member relationship in %(linkrole2)s to %(target2)s. '), modelObject=(
                                     rel, rel.fromModelObject, rel.toModelObject), linkrole=rel.linkrole, linkrole2=rel2.linkrole, source=rel.fromModelObject.qname, target=rel.toModelObject.qname, target2=rel2.toModelObject.qname)

                            checkMemMultDims(rel, None, rel.fromModelObject, rel.linkrole, set())

                    self.modelXbrl.profileActivity('... SD checks 14-18', minTimeToShow=1.0)
                    qnDeiEntityDomain = ModelValue.qname(deiNS, 'dei:EntityDomain')
                    for relSet, dom, priItem, errCode in ((domMemRelSet, rxd.AllProjectsMember, rxd.Pr, 'EFM.6.23.30'),
                     (
                      domMemRelSet, rxd.AllGovernmentsMember, rxd.Gv, 'EFM.6.23.31'),
                     (
                      dimDomRelSet, rxd.BusinessSegmentAxis, rxd.Sm, 'EFM.6.23.33'),
                     (
                      domMemRelSet, qnDeiEntityDomain, rxd.E, 'EFM.6.23.34')):
                        for f in modelXbrl.factsByQname[priItem]:
                            if not f.isNil and f.xValid >= VALID and not relSet.isRelated(dom, 'descendant', f.xValue, isDRS=True):
                                modelXbrl.error(errCode, _('The %(fact)s %(value)s in context %(context)s is not a %(domain)s.'), modelObject=f, fact=priItem, value=f.xValue, context=f.context.id, domain=dom, messageCodes=('EFM.6.23.30',
                                                                                                                                                                                                                               'EFM.6.23.31',
                                                                                                                                                                                                                               'EFM.6.23.33',
                                                                                                                                                                                                                               'EFM.6.23.34'))

                    self.modelXbrl.profileActivity('... SD checks 30, 31, 33, 34', minTimeToShow=1.0)
                    cntxEqualFacts = defaultdict(list)
                    for f in modelXbrl.facts:
                        if f.context is not None:
                            cntxEqualFacts[f.context.contextDimAwareHash].append(f)

                    self.modelXbrl.profileActivity('... SD prepare facts by context', minTimeToShow=1.0)
                    qnCurrencyMeasure = XbrlConst.qnIsoCurrency(deiItems.get('EntityReportingCurrencyISOCode'))
                    currencyMeasures = ([qnCurrencyMeasure], [])
                    qnAllCountriesDomain = ModelValue.qname(countryNs, 'country:AllCountriesDomain')
                    for cntxFacts in cntxEqualFacts.values():
                        qnameFacts = dict((f.qname, f) for f in cntxFacts)
                        context = cntxFacts[0].context
                        contextDims = cntxFacts[0].context.qnameDims
                        for dim, priItem, errCode in ((rxd.PmtAxis, rxd.P, 'EFM.6.23.20'),
                         (
                          rxd.GovernmentAxis, rxd.Payments, 'EFM.6.23.22')):
                            if context.hasDimension(dim) and (priItem not in qnameFacts or qnameFacts[priItem].isNil):
                                modelXbrl.error(errCode, _('The Context %(context)s has dimension %(dimension)s member %(member)s but is missing required fact %(fact)s'), modelObject=context, context=context.id, dimension=dim, member=context.dimMemberQname(dim), fact=priItem, messageCodes=('EFM.6.23.20',
                                                                                                                                                                                                                                                                                                   'EFM.6.23.22'))

                        if rxd.Co in qnameFacts and not qnameFacts[rxd.Co].isNil and not domMemRelSet.isRelated(qnAllCountriesDomain, 'descendant', qnameFacts[rxd.Co].xValue, isDRS=True):
                            modelXbrl.error('EFM.6.23.44', _('Fact rxd:Co value %(value)s in context %(context)s is not in the domain of country:AllCountriesDomain'), modelObject=f, context=context.id, value=qnameFacts[rxd.Co].value)
                        for qnF, fNilOk, qnG, gNilOk, errCode in ((rxd.A, True, rxd.Cu, False, 'EFM.6.23.24'),
                         (
                          rxd.A, True, rxd.D, False, 'EFM.6.23.25'),
                         (
                          rxd.A, False, rxd.Gv, False, 'EFM.6.23.28'),
                         (
                          rxd.A, False, rxd.Co, False, 'EFM.6.23.29'),
                         (
                          rxd.Km, False, rxd.K, False, 'EFM.6.23.35'),
                         (
                          rxd.K, False, rxd.Km, False, 'EFM.6.23.35'),
                         (
                          rxd.Cm, False, rxd.Cu, False, 'EFM.6.23.39'),
                         (
                          rxd.K, False, rxd.A, False, 'EFM.6.23.42'),
                         (
                          rxd.Pr, False, rxd.A, False, 'EFM.6.23.43')):
                            if qnF in qnameFacts and (fNilOk or not qnameFacts[qnF].isNil) and (qnG not in qnameFacts or not gNilOk and qnameFacts[qnG].isNil):
                                modelXbrl.error(errCode, _('The Context %(context)s has a %(fact1)s and is missing required %(fact2NotNil)sfact %(fact2)s'), modelObject=qnameFacts[qnF], context=context.id, fact1=qnF, fact2=qnG, fact2NotNil='' if gNilOk else 'non-nil ', messageCodes=('EFM.6.23.24',
                                                                                                                                                                                                                                                                                            'EFM.6.23.25',
                                                                                                                                                                                                                                                                                            'EFM.6.23.28',
                                                                                                                                                                                                                                                                                            'EFM.6.23.29',
                                                                                                                                                                                                                                                                                            'EFM.6.23.35',
                                                                                                                                                                                                                                                                                            'EFM.6.23.35',
                                                                                                                                                                                                                                                                                            'EFM.6.23.39',
                                                                                                                                                                                                                                                                                            'EFM.6.23.42',
                                                                                                                                                                                                                                                                                            'EFM.6.23.43'))

                        for f in cntxFacts:
                            if not context.hasDimension(rxd.PmtAxis) and f.isNumeric and f.unit is not None and f.unit.measures != currencyMeasures:
                                modelXbrl.error('EFM.6.23.37', _('Fact %(fact)s in context %(context)s has unit %(unit)s not matching dei:EntityReportingCurrencyISOCode %(currency)s'), modelObject=f, fact=f.qname, context=context.id, unit=f.unit.value, currency=qnCurrencyMeasure)

                        if rxd.A in qnameFacts and not qnameFacts[rxd.A].isNil and rxd.Cm in qnameFacts and not qnameFacts[rxd.Cm].isNil and qnameFacts[rxd.A].unit is not None and qnameFacts[rxd.A].unit.measures == currencyMeasures:
                            modelXbrl.error('EFM.6.23.38', _('A value cannot be given for rxd:Cm in context %(context)s because the payment is in the reporting currency %(currency)s.'), modelObject=(
                             qnameFacts[rxd.A], qnameFacts[rxd.Cm]), context=context.id, currency=qnCurrencyMeasure)
                        if rxd.A in qnameFacts and rxd.Cu in qnameFacts and not qnameFacts[rxd.Cu].isNil and qnameFacts[rxd.A].unit is not None and qnameFacts[rxd.A].unit.measures != ([XbrlConst.qnIsoCurrency(qnameFacts[rxd.Cu].xValue)], []):
                            modelXbrl.error('EFM.6.23.41', _('The unit %(unit)s of rxd:A in context %(context)s is not consistent with the value %(currency)s of rxd:Cu.'), modelObject=(
                             qnameFacts[rxd.A], qnameFacts[rxd.Cu]), context=context.id, unit=qnameFacts[rxd.A].unit.value, currency=qnameFacts[rxd.Cu].value)
                        if context.hasDimension(rxd.ProjectAxis) and not any(f.xValue == m for m in (contextDims[rxd.ProjectAxis].memberQname,) for f in modelXbrl.factsByQname[rxd.Pr]):
                            modelXbrl.error('EFM.6.23.19', _('The Context %(context)s has dimension %(dimension)s but is missing any payment.'), modelObject=context, context=context.id, dimension=rxd.GovernmentAxis)
                        if context.hasDimension(rxd.GovernmentAxis) and not any(f.xValue == m and f.context.hasDimension(rxd.PmtAxis) for m in (contextDims[rxd.GovernmentAxis].memberQname,) for f in modelXbrl.factsByQname[rxd.Gv]):
                            modelXbrl.error('EFM.6.23.21', _('The Context %(context)s has dimension %(dimension)s member %(member)s but is missing any payment.'), modelObject=context, context=context.id, dimension=rxd.GovernmentAxis, member=context.dimMemberQname(rxd.GovernmentAxis))
                        if rxd.P in qnameFacts and not any(f.context is not None and not f.context.hasSegment for f in modelXbrl.factsByQname.get(qnameFacts[rxd.P].xValue, ())):
                            modelXbrl.error('EFM.6.23.23', _('The Context %(context)s has payment type %(paymentType)s but is missing a corresponding fact in the required context.'), modelObject=context, context=context.id, paymentType=qnameFacts[rxd.P].xValue)
                        if not context.hasDimension(rxd.PmtAxis) and rxd.A in qnameFacts and not qnameFacts[rxd.A].isNil:
                            modelXbrl.error('EFM.6.23.40', _('There is a non-nil rxd:A in context %(context)s but missing a dimension rxd:PmtAxis.'), modelObject=(
                             context, qnameFacts[rxd.A]), context=context.id)

                    self.modelXbrl.profileActivity('... SD by context for 19-25, 28-29, 35, 37-39, 40-44', minTimeToShow=1.0)
                    for f in modelXbrl.factsByQname[rxd.D]:
                        if not f.isNil and f.xValid >= VALID and f.xValue + datetime.timedelta(1) != f.context.endDatetime:
                            modelXbrl.error('EFM.6.23.32', _('The rxd:D %(value)s in context %(context)s does not match the context end date %(endDate)s.'), modelObject=f, value=f.xValue, context=f.context.id, endDate=XmlUtil.dateunionValue(f.context.endDatetime, subtractOneDay=True))

                    self.modelXbrl.profileActivity('... SD checks 32 (last SD check)', minTimeToShow=1.0)
                    del rxdDoc
                    del cntxEqualFacts
                    hasHypRelSet = hypDimRelSet = dimDefRelSet = domMemRelSet = dimDomRelSet = None
                    memDim.clear()
            else:
                if disclosureSystem.GFM:
                    for deiItem in (disclosureSystem.deiCurrentFiscalYearEndDateElement,
                     disclosureSystem.deiDocumentFiscalYearFocusElement,
                     disclosureSystem.deiFilerNameElement):
                        if deiItem not in deiItems or deiItems[deiItem] == '':
                            modelXbrl.error('GFM.3.02.01', _('dei:%(elementName)s is required in the default context'), modelXbrl=modelXbrl, elementName=deiItem)

                if documentType not in ('SD', 'SD/A'):
                    self.modelXbrl.profileActivity('... filer required facts checks', minTimeToShow=1.0)
            footnoteLinkNbr = 0
            for footnoteLinkElt in xbrlInstDoc.iterdescendants(tag='{http://www.xbrl.org/2003/linkbase}footnoteLink'):
                if isinstance(footnoteLinkElt, ModelObject):
                    footnoteLinkNbr += 1
                    linkrole = footnoteLinkElt.get('{http://www.w3.org/1999/xlink}role')
                    if linkrole != XbrlConst.defaultLinkRole:
                        modelXbrl.error(('EFM.6.05.28.linkrole', 'GFM.1.02.20'), _('FootnoteLink %(footnoteLinkNumber)s has disallowed role %(linkrole)s'), modelObject=footnoteLinkElt, footnoteLinkNumber=footnoteLinkNbr, linkrole=linkrole)
                    relationshipSet = modelXbrl.relationshipSet('XBRL-footnotes', linkrole)
                    locNbr = 0
                    arcNbr = 0
                    for child in footnoteLinkElt:
                        if isinstance(child, ModelObject):
                            xlinkType = child.get('{http://www.w3.org/1999/xlink}type')
                            if child.namespaceURI != XbrlConst.link or xlinkType not in ('locator',
                                                                                         'resource',
                                                                                         'arc') or child.localName not in ('loc',
                                                                                                                           'footnote',
                                                                                                                           'footnoteArc'):
                                modelXbrl.error(('EFM.6.05.27', 'GFM.1.02.19'), _('FootnoteLink %(footnoteLinkNumber)s has disallowed child element %(elementName)s'), modelObject=child, footnoteLinkNumber=footnoteLinkNbr, elementName=child.prefixedName)
                            else:
                                if xlinkType == 'locator':
                                    locNbr += 1
                                    locrole = child.get('{http://www.w3.org/1999/xlink}role')
                                    if locrole is not None and (disclosureSystem.GFM or not disclosureSystem.uriAuthorityValid(locrole)):
                                        modelXbrl.error(('EFM.6.05.29', 'GFM.1.02.21'), _('FootnoteLink %(footnoteLinkNumber)s loc %(locNumber)s has disallowed role %(role)s'), modelObject=child, footnoteLinkNumber=footnoteLinkNbr, xlinkLabel=child.xlinkLabel, locNumber=locNbr, role=locrole)
                                    href = child.get('{http://www.w3.org/1999/xlink}href')
                                    if not href.startswith('#'):
                                        modelXbrl.error(('EFM.6.05.32', 'GFM.1.02.23'), _('FootnoteLink %(footnoteLinkNumber)s loc %(locNumber)s has disallowed href %(locHref)s'), modelObject=child, footnoteLinkNumber=footnoteLinkNbr, locNumber=locNbr, locHref=href, locLabel=child.get('{http://www.w3.org/1999/xlink}label'))
                                    else:
                                        label = child.get('{http://www.w3.org/1999/xlink}label')
                                elif xlinkType == 'arc':
                                    arcNbr += 1
                                    arcrole = child.get('{http://www.w3.org/1999/xlink}arcrole')
                                    if self.validateEFM and not disclosureSystem.uriAuthorityValid(arcrole) or disclosureSystem.GFM and arcrole != XbrlConst.factFootnote and arcrole != XbrlConst.factExplanatoryFact:
                                        modelXbrl.error(('EFM.6.05.30', 'GFM.1.02.22'), _('FootnoteLink %(footnoteLinkNumber)s arc %(arcNumber)s has disallowed arcrole %(arcrole)s'), modelObject=child, footnoteLinkNumber=footnoteLinkNbr, arcNumber=arcNbr, arcToLabel=child.get('{http://www.w3.org/1999/xlink}to'), arcrole=arcrole)
                        else:
                            if xlinkType == 'resource':
                                footnoterole = child.get('{http://www.w3.org/1999/xlink}role')
                                if footnoterole == '':
                                    modelXbrl.error(('EFM.6.05.28.missingRole', 'GFM.1.2.20'), _('Footnote %(xlinkLabel)s is missing a role'), modelObject=child, xlinkLabel=child.get('{http://www.w3.org/1999/xlink}label'))
                            elif self.validateEFM and not disclosureSystem.uriAuthorityValid(footnoterole) or disclosureSystem.GFM and footnoterole != XbrlConst.footnote:
                                modelXbrl.error(('EFM.6.05.28', 'GFM.1.2.20'), _('Footnote %(xlinkLabel)s has disallowed role %(role)s'), modelObject=child, xlinkLabel=child.get('{http://www.w3.org/1999/xlink}label'), role=footnoterole)
                            if self.validateEFM:
                                ValidateFilingText.validateFootnote(modelXbrl, child)
                            foundFact = False
                        if XmlUtil.text(child) != '':
                            if relationshipSet:
                                for relationship in relationshipSet.toModelObject(child):
                                    if isinstance(relationship.fromModelObject, ModelFact):
                                        foundFact = True
                                        break

                            if not foundFact:
                                modelXbrl.error(('EFM.6.05.33', 'GFM.1.02.24'), _('FootnoteLink %(footnoteLinkNumber)s footnote %(footnoteLabel)s has no linked fact'), modelObject=child, footnoteLinkNumber=footnoteLinkNbr, footnoteLabel=child.get('{http://www.w3.org/1999/xlink}label'), text=XmlUtil.text(child)[:100])

            self.modelXbrl.profileActivity('... filer rfootnotes checks', minTimeToShow=1.0)
        else:
            if modelXbrl.modelDocument.type == ModelDocument.Type.SCHEMA and self.validateSBRNL:
                if not any(hrefElt.localName == 'linkbaseRef' and hrefElt.get('{http://www.w3.org/1999/xlink}role') == 'http://www.xbrl.org/2003/role/presentationLinkbaseRef' for hrefElt, hrefDoc, hrefId in modelXbrl.modelDocument.hrefObjects):
                    modelXbrl.error('SBR.NL.2.2.10.01', 'Entrypoint schema must have a presentation linkbase', modelObject=modelXbrl.modelDocument)
                defaultLangStandardLabels = {}
                for concept in modelXbrl.qnameConcepts.values():
                    conceptHasDefaultLangStandardLabel = False
                    for modelLabelRel in labelsRelationshipSet.fromModelObject(concept):
                        modelLabel = modelLabelRel.toModelObject
                        role = modelLabel.role
                        text = modelLabel.text
                        lang = modelLabel.xmlLang
                        if role == XbrlConst.documentationLabel:
                            if concept.modelDocument.targetNamespace in disclosureSystem.standardTaxonomiesDict:
                                modelXbrl.error(('EFM.6.10.05', 'GFM.1.05.05', 'SBR.NL.2.1.0.08'), _('Concept %(concept)s of a standard taxonomy cannot have a documentation label: %(text)s'), modelObject=modelLabel, concept=concept.qname, text=text)
                        elif text and lang and disclosureSystem.defaultXmlLang and lang.startswith(disclosureSystem.defaultXmlLang):
                            if role == XbrlConst.standardLabel:
                                if text in defaultLangStandardLabels:
                                    concept2, modelLabel2 = defaultLangStandardLabels[text]
                                    modelXbrl.error(('EFM.6.10.04', 'GFM.1.05.04'), _('Same labels for concepts %(concept)s and %(concept2)s for %(lang)s standard role: %(text)s.'), modelObject=(
                                     concept, modelLabel, concept2, modelLabel2), concept=concept.qname, concept2=concept2.qname, lang=disclosureSystem.defaultLanguage, text=text[:80])
                                else:
                                    defaultLangStandardLabels[text] = (
                                     concept, modelLabel)
                                conceptHasDefaultLangStandardLabel = True
                            if len(text) > 511:
                                modelXbrl.error(('EFM.6.10.06', 'GFM.1.05.06'), _('Label for concept %(concept)s role %(role)s length %(length)s must be shorter than 511 characters: %(text)s'), modelObject=modelLabel, concept=concept.qname, role=role, length=len(text), text=text[:80])
                            match = modelXbrl.modelManager.disclosureSystem.labelCheckPattern.search(text)
                            if match:
                                modelXbrl.error(('EFM.6.10.06', 'GFM.1.05.07', 'SBR.NL.2.3.8.07'), 'Label for concept %(concept)s role %(role)s has disallowed characters: "%(text)s"', modelObject=modelLabel, concept=concept.qname, role=role, text=match.group())
                        if text is not None and len(text) > 0 and modelXbrl.modelManager.disclosureSystem.labelTrimPattern and (modelXbrl.modelManager.disclosureSystem.labelTrimPattern.match(text[0]) or modelXbrl.modelManager.disclosureSystem.labelTrimPattern.match(text[(-1)])):
                            modelXbrl.error(('EFM.6.10.08', 'GFM.1.05.08'), _('Label for concept %(concept)s role %(role)s lang %(lang)s is not trimmed: %(text)s'), modelObject=modelLabel, concept=concept.qname, role=role, lang=lang, text=text)

                    for modelRefRel in referencesRelationshipSetWithProhibits.fromModelObject(concept):
                        modelReference = modelRefRel.toModelObject
                        text = XmlUtil.innerText(modelReference)
                        if concept.modelDocument.targetNamespace not in disclosureSystem.standardTaxonomiesDict:
                            modelXbrl.error(('EFM.6.18.01', 'GFM.1.9.1'), _('References for extension concept %(concept)s are not allowed: %(text)s'), modelObject=modelReference, concept=concept.qname, text=text, xml=XmlUtil.xmlstring(modelReference, stripXmlns=True, contentsOnly=True))
                        elif (self.validateEFM or self.validateSBRNL) and not self.isStandardUri(modelRefRel.modelDocument.uri):
                            modelXbrl.error(('EFM.6.18.02', 'SBR.NL.2.1.0.08'), _('References for standard taxonomy concept %(concept)s are not allowed in an extension linkbase: %(text)s'), modelObject=modelReference, concept=concept.qname, text=text, xml=XmlUtil.xmlstring(modelReference, stripXmlns=True, contentsOnly=True))

                    if self.validateSBRNL and (concept.isItem or concept.isTuple):
                        if concept.modelDocument.targetNamespace not in disclosureSystem.standardTaxonomiesDict:
                            if not conceptHasDefaultLangStandardLabel:
                                modelXbrl.error('SBR.NL.2.2.2.26', _('Concept %(concept)s missing standard label in local language.'), modelObject=concept, concept=concept.qname)
                            subsGroup = concept.get('substitutionGroup')
                            if (not concept.isAbstract or subsGroup == 'sbr:presentationItem') and not (presentationRelationshipSet.toModelObject(concept) or presentationRelationshipSet.fromModelObject(concept)):
                                modelXbrl.error('SBR.NL.2.2.2.04', _('Concept %(concept)s not referred to by presentation relationship.'), modelObject=concept, concept=concept.qname)
                            else:
                                if (concept.isDimensionItem or subsGroup and (subsGroup.endswith(':domainItem') or subsGroup.endswith(':domainMemberItem'))) and not (presentationRelationshipSet.toModelObject(concept) or presentationRelationshipSet.fromModelObject(concept)):
                                    modelXbrl.error('SBR.NL.2.2.10.03', _('DTS concept %(concept)s not referred to by presentation relationship.'), modelObject=concept, concept=concept.qname)
                                if concept.substitutionGroupQname and concept.substitutionGroupQname.namespaceURI not in disclosureSystem.baseTaxonomyNamespaces:
                                    modelXbrl.error('SBR.NL.2.2.2.05', _('Concept %(concept)s has a substitutionGroup of a non-standard concept.'), modelObject=concept, concept=concept.qname)
                                if concept.isTuple:
                                    for missingQname in set(concept.type.elements) ^ pLinkedNonAbstractDescendantQnames(modelXbrl, concept):
                                        modelXbrl.error('SBR.NL.2.3.4.01', _('Tuple %(concept)s has mismatch between content and presentation children: %(missingQname)s.'), modelObject=concept, concept=concept.qname, missingQname=missingQname)

                                self.checkConceptLabels(modelXbrl, labelsRelationshipSet, disclosureSystem, concept)
                                self.checkConceptLabels(modelXbrl, genLabelsRelationshipSet, disclosureSystem, concept)

                for roleURI, modelRoleTypes in modelXbrl.roleTypes.items():
                    if len(modelRoleTypes) > 1:
                        modelXbrl.error(('EFM.6.07.10', 'GFM.1.03.10'), _('RoleType %(roleType)s is defined in multiple taxonomies'), modelObject=modelRoleTypes, roleType=roleURI, numberOfDeclarations=len(modelRoleTypes))

                for arcroleURI, modelRoleTypes in modelXbrl.arcroleTypes.items():
                    if len(modelRoleTypes) > 1:
                        modelXbrl.error(('EFM.6.07.14', 'GFM.1.03.16'), _('ArcroleType %(arcroleType)s is defined in multiple taxonomies'), modelObject=modelRoleTypes, arcroleType=arcroleURI, numberOfDeclarations=len(modelRoleTypes))

                self.modelXbrl.profileActivity('... filer concepts checks', minTimeToShow=1.0)
                del defaultLangStandardLabels
                ValidateFilingDTS.checkDTS(self, modelXbrl.modelDocument, [])
                self.modelXbrl.profileActivity('... filer DTS checks', minTimeToShow=1.0)
                if self.validateEFM:
                    for conflictClass, modelDocuments in self.standardNamespaceConflicts.items():
                        if len(modelDocuments) > 1:
                            modelXbrl.error('EFM.6.22.03', _('References for conflicting standard %(conflictClass)s taxonomies %(namespaceConflicts)s are not allowed in same DTS'), modelObject=modelXbrl, conflictClass=conflictClass, namespaceConflicts=sorted((d.targetNamespace for d in modelDocuments), key=lambda ns: ns.rpartition('/')[2]))

                conceptRelsUsedWithPreferredLabels = defaultdict(list)
                usedCalcsPresented = defaultdict(set)
                usedCalcFromTosELR = {}
                localPreferredLabels = defaultdict(set)
                drsELRs = set()
                self.summationItemRelsSetAllELRs = modelXbrl.relationshipSet(XbrlConst.summationItem)
                for arcroleFilter in (XbrlConst.summationItem, XbrlConst.parentChild, '*'):
                    for baseSetKey, baseSetModelLinks in modelXbrl.baseSets.items():
                        arcrole, ELR, linkqname, arcqname = baseSetKey
                        if ELR and linkqname and arcqname and not arcrole.startswith('XBRL-'):
                            if not (arcroleFilter == arcrole or arcroleFilter == '*' and arcrole not in (XbrlConst.summationItem, XbrlConst.parentChild)):
                                pass
                            else:
                                if self.validateEFMorGFM or self.validateSBRNL and arcrole == XbrlConst.parentChild:
                                    ineffectiveArcs = ModelRelationshipSet.ineffectiveArcs(baseSetModelLinks, arcrole)
                                    for modelRel in ineffectiveArcs:
                                        if modelRel.fromModelObject is not None and modelRel.toModelObject is not None:
                                            modelXbrl.error(('EFM.6.09.03', 'GFM.1.04.03',
                                                             'SBR.NL.2.3.4.06'), _('Ineffective arc %(arc)s in \nlink role %(linkrole)s \narcrole %(arcrole)s \nfrom %(conceptFrom)s \nto %(conceptTo)s \n%(ineffectivity)s'), modelObject=modelRel, arc=modelRel.qname, arcrole=modelRel.arcrole, linkrole=modelRel.linkrole, linkroleDefinition=modelXbrl.roleTypeDefinition(modelRel.linkrole), conceptFrom=modelRel.fromModelObject.qname, conceptTo=modelRel.toModelObject.qname, ineffectivity=modelRel.ineffectivity)

                                if arcrole == XbrlConst.parentChild:
                                    isStatementSheet = any(linkroleDefinitionStatementSheet.match(roleType.definition or '') for roleType in self.modelXbrl.roleTypes.get(ELR, ()))
                                    conceptsPresented = set()
                                    parentChildRels = modelXbrl.relationshipSet(arcrole, ELR)
                                    for relFrom, siblingRels in parentChildRels.fromModelObjects().items():
                                        targetConceptPreferredLabels = defaultdict(dict)
                                        orderRels = {}
                                        firstRel = True
                                        relFromUsed = True
                                        for rel in siblingRels:
                                            if firstRel:
                                                firstRel = False
                                                if relFrom in conceptsUsed:
                                                    conceptsUsed[relFrom] = True
                                                    relFromUsed = True
                                            relTo = rel.toModelObject
                                            preferredLabel = rel.preferredLabel
                                            if relTo in conceptsUsed:
                                                conceptsUsed[relTo] = True
                                                if preferredLabel and preferredLabel != '':
                                                    conceptRelsUsedWithPreferredLabels[relTo].append(rel)
                                                    if self.validateSBRNL and preferredLabel in ('periodStart',
                                                                                                 'periodEnd'):
                                                        modelXbrl.error('SBR.NL.2.3.4.03', _('Preferred label on presentation relationships not allowed'), modelObject=modelRel)
                                                    preferredLabels = targetConceptPreferredLabels[relTo]
                                                    if preferredLabel in preferredLabels or self.validateSBRNL and not relFrom.isTuple and (not preferredLabel or None in preferredLabels):
                                                        if preferredLabel in preferredLabels:
                                                            rel2, relTo2 = preferredLabels[preferredLabel]
                                                        else:
                                                            rel2 = relTo2 = None
                                                        modelXbrl.error(('EFM.6.12.05',
                                                                         'GFM.1.06.05',
                                                                         'SBR.NL.2.3.4.06'), _('Concept %(concept)s has duplicate preferred label %(preferredLabel)s in link role %(linkrole)s'), modelObject=(
                                                         rel, relTo, rel2, relTo2), concept=relTo.qname, fromConcept=rel.fromModelObject.qname, preferredLabel=preferredLabel, linkrole=rel.linkrole, linkroleDefinition=modelXbrl.roleTypeDefinition(rel.linkrole))
                                                    else:
                                                        preferredLabels[preferredLabel] = (
                                                         rel, relTo)
                                                    if relFromUsed:
                                                        conceptsPresented.add(relFrom.objectIndex)
                                                        conceptsPresented.add(relTo.objectIndex)
                                                    order = rel.order
                                                    if order in orderRels:
                                                        modelXbrl.error(('EFM.6.12.02',
                                                                         'GFM.1.06.02',
                                                                         'SBR.NL.2.3.4.05'), _('Duplicate presentation relations from concept %(conceptFrom)s for order %(order)s in base set role %(linkrole)s to concept %(conceptTo)s and to concept %(conceptTo2)s'), modelObject=(
                                                         rel, orderRels[order]), conceptFrom=relFrom.qname, order=rel.arcElement.get('order'), linkrole=rel.linkrole, linkroleDefinition=modelXbrl.roleTypeDefinition(rel.linkrole), conceptTo=rel.toModelObject.qname, conceptTo2=orderRels[order].toModelObject.qname)
                                                    else:
                                                        orderRels[order] = rel
                                                    if self.validateSBRNL and not relFrom.isTuple:
                                                        if relTo in localPreferredLabels and {
                                                         None, preferredLabel} & localPreferredLabels[relTo]:
                                                            self.modelXbrl.error('SBR.NL.2.3.4.06', _('Non-distinguished preferredLabel presentation relations from concept %(conceptFrom)s in base set role %(linkrole)s'), modelObject=rel, conceptFrom=relFrom.qname, linkrole=rel.linkrole, conceptTo=relTo.qname)
                                                        localPreferredLabels[relTo].add(preferredLabel)

                                        targetConceptPreferredLabels.clear()
                                        orderRels.clear()

                                    localPreferredLabels.clear()
                                    for conceptPresented in conceptsPresented:
                                        if conceptPresented in usedCalcsPresented:
                                            usedCalcPairingsOfConcept = usedCalcsPresented[conceptPresented]
                                            if len(usedCalcPairingsOfConcept & conceptsPresented) > 0:
                                                usedCalcPairingsOfConcept -= conceptsPresented

                                    if validateLoggingSemantic:
                                        for rootConcept in parentChildRels.rootConcepts:
                                            self.checkCalcsTreeWalk(parentChildRels, rootConcept, isStatementSheet, False, conceptsUsed, set())

                                else:
                                    if arcrole == XbrlConst.summationItem:
                                        if self.validateEFMorGFM:
                                            fromRelationships = modelXbrl.relationshipSet(arcrole, ELR).fromModelObjects()
                                            allElrRelSet = modelXbrl.relationshipSet(arcrole)
                                            for relFrom, rels in fromRelationships.items():
                                                orderRels = {}
                                                for rel in rels:
                                                    relTo = rel.toModelObject
                                                    if isinstance(relTo, ModelConcept) and relFrom.periodType != relTo.periodType:
                                                        self.modelXbrl.error(('EFM.6.14.03',
                                                                              'GFM.1.07.03'), 'Calculation relationship period types mismatched in base set role %(linkrole)s from %(conceptFrom)s to %(conceptTo)s', modelObject=rel, linkrole=rel.linkrole, conceptFrom=relFrom.qname, conceptTo=relTo.qname, linkroleDefinition=self.modelXbrl.roleTypeDefinition(ELR))
                                                    if relFrom in conceptsUsed and relTo in conceptsUsed:
                                                        fromObjId = relFrom.objectIndex
                                                        toObjId = relTo.objectIndex
                                                        if fromObjId < toObjId:
                                                            usedCalcsPresented[fromObjId].add(toObjId)
                                                        else:
                                                            usedCalcsPresented[toObjId].add(fromObjId)
                                                        order = rel.order
                                                        if order in orderRels and disclosureSystem.GFM:
                                                            self.modelXbrl.error(('EFM.N/A',
                                                                                  'GFM.1.07.06'), _('Duplicate calculations relations from concept %(conceptFrom)s for order %(order)s in base set role %(linkrole)s to concept %(conceptTo)s and to concept %(conceptTo2)s'), modelObject=(
                                                             rel, orderRels[order]), linkrole=rel.linkrole, conceptFrom=relFrom.qname, order=order, conceptTo=rel.toModelObject.qname, conceptTo2=orderRels[order].toModelObject.qname)
                                                        else:
                                                            orderRels[order] = rel

                                                directedCycleRels = self.directedCycle(relFrom, relFrom, fromRelationships, {relFrom})
                                                if directedCycleRels is not None:
                                                    self.modelXbrl.error(('EFM.6.14.04',
                                                                          'GFM.1.07.04'), _('Calculation relationships have a directed cycle in base set role %(linkrole)s starting from %(concept)s'), modelObject=[
                                                     relFrom] + directedCycleRels, linkrole=ELR, concept=relFrom.qname, linkroleDefinition=self.modelXbrl.roleTypeDefinition(ELR))
                                                orderRels.clear()
                                                if rels and relFrom in conceptsUsed:
                                                    relFromAndTos = (
                                                     relFrom.objectIndex,) + tuple(sorted(rel.toModelObject.objectIndex for rel in rels if isinstance(rel.toModelObject, ModelConcept)))
                                                    if relFromAndTos in usedCalcFromTosELR:
                                                        otherRels = usedCalcFromTosELR[relFromAndTos]
                                                        otherELR = otherRels[0].linkrole
                                                        self.modelXbrl.log('WARNING-SEMANTIC', ('EFM.6.15.04',
                                                                                                'GFM.2.06.04'), _('Calculation relationships should have a same set of targets in %(linkrole)s and %(linkrole2)s starting from %(concept)s'), modelObject=[
                                                         relFrom] + rels + otherRels, linkrole=ELR, linkrole2=otherELR, concept=relFrom.qname)
                                                    else:
                                                        usedCalcFromTosELR[relFromAndTos] = rels

                                        elif self.validateSBRNL:
                                            for modelRel in self.modelXbrl.relationshipSet(arcrole, ELR).modelRelationships:
                                                self.modelXbrl.error('SBR.NL.2.3.9.01', _('Calculation linkbase linkrole %(linkrole)s'), modelObject=modelRel, linkrole=ELR)
                                                break

                                    else:
                                        if arcrole == XbrlConst.all or arcrole == XbrlConst.notAll:
                                            drsELRs.add(ELR)
                                        else:
                                            if arcrole == XbrlConst.dimensionDomain or arcrole == XbrlConst.dimensionDefault and self.validateEFMorGFM:
                                                fromRelationships = modelXbrl.relationshipSet(arcrole, ELR).fromModelObjects()
                                                for relFrom, rels in fromRelationships.items():
                                                    for rel in rels:
                                                        relTo = rel.toModelObject
                                                        if not (isinstance(relTo, ModelConcept) and relTo.type is not None and relTo.type.isDomainItemType) and not self.isStandardUri(rel.modelDocument.uri):
                                                            self.modelXbrl.error(('EFM.6.16.03',
                                                                                  'GFM.1.08.03'), _('Definition relationship from %(conceptFrom)s to %(conceptTo)s in role %(linkrole)s requires domain item target'), modelObject=(
                                                             rel, relFrom, relTo), conceptFrom=relFrom.qname, conceptTo=relTo.qname if relTo is not None else None, linkrole=rel.linkrole)

                                            elif self.validateSBRNL and arcrole == XbrlConst.dimensionDefault:
                                                for modelRel in self.modelXbrl.relationshipSet(arcrole).modelRelationships:
                                                    self.modelXbrl.error('SBR.NL.2.3.6.05', _('Dimension-default in from %(conceptFrom)s to %(conceptTo)s in role %(linkrole)s is not allowed'), modelObject=modelRel, conceptFrom=modelRel.fromModelObject.qname, conceptTo=modelRel.toModelObject.qname, linkrole=modelRel.linkrole)

                                        if XbrlConst.isDefinitionOrXdtArcrole(arcrole) and disclosureSystem.GFM:
                                            fromRelationships = modelXbrl.relationshipSet(arcrole, ELR).fromModelObjects()
                                            for relFrom, rels in fromRelationships.items():
                                                orderRels = {}
                                                for rel in rels:
                                                    relTo = rel.toModelObject
                                                    order = rel.order
                                                    if order in orderRels and disclosureSystem.GFM:
                                                        self.modelXbrl.error('GFM.1.08.10', _('Duplicate definitions relations from concept %(conceptFrom)s for order %(order)s in base set role %(linkrole)s to concept %(conceptTo)s and to concept %(conceptTo2)s'), modelObject=(
                                                         rel, relFrom, relTo), conceptFrom=relFrom.qname, order=order, linkrole=rel.linkrole, conceptTo=rel.toModelObject.qname, conceptTo2=orderRels[order].toModelObject.qname)
                                                    else:
                                                        orderRels[order] = rel
                                                    if arcrole not in (XbrlConst.dimensionDomain, XbrlConst.domainMember) and rel.get('{http://xbrl.org/2005/xbrldt}usable') == 'false':
                                                        self.modelXrl.error('GFM.1.08.11', _("Disallowed xbrldt:usable='false' attribute on %(arc)s relationship from concept %(conceptFrom)s in base set role %(linkrole)s to concept %(conceptTo)s"), modelObject=(
                                                         rel, relFrom, relTo), arc=rel.qname, conceptFrom=relFrom.qname, linkrole=rel.linkrole, conceptTo=rel.toModelObject.qname)

                del localPreferredLabels
                del usedCalcFromTosELR
                del self.summationItemRelsSetAllELRs
                self.modelXbrl.profileActivity('... filer relationships checks', minTimeToShow=1.0)
                ValidateFilingDimensions.checkDimensions(self, drsELRs)
                self.modelXbrl.profileActivity('... filer dimensions checks', minTimeToShow=1.0)
                for concept, hasPresentationRelationship in conceptsUsed.items():
                    if not hasPresentationRelationship:
                        self.modelXbrl.error(('EFM.6.12.03', 'GFM.1.6.3'), _('Concept used in instance %(concept)s does not participate in an effective presentation relationship'), modelObject=[
                         concept] + list(modelXbrl.factsByQname[concept.qname]), concept=concept.qname)

                for fromIndx, toIndxs in usedCalcsPresented.items():
                    for toIndx in toIndxs:
                        fromModelObject = self.modelXbrl.modelObject(fromIndx)
                        toModelObject = self.modelXbrl.modelObject(toIndx)
                        calcRels = modelXbrl.relationshipSet(XbrlConst.summationItem).fromToModelObjects(fromModelObject, toModelObject, checkBothDirections=True)
                        fromFacts = self.modelXbrl.factsByQname[fromModelObject.qname]
                        toFacts = self.modelXbrl.factsByQname[toModelObject.qname]
                        fromFactContexts = set(f.context.contextNonDimAwareHash for f in fromFacts if f.context is not None)
                        contextId = backupId = None
                        for f in toFacts:
                            if f.context is not None:
                                if f.context.contextNonDimAwareHash in fromFactContexts:
                                    contextId = f.context.id
                                    break
                                backupId = f.context.id

                        if contextId is None:
                            contextId = backupId
                        self.modelXbrl.error(('EFM.6.14.05', 'GFM.1.7.5'), _('Used calculation relationship from %(conceptFrom)s to %(conceptTo)s does not participate in an effective presentation relationship'), modelObject=calcRels + [fromModelObject, toModelObject], linkroleDefinition=self.modelXbrl.roleTypeDefinition(calcRels[0].linkrole if calcRels else None), conceptFrom=self.modelXbrl.modelObject(fromIndx).qname, conceptTo=self.modelXbrl.modelObject(toIndx).qname, contextId=contextId)

                if disclosureSystem.defaultXmlLang:
                    for concept, preferredLabelRels in conceptRelsUsedWithPreferredLabels.items():
                        for preferredLabelRel in preferredLabelRels:
                            preferredLabel = preferredLabelRel.preferredLabel
                            hasDefaultLangPreferredLabel = False
                            for modelLabelRel in labelsRelationshipSet.fromModelObject(concept):
                                modelLabel = modelLabelRel.toModelObject
                                if modelLabel.xmlLang.startswith(disclosureSystem.defaultXmlLang) and modelLabel.role == preferredLabel:
                                    hasDefaultLangPreferredLabel = True
                                    break

                            if not hasDefaultLangPreferredLabel:
                                self.modelXbrl.error('GFM.1.06.04', _('Concept %(concept)s missing %(lang)s preferred labels for role %(preferredLabel)s'), modelObject=(
                                 preferredLabelRel, concept), concept=concept.qname, fromConcept=preferredLabelRel.fromModelObject.qname, lang=disclosureSystem.defaultLanguage, preferredLabel=preferredLabel)

                del conceptRelsUsedWithPreferredLabels
                self.modelXbrl.profileActivity('... filer preferred label checks', minTimeToShow=1.0)
                if self.validateEFM:
                    for pluginXbrlMethod in pluginClassMethods('Validate.EFM.Finally'):
                        pluginXbrlMethod(self, conceptsUsed)

            elif self.validateSBRNL:
                for pluginXbrlMethod in pluginClassMethods('Validate.SBRNL.Finally'):
                    pluginXbrlMethod(self, conceptsUsed)

        self.modelXbrl.profileActivity("... plug in '.Finally' checks", minTimeToShow=1.0)
        self.modelXbrl.profileStat(_('validate{0}').format(modelXbrl.modelManager.disclosureSystem.validationType))
        modelXbrl.modelManager.showStatus(_('ready'), 2000)

    def isStandardUri(self, uri):
        try:
            return self._isStandardUri[uri]
        except KeyError:
            isStd = uri in self.disclosureSystem.standardTaxonomiesDict or not isHttpUrl(uri) and '/basis/sbr/' in uri.replace('\\', '/')
            self._isStandardUri[uri] = isStd
            return isStd

    def directedCycle(self, relFrom, origin, fromRelationships, path):
        if relFrom in fromRelationships:
            for rel in fromRelationships[relFrom]:
                relTo = rel.toModelObject
                if relTo == origin:
                    return [rel]
                if relTo not in path:
                    path.add(relTo)
                    foundCycle = self.directedCycle(relTo, origin, fromRelationships, path)
                    if foundCycle is not None:
                        foundCycle.insert(0, rel)
                        return foundCycle
                    path.discard(relTo)

    def checkConceptLabels(self, modelXbrl, labelsRelationshipSet, disclosureSystem, concept):
        hasDefaultLangStandardLabel = False
        dupLabels = {}
        for modelLabelRel in labelsRelationshipSet.fromModelObject(concept):
            modelLabel = modelLabelRel.toModelObject
            if modelLabel is not None and modelLabel.xmlLang:
                if modelLabel.xmlLang.startswith(disclosureSystem.defaultXmlLang) and modelLabel.role == XbrlConst.standardLabel:
                    hasDefaultLangStandardLabel = True
                dupDetectKey = (
                 modelLabel.role or '', modelLabel.xmlLang)
                if dupDetectKey in dupLabels:
                    modelXbrl.error(('EFM.6.10.02', 'GFM.1.5.2', 'SBR.NL.2.2.1.05'), _('Concept %(concept)s has duplicated labels for role %(role)s lang %(lang)s.'), modelObject=(
                     modelLabel, dupLabels[dupDetectKey]), concept=concept.qname, role=dupDetectKey[0], lang=dupDetectKey[1])
                else:
                    dupLabels[dupDetectKey] = modelLabel
                if modelLabel.role in (XbrlConst.periodStartLabel, XbrlConst.periodEndLabel):
                    modelXbrl.error('SBR.NL.2.3.8.03', _('Concept %(concept)s has label for semantical role %(role)s.'), modelObject=modelLabel, concept=concept.qname, role=modelLabel.role)

        if self.validateSBRNL:
            for role, lang in dupLabels.keys():
                if role and lang != disclosureSystem.defaultXmlLang and (role, disclosureSystem.defaultXmlLang) not in dupLabels:
                    modelXbrl.error('SBR.NL.2.3.8.05', _('Concept %(concept)s has en but no nl label in role %(role)s.'), modelObject=(
                     concept, dupLabels[(role, lang)]), concept=concept.qname, role=role)

        if not hasDefaultLangStandardLabel:
            modelXbrl.error(('EFM.6.10.01', 'GFM.1.05.01'), _('Concept used in facts %(concept)s is missing an %(lang)s standard label.'), modelObject=[
             concept] + list(modelXbrl.factsByQname[concept.qname]), concept=concept.qname, lang=disclosureSystem.defaultLanguage)
        try:
            dupLabels[('zzzz', disclosureSystem.defaultXmlLang)] = None
            priorRole = None
            priorLang = None
            hasDefaultLang = True
            for role, lang in sorted(dupLabels.keys()):
                if role != priorRole:
                    if not hasDefaultLang:
                        modelXbrl.error(('EFM.6.10.03', 'GFM.1.5.3'), _('Concept %(concept)s is missing an %(lang)s label for role %(role)s.'), modelObject=list(modelXbrl.factsByQname[concept.qname]) + [dupLabels[(priorRole, priorLang)]], concept=concept.qname, lang=disclosureSystem.defaultLanguage, role=priorRole)
                    hasDefaultLang = False
                    priorLang = lang
                    priorRole = role
                if lang is not None and lang.startswith(disclosureSystem.defaultXmlLang):
                    hasDefaultLang = True

        except Exception as err:
            pass

    def presumptionOfTotal(self, rel, siblingRels, iSibling, isStatementSheet, nestedInTotal, checkLabelRoleOnly):
        """
        A numeric concept target of a parent-child relationship is presumed total if:
        
        (i) its preferredLabel role is a total role (pre XbrlConst static function of 
        current such total roles) or
        
        (ii) if not in a nested total (abstract child relationship to a known total's 
        contributing siblings):
        
        the parent is not SupplementalCashFlowInformationAbstract and the preceding 
        sibling relationship is monetary and it's on a statement sheet and it's the 
        last of more than one monetary item
        
        (a) Last monetary parented by an abstract or non-monetary and not in a nested 
        (breakdown) total, or 
        (b) effective label (en-US of preferred role) has "Total" in its wording.
        (c) (commented out for now due to false positives: Concept name has "Total" 
        in its name)
        (d) last monetary (may be sub level) whose immediate sibling is a calc LB child
        """
        concept = rel.toModelObject
        if isinstance(concept, ModelConcept) and concept.isNumeric:
            preferredLabel = rel.preferredLabel
            if XbrlConst.isTotalRole(preferredLabel):
                return _('preferredLabel {0}').format(os.path.basename(preferredLabel))
            if concept.isMonetary and not checkLabelRoleOnly:
                pass
            effectiveLabel = concept.label(lang='en-US', fallbackToQname=False, preferredLabel=preferredLabel)
            parent = rel.fromModelObject
            if len(siblingRels) > 1 and iSibling == len(siblingRels) - 1 and parent is not None and parent.name not in {'SupplementalCashFlowInformationAbstract'}:
                preceedingSibling = siblingRels[(iSibling - 1)].toModelObject
                if preceedingSibling is not None and preceedingSibling.isMonetary and isStatementSheet:
                    if (parent.isAbstract or not parent.isMonetary) and not nestedInTotal:
                        return _('last monetary item in statement sheet monetary line items parented by nonMonetary concept')
                    if effectiveLabel and 'Total' in effectiveLabel:
                        return _("last monetary item in statement sheet monetary line items with word 'Total' in effective label {0}").format(effectiveLabel)
                    if 'Total' in concept.name:
                        return _("last monetary item in statement sheet monetary line items with word 'Total' in concept name {0}").format(concept.name)
                    if self.summationItemRelsSetAllELRs.isRelated(concept, 'child', preceedingSibling):
                        pass
                    return _('last monetary item in statement sheet monetary line items is calc sum of previous line item')

    def checkCalcsTreeWalk(self, parentChildRels, concept, isStatementSheet, inNestedTotal, conceptsUsed, visited):
        """
        -  EFM-strict validation 6.15.2/3: finding presumed totals in presentation and inspecting for 
           equivalents in calculation (noted as error-semantic, in efm-strict mode).
        
        -  Best practice approach: inspecting for calcuations in the UGT calculations that would hint 
           that like filing constructs should have presentation (noted as warning-semantic in best practices plug-in, when loaded and enabled)
        
        EFM-strict missing-calcs
        
        a. Presumption of total
        
        The presentation linkbase is tree-walked to find items presumed to be totals and their contributing 
        items.  (see description of presumptionOfTotal, above)
        
        b. Finding calculation link roles with least mis-fit to presumed total and its contributing items 
        (presumptionOfTotal in ValidateFiling.py).
        
        For each presumed total (checkForCalculations in ValidateFiling.py):
        
        b.1 Contributing items are found for the presumed total as follows:
        
        From the presumed total, walking back through its preceding sibilings (with caution to avoid 
        looping on allowed direct cycles), a preceding sibling is a contributing item if it has facts, 
        same period type, and numeric.  If a preceding sibling is abstract, the abstract's children are 
        likewise recursively checked (as they often represent a breakdown, and such children of an 
        abstract sibling to the total are also contributing items (except for such children preceding 
        a total at the child level).  
        
        If a preceding sibling is presumed total (on same level), it is a running subtotal (in subsequent
        same-level total) unless it's independent in the calc LB (separate totaled stuff preceding these
        siblings) or related to grandparent sum.
        
        b.2 Finding the facts of these total/contributing item sets
        
        Sets of total and compatible contributing facts that match the sets of total concept and 
        contributing concept must next be found, because each of these different sets (of total 
        and compatible contributing facts) may fit different calculation link roles (according to 
        which compatible contributing facts are present for each total).  This is particularly 
        important when totals and contributing items exist both on face statements and notes, but 
        the contributing compatible fact population is different).
        
        For each fact of the total concept, that has a specified end/instant datetime and unit, if 
        (i) it's not on a statement or 
        (ii) required context is absent or 
        (iii) the fact's end/instant is within the required context's duration, the contributing 
        item facts are those unit and context equivalent to such total fact.
        
        b.3 Finding least-mis-matched calculation link role
        
        Each link role in calculation produces a different set of summation-item arc-sets, and 
        each set of presumed-total facts and compatible contributing item facts is separately 
        considered to find the least-mismatched calculation summation-item arc-set.
        
        The link roles are not intermixed or aggregated, each link role produces independent 
        summation-item arc-sets (XBRL 2.1 section 5.2.5.2).
        
        For each total fact and compatible contributing item facts, the calculation link roles 
        are examined one-by-one for that link-role where the total has children missing the 
        least of the compatible contributing item fact children, and reported either as 6.15.02 
        (for statement sheet presentation link roles) or 6.15.03 (for non-statement link roles).  
        The determination of statement sheet is according to the presentation tree walk.  The 
        search for least-misfit calculation link role does not care or consider the value of the 
        calculation link role, just the summation-item arc-set from the presumed-total concept.
        """
        if concept not in visited:
            visited.add(concept)
            siblingRels = parentChildRels.fromModelObject(concept)
            foundTotalAtThisLevel = False
            for iSibling, rel in enumerate(siblingRels):
                reasonPresumedTotal = self.presumptionOfTotal(rel, siblingRels, iSibling, isStatementSheet, False, inNestedTotal)
                if reasonPresumedTotal:
                    foundTotalAtThisLevel = True
                    self.checkForCalculations(parentChildRels, siblingRels, iSibling, rel.toModelObject, rel, reasonPresumedTotal, isStatementSheet, conceptsUsed, False, set())

            if foundTotalAtThisLevel:
                inNestedTotal = True
            for rel in siblingRels:
                self.checkCalcsTreeWalk(parentChildRels, rel.toModelObject, isStatementSheet, inNestedTotal, conceptsUsed, visited)

            visited.remove(concept)

    def checkForCalculations(self, parentChildRels, siblingRels, iSibling, totalConcept, totalRel, reasonPresumedTotal, isStatementSheet, conceptsUsed, nestedItems, contributingItems):
        for iContributingRel in range(iSibling - 1, -1, -1):
            contributingRel = siblingRels[iContributingRel]
            siblingConcept = contributingRel.toModelObject
            if siblingConcept is not None:
                if siblingConcept is totalConcept:
                    break
                if self.summationItemRelsSetAllELRs.isRelated(totalConcept, 'ancestral-sibling', siblingConcept):
                    break
                if any(self.summationItemRelsSetAllELRs.isRelated(contributingItem, 'child', siblingConcept) for contributingItem in contributingItems):
                    break
                isContributingTotal = self.presumptionOfTotal(contributingRel, siblingRels, iContributingRel, isStatementSheet, True, False)
                if isContributingTotal and self.summationItemRelsSetAllELRs.fromModelObject(siblingConcept) and not self.summationItemRelsSetAllELRs.toModelObject(siblingConcept):
                    break
                if siblingConcept.isAbstract:
                    childRels = parentChildRels.fromModelObject(siblingConcept)
                    self.checkForCalculations(parentChildRels, childRels, len(childRels), totalConcept, totalRel, reasonPresumedTotal, isStatementSheet, conceptsUsed, True, contributingItems)
                else:
                    if siblingConcept in conceptsUsed and siblingConcept.isNumeric and siblingConcept.periodType == totalConcept.periodType:
                        contributingItems.add(siblingConcept)
                    if isContributingTotal:
                        break

        if not nestedItems and contributingItems:
            compatibleItemsFacts = defaultdict(set)
            for totalFact in self.modelXbrl.factsByQname[totalConcept.qname]:
                totalFactContext = totalFact.context
                totalFactUnit = totalFact.unit
                if totalFactContext is not None:
                    if totalFactUnit is not None:
                        pass
                if totalFactContext.endDatetime is not None:
                    if not not isStatementSheet:
                        pass
                if not self.requiredContext is None:
                    if self.requiredContext.startDatetime <= totalFactContext.endDatetime <= self.requiredContext.endDatetime:
                        compatibleItemConcepts = set()
                        compatibleFacts = {totalFact}
                        for itemConcept in contributingItems:
                            for itemFact in self.modelXbrl.factsByQname[itemConcept.qname]:
                                if totalFactContext.isEqualTo(itemFact.context) and totalFactUnit.isEqualTo(itemFact.unit):
                                    compatibleItemConcepts.add(itemConcept)
                                    compatibleFacts.add(itemFact)

                        if len(compatibleItemConcepts) >= 2:
                            compatibleItemsFacts[frozenset(compatibleItemConcepts)].update(compatibleFacts)

            for compatibleItemConcepts, compatibleFacts in compatibleItemsFacts.items():
                foundSummationItemSet = False
                leastMissingItemsSet = compatibleItemConcepts
                for ELR in self.summationItemRelsSetAllELRs.linkRoleUris:
                    relSet = self.modelXbrl.relationshipSet(XbrlConst.summationItem, ELR)
                    missingItems = compatibleItemConcepts - frozenset(r.toModelObject for r in relSet.fromModelObject(totalConcept))
                    missingItems -= set(concept for concept in missingItems if relSet.isRelated(totalConcept, 'sibling-or-descendant', concept))
                    unrequiredItems = set(concept for concept in missingItems if concept.name in 'CommitmentsAndContingencies')
                    missingItems -= unrequiredItems
                    if missingItems:
                        if len(missingItems) < len(leastMissingItemsSet):
                            leastMissingItemsSet = missingItems
                        else:
                            foundSummationItemSet = True

                if not foundSummationItemSet:
                    linkroleDefinition = self.modelXbrl.roleTypeDefinition(contributingRel.linkrole)
                    reasonIssueIsWarning = ''
                    msgCode = 'ERROR-SEMANTIC'
                    if isStatementSheet:
                        errs = ('EFM.6.15.02,6.13.02,6.13.03', 'GFM.2.06.02,2.05.02,2.05.03')
                        msg = _('Financial statement calculation relationship missing from total concept to item concepts, based on required presentation of line items and totals.  %(reasonIssueIsWarning)s\n\nPresentation link role: \n%(linkrole)s \n%(linkroleDefinition)s. \n\nTotal concept: \n%(conceptSum)s.  \n\nReason presumed total: \n%(reasonPresumedTotal)s.  \n\nSummation items missing: \n%(missingConcepts)s.  \n\nExpected item concepts: \n%(itemConcepts)s.  \n\nCorresponding facts in contexts: \n%(contextIDs)s\n')
                    else:
                        errs = ('EFM.6.15.03,6.13.02,6.13.03', 'GFM.2.06.03,2.05.02,2.05.03')
                        msg = _('Notes calculation relationship missing from total concept to item concepts, based on required presentation of line items and totals. %(reasonIssueIsWarning)s\n\nPresentation link role: \n%(linkrole)s \n%(linkroleDefinition)s.\n\nTotal concept: \n%(conceptSum)s.  \n\nReason presumed total: \n%(reasonPresumedTotal)s.  \n\nSummation items missing \n%(missingConcepts)s.  \n\nExpected item concepts \n%(itemConcepts)s.  \n\nCorresponding facts in contexts: \n%(contextIDs)s\n')
                    if all(f.isNil for f in compatibleFacts if f.concept in leastMissingItemsSet):
                        reasonIssueIsWarning = _("\n\nMissing items are nil, which doesn't affect validity but may impair analysis of concept semantics from calculation relationships.  ")
                        msgCode = 'WARNING-SEMANTIC'
                        errs = tuple(e + '.missingItemsNil' for e in errs)
                    if 'parenthetical' in linkroleDefinition.lower():
                        reasonIssueIsWarning += _('\n\nLink role is parenthetical.  ')
                        msgCode = 'WARNING-SEMANTIC'
                        errs = tuple(e + '.parenthetical' for e in errs)
                    self.modelXbrl.log(msgCode, errs, msg, modelObject=[
                     totalConcept, totalRel, siblingConcept, contributingRel] + [f for f in compatibleFacts], reasonIssueIsWarning=reasonIssueIsWarning, conceptSum=totalConcept.qname, linkrole=contributingRel.linkrole, linkroleDefinition=linkroleDefinition, reasonPresumedTotal=reasonPresumedTotal, itemConcepts=', \n'.join(sorted(set(str(c.qname) for c in compatibleItemConcepts))), missingConcepts=', \n'.join(sorted(set(str(c.qname) for c in leastMissingItemsSet))), contextIDs=', '.join(sorted(set(f.contextID for f in compatibleFacts))))
                leastMissingItemsSet = None
                del foundSummationItemSet

            del compatibleItemsFacts

    @property
    def EFM60303(self):
        if self.exhibitType == 'EX-2.01':
            return 'EFM.6.23.01'
        else:
            return 'EFM.6.03.03'


def pLinkedNonAbstractDescendantQnames(modelXbrl, concept, descendants=None):
    if descendants is None:
        descendants = set()
    for rel in modelXbrl.relationshipSet(XbrlConst.parentChild).fromModelObject(concept):
        child = rel.toModelObject
        if child is not None:
            if child.isAbstract:
                pLinkedNonAbstractDescendantQnames(modelXbrl, child, descendants)
            else:
                descendants.add(child.qname)

    return descendants