# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/core/ItuToTokens.py
# Compiled at: 2017-10-03 13:07:16
"""Converts an ITU (i.e. a file like object and tokenises it into extended
preprocessor tokens. This does not act on any preprocessing directives."""
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import logging
from cpip import ExceptionCpip
from cpip.core import PpLexer
from cpip.core import PpToken
from cpip.core import PpTokeniser
from cpip.util import BufGen
from cpip.util import MultiPassString

class ExceptionItuToTokens(ExceptionCpip):
    pass


ITU_TOKEN_TYPES = PpToken.LEX_PPTOKEN_TYPES + [
 'trigraph',
 PpTokeniser.COMMENT_TYPE_C,
 PpTokeniser.COMMENT_TYPE_CXX,
 'keyword',
 'preprocessing-directive',
 'Unknown']

class ItuToTokens(PpTokeniser.PpTokeniser):
    """Tokensises a file like object."""

    def __init__(self, theFileObj=None, theFileId=None, theDiagnostic=None):
        super(ItuToTokens, self).__init__(theFileObj, theFileId, theDiagnostic)
        self._mps = MultiPassString.MultiPassString(theFileObj)

    @property
    def multiPassString(self):
        return self._mps

    def genTokensKeywordPpDirective(self):
        """Process the file and generate tokens.
        This changes the type to a keyword or preprocessing-directive if it can
        do so."""
        self.translatePhases123()
        self._fileLocator.startNewPhase()
        prevNonWs = ''
        for t, tt in self.multiPassString.genWords():
            assert tt in ITU_TOKEN_TYPES, '%s not in %s' % (tt, str(ITU_TOKEN_TYPES))
            logging.debug('genTokensKeywordPpDirective() "%s", "%s"', t, tt)
            if tt == 'identifier':
                if prevNonWs == '#' and t in PpLexer.PREPROCESSING_DIRECTIVES:
                    yield (
                     t, 'preprocessing-directive')
                elif t in PpTokeniser.CHAR_SET_MAP['lex.key']['keywords']:
                    yield (
                     t, 'keyword')
                else:
                    yield (
                     t, tt)
            elif t in ('new', 'delete') and tt == 'preprocessing-op-or-punc':
                yield (
                 t, 'keyword')
            else:
                yield (
                 t, tt)
            if tt != 'whitespace':
                prevNonWs = t
            self._fileLocator.update(t)

    def translatePhases123(self):
        self._translatePhase_1()
        self._translatePhase_2()
        self._translatePhase_3()

    def _translatePhase_1(self):
        """Performs translation phase one.
        Note: We do not (yet) support universal-character-name conversion
        so this only does trigraphs."""
        logging.debug('ItuToTokens._translatePhase_1(): start.')
        myBg = BufGen.BufGen(self._mps.genChars())
        self._fileLocator.startNewPhase()
        try:
            i = 0
            while 1:
                if myBg[i] == PpTokeniser.TRIGRAPH_PREFIX:
                    self._mps.setMarker()
                    if myBg[(i + 1)] == PpTokeniser.TRIGRAPH_PREFIX and myBg[(i + 2)] in PpTokeniser.TRIGRAPH_TABLE:
                        self._mps.removeSetReplaceClear(isTerm=True, theType='trigraph', theRepl=PpTokeniser.TRIGRAPH_TABLE[myBg[(i + 2)]])
                        i += PpTokeniser.TRIGRAPH_SIZE
                        self._fileLocator.incCol(PpTokeniser.TRIGRAPH_SIZE)
                    else:
                        self._mps.clearMarker()
                        i += 1
                        self._fileLocator.update(myBg[i])
                else:
                    i += 1
                    self._fileLocator.update(myBg[i])

        except IndexError:
            pass

        logging.debug('ItuToTokens._translatePhase_1(): end.')

    def _translatePhase_2(self):
        """Performs translation phase two. This does line continuation markers
        Note: We do not (yet) test for accidental UCN creation."""
        logging.debug('ItuToTokens._translatePhase_2(): start.')
        myBg = BufGen.BufGen(self._mps.genChars())
        self._fileLocator.startNewPhase()
        try:
            i = 0
            while 1:
                if myBg[i] == '\\':
                    self._mps.setMarker()
                    if myBg[(i + 1)] == '\n':
                        self._mps.removeMarkedWord(isTerm=True)
                        i += 2
                        self._fileLocator.incLine()
                    else:
                        self._mps.clearMarker()
                        i += 1
                        self._fileLocator.update(myBg[i])
                else:
                    i += 1
                    self._fileLocator.update(myBg[i])

        except IndexError:
            pass

        logging.debug('ItuToTokens._translatePhase_2(): end.')

    def _translatePhase_3(self):
        """Performs translation phase three. Replaces comments and decomposes
        stream into preprocessing tokens."""
        logging.debug('ItuToTokens._translatePhase_3(): start.')
        ofsIdx = 0
        myBg = BufGen.BufGen(self._mps.genChars())
        self._fileLocator.startNewPhase()
        try:
            while 1:
                self._cppTokType = None
                myBg[ofsIdx]
                self._mps.setMarker()
                sliceLen = self._sliceWhitespace(myBg, ofsIdx) or self._sliceLexComment(myBg, ofsIdx) or self._sliceLexPptoken(myBg, ofsIdx)
                if sliceLen > 0:
                    if self._cppTokType in PpTokeniser.COMMENT_TYPES:
                        myIsTerm = self._cppTokType == PpTokeniser.COMMENT_TYPE_C
                        self._mps.removeSetReplaceClear(isTerm=myIsTerm, theType=self._cppTokType, theRepl=' ')
                    else:
                        myIsTerm = self._cppTokType in ('character-literal', 'string-literal',
                                                        'non-whitespace')
                        self._mps.setWordType(self._cppTokType, isTerm=myIsTerm)
                    ofsIdx += sliceLen
                else:
                    break

        except IndexError:
            pass

        try:
            myBg[ofsIdx]
            self._diagnostic.partialTokenStream('lex.pptoken has unparsed tokens %s' % myBg[ofsIdx:], self.fileLocator)
        except IndexError:
            pass

        logging.debug('ItuToTokens._translatePhase_3(): end.')
        return