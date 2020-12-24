# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/CPIPMain.py
# Compiled at: 2017-10-04 05:25:08
"""
CPIPMain.py -- Preprocess the file or the files in a directory.
"""
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__version__ = '0.9.7'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import argparse, collections, datetime, io, logging, multiprocessing, os, pprint, subprocess, sys, time
from cpip import CppCondGraphToHtml
from cpip import ExceptionCpip
from cpip import IncGraphSVG
from cpip import IncGraphSVGBase
from cpip import INDENT_ML
from cpip import ItuToHtml
from cpip import MacroHistoryHtml
from cpip import TokenCss
from cpip import Tu2Html
from cpip.core import CppCond
from cpip.core import CppDiagnostic
from cpip.core import FileIncludeGraph
from cpip.core import IncludeHandler
from cpip.core import PpLexer
from cpip.core import PragmaHandler
from cpip.util import CommonPrefix
from cpip.util import Cpp
from cpip.util import DirWalk
from cpip.util import HtmlUtils
from cpip.util import XmlWrite
MainJobSpec = collections.namedtuple('MainJobSpec', [
 'incHandler',
 'preDefMacros',
 'preIncFiles',
 'diagnostic',
 'pragmaHandler',
 'keepGoing',
 'conditionalLevel',
 'dumpList',
 'helpMap',
 'includeDOT',
 'cmdLine',
 'gccExtensions'])
INCLUDE_GRAPH_INTRO = [
 "This is the relationships of the #include'd files\npresented as a SVG graph or as text.\n",
 'The SVG graph shows the tree of included files\nin a graphical fashion with each file as a node and the #include relationship\nas an edge.\n',
 'You can choose the scale with the selectors at the top.\nMousing over the nodes in the SVG graph pops up information about\nthe #include process.\n']
SOURCE_CODE_INTRO = [
 'HTML representations of the source file and\nthe translation unit as seen by the compiler.\n',
 'Lines in the source file are\nlinked to the translation unit where appropriate. Macros in the source file\nare linked to the macro page.\n']
CONDITIONAL_COMPILATION_INTRO = [
 'The conditional compilation statements as green (i.e. evaluates as True)\nand red (evaluates as False). Each statement is linked to the source code it came from.']
MACROS_INTRO = [
 'A page describing the macros encountered during pre-processing, their definition, where defined,\nwhere used and their dependencies. All linked to the source code.\n']
TOKEN_COUNT_INTRO = [
 'A table of the token types and their count.\n']
FILES_INCLUDED_INTRO = [
 'A table of the source files included, their directories and the number of times they\nwere included.\n',
 'The links lead to the source code.\n']
PpProcessResult = collections.namedtuple('PpProcessResult', [
 'ituPath',
 'indexPath',
 'tuIndexFileName',
 'total_files',
 'total_lines',
 'total_bytes'])

class FigVisitorLargestCommanPrefix(FileIncludeGraph.FigVisitorBase):
    """Simple visitor that walks the tree and finds the largest common file name prefix."""

    def __init__(self):
        self._fileNameS = set()

    def visitGraph(self, theFigNode, theDepth, theLine):
        """Capture the file name."""
        if theFigNode.fileName != PpLexer.UNNAMED_FILE_NAME:
            self._fileNameS.add(os.path.abspath(theFigNode.fileName))

    def lenCommonPrefix(self):
        return CommonPrefix.lenCommonPrefix(self._fileNameS)


class FigVisitorDot(FileIncludeGraph.FigVisitorBase):
    """Simple visitor that collects parent/child links for plotting the graph with dot."""
    FILE_EXT_TO_NODE_COLOURS = {'.h': 'yellow', 
       '.c': 'lawngreen', 
       '.cpp': 'limegreen', 
       '.inl': 'salmon'}

    def __init__(self, lenPrefix=0):
        super(FigVisitorDot, self).__init__()
        self._lenPrefix = lenPrefix
        self._nodeS = set()
        self._rootS = []
        self._lineS = []

    def __str__(self):
        retL = [
         'digraph FigVisitorDot {']
        retL.extend(sorted(self._nodeS))
        if len(self._rootS) > 1:
            retL.append('%s;' % (' -> ').join(self._rootS))
        retL.extend(self._lineS)
        retL.append('}\n')
        return ('\n').join(retL)

    def _fileName(self, theFigNode):
        """Treat the file name consistently."""
        if theFigNode.fileName == PpLexer.UNNAMED_FILE_NAME:
            return theFigNode.fileName
        myF = os.path.abspath(theFigNode.fileName)
        if self._lenPrefix > 0:
            myF = myF[self._lenPrefix:]
        return myF

    def _addNode(self, theFigNode):
        if theFigNode.numTokensSig > 0:
            myF = self._fileName(theFigNode)
            nodeAttrStr = '"%s" [' % myF
            myExt = os.path.splitext(theFigNode.fileName)[1].lower()
            if myF == PpLexer.UNNAMED_FILE_NAME:
                nodeAttrStr += 'color=lightblue,style=filled'
            elif myExt in self.FILE_EXT_TO_NODE_COLOURS:
                nodeAttrStr += 'color=%s,style=filled' % self.FILE_EXT_TO_NODE_COLOURS[myExt]
            else:
                nodeAttrStr += 'color=red,style=filled'
            nodeAttrStr += ',label="%s"' % myF
            nodeAttrStr += '];'
            self._nodeS.add(nodeAttrStr)

    def visitGraph(self, theFigNode, theDepth, theLine):
        """."""
        self._addNode(theFigNode)
        myF = self._fileName(theFigNode)
        if theDepth == 1:
            self._rootS.append('"%s"' % myF)
        hasC = False
        for aC in theFigNode.genChildNodes():
            self._lineS.append('"%s" -> "%s";' % (myF, self._fileName(aC)))
            hasC = True

        if not hasC:
            self._lineS.append('"%s";' % myF)


