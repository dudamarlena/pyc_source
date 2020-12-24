# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\ProgramData\envs\Test\lib\arelle\ModelDocument.py
# Compiled at: 2018-03-15 09:07:18
# Size of source mod 2**32: 100981 bytes
__doc__ = '\nCreated on Oct 3, 2010\n\n@author: Mark V Systems Limited\n(c) Copyright 2010 Mark V Systems Limited, All rights reserved.\n'
import os, io, sys, traceback
from collections import defaultdict
from decimal import Decimal
from lxml import etree
from xml.sax import SAXParseException
from arelle import PackageManager, XbrlConst, XmlUtil, UrlUtil, ValidateFilingText, XhtmlValidate, XmlValidateSchema
from arelle.ModelObject import ModelObject, ModelComment
from arelle.ModelValue import qname
from arelle.ModelDtsObject import ModelLink, ModelResource, ModelRelationship
from arelle.ModelInstanceObject import ModelFact, ModelInlineFact
from arelle.ModelObjectFactory import parser
from arelle.PrototypeDtsObject import LinkPrototype, LocPrototype, ArcPrototype, DocumentPrototype
from arelle.PluginManager import pluginClassMethods
from arelle.PythonUtil import OrderedDefaultDict, Fraction, normalizeSpace
from arelle.XhtmlValidate import ixMsgCode
from arelle.XmlValidate import VALID, validate as xmlValidate
creationSoftwareNames = None

def load(modelXbrl, uri, base=None, referringElement=None, isEntry=False, isDiscovered=False, isIncluded=None, namespace=None, reloadCache=False, **kwargs):
    """Returns a new modelDocument, performing DTS discovery for instance, inline XBRL, schema, 
    linkbase, and versioning report entry urls.
    
    :param uri: Identification of file to load by string filename or by a FileSource object with a selected content file.
    :type uri: str or FileSource
    :param referringElement: Source element causing discovery or loading of this document, such as an import or xlink:href
    :type referringElement: ModelObject
    :param isEntry: True for an entry document
    :type isEntry: bool
    :param isDiscovered: True if this document is discovered by XBRL rules, otherwise False (such as when schemaLocation and xmlns were the cause of loading the schema)
    :type isDiscovered: bool
    :param isIncluded: True if this document is the target of an xs:include
    :type isIncluded: bool
    :param namespace: The schema namespace of this document, if known and applicable
    :type isSupplemental: True if this document is supplemental (not discovered or in DTS but adds labels or instance facts)
    :type namespace: str
    :param reloadCache: True if desired to reload the web cache for any web-referenced files.
    :type reloadCache: bool
    :param checkModifiedTime: True if desired to check modifed time of web cached entry point (ahead of usual time stamp checks).
    :type checkModifiedTime: bool
    """
    if referringElement is None:
        referringElement = modelXbrl
    else:
        normalizedUri = modelXbrl.modelManager.cntlr.webCache.normalizeUrl(uri, base)
        modelDocument = modelXbrl.urlDocs.get(normalizedUri)
        if modelDocument:
            return modelDocument
        if modelXbrl.urlUnloadableDocs.get(normalizedUri):
            return
        if isEntry:
            modelXbrl.entryLoadingUrl = normalizedUri
            modelXbrl.uri = normalizedUri
            modelXbrl.uriDir = os.path.dirname(normalizedUri)
            for i in range(modelXbrl.modelManager.disclosureSystem.maxSubmissionSubdirectoryEntryNesting):
                modelXbrl.uriDir = os.path.dirname(modelXbrl.uriDir)

        if modelXbrl.modelManager.validateDisclosureSystem and not normalizedUri.startswith(modelXbrl.uriDir) and not modelXbrl.modelManager.disclosureSystem.hrefValid(normalizedUri):
            blocked = modelXbrl.modelManager.disclosureSystem.blockDisallowedReferences
            if normalizedUri not in modelXbrl.urlUnloadableDocs:
                modelXbrl.error(('EFM.6.22.02', 'GFM.1.1.3', 'SBR.NL.2.1.0.06' if normalizedUri.startswith('http') else 'SBR.NL.2.2.0.17'), (_('Prohibited file for filings %(blockedIndicator)s: %(url)s')),
                  modelObject=referringElement,
                  url=normalizedUri,
                  blockedIndicator=(_(' blocked') if blocked else ''),
                  messageCodes=('EFM.6.22.02', 'GFM.1.1.3', 'SBR.NL.2.1.0.06', 'SBR.NL.2.2.0.17'))
                modelXbrl.urlUnloadableDocs[normalizedUri] = blocked
            if blocked:
                return
        if modelXbrl.modelManager.skipLoading:
            if modelXbrl.modelManager.skipLoading.match(normalizedUri):
                return
        if modelXbrl.fileSource.isMappedUrl(normalizedUri):
            mappedUri = modelXbrl.fileSource.mappedUrl(normalizedUri)
        else:
            if PackageManager.isMappedUrl(normalizedUri):
                mappedUri = PackageManager.mappedUrl(normalizedUri)
            else:
                mappedUri = modelXbrl.modelManager.disclosureSystem.mappedUrl(normalizedUri)
        if isEntry:
            modelXbrl.entryLoadingUrl = mappedUri
        if modelXbrl.fileSource.isInArchive(mappedUri):
            filepath = mappedUri
        else:
            filepath = modelXbrl.modelManager.cntlr.webCache.getfilename(mappedUri, reload=reloadCache, checkModifiedTime=(kwargs.get('checkModifiedTime', False)))
        if filepath:
            uri = modelXbrl.modelManager.cntlr.webCache.normalizeUrl(filepath)
        if filepath is None:
            if modelXbrl.modelManager.abortOnMajorError:
                if isEntry or isDiscovered:
                    modelXbrl.error('FileNotLoadable', (_('File can not be loaded: %(fileName)s \nLoading terminated.')),
                      modelObject=referringElement,
                      fileName=mappedUri)
                    raise LoadingException()
            if normalizedUri not in modelXbrl.urlUnloadableDocs:
                if 'referringElementUrl' in kwargs:
                    modelXbrl.error('FileNotLoadable', (_('File can not be loaded: %(fileName)s, referenced from %(referencingFileName)s')),
                      modelObject=referringElement,
                      fileName=normalizedUri,
                      referencingFileName=(kwargs['referringElementUrl']))
                else:
                    modelXbrl.error('FileNotLoadable', (_('File can not be loaded: %(fileName)s')),
                      modelObject=referringElement,
                      fileName=normalizedUri)
                modelXbrl.urlUnloadableDocs[normalizedUri] = True
            return
    isPullLoadable = any(pluginMethod(modelXbrl, mappedUri, normalizedUri, filepath, isEntry=isEntry, namespace=namespace, **kwargs) for pluginMethod in pluginClassMethods('ModelDocument.IsPullLoadable'))
    if not isPullLoadable and os.path.splitext(filepath)[1] in ('.xlsx', '.xls', '.csv',
                                                                '.json'):
        modelXbrl.error('FileNotLoadable', (_('File can not be loaded, requires loadFromExcel or loadFromOIM plug-in: %(fileName)s')),
          modelObject=referringElement,
          fileName=normalizedUri)
        return
    else:
        modelXbrl.modelManager.showStatus(_('parsing {0}').format(uri))
        file = None
        try:
            for pluginMethod in pluginClassMethods('ModelDocument.PullLoader'):
                modelDocument = pluginMethod(modelXbrl, normalizedUri, filepath, isEntry=isEntry, namespace=namespace, **kwargs)
                if isinstance(modelDocument, Exception):
                    return
                if modelDocument is not None:
                    return modelDocument

            if modelXbrl.modelManager.validateDisclosureSystem:
                if modelXbrl.modelManager.disclosureSystem.validateFileText:
                    if normalizedUri not in modelXbrl.modelManager.disclosureSystem.standardTaxonomiesDict:
                        file, _encoding = ValidateFilingText.checkfile(modelXbrl, filepath)
            else:
                file, _encoding = modelXbrl.fileSource.file(filepath, stripDeclaration=True)
            xmlDocument = None
            isPluginParserDocument = False
            for pluginMethod in pluginClassMethods('ModelDocument.CustomLoader'):
                modelDocument = pluginMethod(modelXbrl, file, mappedUri, filepath)
                if modelDocument is not None:
                    file.close()
                    return modelDocument

            _parser, _parserLookupName, _parserLookupClass = parser(modelXbrl, filepath)
            xmlDocument = etree.parse(file, parser=_parser, base_url=filepath)
            for error in _parser.error_log:
                modelXbrl.error('xmlSchema:syntax', (_('%(error)s, %(fileName)s, line %(line)s, column %(column)s, %(sourceAction)s source element')),
                  modelObject=referringElement,
                  fileName=(os.path.basename(uri)),
                  error=(error.message),
                  line=(error.line),
                  column=(error.column),
                  sourceAction=('including' if isIncluded else 'importing'))

            file.close()
        except (EnvironmentError, KeyError) as err:
            if file:
                file.close()
            else:
                if not isIncluded:
                    if namespace:
                        if namespace in XbrlConst.standardNamespaceSchemaLocations:
                            if uri != XbrlConst.standardNamespaceSchemaLocations[namespace]:
                                return load(modelXbrl, XbrlConst.standardNamespaceSchemaLocations[namespace], base, referringElement, isEntry, isDiscovered, isIncluded, namespace, reloadCache)
                if modelXbrl.modelManager.abortOnMajorError:
                    if isEntry or isDiscovered:
                        modelXbrl.error('IOerror', (_('%(fileName)s: file error: %(error)s \nLoading terminated.')),
                          modelObject=referringElement,
                          fileName=(os.path.basename(uri)),
                          error=(str(err)))
                        raise LoadingException()
            modelXbrl.error('IOerror', (_('%(fileName)s: file error: %(error)s')),
              modelObject=referringElement,
              fileName=(os.path.basename(uri)),
              error=(str(err)))
            modelXbrl.urlUnloadableDocs[normalizedUri] = True
            return
        except (etree.LxmlError, etree.XMLSyntaxError,
         SAXParseException,
         ValueError) as err:
            if file:
                file.close()
            if not isEntry:
                if str(err) == "Start tag expected, '<' not found, line 1, column 1":
                    return ModelDocument(modelXbrl, Type.UnknownNonXML, normalizedUri, filepath, None)
            modelXbrl.error('xmlSchema:syntax', (_('Unrecoverable error: %(error)s, %(fileName)s, %(sourceAction)s source element')),
              modelObject=referringElement,
              fileName=(os.path.basename(uri)),
              error=(str(err)),
              sourceAction=('including' if isIncluded else 'importing'),
              exc_info=True)
            modelXbrl.urlUnloadableDocs[normalizedUri] = True
            return
        except Exception as err:
            modelXbrl.error((type(err).__name__), (_('Unrecoverable error: %(error)s, %(fileName)s, %(sourceAction)s source element')),
              modelObject=referringElement,
              fileName=(os.path.basename(uri)),
              error=(str(err)),
              sourceAction=('including' if isIncluded else 'importing'),
              exc_info=True)
            modelXbrl.urlUnloadableDocs[normalizedUri] = True
            return

        modelXbrl.modelManager.showStatus(_('loading {0}').format(uri))
        modelDocument = None
        rootNode = xmlDocument.getroot()
        if rootNode is not None:
            ln = rootNode.localName
            ns = rootNode.namespaceURI
            _type = None
            _class = ModelDocument
            if ns == XbrlConst.xsd and ln == 'schema':
                _type = Type.SCHEMA
                if not isEntry and not isIncluded:
                    targetNamespace = rootNode.get('targetNamespace')
                    if targetNamespace:
                        if modelXbrl.namespaceDocs.get(targetNamespace):
                            otherModelDoc = modelXbrl.namespaceDocs[targetNamespace][0]
                            if otherModelDoc.basename == os.path.basename(uri):
                                if os.path.normpath(otherModelDoc.uri) != os.path.normpath(uri):
                                    modelXbrl.urlDocs[uri] = otherModelDoc
                                    modelXbrl.warning('info:duplicatedSchema', (_('Schema file with same targetNamespace %(targetNamespace)s loaded from %(fileName)s and %(otherFileName)s')),
                                      modelObject=referringElement,
                                      targetNamespace=targetNamespace,
                                      fileName=uri,
                                      otherFileName=(otherModelDoc.uri))
                                return otherModelDoc
            else:
                if isEntry or isDiscovered or kwargs.get('isSupplemental', False):
                    if ns == XbrlConst.link:
                        if ln == 'linkbase':
                            _type = Type.LINKBASE
                        else:
                            if ln == 'xbrl':
                                _type = Type.INSTANCE
                            else:
                                _type = Type.UnknownXML
            if isEntry:
                if ns == XbrlConst.xbrli:
                    if ln == 'xbrl':
                        _type = Type.INSTANCE
                    else:
                        _type = Type.UnknownXML
            if ns == XbrlConst.xhtml and (ln == 'html' or ln == 'xhtml'):
                _type = Type.UnknownXML
                if XbrlConst.ixbrlAll.intersection(rootNode.nsmap.values()):
                    _type = Type.INLINEXBRL
            else:
                if ln == 'report':
                    if ns == XbrlConst.ver:
                        _type = Type.VERSIONINGREPORT
                        from arelle.ModelVersReport import ModelVersReport
                        _class = ModelVersReport
            if ln in ('testcases', 'documentation', 'testSuite'):
                _type = Type.TESTCASESINDEX
            else:
                if ln in ('testcase', 'testSet'):
                    _type = Type.TESTCASE
                elif ln == 'registry' and ns == XbrlConst.registry:
                    _type = Type.REGISTRY
                elif ln == 'test-suite' and ns == 'http://www.w3.org/2005/02/query-test-XQTSCatalog':
                    _type = Type.XPATHTESTSUITE
                else:
                    if ln == 'rss':
                        _type = Type.RSSFEED
                        from arelle.ModelRssObject import ModelRssObject
                        _class = ModelRssObject
                    else:
                        if ln == 'ptvl':
                            _type = Type.ARCSINFOSET
                        else:
                            if ln == 'facts':
                                _type = Type.FACTDIMSINFOSET
                            else:
                                if XbrlConst.ixbrlAll.intersection(rootNode.nsmap.values()):
                                    _type = Type.INLINEXBRL
                                else:
                                    for pluginMethod in pluginClassMethods('ModelDocument.IdentifyType'):
                                        _identifiedType = pluginMethod(modelXbrl, rootNode, filepath)
                                        if _identifiedType is not None:
                                            _type, _class, rootNode = _identifiedType
                                            break

            if _type is None:
                _type = Type.UnknownXML
                nestedInline = None
                for htmlElt in rootNode.iter(tag='{http://www.w3.org/1999/xhtml}html'):
                    nestedInline = htmlElt
                    break

                if nestedInline is None:
                    for htmlElt in rootNode.iter(tag='{http://www.w3.org/1999/xhtml}xhtml'):
                        nestedInline = htmlElt
                        break

                if nestedInline is not None:
                    if XbrlConst.ixbrlAll.intersection(nestedInline.nsmap.values()):
                        _type = Type.INLINEXBRL
                        rootNode = nestedInline
            modelDocument = _class(modelXbrl, _type, normalizedUri, filepath, xmlDocument)
            rootNode.init(modelDocument)
            modelDocument.parser = _parser
            modelDocument.parserLookupName = _parserLookupName
            modelDocument.parserLookupClass = _parserLookupClass
            modelDocument.xmlRootElement = rootNode
            modelDocument.schemaLocationElements.add(rootNode)
            modelDocument.documentEncoding = _encoding
            if isEntry or isDiscovered:
                modelDocument.inDTS = True
            if any(pluginMethod(modelDocument) for pluginMethod in pluginClassMethods('ModelDocument.Discover')):
                pass
            else:
                if _type == Type.SCHEMA:
                    modelDocument.schemaDiscover(rootNode, isIncluded, namespace)
                else:
                    if _type == Type.LINKBASE:
                        modelDocument.linkbaseDiscover(rootNode)
                    else:
                        if _type == Type.INSTANCE:
                            modelDocument.instanceDiscover(rootNode)
                        else:
                            if _type == Type.INLINEXBRL:
                                modelDocument.inlineXbrlDiscover(rootNode)
                            else:
                                if _type == Type.VERSIONINGREPORT:
                                    modelDocument.versioningReportDiscover(rootNode)
                                else:
                                    if _type == Type.TESTCASESINDEX:
                                        modelDocument.testcasesIndexDiscover(xmlDocument)
                                    else:
                                        if _type == Type.TESTCASE:
                                            modelDocument.testcaseDiscover(rootNode)
                                        else:
                                            if _type == Type.REGISTRY:
                                                modelDocument.registryDiscover(rootNode)
                                            else:
                                                if _type == Type.XPATHTESTSUITE:
                                                    modelDocument.xPathTestSuiteDiscover(rootNode)
                                                else:
                                                    if _type == Type.VERSIONINGREPORT:
                                                        modelDocument.versioningReportDiscover(rootNode)
                                                    else:
                                                        if _type == Type.RSSFEED:
                                                            modelDocument.rssFeedDiscover(rootNode)
                    if isEntry:
                        for pi in modelDocument.processingInstructions:
                            if pi.target == 'arelle-unit-test':
                                modelXbrl.arelleUnitTests[pi.get('location')] = pi.get('action')

                        while modelXbrl.schemaDocsToValidate:
                            doc = modelXbrl.schemaDocsToValidate.pop()
                            XmlValidateSchema.validate(doc, doc.xmlRootElement, doc.targetNamespace)

                        if hasattr(modelXbrl, 'ixdsHtmlElements'):
                            inlineIxdsDiscover(modelXbrl, modelDocument)
                    if isEntry or kwargs.get('isSupplemental', False):
                        modelXbrl.baseSets = OrderedDefaultDict(modelXbrl.baseSets.default_factory, sorted((modelXbrl.baseSets.items()), key=(lambda i: (i[0][0] or '', i[0][1] or ''))))
        return modelDocument


