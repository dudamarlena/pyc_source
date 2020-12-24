# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/core/PpTokeniser.py
# Compiled at: 2017-10-03 13:07:16
__doc__ = 'Performs translation phases 0, 1, 2, 3 on C/C++ source code.\n\nTranslation phases from :title-reference:`ISO/IEC 9899:1999 (E)`:\n\n5.1.1.2 Translation phases\n5.1.1.2-1 The precedence among the syntax rules of translation is specified by\nthe following phases.\n\nPhase 1. Physical source file multibyte characters are mapped, in an\nimplementation defined manner, to the source character set (introducing\nnew-line characters for end-of-line indicators) if necessary. Trigraph\nsequences are replaced by corresponding single-character internal\nrepresentations.\n\nPhase 2. Each instance of a backslash character (\\) immediately followed by\na new-line character is deleted, splicing physical source lines to form\nlogical source lines. Only the last backslash on any physical source line\nshall be eligible for being part of such a splice. A source file that is\nnot empty shall end in a new-line character, which shall not be immediately\npreceded by a backslash character before any such splicing takes place.\n\nPhase 3. The source file is decomposed into preprocessing tokens6) and\nsequences of white-space characters (including comments). A source file\nshall not end in a partial preprocessing token or in a partial comment.\nEach comment is replaced by one space character. New-line characters are\nretained. Whether each nonempty sequence of white-space characters other\nthan new-line is retained or replaced by one space character is\nimplementation-defined.\n\nTODO: Do phases 0,1,2 as generators i.e. not in memory?\n\nTODO: Check coverage with a complete but minimal example of every token\n\nTODO: remove self._cppTokType and have it as a return value?\n\nTODO: Remove commented out code.\n\nTODO: Performance of phase 1 processing.\n\nTODO: rename next() as genPpTokens()?\n\nTODO: Perf rewrite slice functions to take an integer argument of where in the\narray to start inspecting for a slice. This avoids calls to ...[x:] e.g.\nmyCharS = myCharS[sliceIdx:] in genLexPptokenAndSeqWs.\n'
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
C_KEYWORDS = tuple(('auto\nbreak\ncase\nchar\nconst\ncontinue\ndefault\ndo\ndouble\nelse\nenum\nextern\nfloat\nfor\ngoto\nif\ninline\nint\nlong\nregister\nrestrict\nreturn\nshort\nsigned\nsizeof\nstatic\nstruct\nswitch\ntypedef\nunion\nunsigned\nvoid\nvolatile\nwhile\n_Bool\n_Complex\n_Imaginary\n').split())
from cpip import ExceptionCpip
from cpip.core import FileLocation
from cpip.core import CppDiagnostic
from cpip.core import PpWhitespace
from cpip.core import PpToken
from cpip.util import StrTree, MatrixRep
LEN_SOURCE_CHARACTER_SET = 96
COMMENT_REPLACEMENT = ' '
DIGRAPH_TABLE = {'<%': '{', 
   'and': '&&', 
   'and_eq': '&=', 
   '%>': '}', 
   'bitor': '|', 
   'or_eq': '|=', 
   '<:': '[', 
   'or': '||', 
   'xor_eq': '^=', 
   ':>': ']', 
   'xor': '^', 
   'not': '!', 
   '%:': '#', 
   'compl': '~', 
   'not_eq': '!=', 
   '%:%:': '##', 
   'bitand': '&'}
TRIGRAPH_TABLE = {'=': '#', 
   '(': '[', 
   '<': '{', 
   '/': '\\', 
   ')': ']', 
   '>': '}', 
   "'": '^', 
   '!': '|', 
   '-': '~'}
TRIGRAPH_PREFIX = '?'
TRIGRAPH_SIZE = 3
CHAR_SET_MAP = {'lex.charset': {'source character set': set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}[]#()<>%:;.?*+-/^&|~!=,\\"\'\t\x0b\x0c\n '), 
                   'ucn ordinals': set((36, 64, 96))}, 
   'lex.ppnumber': {'digit': set('0123456789'), 
                    'nonzero-digit': set('123456789'), 
                    'octal-digit': set('01234567'), 
                    'hexadecimal-digit': set('0123456789abcdefABCDEF')}, 
   'lex.header': {'h-char_omit': set('\n>'), 
                  'q-char_omit': set('\n"'), 
                  'undefined_h_words': set(("'", '\\', '"', '//', '/*')), 
                  'undefined_q_words': set(("'", '\\', '/*', '//'))}, 
   'lex.name': {'part_non_digit': set(('_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
     'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E',
     'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
     'V', 'W', 'X', 'Y', 'Z', '$', '@', '`'))}, 
   'lex.key': {'keywords': set(('asm', 'do', 'if', 'return', 'typedef', 'auto', 'double', 'inline', 'short', 'typeid',
     'bool', 'dynamic_cast', 'int', 'signed', 'typename', 'break', 'else', 'long',
     'sizeof', 'union', 'case', 'enum', 'mutable', 'static', 'unsigned', 'catch',
     'explicit', 'namespace', 'static_cast', 'using', 'char', 'export', 'new', 'struct',
     'virtual', 'class', 'extern', 'operator', 'switch', 'void', 'const', 'false',
     'private', 'template', 'volatile', 'const_cast', 'float', 'protected', 'this',
     'wchar_t', 'continue', 'for', 'public', 'throw', 'while', 'default', 'friend',
     'register', 'true', 'delete', 'goto', 'reinterpret_cast', 'try'))}, 
   'lex.op': {'operators': set(('{', '}', '[', ']', '#', '##', '(', ')', '<:', ':>', '<%', '%>', '%:', '%:%:',
     ';', ':', '...', 'new', 'delete', '?', '::', '.', '.*', '+', '-', '*', '/',
     '%', '^', '&', '|', '~', '!', '=', '<', '>', '+=', '-=', '*=', '/=', '%=', '^=',
     '&=', '|=', '<<', '>>', '>>=', '<<=', '==', '!=', '<=', '>=', '&&', '||', '++',
     '--', ',', '->*', '->', 'and', 'and_eq', 'bitand', 'bitor', 'compl', 'not',
     'not_eq', 'or', 'or_eq', 'xor', 'xor_eq'))}, 
   'lex.icon': {'unsigned-suffix': set('uU'), 
                'long-suffix': set('lL')}, 
   'lex.ccon': {'simple-escape-sequence': set('\'"?\\abfnrtv'), 
                'c-con_omit': set("'\\\n")}, 
   'lex.fcon': {'floating-suffix': set('flFL'), 
                'sign': set('-+'), 
                'exponent_prefix': set('eE')}, 
   'lex.string': {'s-char_omit': set('"\\\n')}, 
   'lex.bool': {'set': set(('false', 'true'))}, 
   'cpp': {'lparen': '(', 
           'new-line': '\n'}}
