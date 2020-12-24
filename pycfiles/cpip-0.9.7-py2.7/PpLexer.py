# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/core/PpLexer.py
# Compiled at: 2017-10-03 13:07:16
"""Generates tokens from a C or C++ translation unit.

TODO: Fix accidental token pasting. See: TestFromCppInternalsTokenspacing
and, connected is:
TODO: Set setPrevWs flag on the token where necessary.

TODO: Preprocessor statements in arguments of function like macros. Sect. 3.9
of cpp.pdf and existing MacroEnv tests.
"""
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import logging, os, datetime
from cpip.core import ConstantExpression
from cpip.core import CppCond
from cpip.core import CppDiagnostic
from cpip.core import FileIncludeStack
from cpip.core import IncludeHandler
from cpip.core import MacroEnv
from cpip.core import PpToken
from cpip.core import PpTokeniser
from cpip.core import PpWhitespace
from cpip.core import PragmaHandler
from cpip.util import ListGen
from cpip import ExceptionCpip

class ExceptionPpLexer(ExceptionCpip):
    """Exception when handling PpLexer object."""
    pass


class ExceptionPpLexerPreInclude(ExceptionPpLexer):
    """Exception when loading pre-include files."""
    pass


class ExceptionPpLexerPreIncludeIncNoCp(ExceptionPpLexerPreInclude):
    """Exception when loading a pre-include file that has no current place
    (e.g. a StringIO object) and the pre-include then has an #include
    statement."""
    pass


class ExceptionPpLexerDefine(ExceptionPpLexer):
    """Exception when loading predefined macro definitions."""
    pass


class ExceptionPpLexerNoFile(ExceptionPpLexer):
    """Exception when can not find file."""
    pass


class ExceptionPpLexerPredefine(ExceptionPpLexerDefine):
    """Exception when loading predefined macro definitions."""
    pass


class ExceptionPpLexerCallStack(ExceptionPpLexer):
    """Exception when finding issues with the call stack or nested includes."""
    pass


class ExceptionPpLexerCallStackTooSmall(ExceptionPpLexerCallStack):
    """Exception when sys.getrecursionlimit() is too small."""
    pass


class ExceptionPpLexerNestedInclueLimit(ExceptionPpLexerCallStack):
    """Exception when nested #include limit exceeded."""
    pass


class ExceptionPpLexerCondLevelOutOfRange(ExceptionPpLexer):
    """Exception when handling a conditional token generation level."""
    pass


class ExceptionPpLexerAlreadyGenerating(ExceptionPpLexer):
    """Exception when two generators are created then the internal state will become inconsistent."""

    def __init__(self):
        super(ExceptionPpLexerAlreadyGenerating, self).__init__('A generator is already active and the PpLexer internal state will become inconsistent. Create a new PpLexer for each generator.')


class ExceptionConditionalExpression(ExceptionPpLexer):
    """Exception when eval() conditional expressions."""
    pass


PREPROCESSING_DIRECTIVES = [
 'if',
 'ifdef',
 'ifndef',
 'elif',
 'else',
 'endif',
 'include',
 'define',
 'undef',
 'line',
 'error',
 'pragma']
UNNAMED_FILE_NAME = 'Unnamed Pre-include'