def loadSchemalocatedSchema(modelXbrl, element, relativeUrl, namespace, baseUrl):
    if namespace == XbrlConst.xhtml:
        return
    else:
        importSchemaLocation = modelXbrl.modelManager.cntlr.webCache.normalizeUrl(relativeUrl, baseUrl)
        doc = load(modelXbrl, importSchemaLocation, isIncluded=False, isDiscovered=False, namespace=namespace, referringElement=element, referringElementUrl=baseUrl)
        if doc:
            if doc.targetNamespace != namespace:
                modelXbrl.error('xmlSchema1.4.2.3:refSchemaNamespace', (_('SchemaLocation of %(fileName)s expected namespace %(namespace)s found targetNamespace %(targetNamespace)s')),
                  modelObject=element,
                  fileName=baseUrl,
                  namespace=namespace,
                  targetNamespace=(doc.targetNamespace))
            else:
                doc.inDTS = False
        return doc


def create(modelXbrl, type, uri, schemaRefs=None, isEntry=False, initialXml=None, initialComment=None, base=None, discover=True, documentEncoding='utf-8'):
    """Returns a new modelDocument, created from scratch, with any necessary header elements 
    
    (such as the schema, instance, or RSS feed top level elements)
    :param type: type of model document (value of ModelDocument.Types, an integer)
    :type type: Types
    :param schemaRefs: list of URLs when creating an empty INSTANCE, to use to discover (load) the needed DTS modelDocument objects.
    :type schemaRefs: [str]
    :param isEntry is True when creating an entry (e.g., instance)
    :type isEntry: bool
    :param initialXml is initial xml content for xml documents
    :type isEntry: str
    """
    normalizedUri = modelXbrl.modelManager.cntlr.webCache.normalizeUrl(uri, base)
    if isEntry:
        modelXbrl.uri = normalizedUri
        modelXbrl.entryLoadingUrl = normalizedUri
        modelXbrl.uriDir = os.path.dirname(normalizedUri)
        for i in range(modelXbrl.modelManager.disclosureSystem.maxSubmissionSubdirectoryEntryNesting):
            modelXbrl.uriDir = os.path.dirname(modelXbrl.uriDir)

    else:
        filepath = modelXbrl.modelManager.cntlr.webCache.getfilename(normalizedUri, filenameOnly=True)
        if initialComment:
            initialComment = '<!--' + initialComment + '-->'
        if initialXml:
            if type in (Type.INSTANCE, Type.SCHEMA, Type.LINKBASE, Type.RSSFEED):
                Xml = '<nsmap>{}{}</nsmap>'.format(initialComment or '', initialXml or '')
        if type == Type.INSTANCE:
            Xml = '<nsmap>{}<xbrl xmlns="http://www.xbrl.org/2003/instance" xmlns:link="http://www.xbrl.org/2003/linkbase" xmlns:xlink="http://www.w3.org/1999/xlink">'.format(initialComment)
            if schemaRefs:
                for schemaRef in schemaRefs:
                    Xml += '<link:schemaRef xlink:type="simple" xlink:href="{0}"/>'.format(schemaRef.replace('\\', '/'))

            Xml += '</xbrl></nsmap>'
        else:
            if type == Type.SCHEMA:
                Xml = '<nsmap>{}<schema xmlns="http://www.w3.org/2001/XMLSchema" /></nsmap>'.format(initialComment)
            else:
                if type == Type.RSSFEED:
                    Xml = '<nsmap><rss version="2.0" /></nsmap>'
                else:
                    if type == Type.DTSENTRIES:
                        Xml = None
                    else:
                        type = Type.UnknownXML
                        Xml = '<nsmap>{0}</nsmap>'.format(initialXml or '')
            if Xml:
                import io
                file = io.StringIO(Xml)
                _parser, _parserLookupName, _parserLookupClass = parser(modelXbrl, filepath)
                xmlDocument = etree.parse(file, parser=_parser, base_url=filepath)
                file.close()
            else:
                xmlDocument = None
        if type == Type.RSSFEED:
            from arelle.ModelRssObject import ModelRssObject
            modelDocument = ModelRssObject(modelXbrl, type, uri, filepath, xmlDocument)
        else:
            modelDocument = ModelDocument(modelXbrl, type, normalizedUri, filepath, xmlDocument)
    if Xml:
        modelDocument.parser = _parser
        modelDocument.parserLookupName = _parserLookupName
        modelDocument.parserLookupClass = _parserLookupClass
        modelDocument.documentEncoding = documentEncoding
        rootNode = xmlDocument.getroot()
        rootNode.init(modelDocument)
        if xmlDocument:
            for semanticRoot in rootNode.iterchildren():
                if isinstance(semanticRoot, ModelObject):
                    modelDocument.xmlRootElement = semanticRoot
                    break

        for elt in xmlDocument.iter():
            if isinstance(elt, ModelObject):
                elt.init(modelDocument)

    if type == Type.INSTANCE:
        if discover:
            modelDocument.instanceDiscover(modelDocument.xmlRootElement)
    if type == Type.RSSFEED and discover:
        modelDocument.rssFeedDiscover(modelDocument.xmlRootElement)
    else:
        if type == Type.SCHEMA:
            modelDocument.targetNamespace = None
            modelDocument.isQualifiedElementFormDefault = False
            modelDocument.isQualifiedAttributeFormDefault = False
    modelDocument.definesUTR = False
    return modelDocument