def writeIncludeGraphAsDot(theOutDir, theItu, theLexer):
    logging.info('Creating include Graph for DOT...')
    myFigr = theLexer.fileIncludeGraphRoot
    myVis = FigVisitorDot()
    myFigr.acceptVisitor(myVis)
    dotPath = os.path.abspath(os.path.join(theOutDir, includeGraphFileNameDotTxt(theItu)))
    svgPath = os.path.abspath(os.path.join(theOutDir, includeGraphFileNameDotSVG(theItu)))
    f = open(dotPath, 'w')
    f.write(str(myVis))
    f.close()
    result = False
    try:
        retcode = subprocess.call('dot -Tsvg %s -o %s' % (dotPath, svgPath), shell=True)
        if retcode < 0:
            logging.error('dot was terminated by signal %d' % retcode)
        elif retcode > 0:
            logging.error('dot returned error code %d' % retcode)
        elif retcode == 0:
            result = True
            logging.info('dot returned %d' % retcode)
    except OSError as e:
        logging.error('dot execution failed: %s' % str(e))

    logging.info('Creating include Graph for DOT done.')
    return result


def retFileCountMap(theLexer):
    """Visits the Lexers file include graph and returns a dict of:
    {file_name : (inclusion_count, line_count, bytes_count).
    
    The line_count, bytes_count are obtained by reading the file.
    """
    myFigr = theLexer.fileIncludeGraphRoot
    myFileNameVis = FileIncludeGraph.FigVisitorFileSet()
    myFigr.acceptVisitor(myFileNameVis)
    file_name_map = myFileNameVis.fileNameMap
    ret_map = {}
    for file_name, inc_count in file_name_map.items():
        count_lines = 0
        count_bytes = 0
        if file_name != PpLexer.UNNAMED_FILE_NAME:
            with open(file_name) as (fobj):
                for line in fobj:
                    count_lines += 1
                    count_bytes += len(line)

        ret_map[file_name] = (
         inc_count, count_lines, count_bytes)

    return ret_map


def _dumpCondCompGraph(theLexer):
    print ()
    print (' Conditional Compilation Graph ').center(75, '-')
    myFigr = theLexer.condCompGraph
    print myFigr
    print (' END Conditional Compilation Graph ').center(75, '-')


def _dumpIncludeGraph(theLexer):
    print ()
    print (' Include Graph ').center(75, '-')
    myFigr = theLexer.fileIncludeGraphRoot
    print myFigr
    print (' END Include Graph ').center(75, '-')


def _dumpFileCount(theFileCountMap):
    print ()
    myList = list(theFileCountMap.keys())
    myList.sort()
    print ()
    print (' Count of files encountered ').center(75, '-')
    for f in myList:
        print '%4d  %s' % (theFileCountMap[f], f)

    print (' END Count of files encountered ').center(75, '-')


def _dumpTokenCount(theTokenCounter):
    print ()
    print (' Token count ').center(75, '-')
    myTotal = 0
    for tokType, tokCount in theTokenCounter.tokenTypesAndCounts(isAll=True, allPossibleTypes=True):
        print '%8d  %s' % (tokCount, tokType)
        myTotal += tokCount

    print '%8d  %s' % (myTotal, 'TOTAL')
    print (' END Token count ').center(75, '-')


def _dumpMacroEnv(theLexer):
    print ()
    print (' Macro Environment and History ').center(75, '-')
    print theLexer.macroEnvironment.macroHistory()
    print (' END Macro Environment and History ').center(75, '-')
    print ()


def _dumpMacroEnvDot(theLexer):
    print ()
    print (' Macro dependencies as a DOT file ').center(75, '-')
    print 'digraph MacroDependencyDot {'
    myMacEnv = theLexer.macroEnvironment
    for aPpDef in myMacEnv.genMacros():
        if aPpDef.isReferenced:
            for aRtok in aPpDef.replacementTokens:
                if aRtok.isIdentifier() and myMacEnv.hasMacro(aRtok.t):
                    print '"%s" -> "%s";' % (aPpDef.identifier, aRtok.t)

    print '}\n'
    print (' END Macro dependencies as a DOT file ').center(75, '-')
    print ()


def tuIndexFileName(theTu):
    return 'index_' + HtmlUtils.retHtmlFileName(theTu)


def tuFileName(theTu):
    return os.path.basename(theTu) + '.html'


def includeGraphFileNameSVG(theItu):
    return os.path.basename(theItu) + '.include.svg'


def includeGraphFileNameCcg(theItu):
    return os.path.basename(theItu) + '.ccg.html'


def includeGraphFileNameText(theItu):
    return os.path.basename(theItu) + '.include.txt.html'


def includeGraphFileNameDotTxt(theItu):
    return os.path.basename(theItu) + '.include.dot'


def includeGraphFileNameDotSVG(theItu):
    return os.path.basename(theItu) + '.include.dot.svg'


