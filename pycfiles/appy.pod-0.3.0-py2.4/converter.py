# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/appy/pod/converter.py
# Compiled at: 2009-09-30 05:37:25
import sys, os, os.path, time, signal
from optparse import OptionParser
ODT_FILE_TYPES = {'doc': 'MS Word 97', 'pdf': 'writer_pdf_Export', 'rtf': 'Rich Text Format', 'txt': 'Text', 'html': 'HTML (StarWriter)', 'htm': 'HTML (StarWriter)', 'odt': 'ODT'}

class ConverterError(Exception):
    __module__ = __name__


DOC_NOT_FOUND = 'Document "%s" was not found.'
URL_NOT_FOUND = 'Doc URL "%s" is wrong. %s'
BAD_RESULT_TYPE = 'Bad result type "%s". Available types are %s.'
CANNOT_WRITE_RESULT = 'I cannot write result "%s". %s'
CONNECT_ERROR = 'Could not connect to OpenOffice on port %d. UNO (OpenOffice API) says: %s.'
DEFAULT_PORT = 2002

class Converter:
    """Converts an ODT document into pdf, doc, txt or rtf."""
    __module__ = __name__
    exeVariants = ('soffice.exe', 'soffice')
    pathReplacements = {'program files': 'progra~1', 'openoffice.org 1': 'openof~1', 'openoffice.org 2': 'openof~1'}

    def __init__(self, docPath, resultType, port=DEFAULT_PORT):
        self.port = port
        self.docUrl = self.getDocUrl(docPath)
        self.resultFilter = self.getResultFilter(resultType)
        self.resultUrl = self.getResultUrl(resultType)
        self.ooContext = None
        self.oo = None
        self.doc = None
        return

    def getDocUrl(self, docPath):
        if not os.path.exists(docPath) and not os.path.isfile(docPath):
            raise ConverterError(DOC_NOT_FOUND % docPath)
        docAbsPath = os.path.abspath(docPath)
        docUrl = 'file:///' + docAbsPath.replace('\\', '/')
        return docUrl

    def getResultFilter(self, resultType):
        if ODT_FILE_TYPES.has_key(resultType):
            res = ODT_FILE_TYPES[resultType]
        else:
            raise ConverterError(BAD_RESULT_TYPE % (resultType, ODT_FILE_TYPES.keys()))
        return res

    def getResultUrl(self, resultType):
        baseName = os.path.splitext(self.docUrl)[0]
        if resultType != 'odt':
            res = '%s.%s' % (baseName, resultType)
        else:
            res = '%s.res.%s' % (baseName, resultType)
        fileName = res[8:]
        try:
            f = open(fileName, 'w')
            f.write('Hello')
            f.close()
            os.remove(fileName)
            return res
        except OSError, oe:
            raise ConverterError(CANNOT_WRITE_RESULT % (res, oe))

    def connect(self):
        """Connects to OpenOffice"""
        import socket, uno
        from com.sun.star.connection import NoConnectException
        try:
            localContext = uno.getComponentContext()
            resolver = localContext.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver', localContext)
            self.ooContext = resolver.resolve('uno:socket,host=localhost,port=%d;urp;StarOffice.ComponentContext' % self.port)
            smgr = self.ooContext.ServiceManager
            self.oo = smgr.createInstanceWithContext('com.sun.star.frame.Desktop', self.ooContext)
        except NoConnectException, nce:
            raise ConverterError(CONNECT_ERROR % (self.port, nce))

    def disconnect(self):
        self.doc.close(True)
        self.ooContext.ServiceManager

    def loadDocument(self):
        from com.sun.star.lang import IllegalArgumentException, IndexOutOfBoundsException
        from com.sun.star.beans import PropertyValue
        try:
            prop = PropertyValue()
            prop.Name = 'Hidden'
            prop.Value = True
            self.doc = self.oo.loadComponentFromURL(self.docUrl, '_blank', 0, (
             prop,))
            indexes = self.doc.getDocumentIndexes()
            indexesCount = indexes.getCount()
            if indexesCount != 0:
                for i in range(indexesCount):
                    try:
                        indexes.getByIndex(i).update()
                    except IndexOutOfBoundsException:
                        pass

            self.doc.updateLinks()
            sections = self.doc.getTextSections()
            sectionsCount = sections.getCount()
            if sectionsCount != 0:
                for i in range(sectionsCount - 1, -1, -1):
                    try:
                        section = sections.getByIndex(i)
                        if section.FileLink and section.FileLink.FileURL:
                            section.dispose()
                    except IndexOutOfBoundsException:
                        pass

        except IllegalArgumentException, iae:
            raise ConverterError(URL_NOT_FOUND % (self.docUrl, iae))

    def convertDocument(self):
        if self.resultFilter != 'ODT':
            from com.sun.star.beans import PropertyValue
            prop = PropertyValue()
            prop.Name = 'FilterName'
            prop.Value = self.resultFilter
            self.doc.storeToURL(self.resultUrl, (prop,))
        else:
            self.doc.storeToURL(self.resultUrl, ())

    def run(self):
        self.connect()
        self.loadDocument()
        self.convertDocument()
        self.disconnect()


WRONG_NB_OF_ARGS = 'Wrong number of arguments.'
ERROR_CODE = 1

class ConverterScript:
    __module__ = __name__
    usage = 'usage: python converter.py fileToConvert outputType [options]\n   where fileToConvert is the absolute or relative pathname of\n         the ODT file you want to convert;\n   and   outputType is the output format, that must be one of\n         %s.\n "python" should be a UNO-enabled Python interpreter (ie the one\n which is included in the OpenOffice.org distribution).' % str(ODT_FILE_TYPES.keys())

    def run(self):
        optParser = OptionParser(usage=ConverterScript.usage)
        optParser.add_option('-p', '--port', dest='port', help='The port on which OpenOffice runs Default is %d.' % DEFAULT_PORT, default=DEFAULT_PORT, metavar='PORT', type='int')
        (options, args) = optParser.parse_args()
        if len(args) != 2:
            sys.stderr.write(WRONG_NB_OF_ARGS)
            sys.stderr.write('\n')
            optParser.print_help()
            sys.exit(ERROR_CODE)
        converter = Converter(args[0], args[1], options.port)
        try:
            converter.run()
        except ConverterError, ce:
            sys.stderr.write(str(ce))
            sys.stderr.write('\n')
            optParser.print_help()
            sys.exit(ERROR_CODE)


if __name__ == '__main__':
    ConverterScript().run()