class Type:
    """Type"""
    UnknownXML = 0
    UnknownNonXML = 1
    UnknownTypes = 1
    firstXBRLtype = 2
    SCHEMA = 2
    LINKBASE = 3
    INSTANCE = 4
    INLINEXBRL = 5
    lastXBRLtype = 5
    DTSENTRIES = 6
    INLINEXBRLDOCUMENTSET = 7
    VERSIONINGREPORT = 8
    TESTCASESINDEX = 9
    TESTCASE = 10
    REGISTRY = 11
    REGISTRYTESTCASE = 12
    XPATHTESTSUITE = 13
    RSSFEED = 14
    ARCSINFOSET = 15
    FACTDIMSINFOSET = 16
    TESTCASETYPES = (
     TESTCASESINDEX, TESTCASE, REGISTRY, REGISTRYTESTCASE, XPATHTESTSUITE)
    typeName = ('unknown XML', 'unknown non-XML', 'schema', 'linkbase', 'instance',
                'inline XBRL instance', 'entry point set', 'inline XBRL document set',
                'versioning report', 'testcases index', 'testcase', 'registry', 'registry testcase',
                'xpath test suite', 'RSS feed', 'arcs infoset', 'fact dimensions infoset')

    def identify(filesource, filepath):
        file, = filesource.file(filepath, stripDeclaration=True, binary=True)
        try:
            for _event, elt in etree.iterparse(file, events=('start', )):
                _type = {'{http://www.xbrl.org/2003/instance}xbrl':Type.INSTANCE, 
                 '{http://www.xbrl.org/2003/linkbase}linkbase':Type.LINKBASE, 
                 '{http://www.w3.org/2001/XMLSchema}schema':Type.SCHEMA}.get(elt.tag, Type.UnknownXML)
                if _type == Type.UnknownXML:
                    if elt.tag.endswith('html'):
                        if XbrlConst.ixbrlAll.intersection(elt.nsmap.values()):
                            _type = Type.INLINEXBRL
                break

        except Exception:
            _type = Type.UnknownXML

        file.close()
        return _type


schemaBottom = {
 'element', 'attribute', 'notation', 'simpleType', 'complexType', 'group', 'attributeGroup'}
fractionParts = {'{http://www.xbrl.org/2003/instance}numerator',
 '{http://www.xbrl.org/2003/instance}denominator'}

