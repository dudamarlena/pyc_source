# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/tools/marshallers/ErrorMarshaller.py
# Compiled at: 2008-10-01 10:39:37
import sys, traceback
from cStringIO import StringIO
import xml.sax
from xml.sax import ContentHandler, ErrorHandler
from xml.sax.xmlreader import InputSource
from xml.sax.handler import feature_namespaces
from xml.sax.saxutils import XMLGenerator
from xooof.xmldispatcher.interfaces.interfaces import *
from xooof.xmldispatcher.tools.envelope.constants import *
NS_XD_ERROR = 'http://xmlcatalog/catalog/xmldispatcher/error'

class _ErrorHandler(ContentHandler):
    __module__ = __name__
    _typeMap = {'UserError': XMLDispatcherUserException, 'AppError': XMLDispatcherAppException, 'SystemError': XMLDispatcherSystemException}

    def __init__(self):
        self.__chars = []
        self.__type = None
        self.__descr = None
        self.__source = None
        self.__code = None
        return

    def getException(self):
        return apply(self._typeMap[self.__type], (
         self.__descr, self.__source, self.__code))

    def startElementNS(self, (nsuri, name), qname, atts):
        self.__chars = []

    def characters(self, chars):
        self.__chars.append(chars)

    def endElementNS(self, (nsuri, name), qname):
        if nsuri not in (None, NS_XD_ERROR):
            return
        if name == 'type':
            self.__type = ('').join(self.__chars)
        elif name == 'number':
            number = long(('').join(self.__chars))
            if number == -2147217183:
                self.__type = 'UserError'
            elif number == -2147220270:
                self.__type = 'AppError'
            else:
                self.__type = 'SystemError'
        elif name == 'description':
            self.__descr = ('').join(self.__chars)
        elif name == 'source':
            self.__source = ('').join(self.__chars)
        elif name == 'code':
            self.__code = ('').join(self.__chars)
        return


def unmarshallExceptionFromXML(errorString):
    try:
        eh = _ErrorHandler()
        parser = xml.sax.make_parser()
        parser.setFeature(feature_namespaces, 1)
        parser.setContentHandler(eh)
        parser.setErrorHandler(ErrorHandler())
        inpsrc = InputSource()
        inpsrc.setByteStream(StringIO(errorString))
        parser.parse(inpsrc)
    except:
        raise XMLDispatcherCommException, '%s parsing error as XML [%s]' % (sys.exc_info()[1], errorString)
    else:
        raise eh.getException()


def marshallExceptionToXML((exc_type, exc_value, exc_traceback), encoding='utf-8', withNs=0):
    if isinstance(exc_value, XMLDispatcherException):
        stype = exc_value.getType()
        sdescr = exc_value.getDescr()
        scode = exc_value.getCode()
        ssource = exc_value.getSource()
    else:
        stype = XMLDispatcherSystemException._type
        sdescr = ('').join(traceback.format_exception_only(exc_type, exc_value))
        scode = None
        ssource = None
    if ssource is None:
        ssource = ('').join(traceback.format_tb(exc_traceback))
    out = StringIO()
    xmlgen = XMLGenerator(out, encoding=encoding)
    if withNs:
        ns = NS_XD_ERROR
        xmlgen.startPrefixMapping(None, ns)
    else:
        ns = None
    xmlgen.startElementNS((ns, 'error'), None, {})
    if stype:
        xmlgen.startElementNS((ns, 'type'), None, {})
        xmlgen.characters(stype)
        xmlgen.endElementNS((ns, 'type'), None)
    if ssource:
        xmlgen.startElementNS((ns, 'source'), None, {})
        xmlgen.characters(ssource)
        xmlgen.endElementNS((ns, 'source'), None)
    xmlgen.startElementNS((ns, 'description'), None, {})
    xmlgen.characters(sdescr)
    xmlgen.endElementNS((ns, 'description'), None)
    if scode:
        xmlgen.startElementNS((ns, 'code'), None, {})
        xmlgen.characters(scode)
        xmlgen.endElementNS((ns, 'code'), None)
    xmlgen.endElementNS((ns, 'error'), None)
    if withNs:
        xmlgen.endPrefixMapping(None)
    exc_traceback = None
    return out.getvalue()


if __name__ == '__main__':

    def dotest():
        s = marshallExceptionToXML(sys.exc_info())
        print '====>', s
        try:
            unmarshallExceptionFromXML(s)
        except Exception, e:
            print '---->', e

        s = marshallExceptionToXML(sys.exc_info(), withNs=1)
        print '====>', s
        try:
            unmarshallExceptionFromXML(s)
        except Exception, e:
            print '---->', e


    try:
        raise XMLDispatcherUserException('the user error')
    except:
        dotest()
    else:
        try:
            raise RuntimeError('the runtime error')
        except:
            dotest()