def writeIncludeGraphAsText(theOutDir, theItu, theLexer):

    def _linkToIndex(theS, theItu):
        with XmlWrite.Element(theS, 'p'):
            theS.characters('Return to ')
            with XmlWrite.Element(theS, 'a', {'href': tuIndexFileName(theItu)}):
                theS.characters('Index')

    outPath = os.path.join(theOutDir, includeGraphFileNameText(theItu))
    with XmlWrite.XhtmlStream(outPath, mustIndent=INDENT_ML) as (myS):
        with XmlWrite.Element(myS, 'head'):
            with XmlWrite.Element(myS, 'link', {'href': TokenCss.TT_CSS_FILE, 
               'type': 'text/css', 
               'rel': 'stylesheet'}):
                pass
            with XmlWrite.Element(myS, 'title'):
                myS.characters('Included graph for %s' % theItu)
        with XmlWrite.Element(myS, 'body'):
            with XmlWrite.Element(myS, 'h1'):
                myS.characters('File include graph for: %s' % theItu)
            with XmlWrite.Element(myS, 'p'):
                myS.characters('A text dump of the include graph.')
            _linkToIndex(myS, theItu)
            with XmlWrite.Element(myS, 'pre'):
                myS.characters(str(theLexer.fileIncludeGraphRoot))
            _linkToIndex(myS, theItu)


def _writeParagraphWithBreaks(theS, theParas):
    for i, p in enumerate(theParas):
        with XmlWrite.Element(theS, 'p'):
            theS.characters(p)


def writeTuIndexHtml(theOutDir, theTuPath, theLexer, theFileCountMap, theTokenCntr, hasIncDot, macroHistoryIndexName):
    """Write the index.html for a single TU.
    
    *theOutDir*
        The output directory to write to.
    
    *theTuPath*
        The path to the original ITU.
    
    *theLexer*
        The pre-processing Lexer that has pre-processed the ITU/TU. 
    
    *theFileCountMap*
        dict of {file_path : data, ...} where data is things like inclusion
        count, lines, bytes and so on.
    
    *theTokenCntr*
        :py:class:`cpip.core.PpTokenCount.PpTokenCount` containing the token
        counts.
    
    *hasIncDot*
        bool to emit graphviz .dot files.
    
    *macroHistoryIndexName*
        String of the filename of the macro history.
        
    Returns: (total_files, total_lines, total_bytes) as integers.
    """
    total_files = total_lines = total_bytes = 0
    with XmlWrite.XhtmlStream(os.path.join(theOutDir, tuIndexFileName(theTuPath)), mustIndent=INDENT_ML) as (myS):
        with XmlWrite.Element(myS, 'head'):
            with XmlWrite.Element(myS, 'link', {'href': TokenCss.TT_CSS_FILE, 
               'type': 'text/css', 
               'rel': 'stylesheet'}):
                pass
            with XmlWrite.Element(myS, 'title'):
                myS.characters('CPIP Processing of %s' % theTuPath)
        with XmlWrite.Element(myS, 'body'):
            with XmlWrite.Element(myS, 'h1'):
                myS.characters('CPIP Processing of %s' % theTuPath)
            with XmlWrite.Element(myS, 'p'):
                myS.characters('This has links to individual pages about the\npre-processing of this file.')
            with XmlWrite.Element(myS, 'h2'):
                myS.characters('1. Source Code')
            _writeParagraphWithBreaks(myS, SOURCE_CODE_INTRO)
            with XmlWrite.Element(myS, 'h3'):
                myS.characters('The ')
                with XmlWrite.Element(myS, 'a', {'href': HtmlUtils.retHtmlFileName(theTuPath)}):
                    myS.characters('source file')
                myS.characters(' and ')
                with XmlWrite.Element(myS, 'a', {'href': tuFileName(theTuPath)}):
                    myS.characters('as a translation unit')
            with XmlWrite.Element(myS, 'h2'):
                myS.characters('2. Include Graphs')
            _writeParagraphWithBreaks(myS, INCLUDE_GRAPH_INTRO)
            with XmlWrite.Element(myS, 'h3'):
                myS.characters('A ')
                with XmlWrite.Element(myS, 'a', {'href': includeGraphFileNameSVG(theTuPath)}):
                    myS.characters('visual #include tree in SVG')
                if hasIncDot:
                    myS.characters(', ')
                    with XmlWrite.Element(myS, 'a', {'href': includeGraphFileNameDotSVG(theTuPath)}):
                        myS.characters('Dot dependency [SVG]')
                myS.characters(' or ')
                with XmlWrite.Element(myS, 'a', {'href': includeGraphFileNameText(theTuPath)}):
                    myS.characters('as Text')
            with XmlWrite.Element(myS, 'h2'):
                myS.characters('3. Conditional Compilation')
            _writeParagraphWithBreaks(myS, CONDITIONAL_COMPILATION_INTRO)
            with XmlWrite.Element(myS, 'h3'):
                myS.characters('The ')
                with XmlWrite.Element(myS, 'a', {'href': includeGraphFileNameCcg(theTuPath)}):
                    myS.characters('conditional compilation graph')
            with XmlWrite.Element(myS, 'h2'):
                myS.characters('4. Macros')
            _writeParagraphWithBreaks(myS, MACROS_INTRO)
            with XmlWrite.Element(myS, 'h3'):
                myS.characters('The ')
                with XmlWrite.Element(myS, 'a', {'href': macroHistoryIndexName}):
                    myS.characters('Macro Environment')
            with XmlWrite.Element(myS, 'h2'):
                myS.characters('5. Token Count')
            _writeParagraphWithBreaks(myS, TOKEN_COUNT_INTRO)
            with XmlWrite.Element(myS, 'table', {'class': 'monospace'}):
                with XmlWrite.Element(myS, 'tr'):
                    with XmlWrite.Element(myS, 'th', {'class': 'monospace'}):
                        myS.characters('Token Type')
                    with XmlWrite.Element(myS, 'th', {'class': 'monospace'}):
                        myS.characters('Count')
                myTotal = 0
                for tokType, tokCount in theTokenCntr.tokenTypesAndCounts(isAll=True, allPossibleTypes=True):
                    with XmlWrite.Element(myS, 'tr'):
                        with XmlWrite.Element(myS, 'td', {'class': 'monospace'}):
                            myS.characters(tokType)
                        with XmlWrite.Element(myS, 'td', {'class': 'monospace'}):
                            myStr = '%10d' % tokCount
                            myStr = myStr.replace(' ', '&nbsp;')
                            myS.literal(myStr)
                        myTotal += tokCount

                with XmlWrite.Element(myS, 'tr'):
                    with XmlWrite.Element(myS, 'td', {'class': 'monospace'}):
                        with XmlWrite.Element(myS, 'b'):
                            myS.characters('Total:')
                    with XmlWrite.Element(myS, 'td', {'class': 'monospace'}):
                        with XmlWrite.Element(myS, 'b'):
                            myStr = '%10d' % myTotal
                            myStr = myStr.replace(' ', '&nbsp;')
                            myS.literal(myStr)
            with XmlWrite.Element(myS, 'br'):
                pass
            with XmlWrite.Element(myS, 'h2'):
                myS.characters('6. Files Included and Count')
            _writeParagraphWithBreaks(myS, FILES_INCLUDED_INTRO)
            myFileLinkS = []
            for myItuFile in sorted(theFileCountMap.keys()):
                if myItuFile != PpLexer.UNNAMED_FILE_NAME:
                    myFileLinkS.append((
                     myItuFile,
                     (
                      HtmlUtils.retHtmlFileName(myItuFile),
                      os.path.basename(myItuFile),
                      theFileCountMap[myItuFile])))

            HtmlUtils.writeFilePathsAsTable(None, myS, myFileLinkS, 'filetable', _tdCallback, _trThCallback)
            with XmlWrite.Element(myS, 'br'):
                pass
            with XmlWrite.Element(myS, 'p'):
                myS.characters('Total number of unique files: %d' % len(theFileCountMap))
            for f, l, b in theFileCountMap.values():
                total_files += f
                total_lines += f * l
                total_bytes += f * b

            with XmlWrite.Element(myS, 'p'):
                myS.characters(('Total number of files processed: {:,d}').format(total_files))
            with XmlWrite.Element(myS, 'p'):
                myS.characters(('Total number of lines processed: {:,d}').format(total_lines))
            with XmlWrite.Element(myS, 'p'):
                myS.characters(('Total number of bytes processed: {:,d}').format(total_bytes))
            _writeIndexHtmlTrailer(myS, time_start=None)
            with XmlWrite.Element(myS, 'p'):
                myS.characters('Back to: ')
                with XmlWrite.Element(myS, 'a', {'href': 'index.html'}):
                    myS.characters('Index Page')
    return (
     total_files, total_lines, total_bytes)