CHAR_SET_MAP['lex.charset']['whitespace'] = PpWhitespace.LEX_WHITESPACE
assert len(CHAR_SET_MAP['lex.charset']['whitespace']) == PpWhitespace.LEN_WHITESPACE_CHARACTER_SET
assert len(CHAR_SET_MAP['lex.charset']['source character set'] - CHAR_SET_MAP['lex.charset']['whitespace']) == LEN_SOURCE_CHARACTER_SET - PpWhitespace.LEN_WHITESPACE_CHARACTER_SET
CHAR_SET_MAP['lex.header']['h-char'] = CHAR_SET_MAP['lex.charset']['source character set'] - CHAR_SET_MAP['lex.header']['h-char_omit']
CHAR_SET_MAP['lex.header']['q-char'] = CHAR_SET_MAP['lex.charset']['source character set'] - CHAR_SET_MAP['lex.header']['q-char_omit']
CHAR_SET_MAP['lex.ccon']['c-char'] = CHAR_SET_MAP['lex.charset']['source character set'] - CHAR_SET_MAP['lex.ccon']['c-con_omit']
CHAR_SET_MAP['lex.ccon']['c-char'] |= set([ chr(o) for o in CHAR_SET_MAP['lex.charset']['ucn ordinals'] ])
CHAR_SET_MAP['lex.string']['s-char'] = CHAR_SET_MAP['lex.charset']['source character set'] - CHAR_SET_MAP['lex.string']['s-char_omit']
CHAR_SET_MAP['lex.string']['s-char'] |= set([ chr(o) for o in CHAR_SET_MAP['lex.charset']['ucn ordinals'] ])
assert len(CHAR_SET_MAP['lex.charset']['source character set']) == LEN_SOURCE_CHARACTER_SET
for k in DIGRAPH_TABLE.keys():
    assert k in CHAR_SET_MAP['lex.op']['operators'], "Digraph %s not in CHAR_SET_MAP['lex.op']['operators']" % k

CHAR_SET_STR_TREE_MAP = {'lex.key': {'keywords': StrTree.StrTree(CHAR_SET_MAP['lex.key']['keywords'])}, 
   'lex.op': {'operators': StrTree.StrTree(CHAR_SET_MAP['lex.op']['operators'])}, 
   'lex.bool': {'set': StrTree.StrTree(CHAR_SET_MAP['lex.bool']['set'])}}

class ExceptionCpipTokeniser(ExceptionCpip):
    """Simple specialisation of an exception class for the preprocessor."""


class ExceptionCpipTokeniserUcnConstraint(ExceptionCpipTokeniser):
    """Specialisation for when universal character name exceeds constraints."""


COMMENT_TYPE_C = 'C comment'
COMMENT_TYPE_CXX = 'C++ comment'
COMMENT_TYPES = (COMMENT_TYPE_C, COMMENT_TYPE_CXX)

