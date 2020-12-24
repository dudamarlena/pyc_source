# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\minixsv\pyxsval.py
# Compiled at: 2008-08-08 10:45:46
__all__ = [
 'addUserSpecXmlIfClass', 'parseAndValidate', 'parseAndValidateString', 'parseAndValidateXmlInput', 'parseAndValidateXmlInputString', 'parseAndValidateXmlSchema', 'parseAndValidateXmlSchemaString', 'XsValidator']
import string, genxmlif
from minixsv import *
from xsvalErrorHandler import ErrorHandler
from xsvalXmlIf import XsvXmlElementWrapper
from xsvalBase import XsValBase
from xsvalSchema import XsValSchema
__author__ = 'Roland Leuthe <roland@leuthe-net.de>'
__date__ = '08. August 2008'
__version__ = '0.9.0'
_XS_VAL_DEFAULT_ERROR_LIMIT = 20
rulesTreeWrapper = None

def getVersion():
    return __version__


def addUserSpecXmlIfClass(xmlIfKey, factory):
    if not _xmlIfDict.has_key(xmlIfKey):
        _xmlIfDict[xmlIfKey] = factory
    else:
        raise KeyError, 'xmlIfKey %s already implemented!' % xmlIfKey


def parseAndValidate(inputFile, xsdFile=None, **kw):
    return parseAndValidateXmlInput(inputFile, xsdFile, 1, **kw)


def parseAndValidateString(inputText, xsdText=None, **kw):
    return parseAndValidateXmlInputString(inputText, xsdText, 1, **kw)


def parseAndValidateXmlInput(inputFile, xsdFile=None, validateSchema=0, **kw):
    xsValidator = XsValidator(**kw)
    inputTreeWrapper = xsValidator.parse(inputFile)
    return xsValidator.validateXmlInput(inputFile, inputTreeWrapper, xsdFile, validateSchema)


def parseAndValidateXmlInputString(inputText, xsdText=None, baseUrl='', validateSchema=0, **kw):
    xsValidator = XsValidator(**kw)
    inputTreeWrapper = xsValidator.parseString(inputText, baseUrl)
    return xsValidator.validateXmlInputString(inputTreeWrapper, xsdText, validateSchema)


def parseAndValidateXmlSchema(xsdFile, **kw):
    xsValidator = XsValidator(**kw)
    xsdTreeWrapper = xsValidator.parse(xsdFile)
    return xsValidator.validateXmlSchema(xsdFile, xsdTreeWrapper)


def parseAndValidateXmlSchemaString(xsdText, **kw):
    xsValidator = XsValidator(**kw)
    xsdTreeWrapper = xsValidator.parseString(xsdText)
    return xsValidator.validateXmlSchema('', xsdTreeWrapper)


