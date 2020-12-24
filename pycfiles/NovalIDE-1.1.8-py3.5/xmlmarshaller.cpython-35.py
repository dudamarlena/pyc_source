# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/util/xmlmarshaller.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 54385 bytes
from __future__ import print_function
import sys
from types import *
import logging, xml.sax, xml.sax.handler, xml.sax.saxutils, datetime, noval.util.utillang as utillang, noval.util.objutils as objutils, noval.util.apputils as apputils, noval.util.logger as logger
MODULE_PATH = '__main__'
try:
    long
    unicode
    basestring
except:
    long = int
    unicode = str
    basestring = str

xmlMarshallerLogger = logging.getLogger('novalide.util.xmlmarshaller.marshal')

def ag_className(obj):
    return obj.__class__.__name__


class Error(Exception):
    __doc__ = 'Base class for errors in this module.'


class UnhandledTypeException(Error):
    __doc__ = 'Exception raised when attempting to marshal an unsupported\n    type.\n    '

    def __init__(self, typename):
        self.typename = typename

    def __str__(self):
        return '%s is not supported for marshalling.' % str(self.typename)


class XMLAttributeIsNotStringType(Error):
    __doc__ = 'Exception raised when an object"s attribute is specified to be\n    marshalled as an XML attribute of the enclosing object instead of\n    a nested element.\n    '

    def __init__(self, attrname, typename):
        self.attrname = attrname
        self.typename = typename

    def __str__(self):
        return '%s was set to be marshalled as an XML attribute\n        instead of a nested element, but the object"s type is %s, not\n        string.' % (self.attrname, self.typename)


class MarshallerException(Exception):
    pass


class UnmarshallerException(Exception):
    pass


XMLNS = 'xmlns'
XMLNS_PREFIX = XMLNS + ':'
XMLNS_PREFIX_LENGTH = len(XMLNS_PREFIX)
DEFAULT_NAMESPACE_KEY = '__DEFAULTNS__'
TYPE_QNAME = 'QName'
XMLSCHEMA_XSD_URL = 'http://www.w3.org/2001/XMLSchema'
AG_URL = 'http://www.activegrid.com/ag.xsd'
BASETYPE_ELEMENT_NAME = 'item'
DICT_ITEM_NAME = 'qqDictItem'
DICT_ITEM_KEY_NAME = 'key'
DICT_ITEM_VALUE_NAME = 'value'

def setattrignorecase(object, name, value):
    if name not in object.__dict__:
        namelow = name.lower()
        for attr in object.__dict__:
            if attr.lower() == namelow:
                object.__dict__[attr] = value
                return

    object.__dict__[name] = value


def getComplexType(obj):
    if hasattr(obj, '_instancexsdcomplextype'):
        return obj._instancexsdcomplextype
    if hasattr(obj, '__xsdcomplextype__'):
        return obj.__xsdcomplextype__


def _objectfactory(objtype, objargs=None, objclass=None):
    """dynamically create an object based on the objtype and return it."""
    if not isinstance(objargs, list):
        objargs = [
         objargs]
    if objclass != None:
        obj = None
        if len(objargs) > 0:
            if hasattr(objclass, '__xmlcdatacontent__'):
                obj = objclass()
                contentAttr = obj.__xmlcdatacontent__
                obj.__dict__[contentAttr] = str(objargs[0])
            else:
                obj = objclass(*objargs)
        else:
            obj = objclass()
        if obj != None and hasattr(obj, 'postUnmarshal'):
            obj.postUnmarshal()
        return obj
    return objutils.newInstance(objtype, objargs)


class GenericXMLObject(object):

    def __init__(self, content=None):
        if content != None:
            self._content = content
            self.__xmlcontent__ = '_content'

    def __str__(self):
        return 'GenericXMLObject(%s)' % objutils.toDiffableString(self.__dict__)

    def setXMLAttributes(self, xmlName, attrs=None, children=None, nsMap=None, defaultNS=None):
        if xmlName != None:
            i = xmlName.rfind(':')
            if i < 0:
                pass
            self.__xmlname__ = xmlName
            if defaultNS != None:
                self.__xmldefaultnamespace__ = str(defaultNS)
        else:
            self.__xmlname__ = xmlName[i + 1:]
            prefix = xmlName[:i]
            if nsMap.has_key(prefix):
                self.__xmldefaultnamespace__ = str(nsMap[prefix])
            if attrs != None:
                for attrname, attr in attrs.items():
                    attrname = str(attrname)
                    if not attrname == XMLNS:
                        if attrname.startswith(XMLNS_PREFIX):
                            pass
                        else:
                            if attrname == 'objtype':
                                pass
                            else:
                                if not hasattr(self, '__xmlattributes__'):
                                    self.__xmlattributes__ = []
                                i = attrname.rfind(':')
                                if i >= 0:
                                    prefix = attrname[:i]
                                    attrname = attrname[i + 1:]
                                    if not hasattr(self, '__xmlattrnamespaces__'):
                                        self.__xmlattrnamespaces__ = {}
                                    if self.__xmlattrnamespaces__.has_key(prefix):
                                        alist = self.__xmlattrnamespaces__[prefix]
                                    else:
                                        alist = []
                                    alist.append(attrname)
                                    self.__xmlattrnamespaces__[prefix] = alist
                                self.__xmlattributes__.append(attrname)

                if hasattr(self, '__xmlattributes__'):
                    self.__xmlattributes__.sort()
            if children != None and len(children) > 0:
                childList = []
                flattenList = {}
                for childname, child in children:
                    childstr = str(childname)
                    if childstr in childList:
                        if not flattenList.has_key(childstr):
                            flattenList[childstr] = (
                             childstr,)
                        else:
                            childList.append(childstr)

                if len(flattenList) > 0:
                    self.__xmlflattensequence__ = flattenList

    def initialize(self, arg1=None):
        pass