class ModelDocument:
    """ModelDocument"""

    def __init__(self, modelXbrl, type, uri, filepath, xmlDocument):
        self.modelXbrl = modelXbrl
        self.skipDTS = modelXbrl.skipDTS
        self.type = type
        self.uri = uri
        self.filepath = filepath
        self.xmlDocument = xmlDocument
        self.targetNamespace = None
        modelXbrl.urlDocs[uri] = self
        self.objectIndex = len(modelXbrl.modelObjects)
        modelXbrl.modelObjects.append(self)
        self.referencesDocument = {}
        self.idObjects = {}
        self.hrefObjects = []
        self.schemaLocationElements = set()
        self.referencedNamespaces = set()
        self.inDTS = False
        self.definesUTR = False
        self.isModified = False

    def objectId(self, refId=''):
        return '_{0}_{1}'.format(refId, self.objectIndex)

    @property
    def qname(self):
        try:
            return self._xmlRootElementQname
        except AttributeError:
            self._xmlRootElementQname = qname(self.xmlRootElement)
            return self._xmlRootElementQname

    def relativeUri(self, uri):
        return UrlUtil.relativeUri(self.uri, uri)

    @property
    def modelDocument(self):
        return self

    @property
    def basename(self):
        return os.path.basename(self.filepath)

    @property
    def filepathdir(self):
        return os.path.dirname(self.filepath)

    @property
    def propertyView(self):
        if self.type == Type.VERSIONINGREPORT:
            return (('type', self.gettype()), ('uri', self.uri)) + (('fromDTS', self.fromDTS.uri), ('toDTS', self.toDTS.uri))
        else:
            return ()

    def __repr__(self):
        return '{0}[{1}]{2})'.format(self.__class__.__name__, self.objectId(), self.propertyView)

    def setTitle(self, cntlr):
        try:
            cntlr.parent.wm_title(_('arelle - {0}').format(self.basename))
        except AttributeError:
            pass

    def setTitleInBackground(self):
        try:
            cntlr = self.modelXbrl.modelManager.cntlr
            uiThreadQueue = cntlr.uiThreadQueue
            uiThreadQueue.put((self.setTitle, [cntlr]))
        except AttributeError:
            pass

    def updateFileHistoryIfNeeded(self):
        myCntlr = self.modelXbrl.modelManager.cntlr
        updateFileHistory = getattr(myCntlr, 'updateFileHistory', None)
        if updateFileHistory:
            try:
                cntlr = self.modelXbrl.modelManager.cntlr
                uiThreadQueue = cntlr.uiThreadQueue
                uiThreadQueue.put((updateFileHistory, [self.filepath, False]))
            except AttributeError:
                pass

    def save(self, overrideFilepath=None, outputZip=None, updateFileHistory=True, encoding='utf-8', **kwargs):
        """Saves current document file.
        
        :param overrideFilepath: specify to override saving in instance's modelDocument.filepath
        """
        if outputZip:
            fh = io.StringIO()
        else:
            fh = open((overrideFilepath or self.filepath), 'w', encoding='utf-8')
        (XmlUtil.writexml)(fh, self.xmlDocument, encoding=encoding, **kwargs)
        if outputZip:
            fh.seek(0)
            outputZip.writestr(os.path.basename(overrideFilepath or self.filepath), fh.read())
        fh.close()
        if overrideFilepath:
            self.filepath = overrideFilepath
            self.setTitleInBackground()
        if updateFileHistory:
            self.updateFileHistoryIfNeeded()
        self.isModified = False

    def close(self, visited=None, urlDocs=None):
        try:
            if self.modelXbrl is not None:
                self.modelXbrl = None
        except:
            pass

        if visited is None:
            visited = []
        visited.append(self)
        for pluginMethod in pluginClassMethods('ModelDocument.CustomCloser'):
            pluginMethod(self)

        try:
            for referencedDocument, modelDocumentReference in self.referencesDocument.items():
                if referencedDocument not in visited:
                    referencedDocument.close(visited=visited, urlDocs=urlDocs)
                modelDocumentReference.__dict__.clear()

            self.referencesDocument.clear()
            if self.type == Type.VERSIONINGREPORT:
                if self.fromDTS:
                    self.fromDTS.close()
                if self.toDTS:
                    self.toDTS.close()
            urlDocs.pop(self.uri, None)
            xmlDocument = self.xmlDocument
            dummyRootElement = self.parser.makeelement('{http://dummy}dummy')
            for modelObject in self.xmlRootElement.iter():
                modelObject.__dict__.clear()

            self.xmlRootElement.clear()
            self.parserLookupName.__dict__.clear()
            self.parserLookupClass.__dict__.clear()
            self.__dict__.clear()
            if dummyRootElement is not None:
                xmlDocument._setroot(dummyRootElement)
            del dummyRootElement
        except AttributeError:
            pass

        if len(visited) == 1:
            while urlDocs:
                urlDocs.popitem()[1].close(visited=visited, urlDocs=urlDocs)

        visited.remove(self)

    def gettype(self):
        try:
            return Type.typeName[self.type]
        except AttributeError:
            return 'unknown'

    @property
    def creationSoftwareComment(self):
        try:
            return self._creationSoftwareComment
        except AttributeError:
            initialComment = ''
            node = self.xmlRootElement
            while node.getprevious() is not None:
                node = node.getprevious()
                if isinstance(node, etree._Comment):
                    initialComment = node.text + '\n' + initialComment

            if initialComment:
                self._creationSoftwareComment = initialComment
            else:
                self._creationSoftwareComment = None
                for i, node in enumerate(self.xmlDocument.iter()):
                    if isinstance(node, etree._Comment):
                        self._creationSoftwareComment = node.text
                    elif i > 10:
                        break

            return self._creationSoftwareComment

    @property
    def creationSoftware(self):
        global creationSoftwareNames
        if creationSoftwareNames is None:
            import json, re
            creationSoftwareNames = []
            try:
                with io.open((os.path.join(self.modelXbrl.modelManager.cntlr.configDir, 'creationSoftwareNames.json')), 'rt',
                  encoding='utf-8') as (f):
                    for key, pattern in json.load(f):
                        if key != '_description_':
                            creationSoftwareNames.append((key, re.compile(pattern, re.IGNORECASE)))

            except Exception as ex:
                self.modelXbrl.error('arelle:creationSoftwareNamesTable', (_('Error loading creation software names table %(error)s')),
                  modelObject=self,
                  error=ex)

            creationSoftwareComment = self.creationSoftwareComment
            return creationSoftwareComment or 'None'
        else:
            for productKey, productNamePattern in creationSoftwareNames:
                if productNamePattern.search(creationSoftwareComment):
                    return productKey

            return creationSoftwareComment

    @property
    def processingInstructions(self):
        try:
            return self._processingInstructions
        except AttributeError:
            self._processingInstructions = []
            node = self.xmlRootElement
            while node.getprevious() is not None:
                node = node.getprevious()
                if isinstance(node, etree._ProcessingInstruction):
                    self._processingInstructions.append(node)

            return self._processingInstructions

    def schemaDiscover(self, rootElement, isIncluded, namespace):
        targetNamespace = rootElement.get('targetNamespace')
        if targetNamespace:
            self.targetNamespace = targetNamespace
            self.referencedNamespaces.add(targetNamespace)
            self.modelXbrl.namespaceDocs[targetNamespace].append(self)
            if namespace:
                if targetNamespace != namespace:
                    self.modelXbrl.error('xmlSchema1.4.2.3:refSchemaNamespace', (_('Discovery of %(fileName)s expected namespace %(namespace)s found targetNamespace %(targetNamespace)s')),
                      modelObject=rootElement,
                      fileName=(self.basename),
                      namespace=namespace,
                      targetNamespace=targetNamespace)
            if self.modelXbrl.modelManager.validateDisclosureSystem:
                if self.modelXbrl.modelManager.disclosureSystem.disallowedHrefOfNamespace(self.uri, targetNamespace):
                    self.modelXbrl.error(('EFM.6.22.02', 'GFM.1.1.3', 'SBR.NL.2.1.0.06' if self.uri.startswith('http') else 'SBR.NL.2.2.0.17'), (_('Namespace: %(namespace)s disallowed schemaLocation %(schemaLocation)s')),
                      modelObject=rootElement,
                      namespace=targetNamespace,
                      schemaLocation=(self.uri),
                      url=(self.uri),
                      messageCodes=('EFM.6.22.02', 'GFM.1.1.3', 'SBR.NL.2.1.0.06',
                                    'SBR.NL.2.2.0.17'))
            self.noTargetNamespace = False
        else:
            if isIncluded == True:
                if namespace:
                    self.targetNamespace = namespace
                    self.modelXbrl.namespaceDocs[targetNamespace].append(self)
            self.noTargetNamespace = True
        if targetNamespace == XbrlConst.xbrldt:
            self.modelXbrl.hasXDT = True
        else:
            self.isQualifiedElementFormDefault = rootElement.get('elementFormDefault') == 'qualified'
            self.isQualifiedAttributeFormDefault = rootElement.get('attributeFormDefault') == 'qualified'
            try:
                self.schemaDiscoverChildElements(rootElement)
            except (ValueError, LookupError) as err:
                self.modelXbrl.modelManager.addToLog('discovery: {0} error {1}'.format(self.basename, err))

            if isIncluded or targetNamespace:
                nsDocs = self.modelXbrl.namespaceDocs
                if targetNamespace in nsDocs:
                    if nsDocs[targetNamespace].index(self) == 0:
                        for doc in nsDocs[targetNamespace]:
                            self.modelXbrl.schemaDocsToValidate.add(doc)

            else:
                self.modelXbrl.schemaDocsToValidate.add(self)

    def schemaDiscoverChildElements(self, parentModelObject):
        for modelObject in parentModelObject.iterchildren():
            if isinstance(modelObject, ModelObject):
                ln = modelObject.localName
                ns = modelObject.namespaceURI
                if modelObject.namespaceURI == XbrlConst.xsd:
                    if ln in {'import', 'include', 'redefine'}:
                        self.importDiscover(modelObject)
                if self.inDTS:
                    if ns == XbrlConst.link:
                        if ln == 'roleType':
                            self.modelXbrl.roleTypes[modelObject.roleURI].append(modelObject)
                        else:
                            if ln == 'arcroleType':
                                self.modelXbrl.arcroleTypes[modelObject.arcroleURI].append(modelObject)
                            else:
                                if ln == 'linkbaseRef':
                                    self.schemaLinkbaseRefDiscover(modelObject)
                                elif ln == 'linkbase':
                                    self.linkbaseDiscover(modelObject)
                self.schemaDiscoverChildElements(modelObject)

    def baseForElement(self, element):
        base = ''
        baseElt = element
        while baseElt is not None:
            baseAttr = baseElt.get('{http://www.w3.org/XML/1998/namespace}base')
            if baseAttr:
                if self.modelXbrl.modelManager.validateDisclosureSystem:
                    self.modelXbrl.error(('EFM.6.03.11', 'GFM.1.1.7', 'EBA.2.1', 'EIOPA.2.1'), (_('Prohibited base attribute: %(attribute)s')),
                      modelObject=element,
                      attribute=baseAttr,
                      element=(element.qname))
                else:
                    if baseAttr.startswith('/'):
                        base = baseAttr
                    else:
                        base = baseAttr + base
            baseElt = baseElt.getparent()

        if base:
            if base.startswith('http://') or os.path.isabs(base):
                return base
            return os.path.dirname(self.uri) + '/' + base
        else:
            return self.uri

    def importDiscover(self, element):
        schemaLocation = element.get('schemaLocation')
        if element.localName in ('include', 'redefine'):
            importNamespace = self.targetNamespace
            isIncluded = True
        else:
            importNamespace = element.get('namespace')
            isIncluded = False
        if importNamespace and schemaLocation:
            importElementBase = self.baseForElement(element)
            importSchemaLocation = self.modelXbrl.modelManager.cntlr.webCache.normalizeUrl(schemaLocation, importElementBase)
            if self.modelXbrl.modelManager.validateDisclosureSystem:
                if self.modelXbrl.modelManager.disclosureSystem.blockDisallowedReferences:
                    if self.modelXbrl.modelManager.disclosureSystem.disallowedHrefOfNamespace(importSchemaLocation, importNamespace):
                        self.modelXbrl.error(('EFM.6.22.02', 'GFM.1.1.3', 'SBR.NL.2.1.0.06' if importSchemaLocation.startswith('http') else 'SBR.NL.2.2.0.17'), (_('Namespace: %(namespace)s disallowed schemaLocation blocked %(schemaLocation)s')),
                          modelObject=element,
                          namespace=importNamespace,
                          schemaLocation=importSchemaLocation,
                          url=importSchemaLocation,
                          messageCodes=('EFM.6.22.02', 'GFM.1.1.3', 'SBR.NL.2.1.0.06',
                                        'SBR.NL.2.2.0.17'))
                        return
            doc = None
            importSchemaLocationBasename = os.path.basename(importNamespace)
            for otherDoc in self.modelXbrl.namespaceDocs[importNamespace]:
                doc = otherDoc
                if otherDoc.uri == importSchemaLocation:
                    break
                else:
                    if isIncluded:
                        doc = None
                    else:
                        if doc.basename != importSchemaLocationBasename:
                            doc = None

            if doc is not None:
                if self.inDTS:
                    if not doc.inDTS:
                        doc.inDTS = True
                        doc.schemaDiscoverChildElements(doc.xmlRootElement)
            else:
                doc = load((self.modelXbrl), schemaLocation, base=importElementBase, isDiscovered=(self.inDTS), isIncluded=isIncluded,
                  namespace=importNamespace,
                  referringElement=element)
            if doc is not None:
                if doc not in self.referencesDocument:
                    self.referencesDocument[doc] = ModelDocumentReference(element.localName, element)
                    self.referencedNamespaces.add(importNamespace)

    def schemalocateElementNamespace(self, element):
        if isinstance(element, ModelObject):
            eltNamespace = element.namespaceURI
            if eltNamespace not in self.modelXbrl.namespaceDocs:
                if eltNamespace not in self.referencedNamespaces:
                    schemaLocationElement = XmlUtil.schemaLocation(element, eltNamespace, returnElement=True)
                    if schemaLocationElement is not None:
                        self.schemaLocationElements.add(schemaLocationElement)
                        self.referencedNamespaces.add(eltNamespace)

    def loadSchemalocatedSchemas(self):
        if self.skipDTS:
            return
        for elt in self.schemaLocationElements:
            schemaLocation = elt.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation')
            if schemaLocation:
                ns = None
                for entry in schemaLocation.split():
                    if ns is None:
                        ns = entry
                    elif self.type == Type.INLINEXBRL and ns == XbrlConst.xhtml:
                        pass
                    else:
                        if ns not in self.modelXbrl.namespaceDocs:
                            loadSchemalocatedSchema(self.modelXbrl, elt, entry, ns, self.baseForElement(elt))
                        ns = None

    def schemaLinkbaseRefsDiscover(self, tree):
        for refln in ('{http://www.xbrl.org/2003/linkbase}schemaRef', '{http://www.xbrl.org/2003/linkbase}linkbaseRef'):
            for element in tree.iterdescendants(tag=refln):
                if isinstance(element, ModelObject):
                    self.schemaLinkbaseRefDiscover(element)

    def schemaLinkbaseRefDiscover(self, element):
        return self.discoverHref(element, urlRewritePluginClass='ModelDocument.InstanceSchemaRefRewriter')

    def linkbasesDiscover(self, tree):
        for linkbaseElement in tree.iterdescendants(tag='{http://www.xbrl.org/2003/linkbase}linkbase'):
            if isinstance(linkbaseElement, ModelObject):
                self.linkbaseDiscover(self, linkbaseElement)

    def linkbaseDiscover(self, linkbaseElement, inInstance=False):
        lbElementSequence = 0
        for lbElement in linkbaseElement:
            if isinstance(lbElement, ModelObject):
                lbElementSequence += 1
                lbElement._elementSequence = lbElementSequence
                lbLn = lbElement.localName
                lbNs = lbElement.namespaceURI
                if lbNs == XbrlConst.link:
                    if lbLn == 'roleRef' or lbLn == 'arcroleRef':
                        href = self.discoverHref(lbElement)
                        if href is None:
                            self.modelXbrl.error('xmlSchema:requiredAttribute', (_('Linkbase reference for %(linkbaseRefElement)s href attribute missing or malformed')),
                              modelObject=lbElement,
                              linkbaseRefElement=lbLn)
                            continue
                if lbElement.get('{http://www.w3.org/1999/xlink}type') == 'extended':
                    if isinstance(lbElement, ModelLink):
                        self.schemalocateElementNamespace(lbElement)
                        arcrolesFound = set()
                        dimensionArcFound = False
                        formulaArcFound = False
                        tableRenderingArcFound = False
                        linkQn = qname(lbElement)
                        linkrole = lbElement.get('{http://www.w3.org/1999/xlink}role')
                        isStandardExtLink = XbrlConst.isStandardResourceOrExtLinkElement(lbElement)
                        if inInstance:
                            baseSetKeys = (('XBRL-footnotes', None, None, None),
                             (
                              'XBRL-footnotes', linkrole, None, None))
                            for baseSetKey in baseSetKeys:
                                self.modelXbrl.baseSets[baseSetKey].append(lbElement)

                        linkElementSequence = 0
                        for linkElement in lbElement.iterchildren():
                            if isinstance(linkElement, ModelObject):
                                linkElementSequence += 1
                                linkElement._elementSequence = linkElementSequence
                                self.schemalocateElementNamespace(linkElement)
                                xlinkType = linkElement.get('{http://www.w3.org/1999/xlink}type')
                                modelResource = None
                                if xlinkType == 'locator':
                                    nonDTS = linkElement.namespaceURI != XbrlConst.link or linkElement.localName != 'loc'
                                    href = self.discoverHref(linkElement, nonDTS=nonDTS)
                                    if href is None:
                                        if isStandardExtLink:
                                            self.modelXbrl.error('xmlSchema:requiredAttribute', (_('Locator href attribute "%(href)s" missing or malformed in standard extended link')),
                                              modelObject=linkElement,
                                              href=(linkElement.get('{http://www.w3.org/1999/xlink}href')))
                                        else:
                                            self.modelXbrl.warning('arelle:hrefWarning', (_('Locator href attribute "%(href)s" missing or malformed in non-standard extended link')),
                                              modelObject=linkElement,
                                              href=(linkElement.get('{http://www.w3.org/1999/xlink}href')))
                                    else:
                                        linkElement.modelHref = href
                                        modelResource = linkElement
                                else:
                                    if xlinkType == 'arc':
                                        arcQn = qname(linkElement)
                                        arcrole = linkElement.get('{http://www.w3.org/1999/xlink}arcrole')
                                        if arcrole not in arcrolesFound:
                                            if linkrole == '':
                                                linkrole = XbrlConst.defaultLinkRole
                                            else:
                                                baseSetKeys = [
                                                 (
                                                  arcrole, linkrole, linkQn, arcQn)]
                                                baseSetKeys.append((arcrole, linkrole, None, None))
                                                baseSetKeys.append((arcrole, None, None, None))
                                                if XbrlConst.isDimensionArcrole(arcrole):
                                                    if not dimensionArcFound:
                                                        baseSetKeys.append(('XBRL-dimensions',
                                                                            None,
                                                                            None,
                                                                            None))
                                                        baseSetKeys.append(('XBRL-dimensions', linkrole, None, None))
                                                        dimensionArcFound = True
                                                if XbrlConst.isFormulaArcrole(arcrole):
                                                    if not formulaArcFound:
                                                        baseSetKeys.append(('XBRL-formulae',
                                                                            None,
                                                                            None,
                                                                            None))
                                                        baseSetKeys.append(('XBRL-formulae', linkrole, None, None))
                                                        formulaArcFound = True
                                                if XbrlConst.isTableRenderingArcrole(arcrole):
                                                    if not tableRenderingArcFound:
                                                        baseSetKeys.append(('Table-rendering',
                                                                            None,
                                                                            None,
                                                                            None))
                                                        baseSetKeys.append(('Table-rendering', linkrole, None, None))
                                                        tableRenderingArcFound = True
                                                        self.modelXbrl.hasTableRendering = True
                                                if XbrlConst.isTableIndexingArcrole(arcrole):
                                                    self.modelXbrl.hasTableIndexing = True
                                            for baseSetKey in baseSetKeys:
                                                self.modelXbrl.baseSets[baseSetKey].append(lbElement)

                                            arcrolesFound.add(arcrole)
                                    else:
                                        if xlinkType == 'resource':
                                            modelResource = linkElement
                                            for resourceElt in linkElement.iter():
                                                self.schemalocateElementNamespace(resourceElt)

                                if modelResource is not None:
                                    lbElement.labeledResources[linkElement.get('{http://www.w3.org/1999/xlink}label')].append(modelResource)

                    else:
                        self.modelXbrl.error('xbrl:schemaDefinitionMissing', (_('Linkbase extended link %(element)s missing schema definition')),
                          modelObject=lbElement,
                          element=(lbElement.prefixedName))

    def discoverHref(self, element, nonDTS=False, urlRewritePluginClass=None):
        href = element.get('{http://www.w3.org/1999/xlink}href')
        if href:
            url, id = UrlUtil.splitDecodeFragment(href)
            if url == '':
                doc = self
            else:
                if self.skipDTS:
                    _newDoc = DocumentPrototype
                else:
                    _newDoc = load
            if urlRewritePluginClass:
                for pluginMethod in pluginClassMethods(urlRewritePluginClass):
                    url = pluginMethod(self, url)

            doc = _newDoc((self.modelXbrl), url, isDiscovered=(not nonDTS), base=(self.baseForElement(element)), referringElement=element)
            if not nonDTS:
                if doc is not None:
                    if doc not in self.referencesDocument:
                        self.referencesDocument[doc] = ModelDocumentReference('href', element)
                        if not doc.inDTS:
                            if doc.type > Type.UnknownTypes:
                                doc.inDTS = True
                                if doc.type == Type.SCHEMA:
                                    if not self.skipDTS:
                                        doc.schemaDiscoverChildElements(doc.xmlRootElement)
            href = (
             element, doc, id if len(id) > 0 else None)
            if doc is not None:
                self.hrefObjects.append(href)
            return href

    def instanceDiscover(self, xbrlElement):
        self.schemaLinkbaseRefsDiscover(xbrlElement)
        if not self.skipDTS:
            self.linkbaseDiscover(xbrlElement, inInstance=True)
        xmlValidate(self.modelXbrl, xbrlElement)
        self.instanceContentsDiscover(xbrlElement)

    def instanceContentsDiscover(self, xbrlElement):
        nextUndefinedFact = len(self.modelXbrl.undefinedFacts)
        instElementSequence = 0
        for instElement in xbrlElement.iterchildren():
            if isinstance(instElement, ModelObject):
                instElementSequence += 1
                instElement._elementSequence = instElementSequence
                ln = instElement.localName
                ns = instElement.namespaceURI
                if ns == XbrlConst.xbrli:
                    if ln == 'context':
                        self.contextDiscover(instElement)
                    elif ln == 'unit':
                        self.unitDiscover(instElement)
                    else:
                        if ns == XbrlConst.link:
                            pass
                        elif ns in XbrlConst.ixbrlAll:
                            if ln == 'relationship':
                                continue
                else:
                    self.factDiscover(instElement, self.modelXbrl.facts)

        if len(self.modelXbrl.undefinedFacts) > nextUndefinedFact:
            undefFacts = self.modelXbrl.undefinedFacts[nextUndefinedFact:]
            self.modelXbrl.error('xbrl:schemaImportMissing', (_('Instance facts missing schema concept definition: %(elements)s')),
              modelObject=undefFacts,
              elements=(', '.join(sorted(set(str(f.prefixedName) for f in undefFacts)))))

    def contextDiscover(self, modelContext):
        if not self.skipDTS:
            xmlValidate(self.modelXbrl, modelContext)
        id = modelContext.id
        self.modelXbrl.contexts[id] = modelContext
        for container in (('{http://www.xbrl.org/2003/instance}segment', modelContext.segDimValues, modelContext.segNonDimValues),
         (
          '{http://www.xbrl.org/2003/instance}scenario', modelContext.scenDimValues, modelContext.scenNonDimValues)):
            containerName, containerDimValues, containerNonDimValues = container
            for containerElement in modelContext.iterdescendants(tag=containerName):
                for sElt in containerElement.iterchildren():
                    if isinstance(sElt, ModelObject):
                        if sElt.namespaceURI == XbrlConst.xbrldi and sElt.localName in ('explicitMember',
                                                                                        'typedMember'):
                            modelContext.qnameDims[sElt.dimensionQname] = sElt
                            if not self.skipDTS:
                                dimension = sElt.dimension
                                if dimension is not None:
                                    if dimension not in containerDimValues:
                                        containerDimValues[dimension] = sElt
                                modelContext.errorDimValues.append(sElt)
                    containerNonDimValues.append(sElt)

    def unitDiscover(self, unitElement):
        if not self.skipDTS:
            xmlValidate(self.modelXbrl, unitElement)
        self.modelXbrl.units[unitElement.id] = unitElement

    def inlineXbrlDiscover(self, htmlElement):
        ixNS = None
        conflictingNSelts = []
        for inlineElement in htmlElement.iterdescendants():
            if isinstance(inlineElement, ModelObject) and inlineElement.namespaceURI in XbrlConst.ixbrlAll:
                if ixNS is None:
                    ixNS = inlineElement.namespaceURI
                elif ixNS != inlineElement.namespaceURI:
                    conflictingNSelts.append(inlineElement)

        if ixNS is None:
            for _ns in htmlElement.nsmap.values():
                if _ns in XbrlConst.ixbrlAll:
                    ixNS = _ns
                    break

        if conflictingNSelts:
            self.modelXbrl.error('ix:multipleIxNamespaces', (_('Multiple ix namespaces were found')),
              modelObject=conflictingNSelts)
        self.ixNS = ixNS
        self.ixNStag = ixNStag = '{' + ixNS + '}' if ixNS else ''
        for inlineElement in htmlElement.iterdescendants(tag=(ixNStag + 'references')):
            self.schemaLinkbaseRefsDiscover(inlineElement)
            xmlValidate(self.modelXbrl, inlineElement)

        if htmlElement.namespaceURI == XbrlConst.xhtml:
            XhtmlValidate.xhtmlValidate(self.modelXbrl, htmlElement)
        if not hasattr(self.modelXbrl, 'targetRoleRefs'):
            self.modelXbrl.targetRoleRefs = {}
            self.modelXbrl.targetArcroleRefs = {}
        for inlineElement in htmlElement.iterdescendants(tag=(ixNStag + 'resources')):
            self.instanceContentsDiscover(inlineElement)
            xmlValidate(self.modelXbrl, inlineElement)
            for refElement in inlineElement.iterchildren('{http://www.xbrl.org/2003/linkbase}roleRef'):
                self.modelXbrl.targetRoleRefs[refElement.get('roleURI')] = refElement
                if self.discoverHref(refElement) is None:
                    self.modelXbrl.error('xmlSchema:requiredAttribute', (_('Reference for roleURI href attribute missing or malformed')),
                      modelObject=refElement)

            for refElement in inlineElement.iterchildren('{http://www.xbrl.org/2003/linkbase}arcroleRef'):
                self.modelXbrl.targetArcroleRefs[refElement.get('arcroleURI')] = refElement
                if self.discoverHref(refElement) is None:
                    self.modelXbrl.error('xmlSchema:requiredAttribute', (_('Reference for arcroleURI href attribute missing or malformed')),
                      modelObject=refElement)

        if not hasattr(self.modelXbrl, 'ixdsHtmlElements'):
            self.modelXbrl.ixdsHtmlElements = []
        self.modelXbrl.ixdsHtmlElements.append(htmlElement)

    def factDiscover(self, modelFact, parentModelFacts=None, parentElement=None):
        if parentModelFacts is None:
            if isinstance(parentElement, ModelFact):
                if parentElement.isTuple:
                    parentModelFacts = parentElement.modelTupleFacts
            else:
                parentModelFacts = self.modelXbrl.facts
        else:
            if isinstance(modelFact, ModelFact):
                parentModelFacts.append(modelFact)
                self.modelXbrl.factsInInstance.add(modelFact)
                tupleElementSequence = 0
                for tupleElement in modelFact:
                    if isinstance(tupleElement, ModelObject):
                        tupleElementSequence += 1
                        tupleElement._elementSequence = tupleElementSequence
                        if tupleElement.tag not in fractionParts:
                            self.factDiscover(tupleElement, modelFact.modelTupleFacts)

            else:
                self.modelXbrl.undefinedFacts.append(modelFact)

    def testcasesIndexDiscover(self, rootNode):
        for testcasesElement in rootNode.iter():
            if isinstance(testcasesElement, ModelObject) and testcasesElement.localName in ('testcases',
                                                                                            'testSuite'):
                rootAttr = testcasesElement.get('root')
                if rootAttr:
                    base = os.path.join(os.path.dirname(self.filepath), rootAttr) + os.sep
                else:
                    base = self.filepath
                for testcaseElement in testcasesElement:
                    if isinstance(testcaseElement, ModelObject) and testcaseElement.localName in ('testcase',
                                                                                                  'testSetRef'):
                        uriAttr = testcaseElement.get('uri') or testcaseElement.get('{http://www.w3.org/1999/xlink}href')
                        if uriAttr:
                            doc = load((self.modelXbrl), uriAttr, base=base, referringElement=testcaseElement)
                            if doc is not None:
                                if doc not in self.referencesDocument:
                                    self.referencesDocument[doc] = ModelDocumentReference('testcaseIndex', testcaseElement)
                    else:
                        if isinstance(testcaseElement, ModelObject) and testcaseElement.localName == 'testcases':
                            uriAttr = testcaseElement.get('uri') or testcaseElement.get('{http://www.w3.org/1999/xlink}href')
                            if uriAttr:
                                doc = load((self.modelXbrl), uriAttr, base=base, referringElement=testcaseElement)
                                if doc is not None and doc not in self.referencesDocument:
                                    self.referencesDocument[doc] = ModelDocumentReference('testcaseIndex', testcaseElement)

    def testcaseDiscover(self, testcaseElement):
        isTransformTestcase = testcaseElement.namespaceURI == 'http://xbrl.org/2011/conformance-rendering/transforms'
        if XmlUtil.xmlnsprefix(testcaseElement, XbrlConst.cfcn) or isTransformTestcase:
            self.type = Type.REGISTRYTESTCASE
        self.outpath = self.xmlRootElement.get('outpath') or self.filepathdir
        self.testcaseVariations = []
        priorTransformName = None
        for modelVariation in XmlUtil.descendants(testcaseElement, testcaseElement.namespaceURI, ('variation',
                                                                                                  'testGroup')):
            self.testcaseVariations.append(modelVariation)
            if isTransformTestcase:
                if modelVariation.getparent().get('name') is not None:
                    transformName = modelVariation.getparent().get('name')
                    if transformName != priorTransformName:
                        priorTransformName = transformName
                        variationNumber = 1
                modelVariation._name = '{0} v-{1:02}'.format(priorTransformName, variationNumber)
                variationNumber += 1

        if len(self.testcaseVariations) == 0:
            if XbrlConst.ixbrlAll.intersection(testcaseElement.values()):
                self.testcaseVariations.append(testcaseElement)

    def registryDiscover(self, rootNode):
        base = self.filepath
        for entryElement in rootNode.iterdescendants(tag='{http://xbrl.org/2008/registry}entry'):
            if isinstance(entryElement, ModelObject):
                uri = XmlUtil.childAttr(entryElement, XbrlConst.registry, 'url', '{http://www.w3.org/1999/xlink}href')
                functionDoc = load((self.modelXbrl), uri, base=base, referringElement=entryElement)
                if functionDoc is not None:
                    testUriElt = XmlUtil.child(functionDoc.xmlRootElement, XbrlConst.function, 'conformanceTest')
                    if testUriElt is not None:
                        testuri = testUriElt.get('{http://www.w3.org/1999/xlink}href')
                        testbase = functionDoc.filepath
                        if testuri is not None:
                            testcaseDoc = load((self.modelXbrl), testuri, base=testbase, referringElement=testUriElt)
                            if testcaseDoc is not None and testcaseDoc not in self.referencesDocument:
                                self.referencesDocument[testcaseDoc] = ModelDocumentReference('registryIndex', testUriElt)

    def xPathTestSuiteDiscover(self, rootNode):
        pass


