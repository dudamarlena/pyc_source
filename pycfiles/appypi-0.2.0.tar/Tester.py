# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/appy/pod/test/Tester.py
# Compiled at: 2009-09-30 05:37:25
import os, os.path, sys, zipfile, re, shutil, appy.shared.test
from appy.shared.test import TesterError
from appy.shared.utils import FolderDeleter
from appy.pod.odf_parser import OdfEnvironment, OdfParser
from appy.pod.renderer import Renderer
from appy.pod import XML_SPECIAL_CHARS
TEMPLATE_NOT_FOUND = 'Template file "%s" was not found.'
CONTEXT_NOT_FOUND = 'Context file "%s" was not found.'
EXPECTED_RESULT_NOT_FOUND = 'Expected result "%s" was not found.'

class AnnotationsRemover(OdfParser):
    """This parser is used to remove from content.xml and styles.xml the
       Python tracebacks that may be dumped into OpenDocument annotations by
       pod when generating errors. Indeed, those tracebacks contain lot of
       machine-specific info, like absolute paths to the python files, etc."""
    __module__ = __name__

    def __init__(self, env, caller):
        OdfParser.__init__(self, env, caller)
        self.res = ''
        self.inAnnotation = False
        self.textEncountered = False
        self.ignore = False

    def startElement(self, elem, attrs):
        e = OdfParser.startElement(self, elem, attrs)
        if elem == '%s:annotation' % e.ns(e.NS_OFFICE):
            self.inAnnotation = True
            self.textEncountered = False
        elif elem == '%s:p' % e.ns(e.NS_TEXT):
            if self.inAnnotation:
                if not self.textEncountered:
                    self.textEncountered = True
                else:
                    self.ignore = True
        if not self.ignore:
            self.res += '<%s' % elem
            for (attrName, attrValue) in attrs.items():
                self.res += ' %s="%s"' % (attrName, attrValue)

            self.res += '>'

    def endElement(self, elem):
        e = OdfParser.endElement(self, elem)
        if elem == '%s:annotation' % e.ns(e.NS_OFFICE):
            self.inAnnotation = False
            self.ignore = False
        if not self.ignore:
            self.res += '</%s>' % elem

    def characters(self, content):
        e = OdfParser.characters(self, content)
        if not self.ignore:
            for c in content:
                if XML_SPECIAL_CHARS.has_key(c):
                    self.res += XML_SPECIAL_CHARS[c]
                else:
                    self.res += c

    def getResult(self):
        return self.res


class Test(appy.shared.test.Test):
    """Abstract test class."""
    __module__ = __name__
    interestingOdtContent = ('content.xml', 'styles.xml')

    def __init__(self, testData, testDescription, testFolder, config, flavour):
        appy.shared.test.Test.__init__(self, testData, testDescription, testFolder, config, flavour)
        self.templatesFolder = os.path.join(self.testFolder, 'templates')
        self.contextsFolder = os.path.join(self.testFolder, 'contexts')
        self.resultsFolder = os.path.join(self.testFolder, 'results')
        self.result = None
        return

    def getContext(self, contextName):
        """Gets the objects that are in the context."""
        contextPy = os.path.join(self.contextsFolder, contextName + '.py')
        if not os.path.exists(contextPy):
            raise TesterError(CONTEXT_NOT_FOUND % contextPy)
        contextPkg = 'appy.pod.test.contexts.%s' % contextName
        exec 'import %s' % contextPkg
        exec 'context = dir(%s)' % contextPkg
        res = {}
        for elem in context:
            if not elem.startswith('__'):
                exec 'res[elem] = %s.%s' % (contextPkg, elem)

        return res

    def do(self):
        self.result = os.path.join(self.tempFolder, '%s.%s' % (self.data['Name'], self.data['Result']))
        template = os.path.join(self.templatesFolder, self.data['Template'] + '.odt')
        if not os.path.exists(template):
            raise TesterError(TEMPLATE_NOT_FOUND % template)
        context = self.getContext(self.data['Context'])
        ooPort = self.data['OpenOfficePort']
        pythonWithUno = self.config['pythonWithUnoPath']
        stylesMapping = eval('{' + self.data['StylesMapping'] + '}')
        Renderer(template, context, self.result, ooPort=ooPort, pythonWithUnoPath=pythonWithUno, stylesMapping=stylesMapping).run()

    def getOdtContent(self, odtFile):
        """Creates in the temp folder content.xml and styles.xml extracted
           from p_odtFile."""
        contentXml = None
        stylesXml = None
        if odtFile == self.result:
            filePrefix = 'actual'
        else:
            filePrefix = 'expected'
        zipFile = zipfile.ZipFile(odtFile)
        for zippedFile in zipFile.namelist():
            if zippedFile in self.interestingOdtContent:
                f = file(os.path.join(self.tempFolder, '%s.%s' % (filePrefix, zippedFile)), 'wb')
                fileContent = zipFile.read(zippedFile)
                if zippedFile == 'content.xml':
                    annotationsRemover = AnnotationsRemover(OdfEnvironment(), self)
                    annotationsRemover.parse(fileContent)
                    fileContent = annotationsRemover.getResult()
                f.write(fileContent.encode('utf-8'))
                f.close()

        zipFile.close()
        return

    def checkResult(self):
        """r_ is False if the test succeeded."""
        res = False
        self.getOdtContent(self.result)
        expectedResult = os.path.join(self.resultsFolder, self.data['Name'] + '.odt')
        if not os.path.exists(expectedResult):
            raise TesterError(EXPECTED_RESULT_NOT_FOUND % expectedResult)
        self.getOdtContent(expectedResult)
        for fileName in self.interestingOdtContent:
            diffOccurred = self.compareFiles(os.path.join(self.tempFolder, 'actual.%s' % fileName), os.path.join(self.tempFolder, 'expected.%s' % fileName), areXml=True, xmlTagsToIgnore=((OdfEnvironment.NS_DC, 'date'), (OdfEnvironment.NS_STYLE, 'style')), xmlAttrsToIgnore=('draw:name',
                                                                                                                                                                                                                                                                                  'text:name'), encoding='utf-8')
            if diffOccurred:
                res = True
                break

        return res


class NominalTest(Test):
    """Tests an application model."""
    __module__ = __name__

    def __init__(self, testData, testDescription, testFolder, config, flavour):
        Test.__init__(self, testData, testDescription, testFolder, config, flavour)


class ErrorTest(Test):
    """Tests an application model."""
    __module__ = __name__

    def __init__(self, testData, testDescription, testFolder, config, flavour):
        Test.__init__(self, testData, testDescription, testFolder, config, flavour)

    def onError(self):
        """Compares the error that occurred with the expected error."""
        Test.onError(self)
        return not self.isExpectedError(self.data['Message'])


class PodTestFactory(appy.shared.test.TestFactory):
    __module__ = __name__

    def createTest(testData, testDescription, testFolder, config, flavour):
        if testData.table.instanceOf('ErrorTest'):
            test = ErrorTest(testData, testDescription, testFolder, config, flavour)
        else:
            test = NominalTest(testData, testDescription, testFolder, config, flavour)
        return test

    createTest = staticmethod(createTest)


class PodTester(appy.shared.test.Tester):
    __module__ = __name__

    def __init__(self, testPlan):
        appy.shared.test.Tester.__init__(self, testPlan, [], PodTestFactory)


if __name__ == '__main__':
    PodTester('Tests.rtf').run()