class Element:

    def __init__(self, name, attrs=None, xsname=None):
        self.name = name
        self.attrs = attrs
        self.content = ''
        self.children = []
        self.objclass = None
        self.xsname = xsname
        self.objtype = None

    def getobjtype(self):
        objtype = self.objtype
        if objtype == None:
            if len(self.children) > 0:
                objtype = 'dict'
        else:
            objtype = 'str'
        return objtype


class NsElement(object):

    def __init__(self):
        self.nsMap = {}
        self.targetNS = None
        self.defaultNS = None
        self.prefix = None

    def __str__(self):
        if self.prefix == None:
            strVal = 'prefix = None; '
        else:
            strVal = 'prefix = "%s"; ' % self.prefix
        if self.targetNS == None:
            strVal += 'targetNS = None; '
        else:
            strVal += 'targetNS = "%s"; ' % self.targetNS
        if self.defaultNS == None:
            strVal += 'defaultNS = None; '
        else:
            strVal += 'defaultNS = "%s"; ' % self.defaultNS
        if len(self.nsMap) == 0:
            strVal += 'nsMap = None; '
        else:
            strVal += 'nsMap = {'
            for ik, iv in self.nsMap.iteritems():
                strVal += '%s=%s; ' % (ik, iv)

            strVal += '}'
        return strVal

    def setKnownTypes(self, masterKnownTypes, masterKnownNamespaces, parentNSE):
        if parentNSE != None:
            self.knownTypes = parentNSE.knownTypes.copy()
            if self.defaultNS != None and parentNSE.defaultNS != self.defaultNS:
                newKT = self.knownTypes.copy()
                for tag in newKT:
                    if tag.find(':') < 0:
                        del self.knownTypes[tag]

            newMap = parentNSE.nsMap.copy()
            if self.nsMap != {}:
                for k, v in self.nsMap.iteritems():
                    newMap[k] = v

            self.nsMap = newMap
        else:
            self.knownTypes = {}
        reversedKNS = {}
        for long, short in masterKnownNamespaces.iteritems():
            reversedKNS[short] = long

        mapLongs = self.nsMap.values()
        for tag, mapClass in masterKnownTypes.iteritems():
            i = tag.rfind(':')
            if i >= 0:
                knownTagShort = tag[:i]
                knownTagName = tag[i + 1:]
                knownTagLong = reversedKNS[knownTagShort]
                if knownTagLong in mapLongs:
                    for mShort, mLong in self.nsMap.iteritems():
                        if mLong == knownTagLong:
                            actualShort = mShort
                            actualTag = '%s:%s' % (actualShort, knownTagName)
                            self.knownTypes[actualTag] = mapClass
                            break

                if self.defaultNS == knownTagLong:
                    self.knownTypes[knownTagName] = mapClass
                else:
                    self.knownTypes[tag] = mapClass

    def expandQName(self, eName, attrName, attrValue):
        bigValue = attrValue
        i = attrValue.rfind(':')
        if i < 0:
            if self.defaultNS != None:
                bigValue = '%s:%s' % (self.defaultNS, attrValue)
        else:
            attrNS = attrValue[:i]
            attrNCName = attrValue[i + 1:]
            for shortNs, longNs in self.nsMap.iteritems():
                if shortNs == attrNS:
                    bigValue = '%s:%s' % (longNs, attrNCName)
                    break

        return bigValue