def inlineIxdsDiscover(modelXbrl, modelIxdsDocument):
    ixdsEltById = defaultdict(list)
    for htmlElement in modelXbrl.ixdsHtmlElements:
        for elt in htmlElement.iterfind('.//*[@id]'):
            if isinstance(elt, ModelObject) and elt.id:
                ixdsEltById[elt.id].append(elt)

    footnoteRefs = defaultdict(list)
    tupleElements = []
    continuationElements = {}
    continuationReferences = defaultdict(set)
    tuplesByTupleID = {}
    factsByFactID = {}
    factTargetIDs = set()
    targetReferenceAttrs = defaultdict(dict)
    targetReferencePrefixNs = defaultdict(dict)
    targetReferencesIDs = {}
    hasResources = False
    for htmlElement in modelXbrl.ixdsHtmlElements:
        mdlDoc = htmlElement.modelDocument
        for modelInlineTuple in htmlElement.iterdescendants(tag=(mdlDoc.ixNStag + 'tuple')):
            if isinstance(modelInlineTuple, ModelObject):
                modelInlineTuple.unorderedTupleFacts = defaultdict(list)
                if modelInlineTuple.qname is not None:
                    if modelInlineTuple.tupleID:
                        if modelInlineTuple.tupleID not in tuplesByTupleID:
                            tuplesByTupleID[modelInlineTuple.tupleID] = modelInlineTuple
                        else:
                            modelXbrl.error(ixMsgCode('tupleIdDuplication', modelInlineTuple, sect='validation'), (_('Inline XBRL tuples have same tupleID %(tupleID)s: %(qname1)s and %(qname2)s')),
                              modelObject=(
                             modelInlineTuple, tuplesByTupleID[modelInlineTuple.tupleID]),
                              tupleID=(modelInlineTuple.tupleID),
                              qname1=(modelInlineTuple.qname),
                              qname2=(tuplesByTupleID[modelInlineTuple.tupleID].qname))
                    tupleElements.append(modelInlineTuple)
                    for r in modelInlineTuple.footnoteRefs:
                        footnoteRefs[r].append(modelInlineTuple)

                    if modelInlineTuple.id:
                        factsByFactID[modelInlineTuple.id] = modelInlineTuple
                factTargetIDs.add(modelInlineTuple.get('target'))

        for elt in htmlElement.iterdescendants(tag=(mdlDoc.ixNStag + 'continuation')):
            if isinstance(elt, ModelObject) and elt.id:
                continuationElements[elt.id] = elt

        for elt in htmlElement.iterdescendants(tag=(mdlDoc.ixNStag + 'references')):
            if isinstance(elt, ModelObject):
                target = elt.get('target')
                targetReferenceAttrsDict = targetReferenceAttrs[target]
                for attrName, attrValue in elt.items():
                    if attrName.startswith('{'):
                        if not attrName.startswith(mdlDoc.ixNStag):
                            if attrName != '{http://www.w3.org/XML/1998/namespace}base':
                                if attrName in targetReferenceAttrsDict:
                                    modelXbrl.error(ixMsgCode('referencesAttributeDuplication', ns=(mdlDoc.ixNS), name='references', sect='validation'), (_('Inline XBRL ix:references attribute %(name)s duplicated in target %(target)s')),
                                      modelObject=(
                                     elt, targetReferenceAttrsDict[attrName]),
                                      name=attrName,
                                      target=target)
                                else:
                                    targetReferenceAttrsDict[attrName] = elt

                if elt.id:
                    if ixdsEltById[elt.id] != [elt]:
                        modelXbrl.error(ixMsgCode('referencesIdDuplication', ns=(mdlDoc.ixNS), name='references', sect='validation'), (_('Inline XBRL ix:references id %(id)s duplicated in inline document set')),
                          modelObject=(ixdsEltById[elt.id]),
                          id=(elt.id))
                    else:
                        if target in targetReferencesIDs:
                            modelXbrl.error(ixMsgCode('referencesTargetId', ns=(mdlDoc.ixNS), name='references', sect='validation'), (_('Inline XBRL has multiple ix:references with id in target %(target)s')),
                              modelObject=(
                             elt, targetReferencesIDs[target]),
                              target=target)
                        else:
                            targetReferencesIDs[target] = elt
                targetReferencePrefixNsDict = targetReferencePrefixNs[target]
                for _prefix, _ns in elt.nsmap.items():
                    if _prefix in targetReferencePrefixNsDict:
                        if _ns != targetReferencePrefixNsDict[_prefix][0]:
                            modelXbrl.error(ixMsgCode('referencesNamespacePrefixConflict', ns=(mdlDoc.ixNS), name='references', sect='validation'), (_('Inline XBRL ix:references prefix %(prefix)s has multiple namespaces %(ns1)s and %(ns2)s in target %(target)s')),
                              modelObject=(
                             elt, targetReferencePrefixNsDict[_prefix][1]),
                              prefix=_prefix,
                              ns1=_ns,
                              ns2=(targetReferencePrefixNsDict[_prefix]),
                              target=target)
                    else:
                        targetReferencePrefixNsDict[_prefix] = (
                         _ns, elt)

        for elt in htmlElement.iterdescendants(tag=(mdlDoc.ixNStag + 'resources')):
            hasResources = True
            for subEltTag in ('{http://www.xbrl.org/2003/instance}context', '{http://www.xbrl.org/2003/instance}unit'):
                for resElt in elt.iterdescendants(tag=subEltTag):
                    if resElt.id and ixdsEltById[resElt.id] != [resElt]:
                        modelXbrl.error(ixMsgCode('resourceIdDuplication', ns=(mdlDoc.ixNS), name='resources', sect='validation'), (_('Inline XBRL ix:resources descendant id %(id)s duplicated in inline document set')),
                          modelObject=(ixdsEltById[resElt.id]),
                          id=(resElt.id))

    if not hasResources:
        modelXbrl.error(ixMsgCode('missingResources', ns=(mdlDoc.ixNS), name='resources', sect='validation'), (_('Inline XBRL ix:resources element not found')),
          modelObject=modelXbrl)
    del ixdsEltById
    del targetReferencePrefixNs
    del targetReferencesIDs
    modelXbrl.ixTargetRootElements = {}
    for target in targetReferenceAttrs.keys() | {None}:
        modelXbrl.ixTargetRootElements[target] = XmlUtil.addChild(modelIxdsDocument, (XbrlConst.qnXbrliXbrl), appendChild=False)

    def locateFactInTuple(modelFact, tuplesByTupleID, ixNStag):
        tupleRef = modelFact.tupleRef
        tuple = None
        if tupleRef:
            if tupleRef not in tuplesByTupleID:
                modelXbrl.error(ixMsgCode('tupleRefMissing', modelFact, sect='validation'), (_('Inline XBRL tupleRef %(tupleRef)s not found')),
                  modelObject=modelFact,
                  tupleRef=tupleRef)
            else:
                tuple = tuplesByTupleID[tupleRef]
        else:
            for tupleParent in modelFact.iterancestors(tag=(ixNStag + '*')):
                if tupleParent.localName == 'tuple':
                    tuple = tupleParent
                break

        if tuple is not None:
            if modelFact.order is not None:
                tuple.unorderedTupleFacts[modelFact.order].append(modelFact)
            else:
                modelXbrl.error(ixMsgCode('tupleMemberOrderMissing', modelFact, sect='validation'), (_('Inline XBRL tuple member %(qname)s must have a numeric order attribute')),
                  modelObject=modelFact,
                  qname=(modelFact.qname))
            modelFact._ixFactParent = tuple
        else:
            modelXbrl.modelXbrl.facts.append(modelFact)
        try:
            modelFact._ixFactParent = modelXbrl.ixTargetRootElements[modelFact.get('target')]
        except KeyError:
            modelFact._ixFactParent = modelXbrl.ixTargetRootElements[None]

    def locateContinuation(element, chain=None):
        contAt = element.get('continuedAt')
        if contAt:
            continuationReferences[contAt].add(element)
            if contAt not in continuationElements:
                if contAt in element.modelDocument.idObjects:
                    _contAtTarget = element.modelDocument.idObjects[contAt]
                    modelXbrl.error(ixMsgCode('continuationTarget', element, sect='validation'), (_('continuedAt %(continuationAt)s target is an %(targetElement)s element instead of ix:continuation element.')),
                      modelObject=(
                     element, _contAtTarget),
                      continuationAt=contAt,
                      targetElement=(_contAtTarget.elementQname))
                else:
                    modelXbrl.error(ixMsgCode('continuationMissing', element, sect='validation'), (_('Inline XBRL continuation %(continuationAt)s not found')),
                      modelObject=element,
                      continuationAt=contAt)
            else:
                if chain is None:
                    chain = [
                     element]
                contElt = continuationElements[contAt]
                if contElt in chain:
                    cycle = ', '.join(e.get('continuedAt') for e in chain)
                    chain.append(contElt)
                    modelXbrl.error(ixMsgCode('continuationCycle', element, sect='validation'), (_('Inline XBRL continuation cycle: %(continuationCycle)s')),
                      modelObject=chain,
                      continuationCycle=cycle)
                else:
                    chain.append(contElt)
                    element._continuationElement = contElt
                    locateContinuation(contElt, chain)
        elif chain:
            chainSet = set(chain)
            for chainElt in chain:
                for chainEltAncestor in chainElt.iterancestors(tag=(chainElt.modelDocument.ixNStag + '*')):
                    if chainEltAncestor in chainSet:
                        if hasattr(chain[0], '_continuationElement'):
                            del chain[0]._continuationElement
                        modelXbrl.error(ixMsgCode('continuationChainNested', chainElt, sect='validation'), (_('Inline XBRL continuation chain element %(ancestorElement)s has descendant element %(descendantElement)s')),
                          modelObject=(
                         chainElt, chainEltAncestor),
                          ancestorElement=(chainEltAncestor.id or chainEltAncestor.get('name', chainEltAncestor.get('continuedAt'))),
                          descendantElement=(chainElt.id or chainElt.get('name', chainElt.get('continuedAt'))))

    def checkTupleIxDescendants(tupleFact, parentElt):
        for childElt in parentElt.iterchildren():
            if isinstance(childElt, ModelObject) and childElt.namespaceURI in XbrlConst.ixbrlAll:
                if childElt.localName in ('numerator', 'denominator'):
                    modelXbrl.error(ixMsgCode('tupleContentError', tupleFact, sect='validation'), (_('Inline XBRL tuple content illegal %(qname)s')),
                      modelObject=(
                     tupleFact, childElt),
                      qname=(childElt.qname))
            else:
                checkTupleIxDescendants(tupleFact, childElt)

    for htmlElement in modelXbrl.ixdsHtmlElements:
        mdlDoc = htmlElement.modelDocument
        ixNStag = mdlDoc.ixNStag
        for tupleFact in tupleElements:
            locateFactInTuple(tupleFact, tuplesByTupleID, ixNStag)

        for modelInlineFact in htmlElement.iterdescendants(tag=(ixNStag + '*')):
            if isinstance(modelInlineFact, ModelInlineFact):
                if modelInlineFact.localName in ('nonNumeric', 'nonFraction', 'fraction'):
                    factTargetIDs.add(modelInlineFact.get('target'))
                    if modelInlineFact.qname is not None:
                        if modelInlineFact.concept is None:
                            modelXbrl.error(ixMsgCode('missingReferences', modelInlineFact, name='references', sect='validation'), (_('Instance fact missing schema definition: %(qname)s of Inline Element %(localName)s')),
                              modelObject=modelInlineFact,
                              qname=(modelInlineFact.qname),
                              localName=(modelInlineFact.elementQname))
                        else:
                            if modelInlineFact.isFraction == (modelInlineFact.localName == 'fraction'):
                                mdlDoc.modelXbrl.factsInInstance.add(modelInlineFact)
                                locateFactInTuple(modelInlineFact, tuplesByTupleID, ixNStag)
                                locateContinuation(modelInlineFact)
                                for r in modelInlineFact.footnoteRefs:
                                    footnoteRefs[r].append(modelInlineFact)

                                if modelInlineFact.id:
                                    factsByFactID[modelInlineFact.id] = modelInlineFact
                            else:
                                modelXbrl.error(ixMsgCode('fractionDeclaration', modelInlineFact, name='fraction', sect='validation'), (_('Inline XBRL element %(qname)s base type %(type)s mapped by %(localName)s')),
                                  modelObject=modelInlineFact,
                                  qname=(modelInlineFact.qname),
                                  localName=(modelInlineFact.elementQname),
                                  type=(modelInlineFact.concept.baseXsdType))

        for tupleFact in tupleElements:
            for order, facts in tupleFact.unorderedTupleFacts.items():
                if len(facts) > 1:
                    all(normalizeSpace(facts[0].value) == normalizeSpace(f.value) and all(normalizeSpace(facts[0].get(attr)) == normalizeSpace(f.get(attr)) for attr in facts[0].keys() if attr != 'order') for f in facts[1:]) or modelXbrl.error(ixMsgCode('tupleSameOrderMembersUnequal', (facts[0]), sect='validation'), (_('Inline XBRL tuple members %(qnames)s values %(values)s and attributes not whitespace-normalized equal')),
                      modelObject=facts,
                      qnames=(', '.join(str(f.qname) for f in facts)),
                      values=(', '.join(f.value for f in facts)))

            checkTupleIxDescendants(tupleFact, tupleFact)
            tupleFact.modelTupleFacts = [facts[0] for order, facts in sorted((tupleFact.unorderedTupleFacts.items()), key=(lambda i: i[0])) if len(facts) > 0]

        def checkForTupleCycle(parentTuple, tupleNesting):
            for fact in parentTuple.modelTupleFacts:
                if fact in tupleNesting:
                    tupleNesting.append(fact)
                    modelXbrl.error(ixMsgCode('tupleNestingCycle', fact, sect='validation'), (_('Tuple nesting cycle: %(tupleCycle)s')),
                      modelObject=tupleNesting,
                      tupleCycle=('->'.join(str(t.qname) for t in tupleNesting)))
                    tupleNesting.pop()
                else:
                    tupleNesting.append(fact)
                    checkForTupleCycle(fact, tupleNesting)
                    tupleNesting.pop()

        for tupleFact in tupleElements:
            checkForTupleCycle(tupleFact, [tupleFact])

        fractionTermTags = (
         ixNStag + 'numerator', ixNStag + 'denominator')
        for rootModelFact in modelXbrl.facts:
            if rootModelFact.localName == 'fraction':
                numDenom = [
                 None, None]
                for i, tag in enumerate(fractionTermTags):
                    for modelInlineFractionTerm in rootModelFact.iterchildren(tag=tag):
                        xmlValidate(modelXbrl, modelInlineFractionTerm, ixFacts=True)
                        if modelInlineFractionTerm.xValid >= VALID:
                            numDenom[i] = modelInlineFractionTerm.xValue

                rootModelFact._fractionValue = numDenom
            xmlValidate(modelXbrl, rootModelFact, ixFacts=True)

    if len(targetReferenceAttrs) == 0:
        modelXbrl.error(ixMsgCode('missingReferences', None, name='references', sect='validation'), (_('There must be at least one reference')),
          modelObject=modelXbrl)
    if factTargetIDs - set(targetReferenceAttrs.keys()):
        modelXbrl.error(ixMsgCode('missingReferenceTargets', None, name='references', sect='validation'), (_('Instance fact targets without reference: %(missingReferenceTargets)s')),
          modelObject=modelXbrl,
          missingReferenceTargets=(','.join(sorted(('(default)' if t is None else t) for t in factTargetIDs - set(targetReferenceAttrs.keys())))))
    del targetReferenceAttrs
    del factTargetIDs
    footnoteLinkPrototypes = {}
    for htmlElement in modelXbrl.ixdsHtmlElements:
        mdlDoc = htmlElement.modelDocument
        for modelInlineFootnote in htmlElement.iterdescendants(tag=(XbrlConst.qnIXbrlFootnote.clarkNotation)):
            if isinstance(modelInlineFootnote, ModelObject):
                linkrole = modelInlineFootnote.get('footnoteLinkRole', XbrlConst.defaultLinkRole)
                arcrole = modelInlineFootnote.get('arcrole', XbrlConst.factFootnote)
                footnoteID = modelInlineFootnote.footnoteID or ''
                footnoteLocLabel = footnoteID + '_loc'
                if linkrole in footnoteLinkPrototypes:
                    linkPrototype = footnoteLinkPrototypes[linkrole]
                else:
                    linkPrototype = LinkPrototype(mdlDoc, mdlDoc.xmlRootElement, XbrlConst.qnLinkFootnoteLink, linkrole)
                    footnoteLinkPrototypes[linkrole] = linkPrototype
                    for baseSetKey in (('XBRL-footnotes', None, None, None),
                     (
                      'XBRL-footnotes', linkrole, None, None),
                     (
                      arcrole, linkrole, XbrlConst.qnLinkFootnoteLink, XbrlConst.qnLinkFootnoteArc),
                     (
                      arcrole, linkrole, None, None),
                     (
                      arcrole, None, None, None)):
                        modelXbrl.baseSets[baseSetKey].append(linkPrototype)

                for modelFact in footnoteRefs[footnoteID]:
                    locPrototype = LocPrototype(mdlDoc, linkPrototype, footnoteLocLabel, modelFact)
                    linkPrototype.childElements.append(locPrototype)
                    linkPrototype.labeledResources[footnoteLocLabel].append(locPrototype)

                linkPrototype.childElements.append(modelInlineFootnote)
                linkPrototype.labeledResources[footnoteID].append(modelInlineFootnote)
                linkPrototype.childElements.append(ArcPrototype(mdlDoc, linkPrototype, (XbrlConst.qnLinkFootnoteArc), footnoteLocLabel,
                  footnoteID, linkrole,
                  arcrole, sourceElement=modelInlineFootnote))

        linkPrototypes = {}
        for modelInlineRel in htmlElement.iterdescendants(tag=(XbrlConst.qnIXbrl11Relationship.clarkNotation)):
            if isinstance(modelInlineRel, ModelObject):
                linkrole = modelInlineRel.get('linkRole', XbrlConst.defaultLinkRole)
                if linkrole not in linkPrototypes:
                    linkPrototypes[linkrole] = LinkPrototype(mdlDoc, (mdlDoc.xmlRootElement), (XbrlConst.qnLinkFootnoteLink), linkrole, sourceElement=modelInlineRel)

        modelInlineFootnotesById = {}
        linkModelInlineFootnoteIds = defaultdict(set)
        linkModelLocIds = defaultdict(set)
        for modelInlineFootnote in htmlElement.iterdescendants(tag=(XbrlConst.qnIXbrl11Footnote.clarkNotation)):
            if isinstance(modelInlineFootnote, ModelObject):
                locateContinuation(modelInlineFootnote)
                modelInlineFootnotesById[modelInlineFootnote.footnoteID] = modelInlineFootnote

        for modelInlineRel in htmlElement.iterdescendants(tag=(XbrlConst.qnIXbrl11Relationship.clarkNotation)):
            if isinstance(modelInlineRel, ModelObject):
                linkrole = modelInlineRel.get('linkRole', XbrlConst.defaultLinkRole)
                arcrole = modelInlineRel.get('arcrole', XbrlConst.factFootnote)
                linkPrototype = linkPrototypes[linkrole]
                for baseSetKey in (('XBRL-footnotes', None, None, None),
                 (
                  'XBRL-footnotes', linkrole, None, None),
                 (
                  arcrole, linkrole, XbrlConst.qnLinkFootnoteLink, XbrlConst.qnLinkFootnoteArc),
                 (
                  arcrole, linkrole, None, None),
                 (
                  arcrole, None, None, None)):
                    if linkPrototype not in modelXbrl.baseSets[baseSetKey]:
                        modelXbrl.baseSets[baseSetKey].append(linkPrototype)

                fromLabels = set()
                for fromId in modelInlineRel.get('fromRefs', '').split():
                    fromLabels.add(fromId)
                    if fromId not in linkModelLocIds[linkrole]:
                        linkModelLocIds[linkrole].add(fromId)
                        locPrototype = LocPrototype(mdlDoc, linkPrototype, fromId, fromId, sourceElement=modelInlineRel)
                        linkPrototype.childElements.append(locPrototype)
                        linkPrototype.labeledResources[fromId].append(locPrototype)

                toLabels = set()
                toFootnoteIds = set()
                toFactQnames = set()
                fromToMatchedIds = set()
                toIdsNotFound = []
                for toId in modelInlineRel.get('toRefs', '').split():
                    toLabels.add(toId)
                    if toId in modelInlineFootnotesById:
                        toFootnoteIds.add(toId)
                        modelInlineFootnote = modelInlineFootnotesById[toId]
                        if toId not in linkModelInlineFootnoteIds[linkrole]:
                            linkPrototype.childElements.append(modelInlineFootnote)
                            linkModelInlineFootnoteIds[linkrole].add(toId)
                            linkPrototype.labeledResources[toId].append(modelInlineFootnote)
                        else:
                            if toId in factsByFactID:
                                if toId not in linkModelLocIds[linkrole]:
                                    linkModelLocIds[linkrole].add(toId)
                                    locPrototype = LocPrototype(mdlDoc, linkPrototype, toId, toId, sourceElement=modelInlineRel)
                                    toFactQnames.add(str(locPrototype.dereference().qname))
                                    linkPrototype.childElements.append(locPrototype)
                                    linkPrototype.labeledResources[toId].append(locPrototype)
                            else:
                                toIdsNotFound.append(toId)
                        if toId in fromLabels:
                            fromToMatchedIds.add(toId)

                if toIdsNotFound:
                    modelXbrl.error(ixMsgCode('relationshipToRef', ns=(XbrlConst.ixbrl11), name='relationship', sect='validation'), (_('Inline relationship toRef(s) %(toIds)s not found.')),
                      modelObject=modelInlineRel,
                      toIds=(', '.join(sorted(toIdsNotFound))))
                if fromToMatchedIds:
                    modelXbrl.error(ixMsgCode('relationshipFromToMatch', ns=(XbrlConst.ixbrl11), name='relationship', sect='validation'), (_('Inline relationship has matching values in fromRefs and toRefs: %(fromToMatchedIds)s')),
                      modelObject=modelInlineRel,
                      fromToMatchedIds=(', '.join(sorted(fromToMatchedIds))))
                for fromLabel in fromLabels:
                    for toLabel in toLabels:
                        linkPrototype.childElements.append(ArcPrototype(mdlDoc, linkPrototype, (XbrlConst.qnLinkFootnoteArc), fromLabel,
                          toLabel, linkrole,
                          arcrole, (modelInlineRel.get('order', '1')),
                          sourceElement=modelInlineRel))

                if toFootnoteIds and toFactQnames:
                    modelXbrl.error(ixMsgCode('relationshipReferencesMixed', ns=(XbrlConst.ixbrl11), name='relationship', sect='validation'), (_('Inline relationship references footnote(s) %(toFootnoteIds)s and thereby is not allowed to reference %(toFactQnames)s.')),
                      modelObject=modelInlineRel,
                      toFootnoteIds=(', '.join(sorted(toFootnoteIds))),
                      toFactQnames=(', '.join(sorted(toFactQnames))))

        del linkPrototypes
        del modelInlineFootnotesById
        del linkModelInlineFootnoteIds

    for _contAt, _contReferences in continuationReferences.items():
        if len(_contReferences) > 1:
            _refEltQnames = set(str(_contRef.elementQname) for _contRef in _contReferences)
            modelXbrl.error(ixMsgCode('continuationReferences', ns=(XbrlConst.ixbrl11), name='continuation', sect='validation'), (_('continuedAt %(continuedAt)s has %(referencesCount)s references on %(sourceElements)s elements, only one reference allowed.')),
              modelObject=_contReferences,
              continuedAt=_contAt,
              referencesCount=(len(_contReferences)),
              sourceElements=(', '.join(str(qn) for qn in sorted(_refEltQnames))))

    for _contAt, _contElt in continuationElements.items():
        if _contAt not in continuationReferences:
            modelXbrl.error(ixMsgCode('continuationNotReferenced', ns=(XbrlConst.ixbrl11), name='continuation', sect='validation'), (_('ix:continuation %(continuedAt)s is not referenced by a, ix:footnote, ix:nonNumeric or other ix:continuation element.')),
              modelObject=_contElt,
              continuedAt=_contAt)

    del modelXbrl.ixdsHtmlElements


class LoadingException(Exception):
    pass


class ModelDocumentReference:

    def __init__(self, referenceType, referringModelObject=None):
        self.referenceType = referenceType
        self.referringModelObject = referringModelObject