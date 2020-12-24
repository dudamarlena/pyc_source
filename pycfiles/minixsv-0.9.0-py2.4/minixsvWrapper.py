# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\minixsv\minixsvWrapper.py
# Compiled at: 2008-07-02 07:56:44
import sys, getopt
from genxmlif import GenXmlIfError
from xsvalErrorHandler import ErrorHandler, XsvalError
from minixsv import *
from pyxsval import parseAndValidate
validSyntaxText = 'minixsv XML Schema Validator\nSyntax: minixsv [-h] [-?] [-p Parser] [-s XSD-Filename] XML-Filename\n\nOptions:\n-h, -?:          Display this help text\n-p Parser:       XML Parser to be used \n                 (XMLIF_MINIDOM, XMLIF_ELEMENTTREE, XMLIF_4DOM\n                  default: XMLIF_ELEMENTTREE)\n-s XSD-FileName: specify the schema file for validation \n                 (if not specified in XML-File)\n'

def checkShellInputParameter():
    """check shell input parameters."""
    xmlInputFilename = None
    xsdFilename = None
    xmlParser = 'XMLIF_ELEMENTTREE'
    try:
        (options, arguments) = getopt.getopt(sys.argv[1:], '?hp:s:')
        if ('-?', '') in options or ('-h', '') in options:
            print validSyntaxText
            sys.exit(-1)
        elif len(arguments) == 1:
            xmlInputFilename = arguments[0]
            for (o, a) in options:
                if o == '-s':
                    xsdFilename = a
                if o == '-p':
                    if a in (XMLIF_MINIDOM, XMLIF_ELEMENTTREE, XMLIF_4DOM):
                        xmlParser = a
                    else:
                        print 'Invalid XML parser %s!' % a
                        sys.exit(-1)

        else:
            print 'minixsv needs one argument (XML input file)!'
            sys.exit(-1)
    except getopt.GetoptError, errstr:
        print errstr
        sys.exit(-1)

    return (
     xmlInputFilename, xsdFilename, xmlParser)


def main():
    (xmlInputFilename, xsdFileName, xmlParser) = checkShellInputParameter()
    try:
        parseAndValidate(xmlInputFilename, xsdFile=xsdFileName, xmlIfClass=xmlParser)
    except IOError, errstr:
        print errstr
        sys.exit(-1)
    except GenXmlIfError, errstr:
        print errstr
        sys.exit(-1)
    except XsvalError, errstr:
        print errstr
        sys.exit(-1)


if __name__ == '__main__':
    main()