class XsValidator:
    __module__ = __name__

    def __init__(self, xmlIfClass=XMLIF_MINIDOM, elementWrapperClass=XsvXmlElementWrapper, warningProc=IGNORE_WARNINGS, errorLimit=_XS_VAL_DEFAULT_ERROR_LIMIT, verbose=0, useCaching=1, processXInclude=1):
        self.warningProc = warningProc
        self.errorLimit = errorLimit
        self.verbose = verbose
        self.xmlIf = _xmlIfDict[xmlIfClass](verbose, useCaching, processXInclude)
        self.xmlIf.setElementWrapperClass(elementWrapperClass)
        self.errorHandler = ErrorHandler(errorLimit, warningProc, verbose)
        self.schemaDependancyList = []

    def getVersion(self):
        return __version__

    def parse(self, file, baseUrl='', ownerDoc=None):
        self._verbosePrint('Parsing %s...' % file)
        return self.xmlIf.parse(file, baseUrl, ownerDoc)

    def parseString(self, text, baseUrl=''):
        self._verbosePrint('Parsing XML text string...')
        return self.xmlIf.parseString(text, baseUrl)

    def validateXmlInput(self, xmlInputFile, inputTreeWrapper, xsdFile=None, validateSchema=0):
        xsdTreeWrapperList = self._readReferencedXsdFiles(inputTreeWrapper, validateSchema)
        if xsdTreeWrapperList == []:
            if xsdFile != None:
                xsdTreeWrapper = self.parse(xsdFile)
                xsdTreeWrapperList.append(xsdTreeWrapper)
                if validateSchema:
                    self.validateXmlSchema(xsdFile, xsdTreeWrapper)
            else:
                self.errorHandler.raiseError('No schema file specified!')
        self._validateXmlInput(xmlInputFile, inputTreeWrapper, xsdTreeWrapperList)
        for xsdTreeWrapper in xsdTreeWrapperList:
            xsdTreeWrapper.unlink()

        return inputTreeWrapper

    def validateXmlInputString(self, inputTreeWrapper, xsdText=None, validateSchema=0):
        xsdTreeWrapperList = self._readReferencedXsdFiles(inputTreeWrapper, validateSchema)
        if xsdTreeWrapperList == []:
            if xsdText != None:
                xsdFile = 'schema text'
                xsdTreeWrapper = self.parseString(xsdText)
                xsdTreeWrapperList.append(xsdTreeWrapper)
                if validateSchema:
                    self.validateXmlSchema(xsdFile, xsdTreeWrapper)
            else:
                self.errorHandler.raiseError('No schema specified!')
        self._validateXmlInput('input text', inputTreeWrapper, xsdTreeWrapperList)
        for xsdTreeWrapper in xsdTreeWrapperList:
            xsdTreeWrapper.unlink()

        return inputTreeWrapper

    def validateXmlSchema(self, xsdFile, xsdTreeWrapper):
        global rulesTreeWrapper
        if rulesTreeWrapper == None:
            rulesTreeWrapper = self.parse(os.path.join(MINIXSV_DIR, 'XMLSchema.xsd'))
        self._verbosePrint('Validating %s...' % xsdFile)
        xsvGivenXsdFile = XsValSchema(self.xmlIf, self.errorHandler, self.verbose)
        xsvGivenXsdFile.validate(xsdTreeWrapper, [rulesTreeWrapper])
        self.schemaDependancyList.append(xsdFile)
        self.schemaDependancyList.extend(xsvGivenXsdFile.xsdIncludeDict.keys())
        xsvGivenXsdFile.unlink()
        self.errorHandler.flushOutput()
        return xsdTreeWrapper

    def _validateXmlInput(self, xmlInputFile, inputTreeWrapper, xsdTreeWrapperList):
        self._verbosePrint('Validating %s...' % xmlInputFile)
        xsvInputFile = XsValBase(self.xmlIf, self.errorHandler, self.verbose)
        xsvInputFile.validate(inputTreeWrapper, xsdTreeWrapperList)
        xsvInputFile.unlink()
        self.errorHandler.flushOutput()

    def _readReferencedXsdFiles(self, inputTreeWrapper, validateSchema):
        xsdTreeWrapperList = []
        xsdFileList = self._retrieveReferencedXsdFiles(inputTreeWrapper)
        for (namespace, xsdFile) in xsdFileList:
            try:
                xsdTreeWrapper = self.parse(xsdFile, inputTreeWrapper.getRootNode().getAbsUrl())
            except IOError, e:
                if e.errno == 2:
                    self.errorHandler.raiseError('XML schema file %s not found!' % xsdFile, inputTreeWrapper.getRootNode())
                else:
                    raise IOError(e.errno, e.strerror, e.filename)

            xsdTreeWrapperList.append(xsdTreeWrapper)
            if validateSchema:
                self.validateXmlSchema(xsdFile, xsdTreeWrapper)
            if namespace != xsdTreeWrapper.getRootNode().getAttributeOrDefault('targetNamespace', None):
                self.errorHandler.raiseError("Namespace of 'schemaLocation' attribute doesn't match target namespace of %s!" % xsdFile, inputTreeWrapper.getRootNode())

        return xsdTreeWrapperList

    def _retrieveReferencedXsdFiles(self, inputTreeWrapper):
        inputRootNode = inputTreeWrapper.getRootNode()
        xsdFileList = []
        if inputRootNode.hasAttribute((XSI_NAMESPACE, 'schemaLocation')):
            attributeValue = inputRootNode.getAttribute((XSI_NAMESPACE, 'schemaLocation'))
            attrValList = string.split(attributeValue)
            if len(attrValList) % 2 == 0:
                for i in range(0, len(attrValList), 2):
                    xsdFileList.append((attrValList[i], attrValList[(i + 1)]))

            else:
                self.errorHandler.raiseError("'schemaLocation' attribute must have even number of URIs (pairs of namespace and xsdFile)!")
        if inputRootNode.hasAttribute((XSI_NAMESPACE, 'noNamespaceSchemaLocation')):
            attributeValue = inputRootNode.getAttribute((XSI_NAMESPACE, 'noNamespaceSchemaLocation'))
            attrValList = string.split(attributeValue)
            for attrVal in attrValList:
                xsdFileList.append((None, attrVal))

        return xsdFileList

    def _verbosePrint(self, text):
        if self.verbose:
            print text


def _interfaceFactoryMinidom(verbose, useCaching, processXInclude):
    return genxmlif.chooseXmlIf(genxmlif.XMLIF_MINIDOM, verbose, useCaching, processXInclude)


def _interfaceFactory4Dom(verbose, useCaching, processXInclude):
    return genxmlif.chooseXmlIf(genxmlif.XMLIF_4DOM, verbose, useCaching, processXInclude)


def _interfaceFactoryElementTree(verbose, useCaching, processXInclude):
    return genxmlif.chooseXmlIf(genxmlif.XMLIF_ELEMENTTREE, verbose, useCaching, processXInclude)


_xmlIfDict = {XMLIF_MINIDOM: _interfaceFactoryMinidom, XMLIF_4DOM: _interfaceFactory4Dom, XMLIF_ELEMENTTREE: _interfaceFactoryElementTree}