class XMLObjectFactory(xml.sax.ContentHandler):

    def __init__(self, knownTypes=None, knownNamespaces=None, xmlSource=None, createGenerics=False):
        self.rootelement = None
        if xmlSource == None:
            self.xmlSource = 'unknown'
        else:
            self.xmlSource = xmlSource
        self.createGenerics = createGenerics
        self.skipper = False
        self.elementstack = []
        self.nsstack = []
        self.collectContent = None
        if knownNamespaces == None:
            self.knownNamespaces = {}
        else:
            self.knownNamespaces = knownNamespaces
        self.reversedNamespaces = {}
        for longns, shortns in self.knownNamespaces.items():
            self.reversedNamespaces[shortns] = longns

        self.knownTypes = {}
        if knownTypes != None:
            for tag, cls in knownTypes.items():
                i = tag.rfind(':')
                if i >= 0:
                    shortns = tag[:i]
                    tag = tag[i + 1:]
                    if shortns not in self.reversedNamespaces:
                        errorString = 'Error unmarshalling XML document from source "%s": knownTypes specifies an unmapped short namespace "%s" for element "%s"' % (self.xmlSource, shortns, tag)
                        raise UnmarshallerException(errorString)
                    longns = self.reversedNamespaces[shortns]
                    tag = '%s:%s' % (longns, tag)
                self.knownTypes[tag] = cls

        xml.sax.handler.ContentHandler.__init__(self)

    def appendElementStack(self, newElement, newNS):
        self.elementstack.append(newElement)
        if len(self.nsstack) > 0:
            oldNS = self.nsstack[(-1)]
            if newNS.defaultNS == None:
                newNS.defaultNS = oldNS.defaultNS
            if newNS.targetNS == None:
                newNS.targetNS = oldNS.targetNS
            if len(newNS.nsMap) == 0:
                newNS.nsMap = oldNS.nsMap
        elif len(oldNS.nsMap) > 0:
            map = oldNS.nsMap.copy()
            map.update(newNS.nsMap)
            newNS.nsMap = map
        self.nsstack.append(newNS)
        return newNS

    def popElementStack(self):
        element = self.elementstack.pop()
        nse = self.nsstack.pop()
        return (element, nse)

    def startElement(self, name, attrs):
        if name == 'xs:annotation' or name == 'xsd:annotation':
            self.skipper = True
            self.appendElementStack(Element(name, attrs.copy()), NsElement())
        if self.skipper:
            return
        if self.collectContent != None:
            strVal = '<%s' % name
            for aKey, aVal in attrs.items():
                strVal += ' %s="%s"' % (aKey, aVal)

            strVal += '>'
            self.collectContent.content += strVal
        xsname = name
        i = name.rfind(':')
        if i >= 0:
            nsname = name[:i]
            name = name[i + 1:]
        else:
            nsname = None
        element = Element(name, attrs.copy(), xsname=xsname)
        nse = NsElement()
        objtype = None
        for k in attrs.getNames():
            if k.startswith('xmlns'):
                longNs = attrs[k]
                eLongNs = longNs + '/'
                if str(eLongNs) in self.knownNamespaces:
                    longNs = eLongNs
                if k == 'xmlns':
                    nse.defaultNS = longNs
                else:
                    shortNs = k[6:]
                    nse.nsMap[shortNs] = longNs
            else:
                if k == 'targetNamespace':
                    nse.targetNS = attrs.getValue(k)
                elif k == 'objtype':
                    objtype = attrs.getValue(k)

        nse = self.appendElementStack(element, nse)
        if nsname != None:
            if nsname in nse.nsMap:
                longname = '%s:%s' % (nse.nsMap[nsname], name)
            else:
                if self.reversedNamespaces.has_key(nsname):
                    longname = '%s:%s' % (self.reversedNamespaces[nsname], name)
                else:
                    longname = xsname
        else:
            if nse.defaultNS != None:
                longname = '%s:%s' % (nse.defaultNS, name)
            else:
                longname = name
        element.objtype = objtype
        element.objclass = self.knownTypes.get(longname)
        if element.objclass == None and len(self.knownNamespaces) == 0:
            element.objclass = self.knownTypes.get(name)
        if hasattr(element.objclass, '__xmlcontent__'):
            self.collectContent = element

    def characters(self, content):
        if content != None:
            if self.collectContent != None:
                self.collectContent.content += content
        else:
            self.elementstack[(-1)].content += content

    def endElement(self, name):
        xsname = name
        i = name.rfind(':')
        if i >= 0:
            name = name[i + 1:]
        if self.skipper:
            if xsname == 'xs:annotation' or xsname == 'xsd:annotation':
                self.skipper = False
                self.popElementStack()
            return
        if self.collectContent != None:
            if xsname != self.collectContent.xsname:
                self.collectContent.content += '</%s>' % xsname
                self.popElementStack()
                return
            self.collectContent = None
        oldChildren = self.elementstack[(-1)].children
        element, nse = self.popElementStack()
        if len(self.elementstack) > 1 and self.elementstack[(-1)].getobjtype() == 'None':
            parentElement = self.elementstack[(-2)]
        else:
            if len(self.elementstack) > 0:
                parentElement = self.elementstack[(-1)]
            objtype = element.getobjtype()
            if objtype == 'None':
                return
            constructorarglist = []
            if len(element.content) > 0:
                strippedElementContent = element.content.strip()
                if len(strippedElementContent) > 0:
                    constructorarglist.append(element.content)
            if element.objclass == None and element.attrs.get('objtype') == None and (len(element.attrs) > 0 or len(element.children) > 0) and self.createGenerics:
                element.objclass = GenericXMLObject
            obj = _objectfactory(objtype, constructorarglist, element.objclass)
            if element.objclass == GenericXMLObject:
                obj.setXMLAttributes(str(xsname), element.attrs, element.children, nse.nsMap, nse.defaultNS)
            complexType = getComplexType(obj)
            if obj != None and hasattr(obj, '__xmlname__') and getattr(obj, '__xmlname__') == 'sequence':
                self.elementstack[(-1)].children = oldChildren
                return
            if len(element.attrs) > 0 and not isinstance(obj, list):
                for attrname, attr in element.attrs.items():
                    if attrname == XMLNS or attrname.startswith(XMLNS_PREFIX):
                        if attrname.startswith(XMLNS_PREFIX):
                            ns = attrname[XMLNS_PREFIX_LENGTH:]
                    else:
                        ns = ''
                    if complexType != None or element.objclass == GenericXMLObject:
                        if not hasattr(obj, '__xmlnamespaces__'):
                            obj.__xmlnamespaces__ = {ns: attr}
                        elif ns not in obj.__xmlnamespaces__:
                            if hasattr(obj.__class__, '__xmlnamespaces__') and obj.__xmlnamespaces__ is obj.__class__.__xmlnamespaces__:
                                obj.__xmlnamespaces__ = dict(obj.__xmlnamespaces__)
                            obj.__xmlnamespaces__[ns] = attr
                    elif not attrname == 'objtype':
                        if attrname.find(':') > -1:
                            attrname = attrname[attrname.find(':') + 1:]
                        if complexType != None:
                            xsdElement = complexType.findElement(attrname)
                            if xsdElement != None:
                                type = xsdElement.type
                                if type != None:
                                    if type == TYPE_QNAME:
                                        attr = nse.expandQName(name, attrname, attr)
                                    type = xsdToLangType(type)
                                    if attrname == 'maxOccurs' and attr == 'unbounded':
                                        attr = '-1'
                                    try:
                                        attr = _objectfactory(type, attr)
                                    except Exception as exceptData:
                                        errorString = 'Error unmarshalling attribute "%s" at line %d, column %d in XML document from source "%s": %s' % (attrname, self._locator.getLineNumber(), self._locator.getColumnNumber(), self.xmlSource, str(exceptData))
                                        raise UnmarshallerException(errorString)

                                    try:
                                        setattrignorecase(obj, _toAttrName(obj, attrname), attr)
                                    except AttributeError:
                                        errorString = 'Error setting value of attribute "%s" at line %d, column %d in XML document from source "%s": object type of XML element "%s" is not specified or known' % (attrname, self._locator.getLineNumber(), self._locator.getColumnNumber(), self.xmlSource, name)
                                        raise UnmarshallerException(errorString)

            flattenDict = {}
            if hasattr(obj, '__xmlflattensequence__'):
                flatten = obj.__xmlflattensequence__
                if isinstance(flatten, dict):
                    for sequencename, xmlnametuple in flatten.items():
                        if xmlnametuple == None:
                            flattenDict[sequencename] = sequencename
                        else:
                            if not isinstance(xmlnametuple, (tuple, list)):
                                flattenDict[str(xmlnametuple)] = sequencename
                            else:
                                for xmlname in xmlnametuple:
                                    flattenDict[xmlname] = sequencename

                else:
                    raise Exception('Invalid type for __xmlflattensequence___ : it must be a dict')
                for childname, child in element.children:
                    if childname in flattenDict:
                        sequencename = _toAttrName(obj, flattenDict[childname])
                        if not hasattr(obj, sequencename):
                            obj.__dict__[sequencename] = []
                        sequencevalue = getattr(obj, sequencename)
                        if sequencevalue == None:
                            obj.__dict__[sequencename] = []
                            sequencevalue = getattr(obj, sequencename)
                        sequencevalue.append(child)
                    elif objtype == 'list':
                        obj.append(child)
                    elif isinstance(obj, dict):
                        if childname == DICT_ITEM_NAME:
                            obj[child[DICT_ITEM_KEY_NAME]] = child[DICT_ITEM_VALUE_NAME]
                        else:
                            obj[childname] = child
                    else:
                        childAttrName = _toAttrName(obj, childname)
                        if not hasattr(obj, childAttrName) or getattr(obj, childAttrName) == None or getattr(obj, childAttrName) == [] or not isinstance(child, GenericXMLObject):
                            try:
                                setattrignorecase(obj, childAttrName, child)
                            except AttributeError:
                                raise MarshallerException('Error unmarshalling child element "%s" of XML element "%s": object type not specified or known' % (childname, name))

                if complexType != None:
                    for element in complexType.elements:
                        if element.default:
                            elementName = _toAttrName(obj, element.name)
                            if elementName not in obj.__dict__ or obj.__dict__[elementName] == None:
                                langType = xsdToLangType(element.type)
                                defaultValue = _objectfactory(langType, element.default)
                                obj.__dict__[elementName] = defaultValue

                if isinstance(obj, list) and element.attrs.has_key('mutable') and element.attrs.getValue('mutable') == 'false':
                    obj = tuple(obj)
                if len(self.elementstack) > 0:
                    parentElement.children.append((name, obj))
                else:
                    self.rootelement = obj

    def getRootObject(self):
        return self.rootelement