def _trThCallback(theS, theDepth):
    """Create the table header:
      <tr>
        <th class="filetable" colspan="9">File Path&nbsp;</th>
        <th class="filetable">Include Count</th>
        <th class="filetable">Lines</th>
        <th class="filetable">Bytes</th>
        <th class="filetable">Total Lines</th>
        <th class="filetable">Total Bytes</th>
      </tr>
    """
    with XmlWrite.Element(theS, 'tr', {}):
        with XmlWrite.Element(theS, 'th', {'colspan': '%d' % theDepth, 
           'class': 'filetable'}):
            theS.characters('File Path')
        with XmlWrite.Element(theS, 'th', {'class': 'filetable'}):
            theS.characters('Include Count')
        with XmlWrite.Element(theS, 'th', {'class': 'filetable'}):
            theS.characters('Lines')
        with XmlWrite.Element(theS, 'th', {'class': 'filetable'}):
            theS.characters('Bytes')
        with XmlWrite.Element(theS, 'th', {'class': 'filetable'}):
            theS.characters('Total Lines')
        with XmlWrite.Element(theS, 'th', {'class': 'filetable'}):
            theS.characters('Total Bytes')


def _tdCallback(theS, attrs, _k, href_nav_text_file_data):
    """Callback function for the file count table."""
    attrs['class'] = 'filetable'
    href, navText, file_data = href_nav_text_file_data
    with XmlWrite.Element(theS, 'td', attrs):
        with XmlWrite.Element(theS, 'a', {'href': href}):
            theS.characters(navText)
    td_attrs = {'width': '36px', 
       'class': 'filetable', 
       'align': 'right'}
    count_inc, count_lines, count_bytes = file_data
    with XmlWrite.Element(theS, 'td', td_attrs):
        theS.characters('%d' % count_inc)
    with XmlWrite.Element(theS, 'td', td_attrs):
        theS.characters(('{:,d}').format(count_lines))
    with XmlWrite.Element(theS, 'td', td_attrs):
        theS.characters(('{:,d}').format(count_bytes))
    with XmlWrite.Element(theS, 'td', td_attrs):
        theS.characters(('{:,d}').format(count_lines * count_inc))
    with XmlWrite.Element(theS, 'td', td_attrs):
        theS.characters(('{:,d}').format(count_bytes * count_inc))


