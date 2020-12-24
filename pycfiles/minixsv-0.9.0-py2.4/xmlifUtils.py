# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\genxmlif\xmlifUtils.py
# Compiled at: 2008-08-08 10:48:36
import string, re, os, urllib, urlparse
from types import StringTypes, TupleType
from xml.dom import EMPTY_PREFIX, EMPTY_NAMESPACE
_reWhitespace = re.compile('\\s')
_reWhitespaces = re.compile('\\s+')
_reSplitUrlApplication = re.compile('(file|http|ftp|gopher):(.+)')

def removeWhitespaces(strValue):
    return _reWhitespaces.sub('', strValue)


def collapseString(strValue, lstrip=1, rstrip=1):
    collStr = _reWhitespaces.sub(' ', strValue)
    if lstrip and rstrip:
        return collStr.strip()
    elif lstrip:
        return collStr.lstrip()
    elif rstrip:
        return collStr.rstrip()
    else:
        return collStr


def normalizeString(strValue):
    return _reWhitespace.sub(' ', strValue)


def processWhitespaceAction(strValue, wsAction, lstrip=1, rstrip=1):
    if wsAction == 'collapse':
        return collapseString(strValue, lstrip, rstrip)
    elif wsAction == 'replace':
        return normalizeString(strValue)
    else:
        return strValue


def convertToUrl(fileOrUrl):
    matchObject = _reSplitUrlApplication.match(fileOrUrl)
    if matchObject:
        if matchObject.group(1) == 'file':
            path = re.sub(':', '|', matchObject.group(2))
            url = 'file:' + path
        else:
            url = fileOrUrl
    elif not os.path.isfile(fileOrUrl):
        url = fileOrUrl
    else:
        url = urllib.pathname2url(fileOrUrl)
    return url


def convertToAbsUrl(fileOrUrl, baseUrl):
    if fileOrUrl == '' and baseUrl != '':
        absUrl = 'file:' + urllib.pathname2url(os.path.join(os.getcwd(), baseUrl, '__NO_FILE__'))
    elif os.path.isfile(fileOrUrl):
        absUrl = 'file:' + urllib.pathname2url(os.path.join(os.getcwd(), fileOrUrl))
    else:
        matchObject = _reSplitUrlApplication.match(fileOrUrl)
        if matchObject:
            if matchObject.group(1) == 'file':
                path = re.sub(':', '|', matchObject.group(2))
                absUrl = 'file:' + path
            else:
                absUrl = fileOrUrl
        elif baseUrl != '':
            absUrl = urlparse.urljoin(baseUrl, fileOrUrl)
        else:
            absUrl = fileOrUrl
    return absUrl


def normalizeFilter(filterVar):
    if filterVar == None or filterVar == '*':
        filterVar = ('*', )
    elif not isinstance(filterVar, TupleType):
        filterVar = (
         filterVar,)
    return filterVar


def nsNameToQName(nsLocalName, curNs):
    """Convert a tuple '(namespace, localName)' to a string 'prefix:localName'
    
    Input parameter:
        nsLocalName:   tuple '(namespace, localName)' to be converted
        curNs:         list of current namespaces
    Returns the corresponding string 'prefix:localName' for 'nsLocalName'.
    """
    ns = nsLocalName[0]
    for (prefix, namespace) in curNs:
        if ns == namespace:
            if prefix != None:
                return '%s:%s' % (prefix, nsLocalName[1])
            else:
                return '%s' % nsLocalName[1]
    else:
        if ns == None:
            return nsLocalName[1]
        else:
            raise LookupError, "Prefix for namespaceURI '%s' not found!" % ns

    return


def splitQName(qName):
    """Split the given 'qName' into prefix/namespace and local name.

    Input parameter:
        'qName':  contains a string 'prefix:localName' or '{namespace}localName'
    Returns a tuple (prefixOrNamespace, localName)
    """
    namespaceEndIndex = string.find(qName, '}')
    if namespaceEndIndex != -1:
        prefix = qName[1:namespaceEndIndex]
        localName = qName[namespaceEndIndex + 1:]
    else:
        namespaceEndIndex = string.find(qName, ':')
        if namespaceEndIndex != -1:
            prefix = qName[:namespaceEndIndex]
            localName = qName[namespaceEndIndex + 1:]
        else:
            prefix = None
            localName = qName
    return (
     prefix, localName)


