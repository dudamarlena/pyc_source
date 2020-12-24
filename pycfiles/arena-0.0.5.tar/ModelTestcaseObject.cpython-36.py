# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\ProgramData\lib\site-packages\arelle\ModelTestcaseObject.py
# Compiled at: 2018-02-26 09:10:06
# Size of source mod 2**32: 18775 bytes
__doc__ = '\nCreated on Oct 5, 2010\nRefactored from ModelObject on Jun 11, 2011\n\n@author: Mark V Systems Limited\n(c) Copyright 2010 Mark V Systems Limited, All rights reserved.\n'
import os, io, logging
from collections import defaultdict
from arelle import XmlUtil, XbrlConst, ModelValue
from arelle.ModelObject import ModelObject
from arelle.PluginManager import pluginClassMethods
TXMY_PKG_SRC_ELTS = ('metadata', 'catalog', 'taxonomy')

class ModelTestcaseVariation(ModelObject):

    def init(self, modelDocument):
        super(ModelTestcaseVariation, self).init(modelDocument)
        self.status = ''
        self.actual = []
        self.assertions = None

    @property
    def id(self):
        id = super(ModelTestcaseVariation, self).id
        if id is not None:
            return id
        else:
            return self.objectId()

    @property
    def name(self):
        try:
            return self._name
        except AttributeError:
            if self.get('name'):
                self._name = self.get('name')
            else:
                nameElement = XmlUtil.descendant(self, None, 'name' if self.localName != 'testcase' else 'number')
                if nameElement is not None:
                    self._name = XmlUtil.innerText(nameElement)
                else:
                    self._name = None
            return self._name

    @property
    def description(self):
        nameElement = XmlUtil.descendant(self, None, ('description', 'documentation'))
        if nameElement is not None:
            return XmlUtil.innerText(nameElement)

    @property
    def reference(self):
        efmNameElts = XmlUtil.children(self.getparent(), None, 'name')
        for efmNameElt in efmNameElts:
            if efmNameElt is not None:
                if efmNameElt.text.startswith('EDGAR'):
                    return efmNameElt.text

        referenceElement = XmlUtil.descendant(self, None, 'reference')
        if referenceElement is not None:
            return '{0}#{1}'.format(referenceElement.get('specification'), referenceElement.get('id'))
        referenceElement = XmlUtil.descendant(self, None, 'documentationReference')
        if referenceElement is not None:
            return referenceElement.get('{http://www.w3.org/1999/xlink}href')
        descriptionElement = XmlUtil.descendant(self, None, 'description')
        if descriptionElement is not None:
            if descriptionElement.get('reference'):
                return descriptionElement.get('reference')
        if self.getparent().get('description'):
            return self.getparent().get('description')
        functRegistryRefElt = XmlUtil.descendant(self.getparent(), None, 'reference')
        if functRegistryRefElt is not None:
            return functRegistryRefElt.get('{http://www.w3.org/1999/xlink}href')

    @property
    def readMeFirstUris(self):
        try:
            return self._readMeFirstUris
        except AttributeError:
            self._readMeFirstUris = []
            if any(pluginXbrlMethod(self) for pluginXbrlMethod in pluginClassMethods('ModelTestcaseVariation.ReadMeFirstUris')) or self.localName == 'testGroup':
                instanceTestElement = XmlUtil.descendant(self, None, 'instanceTest')
                if instanceTestElement is not None:
                    self._readMeFirstUris.append(XmlUtil.descendantAttr(instanceTestElement, None, 'instanceDocument', '{http://www.w3.org/1999/xlink}href'))
                else:
                    schemaTestElement = XmlUtil.descendant(self, None, 'schemaTest')
                if schemaTestElement is not None:
                    self._readMeFirstUris.append(XmlUtil.descendantAttr(schemaTestElement, None, 'schemaDocument', '{http://www.w3.org/1999/xlink}href'))
            else:
                if self.localName == 'test-case':
                    inputFileElement = XmlUtil.descendant(self, None, 'input-file')
                    if inputFileElement is not None:
                        self._readMeFirstUris.append('TestSources/' + inputFileElement.text + '.xml')
                else:
                    if self.resultIsTaxonomyPackage:
                        self._readMeFirstUris.append(os.path.join(self.modelDocument.filepathdir, 'tests', self.get('name') + '.zip'))
                    else:
                        for anElement in self.iterdescendants():
                            if isinstance(anElement, ModelObject):
                                if anElement.get('readMeFirst') == 'true':
                                    if anElement.get('{http://www.w3.org/1999/xlink}href'):
                                        uri = anElement.get('{http://www.w3.org/1999/xlink}href')
                                    else:
                                        uri = XmlUtil.innerText(anElement)
                                    if anElement.get('name'):
                                        self._readMeFirstUris.append((ModelValue.qname(anElement, anElement.get('name')), uri))
                                    else:
                                        if anElement.get('dts'):
                                            self._readMeFirstUris.append((anElement.get('dts'), uri))
                                        else:
                                            self._readMeFirstUris.append(uri)

            if not self._readMeFirstUris:
                self._readMeFirstUris.append(os.path.join(self.modelXbrl.modelManager.cntlr.configDir, 'empty-instance.xml'))
            return self._readMeFirstUris

    @property
    def dataUris(self):
        try:
            return self._dataUris
        except AttributeError:
            self._dataUris = defaultdict(list)
            for dataElement in XmlUtil.descendants(self, None, ('data', 'input')):
                for elt in XmlUtil.descendants(dataElement, None, ('xsd', 'schema',
                                                                   'linkbase', 'instance')):
                    self._dataUris[('schema' if elt.localName == 'xsd' else elt.localName)].append(elt.textValue.strip())

            return self._dataUris

    @property
    def parameters(self):
        try:
            return self._parameters
        except AttributeError:
            self._parameters = dict([(ModelValue.qname(paramElt, paramElt.get('name')), (ModelValue.qname(paramElt, paramElt.get('datatype')), paramElt.get('value'))) for paramElt in XmlUtil.descendants(self, self.namespaceURI, 'parameter')])
            return self._parameters

    @property
    def resultIsVersioningReport(self):
        return XmlUtil.descendant(XmlUtil.descendant(self, None, 'result'), None, 'versioningReport') is not None

    @property
    def versioningReportUri(self):
        return XmlUtil.text(XmlUtil.descendant(self, None, 'versioningReport'))

    @property
    def resultIsXbrlInstance(self):
        return XmlUtil.descendant(XmlUtil.descendant(self, None, 'result'), None, 'instance') is not None

    @property
    def resultXbrlInstanceUri(self):
        for pluginXbrlMethod in pluginClassMethods('ModelTestcaseVariation.ResultXbrlInstanceUri'):
            resultInstanceUri = pluginXbrlMethod(self)
            if resultInstanceUri is not None:
                return resultInstanceUri or None

        resultInstance = XmlUtil.descendant(XmlUtil.descendant(self, None, 'result'), None, 'instance')
        if resultInstance is not None:
            return XmlUtil.text(resultInstance)

    @property
    def resultIsInfoset(self):
        if self.modelDocument.outpath:
            result = XmlUtil.descendant(self, None, 'result')
            if result is not None:
                return XmlUtil.child(result, None, 'file') is not None or XmlUtil.text(result).endswith('.xml')
        return False

    @property
    def resultInfosetUri(self):
        result = XmlUtil.descendant(self, None, 'result')
        if result is not None:
            child = XmlUtil.child(result, None, 'file')
            return os.path.join(self.modelDocument.outpath, XmlUtil.text(child if child is not None else result))

    @property
    def resultIsTable(self):
        result = XmlUtil.descendant(self, None, 'result')
        if result is not None:
            child = XmlUtil.child(result, None, 'table')
            if child is not None:
                if XmlUtil.text(child).endswith('.xml'):
                    return True
        return False

    @property
    def resultTableUri(self):
        result = XmlUtil.descendant(self, None, 'result')
        if result is not None:
            child = XmlUtil.child(result, None, 'table')
            if child is not None:
                return os.path.join(self.modelDocument.outpath, XmlUtil.text(child))

    @property
    def resultIsTaxonomyPackage(self):
        return any(e.localName for e in XmlUtil.descendants(self, None, TXMY_PKG_SRC_ELTS))

    @property
    def cfcnCall(self):
        try:
            return self._cfcnCall
        except AttributeError:
            self._cfcnCall = None
            if self.localName == 'test-case':
                queryElement = XmlUtil.descendant(self, None, 'query')
                if queryElement is not None:
                    filepath = self.modelDocument.filepathdir + '/' + 'Queries/XQuery/' + self.get('FilePath') + queryElement.get('name') + '.xq'
                    if os.sep != '/':
                        filepath = filepath.replace('/', os.sep)
                    with io.open(filepath, 'rt', encoding='utf-8') as (f):
                        self._cfcnCall = (
                         f.read(), self)
            else:
                for callElement in XmlUtil.descendants(self, XbrlConst.cfcn, 'call'):
                    self._cfcnCall = (
                     XmlUtil.innerText(callElement), callElement)
                    break

            if self._cfcnCall is None and self.namespaceURI == 'http://xbrl.org/2011/conformance-rendering/transforms':
                name = self.getparent().get('name')
                input = self.get('input')
                if name:
                    if input:
                        self._cfcnCall = (
                         "{0}('{1}')".format(name, input.replace("'", "''")), self)
            return self._cfcnCall

    @property
    def cfcnTest(self):
        try:
            return self._cfcnTest
        except AttributeError:
            self._cfcnTest = None
            if self.localName == 'test-case':
                outputFileElement = XmlUtil.descendant(self, None, 'output-file')
                if outputFileElement is not None:
                    if outputFileElement.get('compare') == 'Text':
                        filepath = self.modelDocument.filepathdir + '/' + 'ExpectedTestResults/' + self.get('FilePath') + outputFileElement.text
                        if os.sep != '/':
                            filepath = filepath.replace('/', os.sep)
                        with io.open(filepath, 'rt', encoding='utf-8') as (f):
                            self._cfcnTest = (
                             "xs:string($result) eq '{0}'".format(f.read()), self)
            else:
                testElement = XmlUtil.descendant(self, XbrlConst.cfcn, 'test')
                if testElement is not None:
                    self._cfcnTest = (
                     XmlUtil.innerText(testElement), testElement)
                else:
                    if self.namespaceURI == 'http://xbrl.org/2011/conformance-rendering/transforms':
                        output = self.get('output')
                        if output:
                            self._cfcnTest = (
                             "$result eq '{0}'".format(output.replace("'", "''")), self)
            return self._cfcnTest

    @property
    def expected(self):
        for pluginXbrlMethod in pluginClassMethods('ModelTestcaseVariation.ExpectedResult'):
            expected = pluginXbrlMethod(self)
            if expected:
                return expected

        if self.localName == 'testcase':
            return self.document.basename[:4]
        elif self.localName == 'testGroup':
            instanceTestElement = XmlUtil.descendant(self, None, 'instanceTest')
            if instanceTestElement is not None:
                return XmlUtil.descendantAttr(instanceTestElement, None, 'expected', 'validity')
            schemaTestElement = XmlUtil.descendant(self, None, 'schemaTest')
            if schemaTestElement is not None:
                return XmlUtil.descendantAttr(schemaTestElement, None, 'expected', 'validity')
            resultElement = XmlUtil.descendant(self, None, 'result')
            if resultElement is not None:
                expected = resultElement.get('expected')
                if expected:
                    if resultElement.get('nonStandardErrorCodes') == 'true':
                        return expected
        else:
            errorElement = XmlUtil.descendant(self, None, 'error')
            if errorElement is not None:
                _errorText = XmlUtil.text(errorElement)
                if ' ' in _errorText:
                    return _errorText
                else:
                    return ModelValue.qname(errorElement, _errorText)
            if resultElement is not None:
                if expected:
                    return expected
                for assertElement in XmlUtil.children(resultElement, None, 'assert'):
                    num = assertElement.get('num')
                    if num == '99999':
                        return assertElement.get('name')
                    if len(num) == 5:
                        return 'EFM.{0}.{1}.{2}'.format(num[0], num[1:3], num[3:6])

                asserTests = {}
                for atElt in XmlUtil.children(resultElement, None, 'assertionTests'):
                    try:
                        asserTests[atElt.get('assertionID')] = (
                         _INT(atElt.get('countSatisfied')), _INT(atElt.get('countNotSatisfied')))
                    except ValueError:
                        pass

                if asserTests:
                    return asserTests
            elif self.get('result'):
                return self.get('result')

    @property
    def expectedCount(self):
        for pluginXbrlMethod in pluginClassMethods('ModelTestcaseVariation.ExpectedCount'):
            _count = pluginXbrlMethod(self)
            if _count is not None:
                return _count

    @property
    def severityLevel(self):
        for pluginXbrlMethod in pluginClassMethods('ModelTestcaseVariation.ExpectedSeverity'):
            severityLevelName = pluginXbrlMethod(self)
            if severityLevelName:
                return logging._checkLevel(severityLevelName)

        if XmlUtil.descendant(self, None, 'assert', attrName='severity', attrValue='wrn') is not None or XmlUtil.descendant(self, None, 'result', attrName='severity', attrValue='warning') is not None:
            return logging._checkLevel('WARNING')
        else:
            return logging._checkLevel('INCONSISTENCY')

    @property
    def blockedMessageCodes(self):
        return XmlUtil.descendantAttr(self, None, 'results', 'blockedMessageCodes')

    @property
    def expectedVersioningReport(self):
        XmlUtil.text(XmlUtil.text(XmlUtil.descendant(XmlUtil.descendant(self, None, 'result'), None, 'versioningReport')))

    @property
    def propertyView(self):
        assertions = []
        for assertionElement in XmlUtil.descendants(self, None, 'assertionTests'):
            assertions.append(('assertion', assertionElement.get('assertionID')))
            assertions.append(('   satisfied', assertionElement.get('countSatisfied')))
            assertions.append(('   not sat.', assertionElement.get('countNotSatisfied')))

        readMeFirsts = [('readFirst', readMeFirstUri) for readMeFirstUri in self.readMeFirstUris]
        parameters = []
        if len(self.parameters) > 0:
            parameters.append(('parameters', None))
        for pName, pTypeValue in self.parameters.items():
            parameters.append((pName, pTypeValue[1]))

        return [
         (
          'id', self.id), ('name', self.name), ('description', self.description)] + readMeFirsts + parameters + [('status', self.status), ('call', self.cfcnCall[0]) if self.cfcnCall else (), ('test', self.cfcnTest[0]) if self.cfcnTest else (), ('infoset', self.resultInfosetUri) if self.resultIsInfoset else (), ('expected', self.expected) if self.expected else (), ('actual', ' '.join(str(i) for i in self.actual) if len(self.actual) > 0 else ())] + assertions

    def __repr__(self):
        return 'modelTestcaseVariation[{0}]{1})'.format(self.objectId(), self.propertyView)