def _writeIndexHtmlTrailer(theS, time_start):
    """Write a trailer to the index.html page with the start/finish time and
    version. If time_start is None then only the current time is written."""
    dt_finish = datetime.datetime.fromtimestamp(time.time())
    time_bits = []
    if time_start is not None:
        dt_start = datetime.datetime.fromtimestamp(time_start)
        seconds = (dt_finish - dt_start).total_seconds()
        factor = 86400
        if seconds > factor:
            time_bits.append(('{:d} days').format(int(seconds // factor)))
            seconds %= factor
        factor = 3600
        if seconds > factor:
            time_bits.append(('{:d} hours').format(int(seconds // factor)))
            seconds %= factor
        factor = 60
        if seconds > factor:
            time_bits.append(('{:d} minutes').format(int(seconds // factor)))
            seconds %= factor
        time_bits.append(('{:.3f} seconds').format(seconds))
        with XmlWrite.Element(theS, 'p'):
            theS.characters(('Time start: {:s}').format(dt_start.strftime('%c')))
            theS.characters((' Time finish: {:s}').format(dt_finish.strftime('%c')))
            theS.characters((' Duration: {:s}.').format((', ').join(time_bits)))
            theS.characters((' CPIP version: {:s}').format(__version__))
    else:
        with XmlWrite.Element(theS, 'p'):
            theS.characters((' Completion time: {:s}').format(dt_finish.strftime('%c')))
            theS.characters((' CPIP version: {:s}').format(__version__))
    return


def writeIndexHtml(theItuS, theOutDir, theJobSpec, time_start, total_files, total_lines, total_bytes):
    """Writes the top level index.html page for a pre-processed file.
    
    theOutDir - The output directory.
    
    theTuS - The list of translation units processed.
    
    theCmdLine - The command line as a string.
    
    theOptMap is a map of {opt_name : (value, help), ...} from the
    command line options.
    TODO: This is fine but has too many levels of indent.
    """
    indexPath = os.path.join(theOutDir, 'index.html')
    assert len(theItuS) == 1, 'Can only process one TU to an output directory.'
    with XmlWrite.XhtmlStream(indexPath, mustIndent=INDENT_ML) as (myS):
        with XmlWrite.Element(myS, 'head'):
            with XmlWrite.Element(myS, 'link', {'href': TokenCss.TT_CSS_FILE, 
               'type': 'text/css', 
               'rel': 'stylesheet'}):
                pass
            with XmlWrite.Element(myS, 'title'):
                myS.characters('CPIP Processing')
        with XmlWrite.Element(myS, 'body'):
            with XmlWrite.Element(myS, 'h1'):
                myS.characters('CPIP Processing in output location: %s' % theOutDir)
            with XmlWrite.Element(myS, 'h2'):
                myS.characters('Files Processed as Translation Units:')
            with XmlWrite.Element(myS, 'ul'):
                for anItu in theItuS:
                    with XmlWrite.Element(myS, 'li'):
                        with XmlWrite.Element(myS, 'tt'):
                            with XmlWrite.Element(myS, 'a', {'href': tuIndexFileName(anItu)}):
                                myS.characters(anItu)

            _writeCommandLineInvocationToHTML(myS, theJobSpec)
        with XmlWrite.Element(myS, 'p'):
            myS.characters(('Total number of files processed: {:,d}').format(total_files))
        with XmlWrite.Element(myS, 'p'):
            myS.characters(('Total number of lines processed: {:,d}').format(total_lines))
        with XmlWrite.Element(myS, 'p'):
            myS.characters(('Total number of bytes processed: {:,d}').format(total_bytes))
        _writeIndexHtmlTrailer(myS, time_start)
    return indexPath


def _writeCommandLineInvocationToHTML(theS, theJobSpec):
    with XmlWrite.Element(theS, 'h2'):
        theS.characters('CPIP Command line:')
    with XmlWrite.Element(theS, 'pre'):
        theS.characters(theJobSpec.cmdLine)
    with XmlWrite.Element(theS, 'table', {'border': '1'}):
        with XmlWrite.Element(theS, 'tr'):
            with XmlWrite.Element(theS, 'th', {'style': 'padding: 2px 6px 2px 6px'}):
                theS.characters('Option')
            with XmlWrite.Element(theS, 'th', {'style': 'padding: 2px 6px 2px 6px'}):
                theS.characters('Value')
            with XmlWrite.Element(theS, 'th', {'style': 'padding: 2px 6px 2px 6px'}):
                theS.characters('Description')
        optS = sorted(theJobSpec.helpMap.keys())
        for o in optS:
            with XmlWrite.Element(theS, 'tr'):
                with XmlWrite.Element(theS, 'td', {'style': 'padding: 2px 6px 2px 6px'}):
                    with XmlWrite.Element(theS, 'tt'):
                        theS.characters(str(o))
                with XmlWrite.Element(theS, 'td', {'style': 'padding: 2px 6px 2px 6px'}):
                    with XmlWrite.Element(theS, 'tt'):
                        myVal = theJobSpec.helpMap[o][0]
                        if type(myVal) == list or type(myVal) == tuple:
                            if len(myVal) > 0:
                                for i, aVal in enumerate(myVal):
                                    if i > 0:
                                        theS.characters(',')
                                        with XmlWrite.Element(theS, 'br'):
                                            pass
                                    theS.characters(str(aVal))

                            else:
                                theS.literal('&nbsp;')
                        else:
                            theS.characters(str(myVal))
                with XmlWrite.Element(theS, 'td', {'style': 'padding: 2px 6px 2px 6px'}):
                    for i, aLine in enumerate(theJobSpec.helpMap[o][1].strip().split('\n')):
                        if i > 0:
                            with XmlWrite.Element(theS, 'br'):
                                pass
                        theS.characters(aLine)


def retOptionMap(theOptParser, theOpts):
    """Returns map of {opt_name : (value, help), ...} from the current options."""
    varsOpts = vars(theOpts)
    retMap = {}
    for k in sorted(theOptParser._option_string_actions.keys()):
        optDest = theOptParser._option_string_actions[k].dest
        optName = ('/').join(theOptParser._option_string_actions[k].option_strings)
        try:
            optValue = varsOpts[optDest]
            if hasattr(theOptParser._option_string_actions[k], 'help'):
                optHelp = theOptParser._option_string_actions[k].help.replace('[default: %(default)s]', '')
                retMap[optName] = (optValue, optHelp)
        except KeyError:
            pass

    return retMap


def preProcessFilesMP(dIn, dOut, jobSpec, glob, recursive, jobs):
    """Multiprocessing code to preprocess directories. Returns a count of ITUs
    processed."""
    if jobs < 0:
        raise ValueError('preProcessFilesMP(): can not run with negative number of jobs: %d' % jobs)
    if jobs == 0:
        jobs = multiprocessing.cpu_count()
    assert jobs > 1, 'preProcessFilesMP(): number of jobs: %d???' % jobs
    logging.info('plotLogPassesMP(): Setting multi-processing jobs to %d' % jobs)
    myTaskS = [ (t.filePathIn, t.filePathOut, jobSpec) for t in DirWalk.dirWalk(dIn, dOut, glob, recursive, bigFirst=True)
              ]
    with multiprocessing.Pool(processes=jobs) as (myPool):
        if jobSpec.keepGoing:
            fn = preprocessFileToOutputNoExcept
        else:
            fn = preprocessFileToOutput
        myResults = [ r.get() for r in [ myPool.apply_async(fn, t) for t in myTaskS ] ]
    return myResults


def _removeCommonPrefixFromResults(titlePathTupleS):
    """Given a list of:
    ``PpProcessResult(ituPath, indexPath, tuIndexFileName(ituPath),
                      total_files, total_lines, total_bytes)``
    This prunes the commmon prefix from the ituPath.
    """
    l = CommonPrefix.lenCommonPrefix([ r.ituPath for r in titlePathTupleS ])
    prefixOut = ''
    if l > 0:
        assert len(titlePathTupleS) > 0
        for tpt in titlePathTupleS:
            if tpt[1] is not None:
                prefixOut = tpt[1][:l]
                break

    return (
     prefixOut, sorted([ PpProcessResult(fields[0][l:], *fields[1:]) for fields in titlePathTupleS ]))


def _writeDirectoryIndexHTML(theInDir, theOutDir, titlePathTupleS, theJobSpec, time_start):
    """Writes a super index.html when a directory has been processed.
    titlePathTuples is a list of:
    ``PpProcessResult(ituPath, indexPath, tuIndexFileName, total_files, total_lines, total_bytes)``
    """
    indexPath = os.path.join(theOutDir, 'index.html')
    TokenCss.writeCssToDir(theOutDir)
    _prefixOut, titlePathTupleS = _removeCommonPrefixFromResults(titlePathTupleS)
    with XmlWrite.XhtmlStream(indexPath, mustIndent=INDENT_ML) as (myS):
        with XmlWrite.Element(myS, 'head'):
            with XmlWrite.Element(myS, 'link', {'href': TokenCss.TT_CSS_FILE, 
               'type': 'text/css', 
               'rel': 'stylesheet'}):
                pass
            with XmlWrite.Element(myS, 'title'):
                myS.characters('CPIP Processing')
        total_files = total_lines = total_bytes = 0
        with XmlWrite.Element(myS, 'body'):
            with XmlWrite.Element(myS, 'h1'):
                myS.characters('CPIP Directory Processing in output location: %s' % theOutDir)
            with XmlWrite.Element(myS, 'h2'):
                myS.characters('Files Processed as Translation Units:')
            with XmlWrite.Element(myS, 'p'):
                myS.characters('Input: ')
                with XmlWrite.Element(myS, 'tt'):
                    myS.characters(theInDir)
            with XmlWrite.Element(myS, 'ul'):
                for titlePathTuple in titlePathTupleS:
                    if titlePathTuple.indexPath is not None and titlePathTuple.tuIndexFileName is not None:
                        indexHTMLPath = os.path.relpath(titlePathTuple.indexPath, theOutDir)
                        indexHTMLPath = os.path.join(os.path.dirname(titlePathTuple.indexPath), titlePathTuple.tuIndexFileName)
                    else:
                        indexHTMLPath = None
                    with XmlWrite.Element(myS, 'li'):
                        with XmlWrite.Element(myS, 'tt'):
                            if indexHTMLPath is not None:
                                with XmlWrite.Element(myS, 'a', {'href': indexHTMLPath}):
                                    myS.characters(titlePathTuple.ituPath)
                            else:
                                myS.characters('%s [FAILED]' % titlePathTuple.ituPath)
                    total_files += titlePathTuple.total_files
                    total_lines += titlePathTuple.total_lines
                    total_bytes += titlePathTuple.total_bytes

            _writeCommandLineInvocationToHTML(myS, theJobSpec)
        with XmlWrite.Element(myS, 'p'):
            myS.characters(('Total number of files processed: {:,d}').format(total_files))
        with XmlWrite.Element(myS, 'p'):
            myS.characters(('Total number of lines processed: {:,d}').format(total_lines))
        with XmlWrite.Element(myS, 'p'):
            myS.characters(('Total number of bytes processed: {:,d}').format(total_bytes))
        _writeIndexHtmlTrailer(myS, time_start)
    return


def preprocessDirToOutput(inDir, outDir, jobSpec, globMatch, recursive, numJobs):
    """Pre-process all the files in a directory. Returns a count of the TUs.
    This uses multiprocessing where possible.
    Any Exception (such as a KeyboardInterupt) will terminate this function but
    write out an index of what has been achieved so far."""
    assert os.path.isdir(inDir)
    time_start = time.time()
    try:
        if numJobs != 1:
            results = preProcessFilesMP(inDir, outDir, jobSpec, globMatch, recursive, numJobs)
        else:
            results = []
            for t in DirWalk.dirWalk(inDir, outDir, globMatch, recursive, bigFirst=False):
                if jobSpec.keepGoing:
                    fn = preprocessFileToOutputNoExcept
                else:
                    fn = preprocessFileToOutput
                results.append(fn(t.filePathIn, t.filePathOut, jobSpec))

    finally:
        _writeDirectoryIndexHTML(inDir, outDir, results, jobSpec, time_start)


def preprocessFileToOutputNoExcept(ituPath, *args, **kwargs):
    """Preprocess a single file and catch all ExceptionCpip
    exceptions and log them."""
    try:
        return preprocessFileToOutput(ituPath, *args, **kwargs)
    except ExceptionCpip as err:
        logging.critical('preprocessFileToOutputNoExcept(): "%s" %s' % (err, ituPath))

    return PpProcessResult(ituPath, None, None, 0, 0, 0)


def preprocessFileToOutput(ituPath, outDir, jobSpec):
    """Preprocess a single file. May raise ExceptionCpip (or worse!).
    Returns a: ``PpProcessResult(ituPath, indexPath, tuIndexFileName(ituPath)
    total_files, total_lines, total_bytes)``
    """
    assert os.path.isfile(ituPath)
    time_start = time.time()
    logging.info('preprocessFileToOutput(): %s' % ituPath)
    if not os.path.exists(outDir):
        try:
            os.makedirs(outDir)
        except OSError:
            pass

    myItuToHtmlFileSet = set()
    myLexer = PpLexer.PpLexer(ituPath, jobSpec.incHandler, preIncFiles=jobSpec.preIncFiles, diagnostic=jobSpec.diagnostic, pragmaHandler=jobSpec.pragmaHandler, stdPredefMacros=jobSpec.preDefMacros, gccExtensions=jobSpec.gccExtensions)
    myDestFile = os.path.join(outDir, tuFileName(ituPath))
    logging.info('TU in HTML:')
    logging.info('  %s', myDestFile)
    myTokCntr, mySetItuLines = Tu2Html.processTuToHtml(myLexer, myDestFile, ituPath, jobSpec.conditionalLevel, tuIndexFileName(ituPath), incItuAnchors=True)
    logging.info('preprocessFileToOutput(): Processing TU done.')
    myFileCountMap = retFileCountMap(myLexer)
    for aSrc in sorted(myFileCountMap.keys()):
        myItuToHtmlFileSet.add(aSrc)

    if 'C' in jobSpec.dumpList:
        _dumpCondCompGraph(myLexer)
    if 'I' in jobSpec.dumpList:
        _dumpIncludeGraph(myLexer)
    if 'F' in jobSpec.dumpList:
        _dumpFileCount(myFileCountMap)
    if 'T' in jobSpec.dumpList:
        _dumpTokenCount(myTokCntr)
    if 'M' in jobSpec.dumpList:
        _dumpMacroEnv(myLexer)
    if 'R' in jobSpec.dumpList:
        _dumpMacroEnvDot(myLexer)
    logging.info('Macro history to:')
    logging.info('  %s', outDir)
    myMacroRefMap, macroHistoryIndexName = MacroHistoryHtml.processMacroHistoryToHtml(myLexer, outDir, ituPath, tuIndexFileName(ituPath))
    outPath = os.path.join(outDir, includeGraphFileNameSVG(ituPath))
    logging.info('Include graph (SVG) to:')
    logging.info('  %s', outPath)
    IncGraphSVGBase.processIncGraphToSvg(myLexer, outPath, IncGraphSVG.SVGTreeNodeMain, 'left', '+')
    logging.info('Writing include graph (TEXT) to:')
    logging.info('  %s', outPath)
    writeIncludeGraphAsText(outDir, ituPath, myLexer)
    if jobSpec.includeDOT:
        logging.info('Writing include graph (DOT) to:')
        logging.info('  %s', outPath)
        hasIncGraphDot = writeIncludeGraphAsDot(outDir, ituPath, myLexer)
    else:
        hasIncGraphDot = False
    outPath = os.path.join(outDir, includeGraphFileNameCcg(ituPath))
    logging.info('Conditional compilation graph in HTML:')
    logging.info('  %s', outPath)
    CppCondGraphToHtml.processCppCondGrphToHtml(myLexer, outPath, 'Conditional Compilation Graph', tuIndexFileName(ituPath))
    total_files, total_lines, total_bytes = writeTuIndexHtml(outDir, ituPath, myLexer, myFileCountMap, myTokCntr, hasIncGraphDot, macroHistoryIndexName)
    logging.info('Done: %s', ituPath)
    myCcgvcl = CppCond.CppCondGraphVisitorConditionalLines()
    myLexer.condCompGraph.visit(myCcgvcl)
    for aSrc in sorted(myItuToHtmlFileSet):
        try:
            if aSrc != PpLexer.UNNAMED_FILE_NAME:
                logging.info('ITU in HTML: .../%s', os.path.basename(aSrc))
                ItuToHtml.ItuToHtml(aSrc, outDir, keepGoing=jobSpec.keepGoing, macroRefMap=myMacroRefMap, cppCondMap=myCcgvcl, ituToTuLineSet=mySetItuLines if aSrc == ituPath else None)
        except ItuToHtml.ExceptionItuToHTML as err:
            logging.error('Can not write ITU "%s" to HTML: %s', aSrc, str(err))

    indexPath = writeIndexHtml([
     ituPath], outDir, jobSpec, time_start, total_files, total_lines, total_bytes)
    logging.info('preprocessFileToOutput(): %s DONE' % ituPath)
    return PpProcessResult(ituPath, indexPath, tuIndexFileName(ituPath), total_files, total_lines, total_bytes)


def main():
    """Processes command line to preprocess a file or a directory."""
    program_version = 'v%s' % __version__
    program_shortdesc = 'CPIPMain.py - Preprocess the file or the files in a directory.'
    program_license = '%s\n  Created by Paul Ross on %s.\n  Copyright 2008-2017. All rights reserved.\n  Version: %s\n  Licensed under GPL 2.0\nUSAGE\n' % (program_shortdesc, program_version, str(__date__))
    parser = argparse.ArgumentParser(description=program_license, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-c', action='store_true', dest='plot_conditional', default=False, help='Add conditionally included files to the plots. [default: %(default)s]')
    parser.add_argument('-d', '--dump', action='append', dest='dump', default=[], help='Dump output, additive. Can be:\nC - Conditional compilation graph.\nF - File names encountered and their count.\nI - Include graph.\nM - Macro environment.\nT - Token count.\nR - Macro dependencies as an input to DOT.\n[default: %(default)s]')
    parser.add_argument('-g', '--glob', action='append', default=[], help='Pattern match to use when processing directories. [default: %(default)s] i.e. every file.')
    parser.add_argument('--heap', action='store_true', dest='heap', default=False, help='Profile memory usage. [default: %(default)s]')
    parser.add_argument('-j', '--jobs', type=int, dest='jobs', default=0, help='Max simultaneous processes when pre-processing\ndirectories. Zero uses number of native CPUs [%d].\n1 means no multiprocessing.' % multiprocessing.cpu_count() + ' [default: %(default)s]')
    parser.add_argument('-k', '--keep-going', action='store_true', dest='keep_going', default=False, help='Keep going. [default: %(default)s]')
    parser.add_argument('-l', '--loglevel', type=int, dest='loglevel', default=30, help='Log Level (debug=10, info=20, warning=30, error=40, critical=50) [default: %(default)s]')
    parser.add_argument('-o', '--output', type=str, dest='output', default='out', help='Output directory. [default: %(default)s]')
    parser.add_argument('-p', action='store_true', dest='ignore_pragma', default=False, help='Ignore pragma statements. [default: %(default)s]')
    parser.add_argument('-r', '--recursive', action='store_true', dest='recursive', default=False, help='Recursively process directories. [default: %(default)s]')
    parser.add_argument('-t', '--dot', action='store_true', dest='include_dot', default=False, help='Write an DOT include dependency table and execute DOT\non it to create a SVG file. [default: %(default)s]')
    parser.add_argument('-G', action='store_true', dest='gcc_extensions', default=False, help='Support GCC extensions. Currently only #include_next. [default: %(default)s]')
    parser.add_argument(dest='path', nargs=1, help='Path to source file or directory.')
    Cpp.addStandardArguments(parser)
    args = parser.parse_args()
    clkStart = time.clock()
    inPath = args.path[0]
    if args.jobs != 1 and os.path.isdir(inPath):
        logFormat = '%(asctime)s %(levelname)-8s [%(process)5d] %(message)s'
    else:
        logFormat = '%(asctime)s %(levelname)-8s %(message)s'
    logging.basicConfig(level=args.loglevel, format=logFormat, stream=sys.stdout)
    if args.heap:
        try:
            from guppy import hpy
        except ImportError:
            print 'Can not profile memory as you do not have guppy installed: http://guppy-pe.sourceforge.net/'
            args.heap = False

    if args.heap:
        myHeap = hpy()
        myHeap.setrelheap()
    else:
        myHeap = None
    myIncH = IncludeHandler.CppIncludeStdOs(theUsrDirs=args.incUsr or [], theSysDirs=args.incSys or [])
    preDefMacros = {}
    if args.predefines:
        for d in args.predefines:
            _tup = d.split('=')
            if len(_tup) == 2:
                preDefMacros[_tup[0]] = _tup[1] + '\n'
            elif len(_tup) == 1:
                preDefMacros[_tup[0]] = '\n'
            else:
                raise ValueError('Can not read macro definition: %s' % d)

    jobSpec = MainJobSpec(incHandler=myIncH, preDefMacros=preDefMacros, preIncFiles=Cpp.predefinedFileObjects(args), diagnostic=CppDiagnostic.PreprocessDiagnosticKeepGoing() if args.keep_going else None, pragmaHandler=PragmaHandler.PragmaHandlerNull() if args.ignore_pragma else None, keepGoing=args.keep_going, conditionalLevel=2 if args.plot_conditional else 0, dumpList=args.dump, helpMap=retOptionMap(parser, args), includeDOT=args.include_dot, cmdLine=(' ').join(sys.argv), gccExtensions=args.gcc_extensions)
    if os.path.isfile(inPath):
        time_start = time.time()
        result = preprocessFileToOutput(inPath, args.output, jobSpec)
        writeIndexHtml([inPath], args.output, jobSpec, time_start, *result[-3:])
    elif os.path.isdir(inPath):
        preprocessDirToOutput(inPath, args.output, jobSpec, globMatch=args.glob, recursive=args.recursive, numJobs=args.jobs)
    else:
        logging.fatal('%s is neither a file or a directory!' % inPath)
        return 1
    if args.heap and myHeap is not None:
        print 'Dump of heap:'
        h = myHeap.heap()
        print h
        print ()
        print 'Dump of heap byrcs:'
        print h.byrcs
        print ()
    clkExec = time.clock() - clkStart
    print 'CPU time = %8.3f (S)' % clkExec
    print 'Bye, bye!'
    return 0


if __name__ == '__main__':
    multiprocessing.freeze_support()
    sys.exit(main())