class PpTokeniser(object):
    """Imitates a Preprocessor that conforms to :title-reference:`ISO/IEC 14882:1998(E).`
    
    Takes an optional file like object.
    If theFileObj has a 'name' attribute then that will be use as the name
    otherwise theFileId will be used as the file name.
    
    **Implementation note:** On all ``_slice...()`` and ``__slice...()`` functions:
    A ``_slice...()`` function takes a buffer-like object and an integer offset as
    arguments. The buffer-like object will be accessed by index so just needs
    to implement ``__getitem__()``. On overrun or other out of bounds index an
    IndexError must be caught by the ``_slice...()`` function.
    i.e. ``len()`` should not be called on the buffer-like object, or rather, if
    ``len()`` (i.e. ``__len__()``) is called a ``TypeError`` will be raised and propagated
    out of this class to the caller.
    
    StrTree, for example, conforms to these requirements.
    
    The function is expected to return an integer that represents the number
    of objects that can be consumed from the buffer-like object. If the
    return value is non-zero the PpTokeniser is side-affected in that
    ``self._cppTokType`` is set to a non-None value. Before doing that a test is
    made and if ``self._cppTokType`` is already non-None then an assertion error
    is raised.
    
    The buffer-like object should not be side-affected by the ``_slice...()``
    function regardless of the return value.
    
    So a ``_slice...()`` function pattern is::
    
        def _slice...(self, theBuf, theOfs):
            i = theOfs
            try:
                # Only access theBuf with [i] so that __getitem__() is called
                ...theBuf[i]...
                # Success as the absence of an IndexError!
                # So return the length of objects that pass
                # First test and set for type of slice found
                if i > theOfs:
                    assert(self._cppTokType is None), '_cppTokType was %s now %s' % (self._cppTokType, ...)
                    self._cppTokType = ...
                # NOTE: Return size of slice not the index of the end of the slice
                return i - theOfs
            except IndexError:
                pass
            # Here either return 0 on IndexError or i-theOfs
            return ...
    
    NOTE: Functions starting with ``__slice...`` do not trap the IndexError, the
    caller must do that.
    
    TODO: :title-reference:`ISO/IEC 14882:1998(E) Escape sequences` Table 5?
    """
    PHASES_SUPPORTED = range(0, 4)
    CONT_STR = '\\\n'

    def __init__(self, theFileObj=None, theFileId=None, theDiagnostic=None):
        """Constructor. Takes an optional file like object.
        If theFileObj has a 'name' attribute then that will be use as the name
        otherwise theFileId will be used as the file name."""
        self._whitespaceHandler = PpWhitespace.PpWhitespace()
        self._file = theFileObj
        if self._file is not None and hasattr(self._file, 'name'):
            self._fileName = self._file.name
        else:
            self._fileName = theFileId
        self._fileLocator = FileLocation.FileLocation(self._fileName)
        self._diagnostic = theDiagnostic or CppDiagnostic.PreprocessDiagnosticStd()
        self._fileOpen = False
        self._cppTokType = None
        self._changeOfTokenTypeIsOk = False
        return

    @property
    def pLineCol(self):
        """Returns the current physical (line, column) as integers."""
        return self._fileLocator.pLineCol

    @property
    def fileLocator(self):
        """Returns the FileLocation object."""
        return self._fileLocator

    @property
    def fileName(self):
        """Returns the ID of the file."""
        return self._fileName

    @property
    def fileLineCol(self):
        """Return an instance of FileLineCol from the current physical line column."""
        return self._fileLocator.fileLineCol()

    @property
    def cppTokType(self):
        """Returns the type of the last preprocessing-token found by _sliceLexPptoken()."""
        assert self._cppTokType is None or self._cppTokType in PpToken.LEX_PPTOKEN_TYPES
        return self._cppTokType

    def resetTokType(self):
        """Erases the memory of the previously seen token type."""
        self._cppTokType = None
        return

    def _rewindFile(self):
        """Sets the file to position zero and resets the FileLocator."""
        if self._file is not None:
            self._file.seek(0)
        self._fileLocator.startNewPhase()
        return

    def lexPhases_0(self):
        """An non-standard phase that just reads the file and returns its
        contents as a list of lines (including EOL characters).
        May raise an ExceptionCpipTokeniser if self has been created with None
        or the file is unreadable"""
        try:
            self._rewindFile()
            return self._file.readlines()
        except Exception as err:
            raise ExceptionCpipTokeniser(str(err))

    def _convertToLexCharset(self, theLineS):
        """Converts a list of lines expanding non-lex.charset characters to
        universal-character-name and returns a set of lines so encoded.
        :title-reference:`ISO/IEC 9899:1999 (E) 6.4.3`
        
        .. note::
        
            :title-reference:`ISO/IEC 9899:1999 (E) 6.4.3-2 "A universal character name` shall
            not specify a character whose short identifier is less than 00A0 other
            than 0024 ($), 0040 (@), or 0060 (back tick), nor one in the range D800 through
            DFFF inclusive.61).
        """
        myCharSet = CHAR_SET_MAP['lex.charset']['source character set']
        myUcnOrdinals = CHAR_SET_MAP['lex.charset']['ucn ordinals']
        myMr = MatrixRep.MatrixRep()
        l = 0
        while l < len(theLineS):
            c = 0
            for c, aChar in enumerate(theLineS[l]):
                if aChar not in myCharSet:
                    myOrd = ord(aChar)
                    if myOrd <= 65535:
                        if False and myOrd < 160 and myOrd not in myUcnOrdinals or myOrd >= 55296 and myOrd <= 55551:
                            raise ExceptionCpipTokeniserUcnConstraint('ISO/IEC 9899:1999 (E) 6.4.3-2 UCN constraint: 0x%x out of range, location=%s file=%s' % (
                             myOrd, self._fileLocator.pLineCol, self._fileLocator.fileName))
                        elif myOrd not in myUcnOrdinals:
                            self._fileLocator.substString(1, 6)
                            repl = '\\u%04X' % myOrd
                            myMr.addLineColRep(l, c, aChar, repl)
                    else:
                        self._fileLocator.substString(1, 8)
                        repl = '\\U%08X' % myOrd
                        myMr.addLineColRep(l, c, aChar, repl)
                self._fileLocator.incCol()

            self._fileLocator.incLine()
            l += 1

        myMr.sideEffect(theLineS)

    def lexPhases_1(self, theLineS):
        """:title-reference:`ISO/IEC 14882:1998(E) 2.1 Phases of translation [lex.phases] - Phase one`
        Takes a list of lines (including EOL characters), replaces trigraphs
        and returns the new list of lines."""
        self._convertToLexCharset(theLineS)
        self._translateTrigraphs(theLineS)

    def _spliceLineS(self, theLineS, i):
        assert theLineS[i].endswith(self.CONT_STR)
        self._fileLocator.spliceLine(theLineS[i])
        j = 0
        while theLineS[i].endswith(self.CONT_STR):
            j += 1
            if i + j == len(theLineS):
                self._diagnostic.undefined('Continuation character in last line of file.')
                break
            if theLineS[(i + j)].endswith(self.CONT_STR):
                self._fileLocator.spliceLine(theLineS[(i + j)])
            possUcnIdx = len(theLineS[i]) - len(self.CONT_STR) - len('\\u')
            theLineS[i] = theLineS[i][:-1 * len(self.CONT_STR)] + theLineS[(i + j)]
            theLineS[i + j] = PpWhitespace.LEX_NEWLINE
            if possUcnIdx >= 0 and self.__sliceUniversalCharacterName(theLineS[i], possUcnIdx) > 0:
                self._diagnostic.undefined('Splicing line results in a universal-character-name.')

        i += j
        return i

    def lexPhases_2(self, theLineS):
        """:title-reference:`ISO/IEC 14882:1998(E) 2.1 Phases of translation [lex.phases] - Phase two`
        This joins physical to logical lines. NOTE: This side-effects the
        supplied lines and returns None."""
        self._fileLocator.startNewPhase()
        i = 0
        while i < len(theLineS):
            if theLineS[i].endswith(self.CONT_STR):
                i = self._spliceLineS(theLineS, i)
            else:
                self._fileLocator.incLine()
                i += 1

    def initLexPhase12(self):
        """Process phases one and two and returns the result as a string."""
        myLines = self.lexPhases_0()
        self.lexPhases_1(myLines)
        self.lexPhases_2(myLines)
        return ('').join(myLines)

    def _translateTrigraphs(self, theLineS):
        """:title-reference:`ISO/IEC 14882:1998(E) 2.3 Trigraph sequences [lex.trigraphs]`
        This returns a new set of lines with the trigraphs replaced and
        updates the FileLocator so that the physical lines and columns
        can be recovered."""
        self._fileLocator.startNewPhase()
        myMr = MatrixRep.MatrixRep()
        for lineNum, aLine in enumerate(theLineS):
            i = 0
            while i <= len(aLine) - TRIGRAPH_SIZE:
                if aLine[i] == TRIGRAPH_PREFIX and aLine[(i + 1)] == TRIGRAPH_PREFIX and aLine[(i + 2)] in TRIGRAPH_TABLE:
                    myMr.addLineColRep(lineNum, i, aLine[i:i + TRIGRAPH_SIZE], TRIGRAPH_TABLE[aLine[(i + 2)]])
                    self._fileLocator.setTrigraph()
                    i += TRIGRAPH_SIZE
                else:
                    i += 1
                self._fileLocator.incCol()

            self._fileLocator.incLine()

        myMr.sideEffect(theLineS)

    def substAltToken(self, tok):
        """If a PpToken is a Digraph this alters its value to its alternative.
        If not the supplied token is returned unchanged.
        There are no side effects on self."""
        if tok.tt in ('identifier', 'preprocessing-op-or-punc') and tok.t in DIGRAPH_TABLE:
            tok.subst(DIGRAPH_TABLE[tok.t], 'preprocessing-op-or-punc')
        return tok

    def next(self):
        """The token generator. On being called this performs translations phases
        1, 2 and 3 (unless already done) and then generates pairs of:
        (preprocessing token, token type)
        Token type is an enumerated integer from LEX_PPTOKEN_TYPES.
        Proprocessing tokens include sequences of whitespace characters and
        these are not necessarily concatenated i.e. this generator can produce
        more than one whitespace token in sequence.
        TODO: Rename this to ppTokens() or something"""
        for aTokTypeObj in self.genLexPptokenAndSeqWs(self.initLexPhase12()):
            r = yield aTokTypeObj
            if r is not None:
                yield
                yield r

        return

    def genLexPptokenAndSeqWs(self, theCharS):
        r"""Generates a sequence of PpToken objects. Either:
        
            * a sequence of whitespace (comments are replaces with a single whitespace).
            * a pre-processing token.
        
        This performs translation phase 3.
        
        NOTE: Whitespace sequences are not merged so ``'  /\*\*/ '`` will generate
        three tokens each of ``PpToken.PpToken(' ', 'whitespace')`` i.e. leading
        whitespace, comment replced by single space, trailing whitespace.
        
        So this yields the tokens from translation phase 3 if supplied with
        the results of translation phase 2.
        
        NOTE: This does not generate 'header-name' tokens as these are context
        dependent i.e. they are only valid in the context of a ``#include``
        directive.
        
        :title-reference:`ISO/IEC 9899:1999 (E) 6.4.7 Header names Para 3` says that:
        *"A header name preprocessing token is recognised only within a #include
        preprocessing directive."*.
        """
        self._fileLocator.startNewPhase()
        ofsIdx = 0
        try:
            while 1:
                myLine = self._fileLocator.lineNum
                myCol = self._fileLocator.colNum
                self._cppTokType = None
                sliceLen = self._sliceWhitespace(theCharS, ofsIdx) or self._sliceLexComment(theCharS, ofsIdx) or self._sliceLexPptoken(theCharS, ofsIdx)
                if sliceLen > 0:
                    assert self._changeOfTokenTypeIsOk or self._cppTokType is not None, 'genLexPptokenAndSeqWs() sliceLen=%d but token type is None for: "%s"' % (
                     sliceLen, theCharS[ofsIdx:ofsIdx + sliceLen])
                    mySlice = theCharS[ofsIdx:ofsIdx + sliceLen]
                    self._fileLocator.update(mySlice)
                    ofsIdx += sliceLen
                    if self._cppTokType in COMMENT_TYPES:
                        myTok = PpToken.PpToken(COMMENT_REPLACEMENT, 'whitespace', myLine, myCol)
                    else:
                        myTok = PpToken.PpToken(mySlice, self._cppTokType, myLine, myCol)
                    yield myTok
                else:
                    break

        except IndexError:
            pass

        try:
            theCharS[ofsIdx]
            self._diagnostic.partialTokenStream('lex.pptoken has unparsed tokens %s' % theCharS[ofsIdx:], self.fileLocator)
        except IndexError:
            pass

        return

    def _sliceLongestMatchOfs(self, theBuf, theOfs, theFnS, isExcl=False):
        """Returns the length of the longest slice of theBuf from theOfs using
        the functions theFnS, or 0.
        This preserves self._cppTokType to be the one that gives the longest match.
        Functions that raise an IndexError will be ignored.
        If isExcl is False (the default) then all functions are tested.
        If isExcl is True then functions after one returning a non-zero value
        are not tested.
        TODO (maybe): Have slice functions return (size, type) and get rid of
        self._changeOfTokenTypeIsOk and self._cppTokType
        """
        m = 0
        fMax = None
        myCottio = self._changeOfTokenTypeIsOk
        self._changeOfTokenTypeIsOk = True
        for f in theFnS:
            try:
                prevTt = self._cppTokType
                j = f(theBuf, theOfs)
                assert j == 0 or j != m or fMax is None, '_sliceLongestMatchOfs(): In theBuf "%s", at offset %d [%s], dupe slice %d found and  f was %s now %s' % (
                 theBuf, theOfs, theBuf[theOfs], m, fMax, f)
                if j > m:
                    m = j
                    fMax = f
                else:
                    self._cppTokType = prevTt
                if j > 0 and isExcl:
                    break
            except IndexError:
                pass

        self._changeOfTokenTypeIsOk = myCottio
        return m

    def _sliceAccumulateOfs(self, theBuf, theOfs, theFn):
        """Repeats the function as many times as possible on theBuf from theOfs.
        An IndexError raised by the function will be caught and not propagated."""
        i = 0
        try:
            while 1:
                j = theFn(theBuf, theOfs + i)
                if j == 0:
                    break
                i += j

        except IndexError:
            pass

        return i

    def _wordsFoundInUpTo(self, theBuf, theLen, theWordS):
        """Searches theCharS for any complete instance of any word in theWordS.
        Returns the index of the find or -1 if none found."""
        if theLen > 0:
            for aWord in theWordS:
                i = self._wordFoundInUpTo(theBuf, theLen, aWord)
                if i >= 0:
                    return i

        return -1

    def _wordFoundInUpTo(self, theBuf, theLen, theWord):
        """Searches theBuf for any complete instance of a word in theBuf.
        Returns the index of the find or -1 if none found."""
        if len(theWord) > 0:
            i = 0
            while i < theLen:
                if theBuf[i] != theWord[0]:
                    i += 1
                else:
                    break

            if i < theLen and theBuf[i] == theWord[0]:
                j = 0
                while i + j < theLen and j < len(theWord) and theBuf[(i + j)] == theWord[j]:
                    j += 1

                if j == len(theWord):
                    return i
        return -1

    def _sliceLexPptoken(self, theBuf, theOfs):
        """:title-reference:`ISO/IEC 14882:1998(E) 2.4 Preprocessing tokens [lex.pptoken].`
        :title-reference:`ISO/IEC 9899:1999 (E) 6.4 Lexical elements`
        NOTE: Does not identify header-name tokens. See NOTE on
        genLexPptokenAndSeqWs()
        Note: _sliceLexPptokenGeneral is an exclusive search as 'bitand' can
        appear to be both an operator (correct) and an identifier (incorrect).
        The order of applying functions is therefore highly significant
        _sliceLexPpnumber must be before _sliceLexOperators as the leading '.'
        on a number can be seen as an operator.
        _sliceCharacterLiteral and _sliceStringLiteral must be before
        _sliceLexName as the leading 'L' on char/string can be seen as a name.
        
        self._sliceLexOperators has to be after self._sliceLexName as otherwise
        #define complex gets seen as:
        # - operator
        define - identifier
        compl - operator because of alternative tokens
        ex - identifier
        """
        retVal = self._sliceLexPptokenGeneral(theBuf, theOfs, (
         self._sliceLexPpnumber,
         self._sliceCharacterLiteral,
         self._sliceStringLiteral,
         self._sliceLexName,
         self._sliceLexOperators))
        if retVal == 0:
            retVal = self._sliceNonWhitespaceSingleChar(theBuf, theOfs)
        return retVal

    def _sliceLexPptokenWithHeaderName(self, theBuf, theOfs):
        """:title-reference:`ISO/IEC 14882:1998(E) 2.4 Preprocessing tokens [lex.pptoken].`
        
        .. note::
        
            This does identify header-name tokens where possible."""
        retVal = self._sliceLexPptokenGeneral(theBuf, theOfs, (
         self._sliceLexHeader,
         self._sliceLexName,
         self._sliceLexPpnumber,
         self._sliceCharacterLiteral,
         self._sliceLexOperators))
        if retVal == 0:
            retVal = self._sliceNonWhitespaceSingleChar(theBuf, theOfs)
        return retVal

    def _sliceLexPptokenGeneral(self, theBuf, theOfs, theFuncS):
        """Applies theFuncS to theCharS and returns the longest match."""
        return self._sliceLongestMatchOfs(theBuf, theOfs, theFuncS, isExcl=True)

    def _sliceWhitespace(self, theBuf, theOfs=0):
        i = self._whitespaceHandler.sliceWhitespace(theBuf, theOfs)
        if i > 0:
            assert self._changeOfTokenTypeIsOk or self._cppTokType is None, '_cppTokType was %s now %s' % (
             self._cppTokType, 'whitespace')
            self._cppTokType = 'whitespace'
        return i

    def _sliceNonWhitespaceSingleChar(self, theBuf, theOfs=0):
        """Returns 1 if the first character is non-whitespace, 0 otherwise.
        :title-reference:`ISO/IEC 9899:1999 (E) 6.4-3 and ISO/IEC 14882:1998(E) 2.4.2`
         States that if the character is ' or " the behaviour is undefined."""
        i = theOfs
        try:
            if theBuf[i] not in CHAR_SET_MAP['lex.charset']['whitespace']:
                i += 1
                assert self._changeOfTokenTypeIsOk or self._cppTokType is None, '_cppTokType was %s now %s' % (
                 self._cppTokType, 'non-whitespace')
                self._cppTokType = 'non-whitespace'
            return i - theOfs
        except IndexError:
            pass

        return 0

    def _sliceHexQuad(self, theBuf, theOfs=0):
        """:title-reference:`ISO/IEC 14882:1998(E) 2.2 Character sets [lex.charset] - hex-quad.`"""
        retLen = 4
        try:
            for i in range(retLen):
                if theBuf[(i + theOfs)] not in CHAR_SET_MAP['lex.ppnumber']['hexadecimal-digit']:
                    return 0

            return retLen
        except IndexError:
            pass

        return 0

    def __sliceUniversalCharacterName(self, theBuf, theOfs=0):
        """:title-reference:`ISO/IEC 14882:1998(E) 2.2 Character sets [lex.charset] - universal-character-name.`"""
        if theBuf[theOfs] == '\\':
            if theBuf[(theOfs + 1)] == 'u' and self._sliceHexQuad(theBuf, theOfs + 2) == 4:
                return 6
            if theBuf[(theOfs + 1)] == 'U' and self._sliceHexQuad(theBuf, theOfs + 2) == 4 and self._sliceHexQuad(theBuf, theOfs + 6) == 4:
                return 10
        return 0

    def _sliceLexComment(self, theBuf, theOfs=0):
        """ISO/IEC 14882:1998(E) 2.7 Comments [lex.comment]."""
        i = theOfs
        cmtStyle = None
        try:
            if theBuf[i] == '/':
                if theBuf[(i + 1)] == '*':
                    cmtStyle = COMMENT_TYPE_C
                    i += 2
                    while 1:
                        if theBuf[i] == '*' and theBuf[(i + 1)] == '/':
                            i += 2
                            break
                        i += 1

                elif theBuf[(i + 1)] == '/':
                    cmtStyle = COMMENT_TYPE_CXX
                    i += 2
                    while 1:
                        if theBuf[i] == PpWhitespace.LEX_NEWLINE:
                            break
                        i += 1

            if i > theOfs:
                assert self._changeOfTokenTypeIsOk or self._cppTokType is None, '_cppTokType was %s now %s' % (
                 self._cppTokType, cmtStyle)
                self._cppTokType = cmtStyle
        except IndexError:
            if i > theOfs:
                self._diagnostic.handleUnclosedComment('Unfinished %s style comment' % cmtStyle, self._fileLocator.fileLineCol())
                self._cppTokType = cmtStyle

        return i - theOfs

    def reduceToksToHeaderName(self, theToks):
        """This takes a list of PpTokens and retuns a list of PpTokens
        that might have a header-name token type in them.
        May raise an ExceptionCpipTokeniser if tokens are not all consumed.
        This is used at lexer level for re-interpreting PpTokens in the
        context of a #include directive."""
        myTt = self._cppTokType
        retTokS = []
        myString = PpToken.tokensStr(theToks, shortForm=True)
        while len(myString):
            while 1:
                self._cppTokType = None
                sliceIdx = self._sliceWhitespace(myString)
                if sliceIdx == 0:
                    break
                retTokS.append(PpToken.PpToken(myString[:sliceIdx], 'whitespace'))
                myString = myString[sliceIdx:]

            self._cppTokType = None
            sliceIdx = self._sliceLexPptokenWithHeaderName(myString, 0)
            if sliceIdx == 0:
                sliceIdx = self._sliceStringLiteral(myString, 0)
            if sliceIdx > 0:
                retTokS.append(PpToken.PpToken(myString[:sliceIdx], self._cppTokType))
                myString = myString[sliceIdx:]
            else:
                break

        self._cppTokType = myTt
        if len(myString) > 0:
            raise ExceptionCpipTokeniser('reduceToksToHeaderName() has unparsed tokens: %s' % myString)
        return retTokS

    def filterHeaderNames(self, theToks):
        """Returns a list of 'header-name' tokens from the supplied stream.
        May raise ExceptionCpipTokeniser if un-parsable or theToks has
        non-(whitespace, header-name)."""
        ret = []
        for t in self.reduceToksToHeaderName(theToks):
            if t.tt != 'whitespace':
                if t.tt == 'header-name':
                    ret.append(t)
                else:
                    return []

        return ret

    def _sliceLexHeader(self, theBuf, theOfs=0):
        """ISO/IEC 14882:1998(E) 2.8 Header names [lex.header].
        Might raise a ExceptionCpipUndefinedLocal."""
        i = theOfs
        try:
            if theBuf[i] == '<':
                i += 1
                j = self._sliceLexHeaderHcharSequence(theBuf, i)
                if j > 0 and theBuf[(theOfs + i + j)] == '>':
                    i += j + 1
                else:
                    i = 0
            elif theBuf[i] == '"':
                i += 1
                j = self._sliceLexHeaderQcharSequence(theBuf, i)
                if j > 0 and theBuf[(theOfs + i + j)] == '"':
                    i += j + 1
                else:
                    i = 0
            else:
                i = 0
            if i > 0:
                assert self._changeOfTokenTypeIsOk or self._cppTokType is None, '_cppTokType was %s now %s' % (
                 self._cppTokType, 'header-name')
                self._cppTokType = 'header-name'
        except IndexError:
            i = 0

        return i

    def _sliceLexHeaderHcharSequence(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.8 Header names [lex.header] - h-char-sequence.
        Might raise a ExceptionCpipUndefinedLocal."""
        retVal = self._sliceAccumulateOfs(theBuf, theOfs, self._sliceLexHeaderHchar)
        if retVal > 0:
            undefWordIndex = self._wordsFoundInUpTo(theBuf, retVal, CHAR_SET_MAP['lex.header']['undefined_h_words'])
            if undefWordIndex > 0:
                return 0
        return retVal

    def _sliceLexHeaderHchar(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.8 Header names [lex.header] - h-char character."""
        try:
            if theBuf[theOfs] in CHAR_SET_MAP['lex.header']['h-char']:
                return 1
        except IndexError:
            pass

        return 0

    def _sliceLexHeaderQcharSequence(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.8 Header names [lex.header] - q-char-sequence.
        Might raise a ExceptionCpipUndefinedLocal."""
        retVal = self._sliceAccumulateOfs(theBuf, theOfs, self._sliceLexHeaderQchar)
        if retVal > 0:
            undefWordIndex = self._wordsFoundInUpTo(theBuf, retVal, CHAR_SET_MAP['lex.header']['undefined_q_words'])
            if undefWordIndex > 0:
                return 0
        return retVal

    def _sliceLexHeaderQchar(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.8 Header names [lex.header] - q-char."""
        try:
            if theBuf[theOfs] in CHAR_SET_MAP['lex.header']['q-char']:
                return 1
        except IndexError:
            pass

        return 0

    def _sliceLexPpnumber(self, theBuf, theOfs=0):
        """ISO/IEC 14882:1998(E) 2.9 Preprocessing numbers [lex.ppnumber].
        TODO: Spec says "Preprocessing number tokens lexically include all integral literal tokens (2.13.1) and all floating literal tokens (2.13.3)."
        But the pp-number list does not specify that.
        NOTE: ISO/IEC 9899:1999 Programming languages - C allows 'p' and 'P' suffixes.
        NOTE: The standard appears to allow '.1.2.3.4.'
        """
        i = theOfs
        try:
            if theBuf[i] in CHAR_SET_MAP['lex.ppnumber']['digit']:
                i += 1
            else:
                if theBuf[i] == '.' and theBuf[(i + 1)] in CHAR_SET_MAP['lex.ppnumber']['digit']:
                    i += 2
                if i == theOfs:
                    return 0
            while 1:
                j = 0
                if theBuf[i] == '.':
                    j = 1
                else:
                    j = self._sliceLongestMatchOfs(theBuf, i, (
                     self.__sliceNondigit,
                     self.__sliceLexPpnumberDigit,
                     self.__sliceLexPpnumberExpSign))
                if j > 0:
                    i += j
                else:
                    break

        except IndexError:
            pass

        if i > theOfs:
            assert self._changeOfTokenTypeIsOk or self._cppTokType is None, '_cppTokType was "%s" now "%s"' % (
             self._cppTokType, 'pp-number')
            self._cppTokType = 'pp-number'
        return i - theOfs

    def __sliceLexPpnumberDigit(self, theBuf, theOfs=0):
        """ISO/IEC 14882:1998(E) 2.9 Preprocessing numbers [lex.ppnumber] - digit."""
        if theBuf[theOfs] in CHAR_SET_MAP['lex.ppnumber']['digit']:
            return 1
        return 0

    def __sliceLexPpnumberExpSign(self, theBuf, theOfs=0):
        """ISO/IEC 14882:1998(E) 2.9 Preprocessing numbers [lex.ppnumber] - exponent and sign.
        Returns 2 if theCharS is 'e' or 'E' followed by a sign."""
        if theBuf[theOfs] in CHAR_SET_MAP['lex.fcon']['exponent_prefix'] and theBuf[(theOfs + 1)] in CHAR_SET_MAP['lex.fcon']['sign']:
            return 2
        return 0

    def _sliceLexName(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.10 Identifiers [lex.name]."""
        try:
            i = self.__sliceNondigit(theBuf, theOfs)
            if i == 0:
                return 0
            i += theOfs
        except IndexError:
            return 0

        try:
            while i > theOfs:
                j = self._sliceLongestMatchOfs(theBuf, i, (
                 self.__sliceNondigit,
                 self.__sliceLexPpnumberDigit))
                if j > 0:
                    i += j
                else:
                    break

            if i > theOfs:
                assert self._changeOfTokenTypeIsOk or self._cppTokType is None, '_cppTokType was %s now %s' % (
                 self._cppTokType, 'identifier')
                self._cppTokType = 'identifier'
        except IndexError:
            pass

        return i - theOfs

    def __sliceNondigit(self, theBuf, theOfs=0):
        """ISO/IEC 14882:1998(E) 2.10 Identifiers [lex.name] - nondigit."""
        i = self.__sliceUniversalCharacterName(theBuf, theOfs)
        if i == 0:
            if theBuf[theOfs] in CHAR_SET_MAP['lex.name']['part_non_digit']:
                return 1
        return i

    def _sliceLexKey(self, theBuf, theOfs=0):
        """ISO/IEC 14882:1998(E) 2.11 Keywords [lex.key]."""
        try:
            return self.__sliceLexKey(theBuf, theOfs)
        except KeyError:
            pass

        return 0

    def __sliceLexKey(self, theBuf, theOfs=0):
        """ISO/IEC 14882:1998(E) 2.11 Keywords [lex.key]."""
        return CHAR_SET_STR_TREE_MAP['lex.key']['keywords'].has(theBuf, theOfs) - theOfs

    def _sliceLexOperators(self, theBuf, theOfs=0):
        """ISO/IEC 14882:1998(E) 2.12 Operators and punctuators [lex.operators].
        i.e. preprocessing-op-or-punc"""
        i = CHAR_SET_STR_TREE_MAP['lex.op']['operators'].has(theBuf, theOfs) - theOfs
        if i > 0:
            assert self._changeOfTokenTypeIsOk or self._cppTokType is None, '_cppTokType was %s now %s' % (
             self._cppTokType, 'preprocessing-op-or-punc')
            self._cppTokType = 'preprocessing-op-or-punc'
        return i

    def _sliceLiteral(self, theBuf, theOfs=0):
        """Returns the length of a slice of theCharS that matches the longest integer literal or 0.
        ISO/IEC 14882:1998(E) 2.13 Literals [lex.literal]."""
        return self._sliceLongestMatchOfs(theBuf, theOfs, (
         self._sliceIntegerLiteral,
         self._sliceCharacterLiteral,
         self._sliceFloatingLiteral,
         self._sliceStringLiteral,
         self._sliceBoolLiteral))

    def _sliceIntegerLiteral(self, theBuf, theOfs=0):
        """Returns the length of a slice of theCharS that matches the longest integer literal or 0.
        ISO/IEC 14882:1998(E) 2.13.1 Integer literals [lex.icon]."""
        i = self._sliceLongestMatchOfs(theBuf, theOfs, (
         self._sliceDecimalLiteral,
         self._sliceOctalLiteral,
         self._sliceHexadecimalLiteral))
        if i:
            i += self._sliceIntegerSuffix(theBuf, theOfs + i)
        return i

    def _sliceDecimalLiteral(self, theBuf, theOfs=0):
        """ISO/IEC 14882:1998(E) 2.13.1 Integer literals [lex.icon] - decimal-literal."""
        i = theOfs
        try:
            if theBuf[i] in CHAR_SET_MAP['lex.ppnumber']['nonzero-digit']:
                i += 1
                while theBuf[i] in CHAR_SET_MAP['lex.ppnumber']['digit']:
                    i += 1

        except IndexError:
            pass

        return i - theOfs

    def _sliceOctalLiteral(self, theBuf, theOfs=0):
        """ISO/IEC 14882:1998(E) 2.13.1 Integer literals [lex.icon] - octal-literal."""
        i = theOfs
        try:
            if theBuf[i] == '0':
                i = 1
                while theBuf[i] in CHAR_SET_MAP['lex.ppnumber']['octal-digit']:
                    i += 1

        except IndexError:
            pass

        return i - theOfs

    def _sliceHexadecimalLiteral(self, theBuf, theOfs=0):
        """ISO/IEC 14882:1998(E) 2.13.1 Integer literals [lex.icon] - hexadecimal-literal."""
        i = theOfs
        try:
            if theBuf[i] == '0' and theBuf[(i + 1)] in ('x', 'X'):
                i += 2
            else:
                return 0
            while theBuf[i] in CHAR_SET_MAP['lex.ppnumber']['hexadecimal-digit']:
                i += 1

        except IndexError:
            pass

        i -= theOfs
        if i > 2:
            return i
        return 0

    def _sliceIntegerSuffix(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.1 Integer literals [lex.icon] - integer-suffix.
        integer-suffix:
            unsigned-suffix long-suffix opt
            long-suffix unsigned-suffix opt"""
        i = 0
        try:
            i = self.__sliceUnsignedSuffix(theBuf, theOfs)
            if i > 0:
                i += self.__sliceLongSuffix(theBuf, theOfs + 1)
            else:
                i = self.__sliceLongSuffix(theBuf, theOfs)
                if i > 0:
                    i += self.__sliceUnsignedSuffix(theBuf, theOfs + 1)
        except IndexError:
            pass

        return i

    def __sliceUnsignedSuffix(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.1 Integer literals [lex.icon] - unsigned-suffix."""
        if theBuf[theOfs] in CHAR_SET_MAP['lex.icon']['unsigned-suffix']:
            return 1
        return 0

    def __sliceLongSuffix(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.1 Integer literals [lex.icon] - long-suffix."""
        if theBuf[theOfs] in CHAR_SET_MAP['lex.icon']['long-suffix']:
            return 1
        return 0

    def _sliceCharacterLiteral(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.2 Character literals [lex.ccon]."""
        i = theOfs
        try:
            if theBuf[i] in PpToken.PpToken.CHARACTER_LITERAL_PREFIXES:
                i += 1
            if theBuf[i] == "'":
                i += 1
                j = self._sliceCCharSequence(theBuf, i)
                i += j
                if theBuf[i] == "'":
                    i += 1
                else:
                    return 0
            else:
                return 0
            if i > theOfs:
                assert self._changeOfTokenTypeIsOk or self._cppTokType is None, '_cppTokType was %s now %s' % (
                 self._cppTokType, 'character-literal')
                self._cppTokType = 'character-literal'
        except IndexError:
            i = theOfs

        return i - theOfs

    def _sliceCCharSequence(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.2 Character literals [lex.ccon] - c-char-sequence."""
        return self._sliceAccumulateOfs(theBuf, theOfs, self._sliceCChar)

    def _sliceCChar(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.2 Character literals [lex.ccon] - c-char."""
        return self._sliceLongestMatchOfs(theBuf, theOfs, (
         self.__sliceCCharCharacter,
         self._sliceEscapeSequence,
         self.__sliceUniversalCharacterName))

    def __sliceCCharCharacter(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.2 Character literals [lex.ccon] - c-char character."""
        if theBuf[theOfs] in CHAR_SET_MAP['lex.ccon']['c-char']:
            return 1
        return 0

    def _sliceEscapeSequence(self, theBuf, theOfs):
        """Returns the length of a slice of theCharS that matches the longest integer literal or 0.
        ISO/IEC 14882:1998(E) 2.13.2 Character literals [lex.ccon] - escape-sequence."""
        return self._sliceLongestMatchOfs(theBuf, theOfs, (
         self.__sliceSimpleEscapeSequence,
         self._sliceOctalEscapeSequence,
         self._sliceHexadecimalEscapeSequence))

    def __sliceSimpleEscapeSequence(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.2 Character literals [lex.ccon] - simple-escape-sequence."""
        if theBuf[theOfs] == '\\' and theBuf[(theOfs + 1)] in CHAR_SET_MAP['lex.ccon']['simple-escape-sequence']:
            return 2
        return 0

    def _sliceOctalEscapeSequence(self, theBuf, theOfs):
        r"""ISO/IEC 14882:1998(E) 2.13.2 Character literals [lex.ccon] - octal-escape-sequence.
        octal-escape-sequence:
            \ octal-digit
            \ octal-digit octal-digit
            \ octal-digit octal-digit octal-digit """
        i = theOfs
        s = CHAR_SET_MAP['lex.ppnumber']['octal-digit']
        try:
            if theBuf[i] == '\\' and theBuf[(i + 1)] in s:
                i += 2
                while theBuf[i] in s:
                    i += 1
                    if i - theOfs == 4:
                        break

        except IndexError:
            pass

        return i - theOfs

    def _sliceHexadecimalEscapeSequence(self, theBuf, theOfs):
        r"""ISO/IEC 14882:1998(E) 2.13.2 Character literals [lex.ccon] - hexadecimal-escape-sequence.
        hexadecimal-escape-sequence:
            \x hexadecimal-digit
            hexadecimal-escape-sequence hexadecimal-digit
        """
        i = theOfs
        s = CHAR_SET_MAP['lex.ppnumber']['hexadecimal-digit']
        try:
            if theBuf[i] == '\\' and theBuf[(i + 1)] == 'x' and theBuf[(i + 2)] in s:
                i += 3
                while theBuf[i] in s:
                    i += 1

        except IndexError:
            pass

        return i - theOfs

    def _sliceFloatingLiteral(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.3 Floating literals [lex.fcon].
        floating-literal:
           fractional-constant exponent-part opt floating-suffix opt
           digit-sequence exponent-part floating-suffix opt
        """
        i = self._sliceFloatingLiteralFractionalConstant(theBuf, theOfs)
        if i > 0:
            i += self._sliceFloatingLiteralExponentPart(theBuf, theOfs + i)
            i += self._sliceFloatingLiteralFloatingSuffix(theBuf, theOfs + i)
        else:
            i = self._sliceFloatingLiteralDigitSequence(theBuf, theOfs)
            if i:
                j = self._sliceFloatingLiteralExponentPart(theBuf, theOfs + i)
                if j:
                    i = i + j
                    i += self._sliceFloatingLiteralFloatingSuffix(theBuf, theOfs + i)
                else:
                    i = 0
        return i

    def _sliceFloatingLiteralFractionalConstant(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.3 Floating literals [lex.fcon] - fractional-constant.
        fractional-constant:
           digit-sequence opt . digit-sequence
           digit-sequence .
        i.e there are three posibilities:
        a: . digit-sequence
        b: digit-sequence .
        c: digit-sequence . digit-sequence
        """
        i = theOfs
        try:
            if theBuf[i] == '.':
                i += 1
                j = self._sliceFloatingLiteralDigitSequence(theBuf, i)
                i += j
                if j > 0:
                    return i - theOfs
                return 0
            else:
                j = self._sliceFloatingLiteralDigitSequence(theBuf, i)
                if j > 0 and theBuf[(i + j)] == '.':
                    i += j + 1
                    i += self._sliceFloatingLiteralDigitSequence(theBuf, i)
        except IndexError:
            pass

        return i - theOfs

    def _sliceFloatingLiteralExponentPart(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.3 Floating literals [lex.fcon] - exponent-part."""
        i = theOfs
        try:
            if theBuf[i] in CHAR_SET_MAP['lex.fcon']['exponent_prefix']:
                i += 1
            else:
                return 0
            i += self._sliceFloatingLiteralSign(theBuf, i)
        except IndexError:
            pass

        j = self._sliceFloatingLiteralDigitSequence(theBuf, i)
        if j == 0:
            return 0
        return i + j - theOfs

    def _sliceFloatingLiteralSign(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.3 Floating literals [lex.fcon] - floating-suffix."""
        try:
            if theBuf[theOfs] in CHAR_SET_MAP['lex.fcon']['sign']:
                return 1
        except IndexError:
            pass

        return 0

    def _sliceFloatingLiteralDigitSequence(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.3 Floating literals [lex.fcon] - digit-sequence."""
        i = theOfs
        try:
            while theBuf[i] in CHAR_SET_MAP['lex.ppnumber']['digit']:
                i += 1

        except IndexError:
            pass

        return i - theOfs

    def _sliceFloatingLiteralFloatingSuffix(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.3 Floating literals [lex.fcon] - floating-suffix."""
        try:
            if theBuf[theOfs] in CHAR_SET_MAP['lex.fcon']['floating-suffix']:
                return 1
        except IndexError:
            pass

        return 0

    def _sliceStringLiteral(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.4 String literals [lex.string]."""
        i = theOfs
        try:
            if theBuf[i] == 'L':
                i += 1
            if theBuf[i] == '"':
                i += 1
                j = self._sliceSCharSequence(theBuf, i)
                i += j
                if theBuf[i] == '"':
                    i += 1
                else:
                    return 0
            else:
                return 0
            if i > theOfs:
                assert self._changeOfTokenTypeIsOk or self._cppTokType is None, '_cppTokType was %s now %s' % (
                 self._cppTokType, 'string-literal')
                self._cppTokType = 'string-literal'
        except IndexError:
            i = theOfs

        return i - theOfs

    def _sliceSCharSequence(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.4 String literals [lex.string] - s-char-sequence."""
        return self._sliceAccumulateOfs(theBuf, theOfs, self._sliceSChar)

    def _sliceSChar(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.4 String literals [lex.string] - s-char."""
        return self._sliceLongestMatchOfs(theBuf, theOfs, (
         self._sliceSCharCharacter,
         self._sliceEscapeSequence,
         self.__sliceUniversalCharacterName))

    def _sliceSCharCharacter(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.4 String literals [lex.string] - s-char character."""
        if theBuf[theOfs] in CHAR_SET_MAP['lex.string']['s-char']:
            return 1
        return 0

    def _sliceBoolLiteral(self, theBuf, theOfs):
        """ISO/IEC 14882:1998(E) 2.13.5 String literals [lex.bool]."""
        return CHAR_SET_STR_TREE_MAP['lex.bool']['set'].has(theBuf, theOfs) - theOfs