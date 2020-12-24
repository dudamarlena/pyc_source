# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\ProgramData\lib\site-packages\arelle\Validate.py
# Compiled at: 2018-02-26 09:10:06
# Size of source mod 2**32: 42736 bytes
__doc__ = '\nCreated on Oct 17, 2010\n\n@author: Mark V Systems Limited\n(c) Copyright 2010 Mark V Systems Limited, All rights reserved.\n'
import os, sys, traceback, re
from collections import defaultdict, OrderedDict
from arelle import FileSource, ModelXbrl, ModelDocument, ModelVersReport, XbrlConst, ValidateXbrl, ValidateFiling, ValidateHmrc, ValidateVersReport, ValidateFormula, ValidateInfoset, RenderingEvaluator, ViewFileRenderedGrid, UrlUtil
from arelle.ModelDocument import Type, ModelDocumentReference, load as modelDocumentLoad
from arelle.ModelDtsObject import ModelResource
from arelle.ModelInstanceObject import ModelFact
from arelle.ModelObject import ModelObject
from arelle.ModelRelationshipSet import ModelRelationshipSet
from arelle.ModelValue import qname, QName
from arelle.PluginManager import pluginClassMethods
from arelle.XmlUtil import collapseWhitespace, xmlstring

def validate(modelXbrl):
    validate = Validate(modelXbrl)
    validate.validate()


class ValidationException(Exception):

    def __init__(self, message, severity, code):
        self.message = message
        self.severity = severity
        self.code = code

    def __repr__(self):
        return '{0}({1})={2}'.format(self.code, self.severity, self.message)