class PpLexer(object):
    """Create a translation unit tokeniser that applies
    :title-reference:`ISO/IEC 9899:1999(E) Section 6`
    and/or :title-reference:`ISO/IEC 14882:1998(E) section 16`.
    
    *tuFileId*
        A file ID that will be given to the include handler to find the
        translation unit. Typically this will be the file path (as a string)
        to the file that is the Initial Translation Unit (ITU)
        i.e. the file being preprocessed.
        
    *includeHandler*
        A handler to file ``#includ``'d files typically a
        :py:class:`.IncludeHandler.IncludeHandlerStd`.
        This might have user and system include path information and a means
        of resolving file references.

    *preIncFiles*
        An ordered list of file like objects that are pre-include files.
        These are processed in order before the ITU is processed.
        Macro redefinition rules apply.

    *diagnostic*
        A diagnostic object, defaults to a
        :py:class:`.CppDiagnostic.PreprocessDiagnosticStd`.
        
    *pragmaHandler*
        A handler for ``#pragma`` statements.
        
        This must have the attribute ``replaceTokens``
        is to be implemented, if True then the tokens stream will be be
        macro replaced before being passed to the pragma handler.
        
        This must have a function ``pragma()`` defined that takes a non-zero
        length list of :py:class:`.PpToken.PpToken` the last of which will be a
        newline token. The tokens returned will be yielded.
        
    *stdPredefMacros*
        A dictionary of Standard pre-defined macros. See for example:
        :title-reference:`ISO/IEC 9899:1999 (E) 6.10.8 Predefined macro names`
        :title-reference:`ISO/IEC 14882:1998 (E) 16.8 Predefined macro names`
        :title-reference:`N2800=08-0310 16.8 Predefined macro names`
                        
        The macros ``__DATE__`` and ``__TIME__`` will be automatically
        updated to current locale date/time (see autoDefineDateTime).
        
    *autoDefineDateTime*
        If True then the macros ``__DATE__`` and ``__TIME__`` will be
        automatically updated to current locale date/time. Mostly this is
        used for testing.
    
    *gccExtensions*
        Support GCC extensions. Currently just ``#include_next`` is supported.

    *annotateLineFile* - if True then PpToken will output line number and file as cpp.
        For example::
        
            # 22 "/usr/include/stdio.h" 3 4
            # 59 "/usr/include/stdio.h" 3 4
            # 1 "/usr/include/sys/cdefs.h" 1 3 4
    
    TODO: Set flags here rather than supplying them to a generator?
    This would make the API simply the ctor and ppTokens/next().
    Flags would be:
    incWs - Include whitespace tokens.
    condLevel - (0, 1, 2) thus:
    
        0: No conditionally compiled tokens. The fileIncludeGraphRoot will
            not have any information about conditionally included files.
        1: Conditionally compiled tokens are generated but not from 
            conditionally included files. The fileIncludeGraphRoot will have
            a reference to a conditionally included file but not that
            included file's includes.
        2: Conditionally compiled tokens including tokens from conditionally
            included files. The fileIncludeGraphRoot will have all the
            information about conditionally included files recursively.
    """
    PP_DIRECTIVE_PREFIX = '#'
    MAX_INCLUDE_DEPTH = 200
    CALL_STACK_DEPTH_ASSUMED_PPTOKENS = 10
    CALL_STACK_DEPTH_FIRST_INCLUDE = 3
    CALL_STACK_DEPTH_PER_INCLUDE = 3
    COND_LEVEL_DEFAULT = 0
    COND_LEVEL_OPTIONS = range(3)

    def __init__(self, tuFileId, includeHandler, preIncFiles=None, diagnostic=None, pragmaHandler=None, stdPredefMacros=None, autoDefineDateTime=True, gccExtensions=False, annotateLineFile=False):
        self._tuFileId = tuFileId
        self._includeHandler = includeHandler
        self._preIncFiles = preIncFiles or []
        self._gccExtensions = gccExtensions
        self._annotateLineFile = annotateLineFile
        self._diagnostic = diagnostic or CppDiagnostic.PreprocessDiagnosticStd()
        self._pragmaHandler = pragmaHandler
        self._wsHandler = PpWhitespace.PpWhitespace()
        self._tuIndex = 0
        self._KEYWORD_DESPATCH = {'if': self._cppIf, 
           'ifdef': self._cppIfdef, 
           'ifndef': self._cppIfndef, 
           'elif': self._cppElif, 
           'else': self._cppElse, 
           'endif': self._cppEndif, 
           'include': self._cppInclude, 
           'define': self._cppDefine, 
           'undef': self._cppUndef, 
           'line': self._cppLine, 
           'error': self._cppError, 
           'pragma': self._cppPragma, 
           'warning': self._cppWarning}
        if self._gccExtensions:
            self._KEYWORD_DESPATCH['include_next'] = self._cppIncludeNext
        for aType in PREPROCESSING_DIRECTIVES:
            assert aType in self._KEYWORD_DESPATCH

        if stdPredefMacros is None:
            stdPredefMacros = {}
        if autoDefineDateTime:
            dt = datetime.datetime.now()
            stdPredefMacros['__DATE__'] = dt.strftime('%b') + ' %2d' % dt.day + dt.strftime(' %Y') + '\n'
            stdPredefMacros['__TIME__'] = dt.strftime('%H:%M:%S') + '\n'
        self._macroEnv = MacroEnv.MacroEnv(stdPredefMacros=stdPredefMacros)
        self._condLevel = self.COND_LEVEL_DEFAULT
        self._condStack = CppCond.CppCond()
        self._condCompGraph = CppCond.CppCondGraph()
        self._isNewline = True
        self._tuFpo = None
        self._fis = FileIncludeStack.FileIncludeStack(self._diagnostic)
        self._isGenerating = False
        return

    def _genPreIncludeTokens(self):
        """Reads all the pre-include files and loads the macro environment."""
        for i, aFileObj in enumerate(self._preIncFiles):
            logging.debug('PpLexer._initialisePreIncludes() [%d] %s', i, aFileObj)
            aFileObj.seek(0)
            try:
                fileId = aFileObj.name
                currPlace = os.path.dirname(aFileObj.name)
            except AttributeError:
                fileId = UNNAMED_FILE_NAME
                currPlace = None

            myFpo = IncludeHandler.FilePathOrigin(aFileObj, fileId, currPlace, 'pre-include')
            self._includeHandler.cpStackPush(myFpo)
            myGen = self._pptPush(myFpo)
            for optionalLineFileToken in self._pptPostPush():
                yield optionalLineFileToken

            try:
                try:
                    for aTok in self._genPpTokensRecursive(myGen):
                        yield aTok

                except CppDiagnostic.ExceptionCppDiagnosticUndefined as err:
                    raise ExceptionPpLexerPredefine(err)
                except ExceptionCpip as err:
                    raise ExceptionPpLexerPreInclude('Failed to process pre-include with error: %s' % str(err))

            finally:
                if self._includeHandler.cpStackSize == 0:
                    raise ExceptionPpLexerPreIncludeIncNoCp('Pre-include [%d] attempted to #inlcude when there is no current place.' % i)
                else:
                    self._includeHandler.cpStackPop()
                self._pptPop()
                for optionalLineFileToken in self._pptPostPop():
                    yield optionalLineFileToken

            logging.debug('PpLexer._initialisePreIncludes() [%d] - Done', i)

        return

    def finalise(self):
        """Finalisation, may raise any Exception."""
        self._includeHandler.finalise()
        self._condStack.close()
        self._fis.finalise()

    def ppTokens(self, incWs=True, minWs=False, condLevel=0):
        """A generator for providing a sequence of :py:class:`.PpToken.PpToken`
        in accordance with section 16 of :title-reference:`ISO/IEC 14882:1998(E)`.
        
        *incWs* - if True than whitespace tokens are included (i.e. tok.isWs() == True).
        
        *minWs* - if True then whitespace runs will be minimised to a single
        space or, if  newline is in the whitespace run, a single newline
        
        *condLevel* - if !=0 then conditionally compiled tokens will be yielded
        and they will have have tok.isCond == True. The fileIncludeGraphRoot
        will be marked up with the appropriate conditionality. Levels are::

            0: No conditionally compiled tokens. The fileIncludeGraphRoot will
            not have any information about conditionally included files.
    
            1: Conditionally compiled tokens are generated but not from 
            conditionally included files. The fileIncludeGraphRoot will have
            a reference to a conditionally included file but not that
            included file's includes.
    
            2: Conditionally compiled tokens including tokens from conditionally
            included files. The fileIncludeGraphRoot will have all the
            information about conditionally included files recursively.

        (see _cppInclude where we check if self._condStack.isTrue():)."""
        if self._isGenerating:
            raise ExceptionPpLexerAlreadyGenerating()
        self._isGenerating = True
        if condLevel not in self.COND_LEVEL_OPTIONS:
            raise ExceptionPpLexerCondLevelOutOfRange('Conditional level %s not in %s.' % (
             condLevel, str(self.COND_LEVEL_OPTIONS)))
        self._condLevel = condLevel
        wsBuf = []
        for aTok in self._genPreIncludeTokens():
            if minWs and aTok.isWs():
                wsBuf.append(aTok)
            elif (incWs or not aTok.isWs()) and (self._condLevel or not aTok.isCond):
                if not aTok.isWs() and len(wsBuf) > 0:
                    for aWsT in wsBuf:
                        if self._wsHandler.isBreakingWhitespace(aWsT.t):
                            yield PpToken.PpToken('\n', 'whitespace')
                            break
                    else:
                        yield PpToken.PpToken(' ', 'whitespace')

                    wsBuf = []
                yield aTok
                self._tuIndex += len(aTok.t)

        if len(wsBuf) > 0:
            for aWsT in wsBuf:
                if self._wsHandler.isBreakingWhitespace(aWsT.t):
                    yield PpToken.PpToken('\n', 'whitespace')
                    break
            else:
                yield PpToken.PpToken(' ', 'whitespace')

            wsBuf = []
        self._tuFpo = self._includeHandler.initialTu(self._tuFileId)
        if self._tuFpo is None:
            raise ExceptionPpLexerNoFile('Can not find file: "%s"' % self._tuFileId)
        self._tuFpo.fileObj.seek(0)
        myGen = self._pptPush(self._tuFpo)
        for optionalLineFileToken in self._pptPostPush():
            yield optionalLineFileToken

        try:
            for aTok in self._genPpTokensRecursive(myGen):
                if minWs and aTok.isWs():
                    wsBuf.append(aTok)
                elif (incWs or not aTok.isWs()) and (self._condLevel or not aTok.isCond):
                    if not aTok.isWs() and len(wsBuf) > 0:
                        for aWsT in wsBuf:
                            if self._wsHandler.isBreakingWhitespace(aWsT.t):
                                yield PpToken.PpToken('\n', 'whitespace')
                                break
                        else:
                            yield PpToken.PpToken(' ', 'whitespace')

                        wsBuf = []
                    yield aTok
                    self._tuIndex += len(aTok.t)

            if len(wsBuf) > 0:
                for aWsT in wsBuf:
                    if self._wsHandler.isBreakingWhitespace(aWsT.t):
                        yield PpToken.PpToken('\n', 'whitespace')
                        break
                else:
                    yield PpToken.PpToken(' ', 'whitespace')

                wsBuf = []
        finally:
            self._isGenerating = False
            try:
                self._includeHandler.endInclude()
                self._pptPop()
                for optionalLineFileToken in self._pptPostPop():
                    yield optionalLineFileToken

            except Exception as err:
                logging.fatal('PpLexer.ppTokens(): Encountered exception in finally clause: %s' % str(err))

        self.finalise()
        return

    def _genPpTokensRecursive(self, theGen):
        """Given a token generator this applies the lexical rules.
        This means handling preprocessor directives and macro replacement.
        With #included files this become recursive."""
        self._diagnostic.debug('_genPpTokensRecursive() START', self._fis.fileLineCol)
        hasReplToksOnLine = False
        lastToken = None
        try:
            while 1:
                myFlc = self.fileLineCol
                myTtt = next(theGen)
                if myTtt.t == self.PP_DIRECTIVE_PREFIX and self._isNewline and not hasReplToksOnLine:
                    for aTtt in self._processCppDirective(myTtt, theGen):
                        if self._condStack.isTrue():
                            lastToken = aTtt
                            yield aTtt
                            self._tuIndex += 1
                        else:
                            aTtt.setIsCond()
                            lastToken = aTtt
                            yield aTtt
                            self._tuIndex += 1

                elif self._condStack.isTrue():
                    self._fis.tokenCountInc(myTtt, True)
                    if self._macroEnv.mightReplace(myTtt):
                        try:
                            hasReplToksOnLine = True
                            if lastToken and lastToken.isReplacement and not lastToken.isWs():
                                yield PpToken.PpToken(' ', 'whitespace')
                            for aTtt in self._macroEnv.replace(myTtt, theGen, myFlc):
                                lastToken = aTtt
                                yield aTtt
                                self._tuIndex += 1

                        except ExceptionCpip as err:
                            self._diagnostic.error(str(err), self._fis.fileLineCol)

                    else:
                        if self._wsHandler.preceedsNewline(myTtt.t):
                            hasReplToksOnLine = False
                            self._isNewline = True
                        lastToken = myTtt
                        yield myTtt
                        self._tuIndex += 1
                else:
                    self._fis.tokenCountInc(myTtt, False)
                    myTtt.setIsCond()
                    lastToken = aTtt
                    yield myTtt
                    self._tuIndex += 1

        finally:
            try:
                self._diagnosticDebugMessage('_genPpTokens() END')
            except Exception as err:
                logging.fatal('PpLexer._genPpTokensRecursive(): Encountered exception in finally clause: %s' % str(err))

        return

    def _pptPush(self, theFpo):
        """This takes a IncludeHandler.FilePathOrigin object and pushes it onto
        the FileIncludeStack which creates a PpTokneiser object on the stack.
        This returns that PpTokeniser generator function."""
        if self._fis.depth > self.MAX_INCLUDE_DEPTH:
            raise ExceptionPpLexerNestedInclueLimit('Include stack of %d is greater than allowable limit of %d' % (
             self._fis.depth, self.MAX_INCLUDE_DEPTH))
        myLine = self.lineNum
        self._fis.includeStart(theFpo, myLine, self._condStack.isTrue(), str(self._condStack), self._includeHandler.findLogic)
        self._isNewline = True
        return self._fis.ppt.next()

    def _pptPop(self):
        """End a #included file."""
        self._fis.includeFinish()

    def _pptPostPush(self):
        """Called immediately after _pptPush() this, optionally, returns a list
        of PpToken's that can be yielded."""
        if self._annotateLineFile:
            flags = [
             '1']
            if self._fis.currentFileIsSystemFile:
                flags.append('3')
            return self._lineFileAnnotation(flags)
        return []

    def _pptPostPop(self):
        """Called immediately after _pptPop() this, optionally, returns a list
        of PpToken's that can be yielded."""
        if self._annotateLineFile:
            if self._fis.depth:
                flags = [
                 '2']
                if self._fis.currentFileIsSystemFile:
                    flags.append('3')
                return self._lineFileAnnotation(flags)
        return []

    def _lineFileAnnotation(self, flags):
        """Returns a list of PpTokens that represent the line number and file
        name. For example::

            # 22 "/usr/include/stdio.h" 3 4
            # 59 "/usr/include/stdio.h" 3 4
            # 1 "/usr/include/sys/cdefs.h" 1 3 4
        
        Trailing numbers are described here: https://gcc.gnu.org/onlinedocs/cpp/Preprocessor-Output.html
        '1' - This indicates the start of a new file. 
        '2' - This indicates returning to a file (after having included another file). 
        '3' - This indicates that the following text comes from a system header
                file, so certain warnings should be suppressed. 
        '4' - This indicates that the following text should be treated as being
                wrapped in an implicit extern "C" block.
        We don't support '4'
        """
        ret_val = [
         PpToken.PpToken('#', 'preprocessing-op-or-punc'),
         PpToken.PpToken(' ', 'whitespace'),
         PpToken.PpToken('%d' % self.fileLineCol.lineNum, 'pp-number'),
         PpToken.PpToken(' ', 'whitespace'),
         PpToken.PpToken('"%s"' % self.currentFile, 'string-literal')]
        if len(flags):
            for flag in flags:
                ret_val.append(PpToken.PpToken(' ', 'whitespace'))
                ret_val.append(PpToken.PpToken(flag, 'pp-number'))

        ret_val.append(PpToken.PpToken('\n', 'whitespace'))
        return ret_val

    @property
    def fileStack(self):
        """Returns the file stack."""
        return self._fis.fileStack

    @property
    def includeDepth(self):
        """Returns the integer depth of the include stack."""
        return self._fis.depth

    @property
    def currentFile(self):
        """Returns the file ID on the top of the file stack."""
        return self._fis.currentFile

    @property
    def fileIncludeGraphRoot(self):
        """Returns the :py:class:`.FileIncludeGraph.FileIncludeGraphRoot` object."""
        return self._fis.fileIncludeGraphRoot

    @property
    def condState(self):
        """The conditional state as (boolean,  string)."""
        return (
         self._condStack.isTrue(), str(self._condStack))

    @property
    def condCompGraph(self):
        """The conditional compilation graph as a :py:class:`.CppCond.CppCondGraph` object."""
        return self._condCompGraph

    @property
    def definedMacros(self):
        """Returns a string representing the currently defined macros."""
        return str(self._macroEnv)

    @property
    def macroEnvironment(self):
        """The current Macro environment as a :py:class:`.MacroEnv.MacroEnv` object.
        
        .. caution::
            Write to this at your own risk. Your write might be ignored or
            cause undefined behaviour."""
        return self._macroEnv

    @property
    def fileLineCol(self):
        """Returns a FileLineCol object or None"""
        if self._fis.depth > 0:
            return self._fis.fileLineCol

    @property
    def tuFileId(self):
        """Returns the user supplied ID of the translation unit."""
        return self._tuFileId

    @property
    def fileName(self):
        """Returns the current file name during processing."""
        return self._fis.currentFile

    @property
    def lineNum(self):
        """Returns the current line number as an integer during processing or None."""
        if self._fis.depth > 0:
            return self._fis.ppt.pLineCol[0]

    @property
    def colNum(self):
        """Returns the current column number as an integer during processing."""
        return self._fis.ppt.pLineCol[1]

    @property
    def tuIndex(self):
        return self._tuIndex

    def _diagnosticDebugMessage(self, theM):
        assert self._diagnostic is not None
        self._diagnostic.debug(theM, self.fileLineCol)
        return

    def _nextNonWsOrNewline(self, theGen, theDiscardList=None):
        """Returns the next non-whitespace token or whitespace that contains a
        newline. If theDiscardList is non-None intermediate tokens will be
        appended to it."""
        while 1:
            myTtt = next(theGen)
            if not myTtt.isWs() or self._wsHandler.isBreakingWhitespace(myTtt.t):
                return myTtt
            if theDiscardList is not None:
                theDiscardList.append(myTtt)

        return

    def _tokensToEol(self, theGen, macroReplace):
        """Returns a list of PpToken objects from a generator up to and
        including the first token that has a newline.
        If macroReplace is True then macros are replaced with the current
        environment."""
        retList = []
        while 1:
            myFlc = self.fileLineCol
            myTtt = next(theGen)
            if self._wsHandler.isBreakingWhitespace(myTtt.t):
                retList.append(myTtt)
                break
            elif macroReplace:
                if self._macroEnv.mightReplace(myTtt):
                    try:
                        for aTtt in self._macroEnv.replace(myTtt, theGen, myFlc):
                            retList.append(aTtt)

                    except ExceptionCpip as err:
                        self._diagnostic.error(str(err), self._fis.fileLineCol)

                    if len(retList) > 0 and self._wsHandler.isBreakingWhitespace(retList[(-1)].t):
                        break
                else:
                    retList.append(myTtt)
            else:
                retList.append(myTtt)

        return retList

    def _countNonWsTokens(self, theTokS):
        """Returns the integer count of non-whitespace tokens in the given list."""
        retCount = 0
        for aTok in theTokS:
            if not aTok.isWs():
                retCount += 1

        return retCount

    def _retListReplacedTokens(self, theTokS):
        """Takes a list of PpToken objects and returns a list of PpToken
        objects where macros are replaced in the current environment
        where possible.
        TODO: get pragma to use this."""
        retList = []
        if len(theTokS) > 0:
            myListAsGen = ListGen.ListAsGenerator(theTokS)
            myGen = next(myListAsGen)
            while not myListAsGen.listIsEmpty:
                myTok = next(myGen)
                if self._macroEnv.mightReplace(myTok):
                    for aTtt in self._macroEnv.replace(myTok, myGen, self.fileLineCol):
                        retList.append(aTtt)

                else:
                    retList.append(myTok)

        return retList

    def _processCppDirective(self, theTtt, theGen):
        """:title-reference:`ISO/IEC ISO/IEC 14882:1998(E) 16 Preprocessing directives [cpp]`
        This consumes tokens and generates others.
        Returns True of all tokens consumed OK, False otherwise.
        """
        assert theTtt.t == self.PP_DIRECTIVE_PREFIX
        assert theTtt.tt == 'preprocessing-op-or-punc'
        myFlc = self.fileLineCol
        myUnresolvedTokens = [theTtt]
        myTtt = self._nextNonWsOrNewline(theGen, myUnresolvedTokens)
        myUnresolvedTokens.append(myTtt)
        if self._wsHandler.isBreakingWhitespace(myTtt.t):
            yield PpToken.PpToken('\n', 'whitespace')
        elif myTtt.tt != 'identifier':
            self._diagnostic.undefined('invalid preprocessing directive "%s"' % ('').join([ t.t for t in myUnresolvedTokens ]), self._fis.fileLineCol)
            if not self._wsHandler.isBreakingWhitespace(myTtt.t):
                myUnresolvedTokens.extend(self._tokensToEol(theGen, macroReplace=False))
            for aTtt in myUnresolvedTokens:
                yield aTtt

        else:
            try:
                mySubGenFn = self._KEYWORD_DESPATCH[myTtt.t]
            except KeyError:
                if self._condStack.isTrue():
                    self._diagnostic.undefined(' identifier "# %s"' % myTtt.t, myFlc)
                    if not self._wsHandler.isBreakingWhitespace(myTtt.t):
                        myUnresolvedTokens.extend(self._tokensToEol(theGen, macroReplace=False))
            else:
                for aTok in mySubGenFn(theGen, myFlc):
                    yield aTok

                myUnresolvedTokens = []

        self._isNewline = True

    def _appendTokenMergingWhitespace(self, theList, theToken):
        """Adds a token to the list merging whitespace if possible."""
        if len(theList) and theList[(-1)].isWs() and theToken.isWs():
            theList.append(theList.pop().copy())
            theList[(-1)].merge(theToken)
        else:
            theList.append(theToken)

    def _retDefinedSubstitution(self, theGen):
        """Returns a list of tokens from the supplied argument with defined...
        and !defined... handled appropriately and other tokens expanded where
        appropriate.
        This is used by #if, #elif.
        Reporting conditional state:
        For example:
        #define F(a) a % 2
        #define X 5

        What to say?     This?        Or?           Or?              Or?
        #if F(X) == 1    F(X) == 1    F(5) == 1    (5 % 2) == 1      1 == 1
        ...
        #else            !F(X) == 1   !F(5) == 1   !(5 % 2) == 1     !(1 == 1)
        ...
        #endif
        The current implementation takes the first as most useful: "F(X) == 1".
        This means capturing the original token stream as well
        as the (possibly replaced) evaluated token stream.
        
        TODO: There is an issue here is  with poorly specified #if/#elif statements
        For example:
        #if deeeefined SPAM
        cpp.exe: <stdin>:1:7: missing binary operator before token "SPAM"
        #if 1 SPAM
        cpp.exe: <stdin>:1:7: missing binary operator before token "SPAM"        
        """
        rawTokS = []
        repTokS = []
        flagInvert = flagHasSeenDefined = False
        macroReplacedTokS = []
        while 1:
            myFlc = self.fileLineCol
            if len(macroReplacedTokS) > 0:
                myTtt = macroReplacedTokS.pop(0)
            else:
                myTtt = next(theGen)
                rawTokS.append(myTtt)
            logging.debug('_retDefinedSubstitution(): %s' % myTtt)
            if self._wsHandler.isBreakingWhitespace(myTtt.t):
                self._appendTokenMergingWhitespace(repTokS, myTtt)
                break
            elif myTtt.t == '!':
                flagInvert = True
            elif myTtt.t == 'defined':
                flagHasSeenDefined = True
            elif myTtt.isIdentifier():
                if flagHasSeenDefined:
                    repTokS.append(self._macroEnv.defined(myTtt, flagInvert, myFlc))
                    flagHasSeenDefined = flagInvert = False
                elif self._macroEnv.mightReplace(myTtt):
                    for aTtt in self._macroEnv.replace(myTtt, theGen, myFlc):
                        self._appendTokenMergingWhitespace(macroReplacedTokS, aTtt)

                elif flagInvert:
                    repTokS.append(PpToken.PpToken('1', 'pp-number'))
                else:
                    repTokS.append(PpToken.PpToken('0', 'pp-number'))
            else:
                self._appendTokenMergingWhitespace(repTokS, myTtt)

        return (repTokS, rawTokS)

    def _retIfEvalAndTokens(self, theGen):
        """Returns (bool | None, tokenStr) from processing a #if or #elif
        conditional statement. This also handles defined... and !defined...
        bool - True/False based on the evaluation of the constant expression.
               This will be None on evaluation failure.
        tokenStr - A string of raw (original) PpTokens that made up the constant
                 expression.
        """
        myTokS, myRawTokS = self._retDefinedSubstitution(theGen)
        myTokStr = ('').join([ t.t for t in myRawTokS ]).strip()
        try:
            myCe = ConstantExpression.ConstantExpression(myTokS)
            myBool = myCe.evaluate()
        except ConstantExpression.ExceptionConstantExpression as err:
            try:
                self._diagnostic.undefined('Can not evaluate constant expression "%s", error: %s' % (
                 myTokStr, str(err)), self._fis.fileLineCol)
            except CppDiagnostic.ExceptionCppDiagnostic as diag_err:
                logging.error('Trapping diagnostic exception: %s' % str(diag_err))

            raise ExceptionConditionalExpression(('Error: {:s} File: {!s:s}').format(str(err), str(self.fileLineCol)))

        return (
         myBool, myTokStr)

    def _retDefineAndTokens(self, theGen):
        """Returns 1 or 0 if a macro is defined."""
        myLiteralTokS = []
        myEvalToks = []
        for aTok in self._tokensToEol(theGen, macroReplace=False):
            myLiteralTokS.append(aTok.t)
            if aTok.isIdentifier():
                myEvalToks.append(self._macroEnv.defined(aTok, False, self.fileLineCol))
            else:
                myEvalToks.append(aTok)

        myCe = ConstantExpression.ConstantExpression(myEvalToks)
        literalStr = (' ').join(myLiteralTokS)
        return (myCe.evaluate(), literalStr.strip())

    def _reportSpuriousTokens(self, theCmd):
        """Reports the presence of spurious tokens in things like:
        #else spurious 1 ) tokens ...
        Used by #else and #endif which expect no semantically significant
        tokens to follow them.
        Typical cpp.exe behaviour:
        cpp.exe: <stdin>:3:7: warning: extra tokens at end of #else directive
        """
        self._diagnostic.implementationDefined('extra tokens at end of #%s directive' % theCmd, self._fis.fileLineCol)

    def _cppIf(self, theGen, theFlc):
        """Handles a if directive."""
        myBool, myStr = self._retIfEvalAndTokens(theGen)
        if myBool is not None:
            self._condStack.oIf(myBool, myStr)
            self._condCompGraph.oIf(theFlc, self._tuIndex, self._condStack.isTrue(), myStr)
        yield PpToken.PpToken('\n', 'whitespace')
        return

    def _cppElif(self, theGen, theFlc):
        """Handles a elif directive."""
        if self._condStack.hasBeenTrueAtCurrentDepth():
            myTokS = self._tokensToEol(theGen, macroReplace=False)
            myStr = ('').join([ t.t for t in myTokS ]).strip()
            myBool = False
        else:
            myBool, myStr = self._retIfEvalAndTokens(theGen)
        if myBool is not None:
            self._condStack.oElif(myBool, myStr)
            self._condCompGraph.oElif(theFlc, self._tuIndex, self._condStack.isTrue(), myStr)
        yield PpToken.PpToken('\n', 'whitespace')
        return

    def _cppIfdef(self, theGen, theFlc):
        """Handles a Ifdef directive."""
        myBool, myStr = self._retDefineAndTokens(theGen)
        self._condStack.oIfdef(myBool, 'def %s' % myStr)
        self._condCompGraph.oIfdef(theFlc, self._tuIndex, self._condStack.isTrue(), myStr)
        yield PpToken.PpToken('\n', 'whitespace')

    def _cppIfndef(self, theGen, theFlc):
        """Handles a ifndef directive."""
        myBool, myStr = self._retDefineAndTokens(theGen)
        self._condStack.oIfndef(myBool, '!def %s' % myStr)
        self._condCompGraph.oIfndef(theFlc, self._tuIndex, self._condStack.isTrue(), myStr)
        yield PpToken.PpToken('\n', 'whitespace')

    def _cppElse(self, theGen, theFlc):
        """Handles a else directive."""
        myTokS = self._tokensToEol(theGen, macroReplace=False)
        if self._countNonWsTokens(myTokS):
            self._reportSpuriousTokens('else')
        self._condStack.oElse()
        self._condCompGraph.oElse(theFlc, self._tuIndex, self._condStack.isTrue())
        yield PpToken.PpToken('\n', 'whitespace')

    def _cppEndif(self, theGen, theFlc):
        """Handles a endif directive."""
        try:
            myTokS = self._tokensToEol(theGen, macroReplace=False)
            if self._countNonWsTokens(myTokS):
                self._reportSpuriousTokens('endif')
        finally:
            try:
                self._condStack.oEndif()
                myEndifState = self._condStack.isTrue()
                self._condCompGraph.oEndif(theFlc, self._tuIndex, myEndifState)
                yield PpToken.PpToken('\n', 'whitespace')
            except Exception as err:
                logging.fatal('PpLexer._cppEndif(): Encountered exception in finally clause: %s' % str(err))

    def _cppInclude(self, theGen, theFlc):
        """Handles an #include directive. This handles:
        # include <h-char-sequence> new-line
        # include "q-char-sequence" new-line
        This gathers a list of PpTokens up to, and including, a newline with
        macro replacement. Then we reinterpret the list using:
        PpTokeniser.reduceToksToHeaderName() to cast tokens to possible
        #include <header-name> token.
        Finally we try and resolve that to a 'file' that can be included.
        
        FWIW cpp.exe does not explore #include statements when they are
        conditional so will not error on unreachable files if they
        are conditionally included. 
        """
        return self._cppIncludeGeneric(theGen, theFlc, self._includeHandler.includeHeaderName)

    def _cppIncludeNext(self, theGen, theFlc):
        """Handles an #include_next GCC extension.
        This behaves in a very similar fashion to self._cppInclude but calls
        includeNextHeaderName() on the include handler
        """
        assert self._gccExtensions, 'Logic error: despatcher called _cppIncludeNext() but self._gccExtensions False'
        return self._cppIncludeGeneric(theGen, theFlc, self._includeHandler.includeNextHeaderName)

    def _cppIncludeGeneric(self, theGen, theFlc, theFileIncludeFunction):
        """Handles the target of an #include or #include_next directive.
        theFileIncludeFunction is the function to call to resolve the target to
        an actual file.
        """
        myHeaderNameTok = self._retHeaderName(theGen)
        logging.debug('#include %s START', myHeaderNameTok)
        if self._condStack.isTrue():
            if myHeaderNameTok is None:
                self._cppIncludeReportError('#include expects "FILENAME" or <FILENAME>')
            elif self._condStack.isTrue() or self._condLevel > 1:
                try:
                    try:
                        myFpo = theFileIncludeFunction(myHeaderNameTok.t)
                        logging.debug('Include search for %s finds %s', myHeaderNameTok.t, myFpo)
                        if myFpo is not None:
                            myGen = self._pptPush(myFpo)
                            for optionalLineFileToken in self._pptPostPush():
                                yield optionalLineFileToken

                            try:
                                for aTtt in self._genPpTokensRecursive(myGen):
                                    yield aTtt

                            finally:
                                try:
                                    self._pptPop()
                                    for optionalLineFileToken in self._pptPostPop():
                                        yield optionalLineFileToken

                                except Exception as err:
                                    logging.fatal('PpLexer._cppInclude(): [0] Encountered exception in finally clause : %s' % str(err))

                        else:
                            self._cppIncludeReportError('%s: No such file or directory' % myHeaderNameTok.t)
                    except IncludeHandler.ExceptionCppInclude as err:
                        logging.error('Include failed with %s', str(err))

                finally:
                    try:
                        self._includeHandler.endInclude()
                    except Exception as err:
                        logging.fatal('PpLexer._cppInclude(): [1] Encountered exception in finally clause : %s' % str(err))

        self._diagnosticDebugMessage('#include %s END' % str(myHeaderNameTok))
        yield PpToken.PpToken('\n', 'whitespace')
        return

    def _cppIncludeReportError(self, theMsg=None):
        """Reports a consistent error message when #indlude is not processed and
        consumes all tokens up to and including the next newline."""
        myMsg = theMsg or '#include expects "FILENAME" or <FILENAME>'
        self._diagnostic.error(myMsg, self._fis.fileLineCol)

    def _retHeaderName(self, theGen):
        """This returns the first PpToken of type header-name it finds up
        to a newline token or None if none found. It handles:
        # include <h-char-sequence> new-line
        # include "q-char-sequence" new-line
        This gathers a list of PpTokens up to, and including, a newline with
        macro replacement. Then it reinterprets the list using
        PpTokeniser.reduceToksToHeaderName() to cast tokens to possible
        #include header-name token.
        """
        myTokS = self._tokensToEol(theGen, macroReplace=False)
        myPpTokeniser = PpTokeniser.PpTokeniser()
        headerS = myPpTokeniser.filterHeaderNames(myTokS)
        if len(headerS) == 1:
            return headerS[0]
        myTokS = self._retListReplacedTokens(myTokS)
        headerS = myPpTokeniser.filterHeaderNames(myTokS)
        if len(headerS) == 1:
            return headerS[0]

    def _cppDefine(self, theGen, theFlc):
        """Handles a define directive."""
        ppTokenPrefix = [
         PpToken.PpToken('#', 'preprocessing-op-or-punc'),
         PpToken.PpToken('define', 'identifier')]
        if self._condStack.isTrue():
            try:
                myIdent = self._macroEnv.define(theGen, theFlc.fileId, theFlc.lineNum)
                for aPrefixTok in ppTokenPrefix:
                    self._fis.tokenCountInc(aPrefixTok, True, num=1)

                self._fis.tokenCounterAdd(self._macroEnv.macro(myIdent).tokenCounter)
            except MacroEnv.ExceptionMacroEnvInvalidRedefinition as err:
                self._diagnostic.warning(str(err))

            yield PpToken.PpToken('\n', 'whitespace')
        else:
            for aPrefixTok in ppTokenPrefix:
                yield aPrefixTok

            for aTtt in self._tokensToEol(theGen, macroReplace=False):
                yield aTtt

    def _cppUndef(self, theGen, theFlc):
        """Handles a undef directive."""
        ppTokenPrefix = [
         PpToken.PpToken('#', 'preprocessing-op-or-punc'),
         PpToken.PpToken('undef', 'identifier')]
        if self._condStack.isTrue():
            try:
                self._macroEnv.undef(theGen, theFlc.fileId, theFlc.lineNum)
                for aPrefixTok in ppTokenPrefix:
                    self._fis.tokenCountInc(aPrefixTok, True, num=1)

                self._fis.tokenCountInc(PpToken.PpToken('\n', 'whitespace'), True, num=2)
                self._fis.tokenCountInc(PpToken.PpToken('whatever', 'identifier'), True, num=1)
            except MacroEnv.ExceptionMacroEnv as err:
                self._diagnostic.error(str(err))

            yield PpToken.PpToken('\n', 'whitespace')
        else:
            for aPrefixTok in ppTokenPrefix:
                yield aPrefixTok

            for aTtt in self._tokensToEol(theGen, macroReplace=False):
                yield aTtt

    def _cppLine(self, theGen, theFlc):
        """Handles a line directive.
        This also handles :title-reference:`ISO/IEC 9899:1999 (E) 6.10.4 Line control`
        In particular 6.10.4-4 where the form is::
        
            # line digit-sequence "s-char-sequenceopt" new-line
        
        digit-sequence is a a token type pp-number.
        
        The s-char-sequenceopt is a token type 'string-literal', this
        will have the double quote delimeters and may have a 'L' prefix.
        for example L"abc"."""
        self._tokensToEol(theGen, macroReplace=False)
        yield PpToken.PpToken('\n', 'whitespace')

    def _cppError(self, theGen, theFlc):
        """Handles a error directive."""
        myTokS = self._tokensToEol(theGen, macroReplace=False)
        if self._condStack.isTrue():
            myErrMsg = ('').join([ t.t for t in myTokS ])
            myErrMsg = myErrMsg.strip()
            self._diagnostic.error(myErrMsg, theFlc)
        yield PpToken.PpToken('\n', 'whitespace')

    def _cppWarning(self, theGen, theFlc):
        """Handles a warning directive. Not in the standard but we support it."""
        myTokS = self._tokensToEol(theGen, macroReplace=False)
        if self._condStack.isTrue():
            myMsg = ('').join([ t.t for t in myTokS ])
            myMsg = myMsg.strip()
            self._diagnostic.warning(myMsg, theFlc)
        yield PpToken.PpToken('\n', 'whitespace')

    def _cppPragma(self, theGen, theFlc):
        """Handles a pragma directive.
        :title-reference:`ISO/IEC 9899:1999 (E) 6.10.6 Pragma directive`
        
        Semantics:
        
        1 A preprocessing directive of the form::
            # pragma pp-tokensopt new-line
        
        where the preprocessing token STDC does not immediately follow pragma in the
        directive (prior to any macro replacement)146) causes the implementation to behave in an
        implementation-defined manner. The behavior might cause translation to fail or cause the
        translator or the resulting program to behave in a non-conforming manner. Any such
        pragma that is not recognized by the implementation is ignored.
        
        Footnote 146: An implementation is not required to perform macro replacement in pragmas, but it is permitted
        except for in standard pragmas (where STDC immediately follows pragma). If the result of macro
        replacement in a non-standard pragma has the same form as a standard pragma, the behavior is still
        implementation-defined; an implementation is permitted to behave as if it were the standard pragma,
        but is not required to."""
        if self._pragmaHandler is not None:
            try:
                myTokS = self._tokensToEol(theGen, macroReplace=self._pragmaHandler.replaceTokens)
                pragmaStr = self._pragmaHandler.pragma(myTokS)
                if pragmaStr:
                    fileId = 'pragma'
                    myFh = IncludeHandler.CppIncludeStringIO(theUsrDirs=[], theSysDirs=[], theInitialTuContent=pragmaStr, theFilePathToContent={fileId: pragmaStr})
                    myFpo = myFh.initialTu(fileId)
                    myGen = self._pptPush(myFpo)
                    for optionalLineFileToken in self._pptPostPush():
                        yield optionalLineFileToken

                    try:
                        if self._pragmaHandler.isLiteral:
                            for aTtt in myGen:
                                yield aTtt

                        else:
                            for aTtt in self._genPpTokensRecursive(myGen):
                                yield aTtt

                    finally:
                        try:
                            self._pptPop()
                            for optionalLineFileToken in self._pptPostPop():
                                yield optionalLineFileToken

                        except Exception as err:
                            logging.fatal('PpLexer._cppPragma(): Encountered exception in finally clause: %s' % str(err))

            except PragmaHandler.ExceptionPragmaHandler as err:
                self._diagnostic.undefined(str(err), theFlc)

        else:
            myTokS = self._tokensToEol(theGen, macroReplace=False)
            self._diagnostic.warning('Can not handle #pragma: %s' % ('').join([ t.t for t in myTokS ]), theFlc)
        yield PpToken.PpToken('\n', 'whitespace')
        return