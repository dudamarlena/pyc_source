# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/ItuToHtml.py
# Compiled at: 2017-10-03 13:07:16
"""Converts an ITU to HTML."""
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import sys, os, time, logging
from optparse import OptionParser
import cpip
from cpip import ExceptionCpip
from cpip.core import ItuToTokens
from cpip.core import CppDiagnostic
from cpip.util import XmlWrite
from cpip.util import HtmlUtils
from cpip import TokenCss

class ExceptionItuToHTML(ExceptionCpip):
    pass


class ItuToHtml(object):
    """Converts an ITU to HTML and write it to the output directory."""
    _condCompClassMap = {-1: 'Maybe', 
       0: 'False', 
       1: 'True'}

    def __init__(self, theItu, theHtmlDir, keepGoing=False, macroRefMap=None, cppCondMap=None, ituToTuLineSet=None):
        """Takes an input source file and an output directory.
        theItu - The original source file path (or file like object for the input).
        theHtmlDir - The output directory for the HTML or a file-like object for the output
        keepGoing - Bool, if True raise on error.
        macroRefMap - Map of {identifier : href_text, ...) to link to macro definitions.
        ituToTuLineSet - Set of integer line numbers which are lines that can be linked
        to the translation unit representation."""
        try:
            self._fpIn = theItu
            self._ituFileObj = open(self._fpIn)
        except TypeError:
            self._fpIn = 'Unknown'
            self._ituFileObj = theItu

        if isinstance(theHtmlDir, str):
            if not os.path.exists(theHtmlDir):
                os.makedirs(theHtmlDir)
            self._fOut = open(os.path.join(theHtmlDir, HtmlUtils.retHtmlFileName(self._fpIn)), 'w')
        else:
            self._fOut = theHtmlDir
        self._keepGoing = keepGoing
        self._macroRefMap = macroRefMap or {}
        self._cppCondMap = cppCondMap
        self._ituToTuLineSet = ituToTuLineSet
        self._lineNum = 0
        self._convert()

    def _convert(self):
        """Convert ITU to HTML."""
        myItt = self._initReader()
        if self._fOut is None:
            return
        else:
            try:
                with XmlWrite.XhtmlStream(self._fOut, mustIndent=cpip.INDENT_ML) as (myS):
                    with XmlWrite.Element(myS, 'head'):
                        with XmlWrite.Element(myS, 'link', {'href': TokenCss.TT_CSS_FILE, 
                           'type': 'text/css', 
                           'rel': 'stylesheet'}):
                            pass
                        with XmlWrite.Element(myS, 'title'):
                            myS.characters('File: %s' % self._fpIn)
                    with XmlWrite.Element(myS, 'body'):
                        with XmlWrite.Element(myS, 'h1'):
                            myS.characters('File: %s' % self._fpIn)
                        with XmlWrite.Element(myS, 'p'):
                            myS.characters('Green shading in the line number column\nmeans the source is part of the translation unit, red means it is conditionally excluded.\nHighlighted line numbers link to the translation unit page. Highlighted macros link to\nthe macro page.')
                        with XmlWrite.Element(myS, 'pre'):
                            myS.xmlSpacePreserve()
                            self._incAndWriteLine(myS)
                            for t, tt in myItt.genTokensKeywordPpDirective():
                                self._handleToken(myS, t, tt)

            except IOError as err:
                raise ExceptionItuToHTML('%s line=%d, col=%d' % (
                 str(err),
                 myItt.fileLocator.lineNum,
                 myItt.fileLocator.colNum))

            return

    def _handleToken(self, theS, t, tt):
        logging.debug('_handleToken(): "%s", %s', t, tt)
        if tt == 'whitespace':
            self._writeTextWithNewlines(theS, t, None)
        elif tt in ('C comment', 'C++ comment'):
            self._writeTextWithNewlines(theS, t, TokenCss.retClass(tt))
        elif False and tt == 'preprocessing-op-or-punc':
            theS.characters(t)
        elif tt == 'identifier' and t in self._macroRefMap:
            assert len(self._macroRefMap[t]) > 0
            href = self._macroRefMap[t][(-1)][2]
            with XmlWrite.Element(theS, 'a', {'href': href}):
                with XmlWrite.Element(theS, 'span', {'class': '%s' % TokenCss.retClass(tt)}):
                    theS.characters(t)
        else:
            with XmlWrite.Element(theS, 'span', {'class': '%s' % TokenCss.retClass(tt)}):
                self._lineNum += t.count('\n')
                theS.characters(t)
        return

    def _writeTextWithNewlines(self, theS, theText, spanClass):
        """Splits text by newlines and writes it out."""
        myL = theText.split('\n')
        if len(myL) > 1:
            for s in myL[:-1]:
                if spanClass is not None:
                    with XmlWrite.Element(theS, 'span', {'class': spanClass}):
                        theS.characters(s.replace('\t', '    '))
                else:
                    theS.characters(s.replace('\t', '    '))
                theS.characters('\n')
                self._incAndWriteLine(theS)

        if spanClass is not None:
            with XmlWrite.Element(theS, 'span', {'class': spanClass}):
                theS.characters(myL[(-1)].replace('\t', '    '))
        else:
            theS.characters(myL[(-1)].replace('\t', '    '))
        return

    def _incAndWriteLine(self, theS):
        self._lineNum += 1
        classAttr = 'line'
        if self._cppCondMap is not None:
            try:
                lineIsCompiled = self._cppCondMap.isCompiled(self._fpIn, self._lineNum)
            except KeyError:
                logging.error(('_incAndWriteLine(): Ambiguous compilation: path: "{!r:s}" Line: {!r:s}').format(self._fpIn, self._lineNum))
            else:
                classAttr = self._condCompClassMap[lineIsCompiled]

        if self._ituToTuLineSet is not None and self._lineNum in self._ituToTuLineSet:
            myHref = '%s.html#%d' % (os.path.basename(self._fpIn), self._lineNum)
        else:
            myHref = None
        HtmlUtils.writeHtmlFileAnchor(theS, self._lineNum, '%8d:' % self._lineNum, classAttr, theHref=myHref)
        theS.characters(' ')
        return

    def _initReader(self):
        """Create and return a reader, initialise internals."""
        if self._keepGoing:
            myDiagnostic = CppDiagnostic.PreprocessDiagnosticKeepGoing()
        else:
            myDiagnostic = None
        try:
            myItt = ItuToTokens.ItuToTokens(theFileObj=self._ituFileObj, theFileId=self._fpIn, theDiagnostic=myDiagnostic)
        except IOError as err:
            raise ExceptionItuToHTML(str(err))

        self._lineNum = 0
        return myItt


def main():
    usage = 'usage: %prog [options] source out_dir\nConverts a source code file to HTML in the output directory.'
    print 'Cmd: %s' % (' ').join(sys.argv)
    optParser = OptionParser(usage, version='%prog ' + __version__)
    optParser.add_option('-l', '--loglevel', type='int', dest='loglevel', default=30, help='Log Level (debug=10, info=20, warning=30, error=40, critical=50) [default: %default]')
    opts, args = optParser.parse_args()
    clkStart = time.clock()
    logging.basicConfig(level=opts.loglevel, format='%(asctime)s %(levelname)-8s %(message)s', stream=sys.stdout)
    if len(args) != 2:
        optParser.print_help()
        optParser.error('No arguments!')
        return 1
    TokenCss.writeCssToDir(args[1])
    ItuToHtml(args[0], args[1])
    clkExec = time.clock() - clkStart
    print 'CPU time = %8.3f (S)' % clkExec
    print 'Bye, bye!'
    return 0


if __name__ == '__main__':
    sys.exit(main())