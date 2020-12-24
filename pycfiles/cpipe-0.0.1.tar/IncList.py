# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/IncList.py
# Compiled at: 2017-10-03 13:07:16
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import sys, logging, time
from optparse import OptionParser
import io
from cpip.core import PpLexer
from cpip.core import IncludeHandler
from cpip.core import CppDiagnostic
from cpip.core import FileIncludeGraph
from cpip.core import PragmaHandler

def retIncludedFileSet(theLexer):
    myFigr = theLexer.fileIncludeGraphRoot
    myFileNameVis = FileIncludeGraph.FigVisitorFileSet()
    myFigr.acceptVisitor(myFileNameVis)
    return myFileNameVis.fileNameSet


def preProcessForIncludes(theItu, incUsr, incSys, theDefineS, preIncS, keepGoing, ignorePragma):
    myIncH = IncludeHandler.CppIncludeStdOs(theUsrDirs=incUsr or [], theSysDirs=incSys or [])
    myPreIncFiles = []
    if theDefineS:
        myStr = ('\n').join([ '#define ' + (' ').join(d.split('=')) for d in theDefineS ]) + '\n'
        myPreIncFiles = [io.StringIO(myStr)]
    myPreIncFiles.extend([ open(f) for f in preIncS ])
    myDiag = None
    if keepGoing:
        myDiag = CppDiagnostic.PreprocessDiagnosticKeepGoing()
    myPh = None
    if ignorePragma:
        myPh = PragmaHandler.PragmaHandlerNull()
    myLexer = PpLexer.PpLexer(theItu, myIncH, preIncFiles=myPreIncFiles, diagnostic=myDiag, pragmaHandler=myPh)
    logging.info('Preprocessing TU: %s' % theItu)
    for t in myLexer.ppTokens():
        pass

    logging.info('Preprocessing TU done.')
    retVal = retIncludedFileSet(myLexer)
    try:
        retVal.remove(PpLexer.UNNAMED_FILE_NAME)
    except KeyError:
        pass

    return retVal


def main():
    usage = 'usage: %prog [options] files...\nPreprocess the files and lists included files.'
    optParser = OptionParser(usage, version='%prog ' + __version__)
    optParser.add_option('-k', action='store_true', dest='keep_going', default=False, help='Keep going. [default: %default]')
    optParser.add_option('-l', '--loglevel', type='int', dest='loglevel', default=30, help='Log Level (debug=10, info=20, warning=30, error=40, critical=50) [default: %default]')
    optParser.add_option('-n', action='store_true', dest='nervous', default=False, help='Nervous mode (do no harm). [default: %default]')
    optParser.add_option('-p', action='store_true', dest='ignore_pragma', default=False, help='Ignore pragma statements. [default: %default]')
    optParser.add_option('-I', '--usr', action='append', dest='incUsr', default=[], help='Add user include search path. [default: %default]')
    optParser.add_option('-J', '--sys', action='append', dest='incSys', default=[], help='Add system include search path. [default: %default]')
    optParser.add_option('-P', '--pre', action='append', dest='preInc', default=[], help='Add pre-include file path. [default: %default]')
    optParser.add_option('-D', '--define', action='append', dest='defines', default=[], help='Add macro defintions of the form name<=defintion>.\n                      These are introduced into the environment before any pre-include. [default: %default]')
    opts, args = optParser.parse_args()
    clkStart = time.clock()
    logging.basicConfig(level=opts.loglevel, format='%(asctime)s %(levelname)-8s %(message)s', stream=sys.stdout)
    if len(args) > 0:
        myFileSet = set()
        for anItu in args:
            myFileSet.update(preProcessForIncludes(anItu, opts.incUsr, opts.incSys, opts.defines, opts.preInc, opts.keep_going, opts.ignore_pragma))

        logging.info('All done.')
        myFileS = list(myFileSet)
        myFileS.sort()
        message = ' Included files [%d] ' % len(myFileS)
        print message.center(75, '-')
        print ('\n').join(myFileS)
        print (' Included files ').center(75, '-')
    else:
        optParser.print_help()
        optParser.error('No arguments!')
        return 1
    clkExec = time.clock() - clkStart
    print 'CPU time = %8.3f (S)' % clkExec
    print 'Bye, bye!'
    return 0


if __name__ == '__main__':
    sys.exit(main())