class Validate:
    """Validate"""

    def __init__(self, modelXbrl):
        self.modelXbrl = modelXbrl
        if modelXbrl.modelManager.validateDisclosureSystem:
            if modelXbrl.modelManager.disclosureSystem.HMRC:
                self.instValidator = ValidateHmrc.ValidateHmrc(modelXbrl)
            else:
                if modelXbrl.modelManager.disclosureSystem.EFMorGFM or modelXbrl.modelManager.disclosureSystem.SBRNL:
                    self.instValidator = ValidateFiling.ValidateFiling(modelXbrl)
                else:
                    self.instValidator = ValidateXbrl.ValidateXbrl(modelXbrl)
            self.formulaValidator = ValidateXbrl.ValidateXbrl(modelXbrl)
        else:
            self.instValidator = ValidateXbrl.ValidateXbrl(modelXbrl)
            self.formulaValidator = self.instValidator
        if hasattr(modelXbrl, 'fileSource'):
            self.useFileSource = modelXbrl.fileSource
        else:
            self.useFileSource = None

    def close(self):
        self.instValidator.close(reusable=False)
        self.formulaValidator.close(reusable=False)
        self.__dict__.clear()

    def validate(self):
        if self.modelXbrl.modelDocument is None:
            self.modelXbrl.info('arelle:notValdated', (_('Validation skipped, document not successfully loaded: %(file)s')),
              modelXbrl=(self.modelXbrl),
              file=(self.modelXbrl.modelDocument.basename))
        else:
            if self.modelXbrl.modelDocument.type in (Type.TESTCASESINDEX, Type.REGISTRY, Type.TESTCASE, Type.REGISTRYTESTCASE):
                try:
                    _disclosureSystem = self.modelXbrl.modelManager.disclosureSystem
                    if _disclosureSystem.name:
                        self.modelXbrl.info('info', (_('Disclosure system %(disclosureSystemName)s, version %(disclosureSystemVersion)s')),
                          modelXbrl=(self.modelXbrl),
                          disclosureSystemName=(_disclosureSystem.name),
                          disclosureSystemVersion=(_disclosureSystem.version))
                    if self.modelXbrl.modelDocument.type in (Type.TESTCASESINDEX, Type.REGISTRY):
                        _name = self.modelXbrl.modelDocument.basename
                        for testcasesElement in self.modelXbrl.modelDocument.xmlRootElement.iter():
                            if isinstance(testcasesElement, ModelObject):
                                if testcasesElement.localName in ('testcases', 'testSuite'):
                                    if testcasesElement.get('name'):
                                        _name = testcasesElement.get('name')
                                    break

                        self.modelXbrl.info('info', (_('Testcases - %(name)s')), modelXbrl=(self.modelXbrl.modelDocument), name=_name)
                        _statusCounts = OrderedDict((('pass', 0), ('fail', 0)))
                        for doc in sorted((self.modelXbrl.modelDocument.referencesDocument.keys()), key=(lambda doc: doc.uri)):
                            self.validateTestcase(doc)
                            for tv in getattr(doc, 'testcaseVariations', ()):
                                _statusCounts[tv.status] = _statusCounts.get(tv.status, 0) + 1

                        self.modelXbrl.info('arelle:testResults', ', '.join('{}={}'.format(k, c) for k, c in _statusCounts.items() if k))
                    else:
                        if self.modelXbrl.modelDocument.type in (Type.TESTCASE, Type.REGISTRYTESTCASE):
                            self.validateTestcase(self.modelXbrl.modelDocument)
                except Exception as err:
                    self.modelXbrl.error(('exception:' + type(err).__name__), (_('Testcase validation exception: %(error)s, testcase: %(testcase)s')),
                      modelXbrl=(self.modelXbrl),
                      testcase=(self.modelXbrl.modelDocument.basename),
                      error=err,
                      exc_info=True)

            else:
                if self.modelXbrl.modelDocument.type == Type.VERSIONINGREPORT:
                    try:
                        ValidateVersReport.ValidateVersReport(self.modelXbrl).validate(self.modelXbrl)
                    except Exception as err:
                        self.modelXbrl.error(('exception:' + type(err).__name__), (_('Versioning report exception: %(error)s, testcase: %(reportFile)s')),
                          modelXbrl=(self.modelXbrl),
                          reportFile=(self.modelXbrl.modelDocument.basename),
                          error=err,
                          exc_info=True)

                else:
                    if self.modelXbrl.modelDocument.type == Type.RSSFEED:
                        self.validateRssFeed()
                    else:
                        try:
                            self.instValidator.validate(self.modelXbrl, self.modelXbrl.modelManager.formulaOptions.typedParameters(self.modelXbrl.prefixedNamespaces))
                            self.instValidator.close()
                        except Exception as err:
                            self.modelXbrl.error(('exception:' + type(err).__name__), (_('Instance validation exception: %(error)s, instance: %(instance)s')),
                              modelXbrl=(self.modelXbrl),
                              instance=(self.modelXbrl.modelDocument.basename),
                              error=err,
                              exc_info=True)

        self.close()

    def validateRssFeed(self):
        self.modelXbrl.info('info', 'RSS Feed', modelDocument=(self.modelXbrl))
        from arelle.FileSource import openFileSource
        reloadCache = getattr(self.modelXbrl, 'reloadCache', False)
        for rssItem in self.modelXbrl.modelDocument.rssItems:
            if getattr(rssItem, 'skipRssItem', False):
                self.modelXbrl.info('info', (_('skipping RSS Item %(accessionNumber)s %(formType)s %(companyName)s %(period)s')), modelObject=rssItem,
                  accessionNumber=(rssItem.accessionNumber),
                  formType=(rssItem.formType),
                  companyName=(rssItem.companyName),
                  period=(rssItem.period))
            else:
                self.modelXbrl.info('info', (_('RSS Item %(accessionNumber)s %(formType)s %(companyName)s %(period)s')), modelObject=rssItem,
                  accessionNumber=(rssItem.accessionNumber),
                  formType=(rssItem.formType),
                  companyName=(rssItem.companyName),
                  period=(rssItem.period))
                modelXbrl = None
                try:
                    modelXbrl = ModelXbrl.load((self.modelXbrl.modelManager), openFileSource((rssItem.zippedUrl), (self.modelXbrl.modelManager.cntlr), reloadCache=reloadCache),
                      (_('validating')),
                      rssItem=rssItem)
                    for pluginXbrlMethod in pluginClassMethods('RssItem.Xbrl.Loaded'):
                        pluginXbrlMethod(modelXbrl, {}, rssItem)

                    if getattr(rssItem, 'doNotProcessRSSitem', False) or modelXbrl.modelDocument is None:
                        modelXbrl.close()
                        continue
                    self.instValidator.validate(modelXbrl, self.modelXbrl.modelManager.formulaOptions.typedParameters(self.modelXbrl.prefixedNamespaces))
                    self.instValidator.close()
                    rssItem.setResults(modelXbrl)
                    self.modelXbrl.modelManager.viewModelObject(self.modelXbrl, rssItem.objectId())
                    for pluginXbrlMethod in pluginClassMethods('Validate.RssItem'):
                        pluginXbrlMethod(self, modelXbrl, rssItem)

                    modelXbrl.close()
                except Exception as err:
                    self.modelXbrl.error(('exception:' + type(err).__name__), (_('RSS item validation exception: %(error)s, instance: %(instance)s')),
                      modelXbrl=(
                     self.modelXbrl, modelXbrl),
                      instance=(rssItem.zippedUrl),
                      error=err,
                      exc_info=True)
                    try:
                        self.instValidator.close()
                        if modelXbrl is not None:
                            modelXbrl.close()
                    except Exception as err:
                        pass

                del modelXbrl

    def validateTestcase(self, testcase):
        self.modelXbrl.info('info', 'Testcase', modelDocument=testcase)
        self.modelXbrl.viewModelObject(testcase.objectId())
        if testcase.type == Type.TESTCASESINDEX:
            for doc in sorted((testcase.referencesDocument.keys()), key=(lambda doc: doc.uri)):
                self.validateTestcase(doc)

        elif hasattr(testcase, 'testcaseVariations'):
            for modelTestcaseVariation in testcase.testcaseVariations:
                self.modelXbrl.modelManager.viewModelObject(self.modelXbrl, modelTestcaseVariation.objectId())
                resultIsVersioningReport = modelTestcaseVariation.resultIsVersioningReport
                resultIsXbrlInstance = modelTestcaseVariation.resultIsXbrlInstance
                resultIsTaxonomyPackage = modelTestcaseVariation.resultIsTaxonomyPackage
                formulaOutputInstance = None
                inputDTSes = defaultdict(list)
                baseForElement = testcase.baseForElement(modelTestcaseVariation)
                self.modelXbrl.info('info', (_('Variation %(id)s %(name)s: %(expected)s - %(description)s')), modelObject=modelTestcaseVariation,
                  id=(modelTestcaseVariation.id),
                  name=(modelTestcaseVariation.name),
                  expected=(modelTestcaseVariation.expected),
                  description=(modelTestcaseVariation.description))
                errorCaptureLevel = modelTestcaseVariation.severityLevel
                parameters = modelTestcaseVariation.parameters.copy()
                for readMeFirstUri in modelTestcaseVariation.readMeFirstUris:
                    if isinstance(readMeFirstUri, tuple):
                        dtsName, readMeFirstUri = readMeFirstUri
                    else:
                        if resultIsVersioningReport:
                            if inputDTSes:
                                dtsName = 'to'
                            else:
                                dtsName = 'from'
                        else:
                            dtsName = None
                    if resultIsVersioningReport:
                        if dtsName:
                            if dtsName in inputDTSes:
                                dtsName = inputDTSes[dtsName]
                            else:
                                modelXbrl = ModelXbrl.create((self.modelXbrl.modelManager), (Type.DTSENTRIES),
                                  (self.modelXbrl.modelManager.cntlr.webCache.normalizeUrl(readMeFirstUri[:-4] + '.dts', baseForElement)),
                                  isEntry=True,
                                  errorCaptureLevel=errorCaptureLevel)
                            DTSdoc = modelXbrl.modelDocument
                            DTSdoc.inDTS = True
                            doc = modelDocumentLoad(modelXbrl, readMeFirstUri, base=baseForElement)
                            if doc is not None:
                                DTSdoc.referencesDocument[doc] = ModelDocumentReference('import', DTSdoc.xmlRootElement)
                                doc.inDTS = True
                        else:
                            if resultIsTaxonomyPackage:
                                from arelle import PackageManager, PrototypeInstanceObject
                                dtsName = readMeFirstUri
                                modelXbrl = PrototypeInstanceObject.XbrlPrototype(self.modelXbrl.modelManager, readMeFirstUri)
                                PackageManager.packageInfo((self.modelXbrl.modelManager.cntlr), readMeFirstUri, reload=True, errors=(modelXbrl.errors))
                            else:
                                if self.useFileSource.isArchive:
                                    modelXbrl = ModelXbrl.load((self.modelXbrl.modelManager), readMeFirstUri,
                                      (_('validating')),
                                      base=baseForElement,
                                      useFileSource=(self.useFileSource),
                                      errorCaptureLevel=errorCaptureLevel)
                                else:
                                    filesource = FileSource.FileSource(readMeFirstUri, self.modelXbrl.modelManager.cntlr)
                                    if filesource:
                                        if not filesource.selection:
                                            if filesource.isArchive:
                                                for _archiveFile in filesource.dir or ():
                                                    filesource.select(_archiveFile)
                                                    if ModelDocument.Type.identify(filesource, filesource.url) in (ModelDocument.Type.INSTANCE, ModelDocument.Type.INLINEXBRL):
                                                        break

                                    modelXbrl = ModelXbrl.load((self.modelXbrl.modelManager), filesource,
                                      (_('validating')),
                                      base=baseForElement,
                                      errorCaptureLevel=errorCaptureLevel)
                    else:
                        modelXbrl.isTestcaseVariation = True
                    if modelXbrl.modelDocument is None:
                        modelXbrl.error('arelle:notLoaded', (_('Variation %(id)s %(name)s readMeFirst document not loaded: %(file)s')),
                          modelXbrl=testcase,
                          id=(modelTestcaseVariation.id),
                          name=(modelTestcaseVariation.name),
                          file=(os.path.basename(readMeFirstUri)))
                        self.determineNotLoadedTestStatus(modelTestcaseVariation, modelXbrl.errors)
                        modelXbrl.close()
                    elif resultIsVersioningReport or resultIsTaxonomyPackage:
                        inputDTSes[dtsName] = modelXbrl
                    elif modelXbrl.modelDocument.type == Type.VERSIONINGREPORT:
                        ValidateVersReport.ValidateVersReport(self.modelXbrl).validate(modelXbrl)
                        self.determineTestStatus(modelTestcaseVariation, modelXbrl.errors)
                        modelXbrl.close()
                    elif testcase.type == Type.REGISTRYTESTCASE:
                        self.instValidator.validate(modelXbrl)
                        self.instValidator.executeCallTest(modelXbrl, modelTestcaseVariation.id, modelTestcaseVariation.cfcnCall, modelTestcaseVariation.cfcnTest)
                        self.determineTestStatus(modelTestcaseVariation, modelXbrl.errors)
                        self.instValidator.close()
                        modelXbrl.close()
                    else:
                        inputDTSes[dtsName].append(modelXbrl)
                        _hasFormulae = modelXbrl.hasFormulae
                        modelXbrl.hasFormulae = False
                        try:
                            for pluginXbrlMethod in pluginClassMethods('TestcaseVariation.Xbrl.Loaded'):
                                pluginXbrlMethod(self.modelXbrl, modelXbrl, modelTestcaseVariation)

                            self.instValidator.validate(modelXbrl, parameters)
                            for pluginXbrlMethod in pluginClassMethods('TestcaseVariation.Xbrl.Validated'):
                                pluginXbrlMethod(self.modelXbrl, modelXbrl)

                        except Exception as err:
                            modelXbrl.error(('exception:' + type(err).__name__), (_('Testcase variation validation exception: %(error)s, instance: %(instance)s')),
                              modelXbrl=modelXbrl,
                              instance=(modelXbrl.modelDocument.basename),
                              error=err,
                              exc_info=True)

                        modelXbrl.hasFormulae = _hasFormulae

                if resultIsVersioningReport:
                    if modelXbrl.modelDocument:
                        versReportFile = modelXbrl.modelManager.cntlr.webCache.normalizeUrl(modelTestcaseVariation.versioningReportUri, baseForElement)
                        if os.path.exists(versReportFile):
                            modelVersReport = ModelXbrl.load(self.modelXbrl.modelManager, versReportFile, _('validating existing version report'))
                            if modelVersReport:
                                if modelVersReport.modelDocument:
                                    if modelVersReport.modelDocument.type == Type.VERSIONINGREPORT:
                                        ValidateVersReport.ValidateVersReport(self.modelXbrl).validate(modelVersReport)
                                        self.determineTestStatus(modelTestcaseVariation, modelVersReport.errors)
                                        modelVersReport.close()
                        else:
                            if len(inputDTSes) == 2:
                                ModelVersReport.ModelVersReport(self.modelXbrl).diffDTSes(versReportFile, inputDTSes['from'], inputDTSes['to'])
                                modelTestcaseVariation.status = 'generated'
                            else:
                                modelXbrl.error('arelle:notLoaded', (_('Variation %(id)s %(name)s input DTSes not loaded, unable to generate versioning report: %(file)s')),
                                  modelXbrl=testcase,
                                  id=(modelTestcaseVariation.id),
                                  name=(modelTestcaseVariation.name),
                                  file=(os.path.basename(readMeFirstUri)))
                                modelTestcaseVariation.status = 'failed'
                        for inputDTS in inputDTSes.values():
                            inputDTS.close()

                        del inputDTSes
                if resultIsTaxonomyPackage:
                    self.determineTestStatus(modelTestcaseVariation, modelXbrl.errors)
                    modelXbrl.close()
                else:
                    if inputDTSes:
                        modelXbrl = inputDTSes[None][0]
                        expectedDataFiles = set(modelXbrl.modelManager.cntlr.webCache.normalizeUrl(uri, baseForElement) for d in modelTestcaseVariation.dataUris.values() for uri in d)
                        foundDataFiles = set()
                        variationBase = os.path.dirname(baseForElement)
                        for dtsName, inputDTS in inputDTSes.items():
                            if dtsName:
                                parameters[dtsName] = (
                                 None, inputDTS)
                            else:
                                if len(inputDTS) > 1:
                                    parameters[XbrlConst.qnStandardInputInstance] = (
                                     None, inputDTS)
                            for _inputDTS in inputDTS:
                                for docUrl in _inputDTS.urlDocs.keys():
                                    if docUrl.startswith(variationBase):
                                        foundDataFiles.add(docUrl)

                        if expectedDataFiles - foundDataFiles:
                            modelXbrl.error('arelle:testcaseDataNotUsed', (_('Variation %(id)s %(name)s data files not used: %(missingDataFiles)s')),
                              modelObject=modelTestcaseVariation,
                              name=(modelTestcaseVariation.name),
                              id=(modelTestcaseVariation.id),
                              missingDataFiles=(', '.join(sorted(os.path.basename(f) for f in expectedDataFiles - foundDataFiles))))
                        if foundDataFiles - expectedDataFiles:
                            modelXbrl.warning('arelle:testcaseDataUnexpected', (_('Variation %(id)s %(name)s files not in variation data: %(unexpectedDataFiles)s')),
                              modelObject=modelTestcaseVariation,
                              name=(modelTestcaseVariation.name),
                              id=(modelTestcaseVariation.id),
                              unexpectedDataFiles=(', '.join(sorted(os.path.basename(f) for f in foundDataFiles - expectedDataFiles))))
                        if modelXbrl.hasTableRendering or modelTestcaseVariation.resultIsTable:
                            try:
                                RenderingEvaluator.init(modelXbrl)
                            except Exception as err:
                                modelXbrl.error(('exception:' + type(err).__name__), (_('Testcase RenderingEvaluator.init exception: %(error)s, instance: %(instance)s')),
                                  modelXbrl=modelXbrl,
                                  instance=(modelXbrl.modelDocument.basename),
                                  error=err,
                                  exc_info=True)

                        modelXbrlHasFormulae = modelXbrl.hasFormulae
                        if modelXbrlHasFormulae:
                            try:
                                self.instValidator.parameters = parameters
                                ValidateFormula.validate(self.instValidator)
                            except Exception as err:
                                modelXbrl.error(('exception:' + type(err).__name__), (_('Testcase formula variation validation exception: %(error)s, instance: %(instance)s')),
                                  modelXbrl=modelXbrl,
                                  instance=(modelXbrl.modelDocument.basename),
                                  error=err,
                                  exc_info=True)

                        if modelTestcaseVariation.resultIsInfoset:
                            if self.modelXbrl.modelManager.validateInfoset:
                                for pluginXbrlMethod in pluginClassMethods('Validate.Infoset'):
                                    pluginXbrlMethod(modelXbrl, modelTestcaseVariation.resultInfosetUri)

                                infoset = ModelXbrl.load((self.modelXbrl.modelManager), (modelTestcaseVariation.resultInfosetUri),
                                  (_('loading result infoset')),
                                  base=baseForElement,
                                  useFileSource=(self.useFileSource),
                                  errorCaptureLevel=errorCaptureLevel)
                                if infoset.modelDocument is None:
                                    modelXbrl.error('arelle:notLoaded', (_('Variation %(id)s %(name)s result infoset not loaded: %(file)s')),
                                      modelXbrl=testcase,
                                      id=(modelTestcaseVariation.id),
                                      name=(modelTestcaseVariation.name),
                                      file=(os.path.basename(modelTestcaseVariation.resultXbrlInstance)))
                                    modelTestcaseVariation.status = 'result infoset not loadable'
                                else:
                                    ValidateInfoset.validate(self.instValidator, modelXbrl, infoset)
                                infoset.close()
                        if modelXbrl.hasTableRendering or modelTestcaseVariation.resultIsTable:
                            resultTableUri = modelXbrl.modelManager.cntlr.webCache.normalizeUrl(modelTestcaseVariation.resultTableUri, baseForElement)
                            if not any(alternativeValidation(modelXbrl, resultTableUri) for alternativeValidation in pluginClassMethods('Validate.TableInfoset')):
                                try:
                                    ViewFileRenderedGrid.viewRenderedGrid(modelXbrl, resultTableUri, diffToFile=True)
                                except Exception as err:
                                    modelXbrl.error(('exception:' + type(err).__name__), (_('Testcase table linkbase validation exception: %(error)s, instance: %(instance)s')),
                                      modelXbrl=modelXbrl,
                                      instance=(modelXbrl.modelDocument.basename),
                                      error=err,
                                      exc_info=True)

                        self.instValidator.close()
                        extraErrors = []
                        for pluginXbrlMethod in pluginClassMethods('TestcaseVariation.Validated'):
                            pluginXbrlMethod(self.modelXbrl, modelXbrl, extraErrors)

                        self.determineTestStatus(modelTestcaseVariation, [e for inputDTSlist in inputDTSes.values() for inputDTS in inputDTSlist for e in inputDTS.errors] + extraErrors)
                        if modelXbrl.formulaOutputInstance:
                            if self.noErrorCodes(modelTestcaseVariation.actual):
                                modelXbrl.formulaOutputInstance.hasFormulae = False
                                self.instValidator.validate(modelXbrl.formulaOutputInstance, modelTestcaseVariation.parameters)
                                self.determineTestStatus(modelTestcaseVariation, modelXbrl.formulaOutputInstance.errors)
                                if self.noErrorCodes(modelTestcaseVariation.actual):
                                    formulaOutputInstance = modelXbrl.formulaOutputInstance
                                    modelXbrl.formulaOutputInstance = None
                                self.instValidator.close()
                        compareIxResultInstance = modelXbrl.modelDocument.type in (Type.INLINEXBRL, Type.INLINEXBRLDOCUMENTSET) and modelTestcaseVariation.resultXbrlInstanceUri is not None
                        if compareIxResultInstance:
                            formulaOutputInstance = modelXbrl
                            errMsgPrefix = 'ix'
                        else:
                            for inputDTSlist in inputDTSes.values():
                                for inputDTS in inputDTSlist:
                                    inputDTS.close()

                            del inputDTSes
                            errMsgPrefix = 'formula'
                        if resultIsXbrlInstance:
                            if formulaOutputInstance:
                                if formulaOutputInstance.modelDocument:
                                    _matchExpectedResultIDs = not modelXbrlHasFormulae
                                    expectedInstance = ModelXbrl.load((self.modelXbrl.modelManager), (modelTestcaseVariation.resultXbrlInstanceUri),
                                      (_('loading expected result XBRL instance')),
                                      base=baseForElement,
                                      useFileSource=(self.useFileSource),
                                      errorCaptureLevel=errorCaptureLevel)
                                    if expectedInstance.modelDocument is None:
                                        self.modelXbrl.error(('{}:expectedResultNotLoaded'.format(errMsgPrefix)), (_('Testcase "%(name)s" %(id)s expected result instance not loaded: %(file)s')),
                                          modelXbrl=testcase,
                                          id=(modelTestcaseVariation.id),
                                          name=(modelTestcaseVariation.name),
                                          file=(os.path.basename(modelTestcaseVariation.resultXbrlInstanceUri)),
                                          messageCodes=('formula:expectedResultNotLoaded',
                                                        'ix:expectedResultNotLoaded'))
                                        modelTestcaseVariation.status = 'result not loadable'
                                    else:
                                        if len(expectedInstance.facts) != len(formulaOutputInstance.facts):
                                            formulaOutputInstance.error(('{}:resultFactCounts'.format(errMsgPrefix)), (_('Formula output %(countFacts)s facts, expected %(expectedFacts)s facts')),
                                              modelXbrl=modelXbrl,
                                              countFacts=(len(formulaOutputInstance.facts)),
                                              expectedFacts=(len(expectedInstance.facts)),
                                              messageCodes=('formula:resultFactCounts',
                                                            'ix:resultFactCounts'))
                                        else:
                                            formulaOutputFootnotesRelSet = ModelRelationshipSet(formulaOutputInstance, 'XBRL-footnotes')
                                            expectedFootnotesRelSet = ModelRelationshipSet(expectedInstance, 'XBRL-footnotes')

                                            def factFootnotes(fact, footnotesRelSet):
                                                footnotes = {}
                                                footnoteRels = footnotesRelSet.fromModelObject(fact)
                                                if footnoteRels:
                                                    for i, footnoteRel in enumerate(sorted(footnoteRels, key=(lambda r: (
                                                     r.fromLabel, r.toLabel)))):
                                                        modelObject = footnoteRel.toModelObject
                                                        if isinstance(modelObject, ModelResource):
                                                            xml = modelObject.viewText().strip()
                                                            footnotes['Footnote {}'.format(i + 1)] = xml
                                                        else:
                                                            if isinstance(modelObject, ModelFact):
                                                                footnotes['Footnoted fact {}'.format(i + 1)] = '{} context: {} value: {}'.format(modelObject.qname, modelObject.contextID, collapseWhitespace(modelObject.value))

                                                return footnotes

                                            for expectedInstanceFact in expectedInstance.facts:
                                                unmatchedFactsStack = []
                                                formulaOutputFact = formulaOutputInstance.matchFact(expectedInstanceFact, unmatchedFactsStack, deemP0inf=True, matchId=_matchExpectedResultIDs, matchLang=False)
                                                if formulaOutputFact is None:
                                                    if unmatchedFactsStack:
                                                        missingFact = unmatchedFactsStack[(-1)]
                                                    else:
                                                        missingFact = expectedInstanceFact
                                                    formulaOutputInstance.error(('{}:expectedFactMissing'.format(errMsgPrefix)), (_('Output missing expected fact %(fact)s')),
                                                      modelXbrl=missingFact,
                                                      fact=(missingFact.qname),
                                                      messageCodes=('formula:expectedFactMissing',
                                                                    'ix:expectedFactMissing'))
                                                else:
                                                    expectedInstanceFactFootnotes = factFootnotes(expectedInstanceFact, expectedFootnotesRelSet)
                                                    formulaOutputFactFootnotes = factFootnotes(formulaOutputFact, formulaOutputFootnotesRelSet)
                                                    if len(expectedInstanceFactFootnotes) != len(formulaOutputFactFootnotes) or set(expectedInstanceFactFootnotes.values()) != set(formulaOutputFactFootnotes.values()):
                                                        formulaOutputInstance.error(('{}:expectedFactFootnoteDifference'.format(errMsgPrefix)), (_('Output expected fact %(fact)s expected footnotes %(footnotes1)s produced footnotes %(footnotes2)s')),
                                                          modelXbrl=(
                                                         formulaOutputFact, expectedInstanceFact),
                                                          fact=(expectedInstanceFact.qname),
                                                          footnotes1=(sorted(expectedInstanceFactFootnotes.items())),
                                                          footnotes2=(sorted(formulaOutputFactFootnotes.items())),
                                                          messageCodes=('formula:expectedFactFootnoteDifference',
                                                                        'ix:expectedFactFootnoteDifference'))

                                        expectedInstance.close()
                                        del expectedInstance
                                        self.determineTestStatus(modelTestcaseVariation, formulaOutputInstance.errors)
                                        formulaOutputInstance.close()
                                        del formulaOutputInstance
                        if compareIxResultInstance:
                            for inputDTSlist in inputDTSes.values():
                                for inputDTS in inputDTSlist:
                                    inputDTS.close()

                            del inputDTSes
                self.modelXbrl.modelManager.viewModelObject(self.modelXbrl, modelTestcaseVariation.objectId())

            self.modelXbrl.modelManager.showStatus(_('ready'), 2000)

    def noErrorCodes(self, modelTestcaseVariation):
        return not any(not isinstance(actual, dict) for actual in modelTestcaseVariation)

    def determineTestStatus(self, modelTestcaseVariation, errors):
        _blockedMessageCodes = modelTestcaseVariation.blockedMessageCodes
        if _blockedMessageCodes:
            _blockPattern = re.compile(_blockedMessageCodes)
            _errors = [e for e in errors if not _blockPattern.match(e)]
        else:
            _errors = errors
        numErrors = len(_errors)
        expected = modelTestcaseVariation.expected
        expectedCount = modelTestcaseVariation.expectedCount
        if expected == 'valid':
            if numErrors == 0:
                status = 'pass'
            else:
                status = 'fail'
        elif expected == 'invalid':
            if numErrors == 0:
                status = 'fail'
            else:
                status = 'pass'
        else:
            if expected is None and numErrors == 0:
                status = 'pass'
            else:
                if isinstance(expected, (QName, _STR_BASE, dict)):
                    status = 'fail'
                    _passCount = 0
                    for testErr in _errors:
                        if isinstance(expected, QName) and isinstance(testErr, _STR_BASE):
                            errPrefix, sep, errLocalName = testErr.rpartition(':')
                            if not sep and errLocalName == expected.localName or expected == qname(XbrlConst.errMsgPrefixNS.get(errPrefix) or errPrefix == expected.prefix and expected.namespaceURI, errLocalName) or expected.namespaceURI == XbrlConst.xdtSchemaErrorNS and errPrefix == 'xmlSchema':
                                _passCount += 1
                        else:
                            if type(testErr) == type(expected):
                                if testErr == expected or isinstance(expected, _STR_BASE) and (expected == 'EFM.6.03.04' and testErr.startswith('xmlSchema:') or expected == 'EFM.6.03.05' and (testErr.startswith('xmlSchema:') or testErr == 'EFM.5.02.01.01') or expected == 'EFM.6.04.03' and (testErr.startswith('xmlSchema:') or testErr.startswith('utr:') or testErr.startswith('xbrl.') or testErr.startswith('xlink:')) or expected == 'EFM.6.05.35' and testErr.startswith('utre:') or expected.startswith('EFM.') and testErr.startswith(expected) or expected == 'vere:invalidDTSIdentifier' and testErr.startswith('xbrl')):
                                    _passCount += 1

                    if _passCount > 0:
                        if expectedCount is not None:
                            if expectedCount != _passCount:
                                status = 'fail (count)'
                        else:
                            status = 'pass'
                    if status == 'fail':
                        if isinstance(expected, _STR_BASE):
                            if ' ' in expected:
                                if all(any(testErr == e for testErr in _errors) for e in expected.split()):
                                    status = 'pass'
                    if not _errors:
                        if status == 'fail':
                            if modelTestcaseVariation.assertions:
                                if modelTestcaseVariation.assertions == expected:
                                    status = 'pass'
                            else:
                                if isinstance(expected, dict) and all(countSatisfied == 0 and countNotSatisfied == 0 for countSatisfied, countNotSatisfied in expected.values()):
                                    status = 'pass'
                else:
                    status = 'fail'
            modelTestcaseVariation.status = status
            _actual = {}
        if numErrors > 0:
            for error in _errors:
                if isinstance(error, dict):
                    modelTestcaseVariation.assertions = error
                else:
                    _actual[error] = _actual.get(error, 0) + 1

            modelTestcaseVariation.actual = [error if qty == 1 else '{} ({})'.format(error, qty) for error, qty in sorted((_actual.items()), key=(lambda i: i[0]))]
            for error in _errors:
                if isinstance(error, dict):
                    modelTestcaseVariation.actual.append(error)

    def determineNotLoadedTestStatus(self, modelTestcaseVariation, errors):
        if errors:
            self.determineTestStatus(modelTestcaseVariation, errors)
            return
        expected = modelTestcaseVariation.expected
        status = 'not loadable'
        if expected in ('EFM.6.03.04', 'EFM.6.03.05'):
            status = 'pass'
        modelTestcaseVariation.status = status


import logging

class ValidationLogListener(logging.Handler):

    def __init__(self, logView):
        self.logView = logView
        self.level = logging.DEBUG

    def flush(self):
        """ Nothing to flush """
        pass

    def emit(self, logRecord):
        msg = self.format(logRecord)
        try:
            self.logView.append(msg)
        except:
            pass