def _toAttrName(obj, name):
    if hasattr(obj, '__xmlrename__'):
        for key, val in obj.__xmlrename__.items():
            if name == val:
                name = key
                break

    return str(name)


def printKnownTypes(kt, where):
    print('KnownTypes from %s' % where)
    for tag, cls in kt.iteritems():
        print('%s => %s' % (tag, str(cls)))


__typeMappingXsdToLang = {'string': 'str', 
 'char': 'str', 
 'varchar': 'str', 
 'date': 'str', 
 'boolean': 'bool', 
 'decimal': 'float', 
 'int': 'int', 
 'integer': 'int', 
 'long': 'long', 
 'float': 'float', 
 'bool': 'bool', 
 'str': 'str', 
 'unicode': 'unicode', 
 'short': 'int', 
 'duration': 'str', 
 'datetime': 'str', 
 'time': 'str', 
 'double': 'float', 
 'QName': 'str', 
 'blob': 'str', 
 'currency': 'str'}

def xsdToLangType(xsdType):
    if xsdType.startswith(XMLSCHEMA_XSD_URL):
        xsdType = xsdType[len(XMLSCHEMA_XSD_URL) + 1:]
    elif xsdType.startswith(AG_URL):
        xsdType = xsdType[len(AG_URL) + 1:]
    langType = __typeMappingXsdToLang.get(xsdType)
    if langType == None:
        raise Exception('Unknown xsd type %s' % xsdType)
    return langType


def langToXsdType(langType):
    if langType in asDict(__typeMappingXsdToLang):
        return '%s:%s' % (XMLSCHEMA_XSD_URL, langType)
    return langType


def _getXmlValue(langValue):
    if isinstance(langValue, bool):
        return str(langValue).lower()
    else:
        if isinstance(langValue, unicode):
            return langValue.encode()
        return str(langValue)


def unmarshal(xmlstr, knownTypes=None, knownNamespaces=None, xmlSource=None, createGenerics=False):
    objectfactory = XMLObjectFactory(knownTypes, knownNamespaces, xmlSource, createGenerics)
    if not apputils.is_windows():
        xmlstr = str(xmlstr)
    try:
        xml.sax.parseString(xmlstr, objectfactory)
    except xml.sax.SAXParseException as errorData:
        if xmlSource == None:
            xmlSource = 'unknown'
        errorString = 'SAXParseException ("%s") detected at line %d, column %d in XML document from source "%s" ' % (errorData.getMessage(), errorData.getLineNumber(), errorData.getColumnNumber(), xmlSource)
        raise UnmarshallerException(errorString)

    return objectfactory.getRootObject()