def toClarkQName(tupleOrLocalName):
    """converts a tuple (namespace, localName) into clark notation {namespace}localName
       qNames without namespace remain unchanged

    Input parameter:
        'tupleOrLocalName':  tuple '(namespace, localName)' to be converted
    Returns a string {namespace}localName
    """
    if isinstance(tupleOrLocalName, TupleType):
        if tupleOrLocalName[0] != EMPTY_NAMESPACE:
            return '{%s}%s' % (tupleOrLocalName[0], tupleOrLocalName[1])
        else:
            return tupleOrLocalName[1]
    else:
        return tupleOrLocalName


def splitClarkQName(qName):
    """converts clark notation {namespace}localName into a tuple (namespace, localName)

    Input parameter:
        'qName':  {namespace}localName to be converted
    Returns prefix and localName as separate strings
    """
    namespaceEndIndex = string.find(qName, '}')
    if namespaceEndIndex != -1:
        prefix = qName[1:namespaceEndIndex]
        localName = qName[namespaceEndIndex + 1:]
    else:
        prefix = None
        localName = qName
    return (
     prefix, localName)


_escape = re.compile(eval('u"[&<>\\"\\u0080-\\uffff]+"'))
_escapeDict = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}

def _raiseSerializationError(text):
    raise TypeError('cannot serialize %r (type %s)' % (text, type(text).__name__))


def _encode(text, encoding):
    try:
        return text.encode(encoding)
    except AttributeError:
        return text


def _encodeEntity(text, pattern=_escape):

    def escapeEntities(m, map=_escapeDict):
        out = []
        append = out.append
        for char in m.group():
            text = map.get(char)
            if text is None:
                text = '&#%d;' % ord(char)
            append(text)

        return string.join(out, '')

    try:
        return _encode(pattern.sub(escapeEntities, text), 'ascii')
    except TypeError:
        _raise_serialization_error(text)


def escapeCdata(text, encoding=None, replace=string.replace):
    try:
        if encoding:
            try:
                text = _encode(text, encoding)
            except UnicodeError:
                return _encodeEntity(text)

        text = replace(text, '&', '&amp;')
        text = replace(text, '<', '&lt;')
        text = replace(text, '>', '&gt;')
        return text
    except (TypeError, AttributeError):
        _raiseSerializationError(text)


def escapeAttribute(text, encoding=None, replace=string.replace):
    try:
        if encoding:
            try:
                text = _encode(text, encoding)
            except UnicodeError:
                return _encodeEntity(text)

        text = replace(text, '&', '&amp;')
        text = replace(text, "'", '&apos;')
        text = replace(text, '"', '&quot;')
        text = replace(text, '<', '&lt;')
        text = replace(text, '>', '&gt;')
        return text
    except (TypeError, AttributeError):
        _raiseSerializationError(text)


class QNameTuple(tuple):
    __module__ = __name__

    def __str__(self):
        if self[0] != EMPTY_PREFIX:
            return '%s:%s' % (self[0], self[1])
        else:
            return self[1]


def QNameTupleFactory(initValue):
    if isinstance(initValue, StringTypes):
        separatorIndex = string.find(initValue, ':')
        if separatorIndex != -1:
            initValue = (
             initValue[:separatorIndex], initValue[separatorIndex + 1:])
        else:
            initValue = (
             EMPTY_PREFIX, initValue)
    return QNameTuple(initValue)


class NsNameTuple(tuple):
    __module__ = __name__

    def __str__(self):
        if self[0] != EMPTY_NAMESPACE:
            return '{%s}%s' % (self[0], self[1])
        elif self[1] != None:
            return self[1]
        else:
            return 'None'
        return


def NsNameTupleFactory(initValue):
    if isinstance(initValue, StringTypes):
        initValue = splitClarkQName(initValue)
    elif initValue == None:
        initValue = (
         EMPTY_NAMESPACE, initValue)
    return NsNameTuple(initValue)