def marshal(obj, elementName=None, prettyPrint=False, marshalType=True, indent=0, knownTypes=None, knownNamespaces=None, encoding=-1):
    global xmlMarshallerLogger
    worker = XMLMarshalWorker(prettyPrint=prettyPrint, marshalType=marshalType, knownTypes=knownTypes, knownNamespaces=knownNamespaces)
    if obj != None and hasattr(obj, '__xmldeepexclude__'):
        worker.xmldeepexclude = obj.__xmldeepexclude__
    xmlstr = ''.join(worker._marshal(obj, elementName, indent=indent))
    xmlMarshallerLogger.info('marshal produced string of type %s', type(xmlstr))
    if encoding == None:
        return xmlstr
    if not isinstance(encoding, basestring):
        encoding = sys.getdefaultencoding()
    if not isinstance(xmlstr, unicode):
        xmlstr = xmlstr.decode()
    xmlstr = '<?xml version="1.0" encoding="%s"?>\n%s' % (encoding, xmlstr)
    return xmlstr.encode(encoding)


class XMLMarshalWorker(object):

    def __init__(self, marshalType=True, prettyPrint=False, knownTypes=None, knownNamespaces=None):
        if knownTypes == None:
            self.knownTypes = {}
        else:
            self.knownTypes = knownTypes
        if knownNamespaces == None:
            self.knownNamespaces = {}
        else:
            self.knownNamespaces = knownNamespaces
        self.prettyPrint = prettyPrint
        self.marshalType = marshalType
        self.xmldeepexclude = []
        self.nsstack = []

    def getNSPrefix(self):
        if len(self.nsstack) > 0:
            return self.nsstack[(-1)].prefix
        return ''

    def isKnownType(self, elementName):
        tagLongNs = None
        nse = self.nsstack[(-1)]
        i = elementName.rfind(':')
        if i > 0:
            prefix = elementName[:i]
            name = elementName[i + 1:]
        else:
            prefix = DEFAULT_NAMESPACE_KEY
            name = elementName
        for shortNs, longNs in nse.nameSpaces.items():
            if shortNs == prefix:
                tagLongNs = longNs
                break

        if tagLongNs == None:
            knownTagName = elementName
        else:
            knownShortNs = self.knownNamespaces[tagLongNs]
            knownTagName = knownShortNs + ':' + name
        if knownTagName in self.knownTypes:
            knownClass = self.knownTypes[knownTagName]
            return True
        return False

    def popNSStack(self):
        self.nsstack.pop()

    def appendNSStack(self, obj):
        nameSpaces = {}
        defaultLongNS = None
        for nse in self.nsstack:
            for k, v in nse.nsMap.items():
                nameSpaces[k] = v
                if k == DEFAULT_NAMESPACE_KEY:
                    defaultLongNS = v

        newNS = NsElement()
        nameSpaceAttrs = ''
        if hasattr(obj, '__xmlnamespaces__'):
            ns = getattr(obj, '__xmlnamespaces__')
            keys = list(ns.keys())
            keys.sort()
            for nameSpaceKey in keys:
                nameSpaceUrl = ns[nameSpaceKey]
                if nameSpaceUrl in nameSpaces.values():
                    for k, v in nameSpaces.iteritems():
                        if v == nameSpaceUrl:
                            nameSpaceKey = k
                            break

                elif nameSpaceKey == '':
                    defaultLongNS = nameSpaceUrl
                    nameSpaces[DEFAULT_NAMESPACE_KEY] = nameSpaceUrl
                    newNS.nsMap[DEFAULT_NAMESPACE_KEY] = nameSpaceUrl
                    nameSpaceAttrs += ' xmlns="%s" ' % nameSpaceUrl
                else:
                    nameSpaces[nameSpaceKey] = nameSpaceUrl
                    newNS.nsMap[nameSpaceKey] = nameSpaceUrl
                    nameSpaceAttrs += ' xmlns:%s="%s" ' % (nameSpaceKey, nameSpaceUrl)

            nameSpaceAttrs = nameSpaceAttrs.rstrip()
        if len(self.nsstack) > 0:
            newNS.prefix = self.nsstack[(-1)].prefix
        else:
            newNS.prefix = ''
        if obj != None and hasattr(obj, '__xmldefaultnamespace__'):
            longPrefixNS = getattr(obj, '__xmldefaultnamespace__')
            if longPrefixNS == defaultLongNS:
                newNS.prefix = ''
            else:
                try:
                    for k, v in nameSpaces.items():
                        if v == longPrefixNS:
                            newNS.prefix = k + ':'
                            break

                except:
                    if longPrefixNS in self.knownNamespaces:
                        newNS.prefix = self.knownNamespaces[longPrefixNS] + ':'
                    else:
                        raise MarshallerException('Error marshalling __xmldefaultnamespace__ ("%s") not defined in namespace stack' % longPrefixNS)

            if obj != None and hasattr(obj, 'targetNamespace'):
                newNS.targetNS = obj.targetNamespace
        elif len(self.nsstack) > 0:
            newNS.targetNS = self.nsstack[(-1)].targetNS
        newNS.nameSpaces = nameSpaces
        self.nsstack.append(newNS)
        return nameSpaceAttrs

    def contractQName(self, value, obj, attr):
        value = langToXsdType(value)
        i = value.rfind(':')
        if i >= 0:
            longNS = value[:i]
        else:
            return value
        if longNS in self.nsstack[(-1)].nameSpaces.values():
            for kShort, vLong in self.nsstack[(-1)].nameSpaces.iteritems():
                if vLong == longNS:
                    shortNS = kShort
                    break

        else:
            shortNS = longNS
        if shortNS == DEFAULT_NAMESPACE_KEY:
            value = value[i + 1:]
        else:
            value = shortNS + ':' + value[i + 1:]
        return value

    def _genObjTypeStr(self, typeString):
        if self.marshalType:
            return ' objtype="%s"' % typeString
        return ''

    def _marshal(self, obj, elementName=None, nameSpacePrefix='', indent=0):
        if obj != None:
            xmlMarshallerLogger.debug('--> _marshal: elementName=%s%s, type=%s, obj=%s, indent=%d', nameSpacePrefix, elementName, type(obj), str(obj), indent)
        else:
            xmlMarshallerLogger.debug('--> _marshal: elementName=%s%s, obj is None, indent=%d', nameSpacePrefix, elementName, indent)
        if obj != None and hasattr(obj, 'preMarshal'):
            obj.preMarshal()
        excludeAttrs = []
        excludeAttrs.extend(self.xmldeepexclude)
        if hasattr(obj, '__xmlexclude__'):
            excludeAttrs.extend(obj.__xmlexclude__)
        prettyPrint = self.prettyPrint
        knownTypes = self.knownTypes
        xmlString = None
        if self.prettyPrint or indent:
            prefix = ' ' * indent
            newline = '\n'
            increment = 2
        else:
            prefix = ''
            newline = ''
            increment = 0
        nameSpaceAttrs = self.appendNSStack(obj)
        nameSpacePrefix = self.getNSPrefix()
        if not elementName:
            if hasattr(obj, '__xmlname__'):
                elementName = nameSpacePrefix + obj.__xmlname__
            else:
                elementName = nameSpacePrefix + BASETYPE_ELEMENT_NAME
        else:
            elementName = nameSpacePrefix + elementName
        if hasattr(obj, '__xmlsequencer__') and obj.__xmlsequencer__ != None:
            if XMLSCHEMA_XSD_URL in self.nsstack[(-1)].nameSpaces.values():
                for kShort, vLong in self.nsstack[(-1)].nameSpaces.iteritems():
                    if vLong == XMLSCHEMA_XSD_URL:
                        if kShort != DEFAULT_NAMESPACE_KEY:
                            xsdPrefix = kShort + ':'
                        else:
                            xsdPrefix = ''
                        break

            else:
                xsdPrefix = 'xs:'
            elementAdd = xsdPrefix + obj.__xmlsequencer__
        else:
            elementAdd = None
        members_to_skip = []
        members_to_skip.extend(excludeAttrs)
        objattrs = ''
        className = ag_className(obj)
        classNamePrefix = '_' + className
        if hasattr(obj, '__xmlattributes__'):
            xmlattributes = obj.__xmlattributes__
            members_to_skip.extend(xmlattributes)
            for attr in xmlattributes:
                internalAttrName = attr
                if attr.startswith('__') and not attr.endswith('__'):
                    internalAttrName = classNamePrefix + attr
                attrNameSpacePrefix = ''
                if hasattr(obj, '__xmlattrnamespaces__'):
                    for nameSpaceKey, nameSpaceAttributes in getattr(obj, '__xmlattrnamespaces__').items():
                        if nameSpaceKey == nameSpacePrefix[:-1]:
                            pass
                        elif attr in nameSpaceAttributes:
                            attrNameSpacePrefix = nameSpaceKey + ':'
                            break

                attrs = obj.__dict__
                value = attrs.get(internalAttrName)
                if hasattr(obj, '__xmlrename__') and attr in obj.__xmlrename__:
                    attr = obj.__xmlrename__[attr]
                xsdElement = None
                complexType = getComplexType(obj)
                if complexType != None:
                    xsdElement = complexType.findElement(attr)
                if xsdElement != None:
                    default = xsdElement.default
                    if default != None:
                        if not default == value:
                            if default == _getXmlValue(value):
                                pass
                            continue
                        else:
                            if value == None:
                                continue
                            elif xsdElement.type == TYPE_QNAME:
                                value = self.contractQName(value, obj, attr)
                    else:
                        if value == None:
                            continue
                        if attr == 'maxOccurs' and value == -1:
                            value = 'unbounded'
                        if isinstance(value, bool):
                            if value == True:
                                value = 'true'
                            else:
                                value = 'false'
                        else:
                            value = objutils.toDiffableRepr(value)
                    objattrs += ' %s%s="%s"' % (attrNameSpacePrefix, attr, utillang.escape(value))

        if obj == None:
            xmlString = [
             '']
        else:
            if isinstance(obj, bool):
                objTypeStr = self._genObjTypeStr('bool')
                xmlString = ['%s<%s%s>%s</%s>%s' % (prefix, elementName, objTypeStr, obj, elementName, newline)]
            else:
                if isinstance(obj, int):
                    objTypeStr = self._genObjTypeStr('int')
                    xmlString = ['%s<%s%s>%s</%s>%s' % (prefix, elementName, objTypeStr, str(obj), elementName, newline)]
                else:
                    if isinstance(obj, long):
                        objTypeStr = self._genObjTypeStr('long')
                        xmlString = ['%s<%s%s>%s</%s>%s' % (prefix, elementName, objTypeStr, str(obj), elementName, newline)]
                    else:
                        if isinstance(obj, float):
                            objTypeStr = self._genObjTypeStr('float')
                            xmlString = ['%s<%s%s>%s</%s>%s' % (prefix, elementName, objTypeStr, str(obj), elementName, newline)]
                        else:
                            if isinstance(obj, unicode):
                                xmlString = [
                                 '%s<%s>%s</%s>%s' % (prefix, elementName, utillang.escape(obj), elementName, newline)]
                            else:
                                if isinstance(obj, basestring):
                                    xmlString = [
                                     '%s<%s>%s</%s>%s' % (prefix, elementName, utillang.escape(obj.encode()), elementName, newline)]
                                else:
                                    if isinstance(obj, datetime.datetime):
                                        objTypeStr = self._genObjTypeStr('datetime')
                                        xmlString = ['%s<%s%s>%s</%s>%s' % (prefix, elementName, objTypeStr, str(obj), elementName, newline)]
                                    else:
                                        if isinstance(obj, datetime.date):
                                            objTypeStr = self._genObjTypeStr('date')
                                            xmlString = ['%s<%s%s>%s</%s>%s' % (prefix, elementName, objTypeStr, str(obj), elementName, newline)]
                                        else:
                                            if isinstance(obj, datetime.time):
                                                objTypeStr = self._genObjTypeStr('time')
                                                xmlString = ['%s<%s%s>%s</%s>%s' % (prefix, elementName, objTypeStr, str(obj), elementName, newline)]
                                            else:
                                                if isinstance(obj, list):
                                                    if len(obj) < 1:
                                                        xmlString = ''
                                                    else:
                                                        objTypeStr = self._genObjTypeStr('list')
                                                        xmlString = ['%s<%s%s>%s' % (prefix, elementName, objTypeStr, newline)]
                                                        for item in obj:
                                                            xmlString.extend(self._marshal(item, indent=indent + increment))

                                                        xmlString.append('%s</%s>%s' % (prefix, elementName, newline))
                                                else:
                                                    if isinstance(obj, tuple):
                                                        if len(obj) < 1:
                                                            xmlString = ''
                                                        else:
                                                            objTypeStr = self._genObjTypeStr('list')
                                                            xmlString = ['%s<%s%s mutable="false">%s' % (prefix, elementName, objTypeStr, newline)]
                                                            for item in obj:
                                                                xmlString.extend(self._marshal(item, indent=indent + increment))

                                                            xmlString.append('%s</%s>%s' % (prefix, elementName, newline))
                                                    else:
                                                        if isinstance(obj, dict):
                                                            objTypeStr = self._genObjTypeStr('dict')
                                                            xmlString = ['%s<%s%s>%s' % (prefix, elementName, objTypeStr, newline)]
                                                            subprefix = prefix + ' ' * increment
                                                            subindent = indent + 2 * increment
                                                            keys = obj.keys()
                                                            keys.sort()
                                                            for key in keys:
                                                                xmlString.append('%s<%s>%s' % (subprefix, DICT_ITEM_NAME, newline))
                                                                xmlString.extend(self._marshal(key, elementName=DICT_ITEM_KEY_NAME, indent=subindent))
                                                                xmlString.extend(self._marshal(obj[key], elementName=DICT_ITEM_VALUE_NAME, indent=subindent))
                                                                xmlString.append('%s</%s>%s' % (subprefix, DICT_ITEM_NAME, newline))

                                                            xmlString.append('%s</%s>%s' % (prefix, elementName, newline))
                                                        else:
                                                            if hasattr(obj, '__xmlcontent__'):
                                                                contentValue = getattr(obj, obj.__xmlcontent__)
                                                                if contentValue == None:
                                                                    xmlString = [
                                                                     '%s<%s%s%s/>%s' % (prefix, elementName, nameSpaceAttrs, objattrs, newline)]
                                                                else:
                                                                    contentValue = utillang.escape(contentValue)
                                                                    xmlString = ['%s<%s%s%s>%s</%s>%s' % (prefix, elementName, nameSpaceAttrs, objattrs, contentValue, elementName, newline)]
                                                            else:
                                                                if isinstance(obj, GenericXMLObject):
                                                                    objTypeStr = ''
                                                                else:
                                                                    if self.isKnownType(elementName) == True:
                                                                        objTypeStr = ''
                                                                    else:
                                                                        objTypeStr = self._genObjTypeStr('%s.%s' % (obj.__class__.__module__, className))
                                                                    xmlString = [
                                                                     '%s<%s%s%s%s' % (prefix, elementName, nameSpaceAttrs, objattrs, objTypeStr)]
                                                                    if elementAdd != None:
                                                                        prefix += increment * ' '
                                                                        indent += increment
                                                                    xmlMemberString = []
                                                                    if hasattr(obj, '__xmlbody__'):
                                                                        xmlbody = getattr(obj, obj.__xmlbody__)
                                                                        if xmlbody != None:
                                                                            xmlMemberString.append(utillang.escape(xmlbody))
                                                                    else:
                                                                        if hasattr(obj, '__xmlattrgroups__'):
                                                                            attrGroups = obj.__xmlattrgroups__.copy()
                                                                            if not isinstance(attrGroups, dict):
                                                                                raise Exception('__xmlattrgroups__ is not a dict, but must be')
                                                                            for n in attrGroups.iterkeys():
                                                                                members_to_skip.extend(attrGroups[n])

                                                                        else:
                                                                            attrGroups = {}
                                                                        eList = list(obj.__dict__.keys())
                                                                        eList.sort()
                                                                        attrGroups['__nogroup__'] = eList
                                                                        for eName, eList in attrGroups.items():
                                                                            if eName != '__nogroup__':
                                                                                prefix += increment * ' '
                                                                                indent += increment
                                                                                objTypeStr = self._genObjTypeStr('None')
                                                                                xmlMemberString.append('%s<%s%s>%s' % (prefix, eName, objTypeStr, newline))
                                                                            for name in eList:
                                                                                value = obj.__dict__[name]
                                                                                if eName == '__nogroup__' and name in members_to_skip:
                                                                                    pass
                                                                                else:
                                                                                    if name.startswith('__') and name.endswith('__'):
                                                                                        pass
                                                                                    else:
                                                                                        if hasattr(obj, '__xmlcdatacontent__') and obj.__xmlcdatacontent__ == name:
                                                                                            pass
                                                                                        else:
                                                                                            subElementNameSpacePrefix = nameSpacePrefix
                                                                                            if hasattr(obj, '__xmlattrnamespaces__'):
                                                                                                for nameSpaceKey, nameSpaceValues in getattr(obj, '__xmlattrnamespaces__').items():
                                                                                                    if name in nameSpaceValues:
                                                                                                        subElementNameSpacePrefix = nameSpaceKey + ':'
                                                                                                        break

                                                                                            if hasattr(obj, '__xmlflattensequence__') and value != None and name in obj.__xmlflattensequence__:
                                                                                                xmlnametuple = obj.__xmlflattensequence__[name]
                                                                                                if xmlnametuple == None:
                                                                                                    xmlnametuple = [
                                                                                                     name]
                                                                                                else:
                                                                                                    if not isinstance(xmlnametuple, (tuple, list)):
                                                                                                        xmlnametuple = [
                                                                                                         str(xmlnametuple)]
                                                                                                    xmlname = None
                                                                                                    if len(xmlnametuple) == 1:
                                                                                                        xmlname = xmlnametuple[0]
                                                                                                    if not isinstance(value, (list, tuple)):
                                                                                                        value = [
                                                                                                         value]
                                                                                                for seqitem in value:
                                                                                                    xmlMemberString.extend(self._marshal(seqitem, xmlname, subElementNameSpacePrefix, indent=indent + increment))

                                                                                            else:
                                                                                                if hasattr(obj, '__xmlrename__') and name in obj.__xmlrename__:
                                                                                                    xmlname = obj.__xmlrename__[name]
                                                                                                else:
                                                                                                    xmlname = name
                                                                                                if value != None:
                                                                                                    xmlMemberString.extend(self._marshal(value, xmlname, subElementNameSpacePrefix, indent=indent + increment))

                                                                            if eName != '__nogroup__':
                                                                                xmlMemberString.append('%s</%s>%s' % (prefix, eName, newline))
                                                                                prefix = prefix[:-increment]
                                                                                indent -= increment

                                                                    newList = []
                                                                    for s in xmlMemberString:
                                                                        if len(s) > 0:
                                                                            newList.append(s)

                                                                    xmlMemberString = newList
                                                                    if len(xmlMemberString) > 0:
                                                                        xmlString.append('>')
                                                                        if hasattr(obj, '__xmlbody__'):
                                                                            xmlString.extend(xmlMemberString)
                                                                            xmlString.append('</%s>%s' % (elementName, newline))
                                                                        else:
                                                                            xmlString.append(newline)
                                                                            if elementAdd != None:
                                                                                xmlString.append('%s<%s>%s' % (prefix, elementAdd, newline))
                                                                            xmlString.extend(xmlMemberString)
                                                                            if elementAdd != None:
                                                                                xmlString.append('%s</%s>%s' % (prefix, elementAdd, newline))
                                                                                prefix = prefix[:-increment]
                                                                                indent -= increment
                                                                            xmlString.append('%s</%s>%s' % (prefix, elementName, newline))
                                                                    else:
                                                                        if hasattr(obj, '__xmlcdatacontent__'):
                                                                            cdataAttr = obj.__xmlcdatacontent__
                                                                            cdataContent = obj.__dict__[cdataAttr]
                                                                            xmlString.append('><![CDATA[%s]]></%s>%s' % (cdataContent, elementName, newline))
                                                                        else:
                                                                            xmlString.append('/>%s' % newline)
        xmlMarshallerLogger.debug('<-- _marshal: %s', objutils.toDiffableString(xmlString))
        self.popNSStack()
        return xmlString


class MarshallerPerson:
    __xmlname__ = 'person'
    __xmlexclude__ = ['fabulousness']
    __xmlattributes__ = ('nonSmoker', )
    __xmlrename__ = {'_phoneNumber': 'telephone'}
    __xmlflattensequence__ = {'favoriteWords': ('vocabulary', )}
    __xmlattrgroups__ = {'name': ['firstName', 'lastName'], 'address': ['addressLine1', 'city', 'state', 'zip']}

    def setPerson(self):
        self.firstName = 'Albert'
        self.lastName = 'Camus'
        self.addressLine1 = '23 Absurd St.'
        self.city = 'Ennui'
        self.state = 'MO'
        self.zip = '54321'
        self._phoneNumber = '808-303-2323'
        self.favoriteWords = ['angst', 'ennui', 'existence']
        self.phobias = ['war', 'tuberculosis', 'cars']
        self.weight = 150
        self.fabulousness = 'tres tres'
        self.nonSmoker = False


if __name__ == '__main__':
    p1 = MarshallerPerson()
    p1.setPerson()
    xmlP1 = marshal(p1, prettyPrint=True, encoding='utf-8')
    print('\n########################')
    print('# testPerson test case #')
    print('########################')
    print(xmlP1)
    p2 = unmarshal(xmlP1)
    xmlP2 = marshal(p2, prettyPrint=True, encoding='utf-8')
    if xmlP1 == xmlP2:
        print('Success: repeated marshalling yields identical results')
else:
    print('Failure: repeated marshalling yields different results')
    print(xmlP2)