# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/core/PpDefine.py
# Compiled at: 2017-10-03 13:07:16
"""This handles definition, undefinition, redefintion, replacement
and rescaning of macro declarations

It implements: :title-reference:`ISO/IEC 9899:1999(E) section 6 (aka 'C99')`
and/or: :title-reference:`ISO/IEC 14882:1998(E) section 16 (aka 'C++98')`

"""
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import logging, copy
from cpip import ExceptionCpip
from cpip.core import PpToken
from cpip.core import PpTokenCount
from cpip.core import PpWhitespace
from cpip.core import FileLocation

class ExceptionCpipDefine(ExceptionCpip):
    """Exception when handling PpDefine object."""
    pass


class ExceptionCpipDefineInit(ExceptionCpipDefine):
    """Exception when creating PpDefine object fails."""
    pass


class ExceptionCpipDefineMissingWs(ExceptionCpipDefineInit):
    """Exception when calling missing ws between identifier and replacement tokens.
    
    See: :title-reference:`ISO/IEC 9899:1999(E) Section 6.10.3-3`
    and :title-reference:`ISO/IEC 14882:1998(E) Section ???`
    
    .. note::
        
        The executable, cpp, says for ``#define PLUS+`` ::
        
            src.h:1:13: warning: ISO C requires whitespace after the macro name"""
    pass


class ExceptionCpipDefineBadWs(ExceptionCpipDefineInit):
    """Exception when calling bad whitespace is in a define statement.
    See: :title-reference:`ISO/IEC 9899:1999(E) Section 6.10-f`
    and :title-reference:`ISO/IEC 14882:1998(E) 16-2`
    """
    pass


class ExceptionCpipDefineInvalidCmp(ExceptionCpipDefineInit):
    """Exception for a redefinition where the identifers are different."""
    pass


class ExceptionCpipDefineDupeId(ExceptionCpipDefineInit):
    """Exception for a function-like macro has duplicates
    in the identifier-list."""
    pass


class ExceptionCpipDefineInitBadLine(ExceptionCpipDefineInit):
    """Exception for a bad line number given as argument."""
    pass


class ExceptionCpipDefineReplace(ExceptionCpipDefine):
    """Exception when replacing a macro definition fails."""
    pass


class ExceptionCpipDefineBadArguments(ExceptionCpipDefine):
    """Exception when scanning an argument list for a function style macro
    fails.
    NOTE: This is only raised during replacement not during
    initialisation."""
    pass


class PpDefine(object):
    """Represents a single #define directive and performs
    :title-reference:`ISO/IECISO/IEC 9899:1999 (E) 6.10.3 Macro replacement.`
    
    *theTokGen*
        A PpToken generator that is expected to
        generate pp-tokens that appear after the start of the #define directive
        from the first non-whitespace token onwards i.e. the __init__ will,
        itself, consume leading whitespace.
    
    *theFileId*
        A string that represents the file ID.
    
    *theLine*
        A positive integer that represents the line in theFile that
        the ``#define`` statement occurred.
    
    Definition example, object-like macros: ::
    
        [identifier, [replacement-list (opt)], new-line, ...]
    
    Or function-like macros: ::
    
        [
            identifier,
            lparen,
            [identifier-list(opt),],
            ')',
            replacement-list,
            new-line,
            ...
        ]
    
    .. note::
        No whitespace is allowed between the identifier and the lparen
        of function-like macros.
    
    The ``identifier-list`` of parameters is stored as a list of names.
    The replacement-list is stored as a list of
    preprocessor tokens.
    Leading and trailing whitespace in the replacement
    list is removed to facilitate redefinition comparison.
    """
    LPAREN = '('
    RPAREN = ')'
    IDENTIFIER_SEPERATOR = ','
    CPP_STRINGIZE_OP = '#'
    CPP_CONCAT_OP = '##'
    PLACEMARKER = None
    STRINGIZE_WHITESPACE_CHAR = ' '
    VARIABLE_ARGUMENT_IDENTIFIER = '...'
    VARIABLE_ARGUMENT_SUBSTITUTE = '__VA_ARGS__'
    INITIAL_REF_COUNT = 0

    def __init__(self, theTokGen, theFileId, theLine):
        """Takes a preprocess token generator and creates a macro.
        The generator (e.g. a instance of PpTokeniser.next()) can
        generate pp-tokens that appear after the start of the #define directive
        from the first non-whitespace token onwards i.e. this __init__ will,
        itself, consume leading whitespace.
        
        theFileId is a string that represents the file ID.
        
        theLine is a positive integer that represents the line in theFile that
        the #define statement occurred. This must be >= 1.
        
        Definition example, object-like macros:
        [identifier, [replacement-list (opt)], new-line, ...]
        Or function-like macros: ::
        
            [
                identifier,
                lparen,
                [identifier-list(opt),
                ],
                ')',
                replacement-list,
                new-line,
                ...
            ]
        
        NOTE: No whitespace is allowed between the identifier and the lparen
        of function-like macros.
        
        The replacement-list is stored as a list of
        preprocessor tokens. The identifier-list is stored as a list of names.
        Leading and trailing whitespace in the replacement
        list is removed to facilitate redefinition comparison.
        """
        if theLine < FileLocation.START_LINE:
            raise ExceptionCpipDefineInitBadLine('Irresponsible line number: %s' % theLine)
        self._fileLine = FileLocation.FileLine(theFileId, theLine)
        self._undefFileLine = None
        self._tokenCount = PpTokenCount.PpTokenCount()
        self._identifier = None
        self._replaceTokTypesS = []
        self._paramS = None
        self._wsHandler = PpWhitespace.PpWhitespace()
        self._expandArguments = None
        self._refCount = self.INITIAL_REF_COUNT
        self._refFileLineColS = []
        self._isVariadic = False
        try:
            myTtt = self._nextNonWsOrNewline(theTokGen)
            if self._wsHandler.isBreakingWhitespace(myTtt.t):
                raise ExceptionCpipDefineInit('Premature newline in token stream.')
            if not myTtt.isIdentifier():
                self._consumeAndRaise(theTokGen, ExceptionCpipDefineInit('Missing #define <name> but token type "%s" value "%s" in token stream at %s' % (
                 myTtt.tt, myTtt.t, self._fileLine)))
            self._identifier = myTtt
            myTtt = self._retToken(theTokGen)
            if myTtt.t == self.LPAREN:
                self._ctorFunctionMacro(theTokGen)
            elif not myTtt.isWs():
                self._consumeAndRaise(theTokGen, ExceptionCpipDefineMissingWs('Missunderstood (6.10.3-3) token "%s" type "%s"' % (
                 myTtt.t, myTtt.tt)))
            else:
                self._paramS = None
                self._isVariadic = False
                if not self._wsHandler.isBreakingWhitespace(myTtt.t):
                    self._appendToReplacementList(theTokGen)
                self._expandArguments = False
            self.assertReplListIntegrity()
            assert self._expandArguments is not None
        except StopIteration:
            raise ExceptionCpipDefineInit('Token stream is too short')

        assert self.isCurrentlyDefined
        return

    def _appendArgIdentifier(self, theTok, theGenTok):
        """Appends the token text to the argument identifier list."""
        if theTok.t in self._paramS:
            self._consumeAndRaise(theGenTok, ExceptionCpipDefineDupeId('Token %s already in %s' % (
             theTok.t, self._paramS)))
        self._paramS.append(theTok.t)

    def _ctorFunctionMacro(self, theGenTok):
        """Construct function type macros.
        [[identifier-list,] ,')', replacement-list, new-line, ...]
        The identifier-list is not specified in the specification but there
        seems to be some disparity between the standards and cpp.exe.
        The relevant bits of the standards [C: ISO/IEC 9899:1999(E) 6.10.3-10
        and -11 and C++: ISO/IEC 14882:1998(E) 16.3-9 (C++)] appear, to me,
        to suggest that left and right parenthesis are allowed in the
        identifier-list and that (,) is ignored. But cpp.exe will not accept
        that.
        
        Playing with cpp -E it seems that it is a comma separated
        list where whitespace is ignored, nothing else is allowed.
        See unit tests testInitFunction_70(), 71 and 72.
        cpp.exe also is not so strict when it comes the the above sections. For
        example in this:
        #define FOO(a,b,c) a+b+c
        FOO (1,(2),3)
        The whitespace between FOO and LPAREN is ignored and the replacement
        occurs."""
        assert self.isCurrentlyDefined
        self._paramS = []
        self._expandArguments = True
        while 1:
            aTtt = self._retToken(theGenTok)
            if not aTtt.isWs():
                if aTtt.t == self.RPAREN:
                    break
                elif aTtt.t == ',':
                    pass
                elif aTtt.isIdentifier():
                    self._appendArgIdentifier(aTtt, theGenTok)
                elif aTtt.t == self.VARIABLE_ARGUMENT_IDENTIFIER:
                    self._appendArgIdentifier(aTtt, theGenTok)
                else:
                    self._consumeAndRaise(theGenTok, ExceptionCpipDefineInit('Don\'t understand token "%s" type %s in function like macro' % (
                     aTtt.t, aTtt.tt)))
            elif self._wsHandler.isBreakingWhitespace(aTtt.t):
                raise ExceptionCpipDefineInit('Premature newline in function like macro')

        self._isVariadic = False
        for aId in self._paramS:
            if aId == self.VARIABLE_ARGUMENT_IDENTIFIER:
                self._isVariadic = True
            elif self._isVariadic:
                self._consumeAndRaise(theGenTok, ExceptionCpipDefineInit('Variadic identifier seen but not as last identifier in argument list'))

        self._appendToReplacementList(theGenTok)

    def _appendToReplacementList(self, theGenTok):
        """Takes a token sequence up to a newline and assign it
        to the replacement-list. Leading and trailing whitespace is ignored.
        TODO: Set setPrevWs flag where necessary."""
        assert self.isCurrentlyDefined
        trailingWs = []
        flagNextNonWsIsId = False
        while 1:
            aTok = self._retToken(theGenTok)
            if aTok.isWs():
                if self._wsHandler.isBreakingWhitespace(aTok.t):
                    break
                if len(self._replaceTokTypesS) != 0:
                    trailingWs.append(aTok)
            else:
                if flagNextNonWsIsId:
                    if aTok.t in self._paramS or self._isVariadic and aTok.t == self.VARIABLE_ARGUMENT_SUBSTITUTE:
                        flagNextNonWsIsId = False
                    else:
                        self._consumeAndRaise(theGenTok, ExceptionCpipDefineInit('\'#\' is not followed by a macro parameter but "%s" of type %s' % (
                         aTok.t, aTok.tt)))
                if not self.isObjectTypeMacro:
                    if aTok.t == self.CPP_STRINGIZE_OP:
                        flagNextNonWsIsId = True
                        self._expandArguments = False
                    if aTok.t == self.CPP_CONCAT_OP:
                        self._expandArguments = False
                if len(trailingWs):
                    for t in trailingWs:
                        self.__addTokenAndTypeToReplacementList(t)

                    trailingWs = []
                self.__addTokenAndTypeToReplacementList(aTok)

        if len(self._replaceTokTypesS) > 0:
            if self._replaceTokTypesS[0].t == self.CPP_CONCAT_OP:
                self._consumeAndRaise(theGenTok, ExceptionCpipDefineInit("'##' cannot appear at the begining of a macro expansion"))
            if self._replaceTokTypesS[(-1)].t == self.CPP_CONCAT_OP:
                self._consumeAndRaise(theGenTok, ExceptionCpipDefineInit("'##' cannot appear at the end of a macro expansion"))
        if not self._isVariadic:
            for aRepTtt in self._replaceTokTypesS:
                if aRepTtt.t == self.VARIABLE_ARGUMENT_SUBSTITUTE:
                    raise ExceptionCpipDefineInit('%s can only appear in the expansion of a C99 variadic macro' % self.VARIABLE_ARGUMENT_SUBSTITUTE)

    def __addTokenAndTypeToReplacementList(self, theTtt):
        """Adds a token and a token type to the replacement list. Runs of
        whitespace tokens are concatenated."""
        assert self.isCurrentlyDefined
        if len(self._replaceTokTypesS) > 0 and theTtt.isWs() and self._replaceTokTypesS[(-1)].isWs():
            self._replaceTokTypesS[(-1)].merge(theTtt)
        else:
            theTtt.isReplacement = True
            self._replaceTokTypesS.append(theTtt)

    def _isPlacemarker(self, theTok):
        """Returns True if the Token represents a PLACEMARKER token.
        This is the correct comparison operator can be used if self.PLACEMARKER
        is defined as None."""
        return theTok is self.PLACEMARKER

    def strIdentPlusParam(self):
        """Returns the identifier name and parameters if a function-like macro
        as a string."""
        retList = [
         self.identifier]
        if not self.isObjectTypeMacro:
            idList = []
            for anId in self._paramS:
                if self._isPlacemarker(anId):
                    anId = ''
                idList.append(anId)

            retList.append('(%s)' % (',').join(idList))
        return ('').join(retList)

    def strReplacements(self):
        """Returns the replacements tokens with minimised whitespace as a string."""
        retList = []
        if len(self._replaceTokTypesS) > 0:
            for aTok in self._replaceTokTypesS:
                if aTok.isWs():
                    retList.append(' ')
                else:
                    retList.append(aTok.t)

        return ('').join(retList)

    def __str__(self):
        retList = [
         '#define %s' % self.strIdentPlusParam()]
        if len(self._replaceTokTypesS) > 0:
            retList.append(' ')
            retList.append(self.strReplacements())
        cmtStr = '%s#%d Ref: %d %s' % (
         self.fileId,
         self.line,
         self.refCount,
         self.isCurrentlyDefined)
        if not self.isCurrentlyDefined:
            cmtStr += ' %s#%d' % (self.undefFileId, self.undefLine)
        retList.append(' /* %s */' % cmtStr)
        return ('').join(retList)

    def _retToken(self, theGen):
        """Returns the next token object and increments the IR."""
        assert self.isCurrentlyDefined
        retTok = next(theGen)
        self._tokenCount.inc(retTok, True)
        if retTok.isWs() and not self._wsHandler.isAllMacroWhitespace(retTok.t):
            if self._wsHandler.isBreakingWhitespace(retTok.t):
                raise ExceptionCpipDefineBadWs('Invalid macro whitespace in "%s"' % retTok.t)
            else:
                self._consumeAndRaise(theGen, ExceptionCpipDefineBadWs('Invalid macro whitespace in "%s"' % retTok.t))
        return retTok

    def _nextNonWsOrNewline(self, theGen):
        """Returns the next non-whitespace token or whitespace that contains a
        newline."""
        assert self.isCurrentlyDefined
        while 1:
            myTtt = self._retToken(theGen)
            if not myTtt.isWs() or self._wsHandler.isBreakingWhitespace(myTtt.t):
                return myTtt

    def _consumeNewline(self, theGen):
        """Consumes all tokens up to and including the next newline."""
        assert self.isCurrentlyDefined
        while 1:
            myTtt = self._retToken(theGen)
            if self._wsHandler.isBreakingWhitespace(myTtt.t):
                break

    def _consumeAndRaise(self, theGen, theException):
        """Consumes all tokens up to and including the next newline then raises
        an exception. This is commonly used to get rid of bad token streams but
        allow the caller to catch the exception, report the error and
        continue."""
        assert self.isCurrentlyDefined
        self._consumeNewline(theGen)
        raise theException

    def assertReplListIntegrity(self):
        """Tests that any identifier tokens in the replacement list are
        actually replaceable. This will raise an assertion failure if
        not. It is really an integrity tests to see if an external entity
        has grabbed a reference to the replacement list and set a token
        to be not replaceable."""
        assert self.isCurrentlyDefined
        for aTtt in self._replaceTokTypesS:
            assert not aTtt.isIdentifier() or aTtt.canReplace, 'Token %s is invalid' % str(aTtt)

    def incRefCount(self, theFileLineCol=None):
        """Increment the reference count. Typically callers do this when
        replacement is certain of in the event of definition testing
        
        *theFileLineCol*
            A FileLocation.FileLineCol object.
        
        For example:
        
        ``#ifdef SPAM or defined(SPAM)`` etc.
        
        Or if the macro is expanded e.g. ``#define SPAM_N_EGGS spam and eggs``
        
        The menu is SPAM_N_EGGS.
        
        """
        if not self.isCurrentlyDefined:
            raise ExceptionCpipDefine("incRefCount() on already #undef'd macro instance of self")
        self._refCount += 1
        if theFileLineCol is not None:
            self._refFileLineColS.append(theFileLineCol)
        return

    def replaceObjectStyleMacro(self):
        """Returns a list of ``[(token, token_type), ...]`` from the replacement
        of an object style macro."""
        assert self.isCurrentlyDefined
        assert self.isObjectTypeMacro, 'replaceObjectStyleMacro() called on function style macro'
        return self._objectLikeReplacement()

    def _objectLikeReplacement(self):
        """Returns the replacement list for an object like macro.
        This handles the ``##`` token i.e. [cpp.concat].
        
        Returns a list of pairs i.e. ``[(token, token_type), ...]``"""
        assert self.isCurrentlyDefined
        assert self.isObjectTypeMacro, '_objectLikeReplacement() called on non-object like macro'
        retReplList = []
        flagConcatSeen = False
        for aTtt in copy.deepcopy(self._replaceTokTypesS):
            if aTtt.t == self.CPP_CONCAT_OP:
                flagConcatSeen = True
                while 1:
                    assert len(retReplList) > 0, 'Leading ## has crept through the constructor'
                    rTtt = retReplList[(-1)]
                    if not rTtt.isWs():
                        break
                    else:
                        retReplList.pop()

            elif flagConcatSeen:
                if not aTtt.isWs():
                    retReplList[(-1)].merge(aTtt)
                    flagConcatSeen = False
            else:
                retReplList.append(aTtt)

        assert not flagConcatSeen, 'Trailing ## has crept through the constructor'
        return retReplList

    def consumeFunctionPreamble(self, theGen):
        """This consumes tokens to the preamble of a Function style macro
        invocation. This really means consuming whitespace and the opening
        ``LPAREN``.
        
        This will return either:
        
        * None - Tokens including the leading LPAREN have been consumed.
        * List of ``(token, token_type)`` if the LPAREN is not found.
        
        For example given this: ::

            #define t(a) a+2
            t   (21) - t  ;

        For the first ``t`` this would consume ``'   ('`` and return None leaving the
        next token to be ('21', 'pp-number').
        
        For the second ``t`` this would consume ``'  ;'`` and return: ::

            [
                ('  ', 'whitespace'),
                (';',   'preprocessing-op-or-punc'),
            ]

        This allows the MacroReplacementEnv to generate the correct result: ::
        
            21 +2 - t ;
        """
        assert self.isCurrentlyDefined
        assert not self.isObjectTypeMacro, 'consumeFunctionPreamble() called on object like macro'
        failTokList = []
        while 1:
            try:
                myTtt = self._retToken(theGen)
            except StopIteration:
                return failTokList

            if not myTtt.isWs():
                break
            failTokList.append(myTtt)

        if myTtt.t != self.LPAREN:
            theGen.send(myTtt)
            return failTokList
        else:
            return

    def retArgumentListTokens(self, theGen):
        """For a function macro this reads the tokens following a ``LPAREN`` and
        returns a list of arguments where each argument is a list of
        PpToken objects.
        
        Thus this function returns a list of lists of :py:class:`.PpToken.PpToken` objects,
        for example given this: ::
        
            #define f(x,y) ...
            f(a,b)
        
        This function, then passed ``a,b)`` returns: ::
        
            [
                [
                    PpToken.PpToken('a', 'identifier'),
                ],
                [
                    PpToken.PpToken('b', 'identifier'),
                ],
            ]
        
        And an invocation of:
        ``f(1(,)2,3)`` i.e. this gets passed via the generator ``"1(,)2,3)"``
        and returns two argunments: ::
        
            [
                [
                    PpToken('1', 'pp-number'),
                    PpToken('(', 'preprocessing-op-or-punc'),
                    PpToken(',', 'preprocessing-op-or-punc'),
                    PpToken(')', 'preprocessing-op-or-punc'),
                    PpToken('2', 'pp-number'),
                ],
                [
                    PpToken('3', 'pp-number'),
                ],
            ]
        
        So this function supports two cases:
        
        1. Parsing function style macro declarations.
        2. Interpreting function style macro invocations where the argument list
           is subject to replacement before invoking the macro.
        
        In the case that an argument is missing a ``PpDefine.PLACEMARKER``
        token is inserted. For example: ::
        
            #define FUNCTION_STYLE(a,b,c) ...
            FUNCTION_STYLE(,2,3)
        
        Gives: ::
        
            [
                PpDefine.PLACEMARKER,
                [
                    PpToken.PpToken('2',       'pp-number'),
                ],
                [
                    PpToken.PpToken('3',       'pp-number'),
                ],
            ]
        
        Placemarker tokens are not used if the macro is defined with no
        arguments.
        This might raise a :py:class:`ExceptionCpipDefineBadArguments` if the list
        does not match the prototype or a StopIteration if the token list is
        too short.
        This ignores leading and trailing whitespace for each argument.
        
        TODO: Raise an :py:class:`ExceptionCpipDefineBadArguments` if there is a
        ``#define`` statement. e.g.: ::
    
            #define f(x) x x
            f (1
            #undef f
            #define f 2
            f)
        """
        if not self.isCurrentlyDefined:
            raise AssertionError
            assert not self.isObjectTypeMacro, 'retArgumentListTokens() called on object like macro'
            pDepth = 1
            myArg = []
            myArgS = []
            trailingWs = []
            while 1:
                myTtt = self._retToken(theGen)
                if myTtt.t == self.LPAREN:
                    pDepth += 1
                    myArg.append(myTtt)
            else:
                if myTtt.t == self.RPAREN or myTtt.t == ',':
                    if myTtt.t == self.RPAREN:
                        pDepth -= 1
                    if pDepth == 0 or pDepth == 1 and myTtt.t == ',':
                        if len(myArg) == 0:
                            myArgS.append(self.PLACEMARKER)
                        else:
                            myArgS.append(myArg)
                        myArg = []
                        trailingWs = []
                        if pDepth == 0:
                            break
                    else:
                        assert not self._wsHandler.isAllWhitespace(myTtt.t)
                        myArg += trailingWs
                        trailingWs = []
                        myArg.append(myTtt)
                elif self._wsHandler.isAllWhitespace(myTtt.t):
                    if len(myArg) > 0:
                        trailingWs.append(myTtt)
                    else:
                        continue
                        myArg += trailingWs
                        trailingWs = []
                        myArg.append(myTtt)

            if len(self._paramS) == 0 and len(myArgS) == 1 and self._isPlacemarker(myArgS[0]):
                myArgS = []
            if self._isVariadic or len(myArgS) != len(self._paramS):
                if len(myArgS) < len(self._paramS):
                    msg = 'macro "%s" requires %d arguments, but only %d given' % (
                     self.identifier, len(self._paramS), len(myArgS))
                else:
                    msg = 'macro "%s" passed %d arguments, but takes just %d' % (
                     self.identifier, len(myArgS), len(self._paramS))
                raise ExceptionCpipDefineBadArguments(msg)
        elif len(myArgS) < len(self._paramS) - 1:
            msg = 'macro "%s" requires %d arguments, but only %d given' % (
             self.identifier, len(self._paramS) - 1, len(myArgS))
            raise ExceptionCpipDefineBadArguments(msg)
        return myArgS

    def replaceArgumentList(self, theArgList):
        """Given an list of arguments this does argument substitution and
        returns the replacement token list. The argument list is of the form
        given by :py:meth:`retArgumentListTokens`. The caller must have replaced any
        macro invocations in theArgList before calling this method.
        
        .. note::
            For function style macros only.
        """
        assert self.isCurrentlyDefined
        assert not self.isObjectTypeMacro, 'replaceArgumentList() called on object like macro'
        myReplaceMap = self._retReplacementMap(theArgList)
        myReplacements = self._functionLikeReplacement(myReplaceMap)
        return myReplacements

    def _retReplacementMap(self, theArgs):
        """Given a list of lists of (token, type) this returns a map of:
        {identifier : [replacement_token and token types, ...], ...}
        For example for:
        #define FOO(c,b,a) a+b+c
        FOO(1+7,2,3)
        i.e theArgs is (types are shown as text for clarity, in practice they
        would be enumerated):
        [
            [
                PpToken.PpToken('1', 'pp-number'),
                PpToken.PpToken('+', 'preprocessing-op-or-punc'),
                PpToken.PpToken('7', 'pp-number')
            ],
            [
                PpToken.PpToken('2', 'pp-number'),
            ],
            [
                PpToken.PpToken('3', 'pp-number'),
            ],
        ]
        Map would be:
        {
            'a' : [
                    PpToken.PpToken('3', 'pp-number'),
                ],
            'b' : [
                    PpToken.PpToken('2', 'pp-number'),
                ],
            'c' : [
                    PpToken.PpToken('1', 'pp-number'),
                    PpToken.PpToken('+', 'preprocessing-op-or-punc'),
                    PpToken.PpToken('7', 'pp-number')
                ],
        }
        Note that values that are placemarker tokens are
        PpDefine.PLACEMARKER. For example:
        #define FOO(a,b,c) a+b+c
        FOO(,2,)
        Generates:
        {
            'a' : PpDefine.PLACEMARKER,
            'b' : [
                    ('2', 'pp-number'),
                ]
            'c' : PpDefine.PLACEMARKER,
        }
        PERF: See TODO below.
        TODO: Return a map of identifiers to indexes in the supplied argument as
        this will save making a copy of the argument tokens?
        So:
        #define FOO(c,b,a) a+b+c
        FOO(1+7,2,3)
        Would return a map of:
        {
            'a' : 2,
            'b' : 1,
            'c' : 0,
        }
        And use index -1 for a placemarker token???:
        #define FOO(a,b,c) a+b+c
        FOO(,2,)
        Generates:
        {
            'a' : -1,
            'b' : 1
            'c' : -1,
        }
        """
        assert self.isCurrentlyDefined
        assert not self.isObjectTypeMacro, '_retReplacementMap() called on object like macro'
        assert self._isVariadic or len(theArgs) == len(self._paramS)
        retMap = {}
        for i, tok in enumerate(self._paramS):
            if not tok not in retMap:
                raise AssertionError('Duplicate identifier in function macro has slipped through the constructor.')
                if self._isVariadic and i >= len(theArgs):
                    break
                myArgList = self._isPlacemarker(theArgs[i]) or []
                if self._isVariadic and tok == self.VARIABLE_ARGUMENT_IDENTIFIER:
                    myArgList.extend(theArgs[i])
                    i += 1
                    while i < len(theArgs):
                        myArgList.append(PpToken.PpToken(',', 'preprocessing-op-or-punc'))
                        if not self._isPlacemarker(theArgs[i]):
                            myArgList.extend(theArgs[i])
                        i += 1

                    retMap[tok] = myArgList
                    break
                else:
                    for aTtt in theArgs[i]:
                        if aTtt.isWs():
                            aTtt.replaceNewLine()
                        myArgList.append(aTtt)

                    retMap[tok] = myArgList
            elif self._isVariadic and tok == self.VARIABLE_ARGUMENT_IDENTIFIER:
                myArgList = []
                i += 1
                while i < len(theArgs):
                    myArgList.append(PpToken.PpToken(',', 'preprocessing-op-or-punc'))
                    if self._isPlacemarker(theArgs[i]):
                        pass
                    else:
                        myArgList.extend(theArgs[i])
                    i += 1

                retMap[tok] = myArgList
                break
            elif not self._isPlacemarker(tok):
                retMap[tok] = self.PLACEMARKER

        for arg in retMap:
            if retMap[arg] is not self.PLACEMARKER:
                for t in retMap[arg]:
                    t.isReplacement = True

        return retMap

    def _functionLikeReplacement(self, theArgMap):
        """Returns the replacement list where if a token is encountered that
        is a key in the map then the value in the map is inserted into the
        replacement list.
        theArgMap is of the form returned by _retReplacementMap().
        This also handles the '#' token i.e. [cpp.stringize]
        and '##' token i.e. [cpp.concat].
        Returns a list of pairs i.e. [(token, token_type), ...]
        
        TODO: Accidental token pasting
        #define f(x) =x=
        f(=)
        We want '= = =' not '==='.
        """
        assert self.isCurrentlyDefined, '_functionLikeReplacement() called on undefined macro'
        assert not self.isObjectTypeMacro, '_functionLikeReplacement() called on object like macro'

        def _avoidTokenPasting(retReplList, t):
            if len(retReplList) and t.tt == 'preprocessing-op-or-punc' and retReplList[(-1)].tt == 'preprocessing-op-or-punc' and retReplList[(-1)].t == t.t:
                retReplList.append(PpToken.PpToken(' ', 'whitespace'))

        retReplList = []
        flagStringize = False
        flagConcatSeen = False
        for myTtt in copy.deepcopy(self._replaceTokTypesS):
            if myTtt.t in theArgMap:
                if self._isPlacemarker(theArgMap[myTtt.t]):
                    if flagStringize:
                        retReplList.append(self._cppStringize(''))
                        flagStringize = False
                elif flagStringize:
                    retReplList.append(self._cppStringize(theArgMap[myTtt.t]))
                    flagStringize = False
                elif flagConcatSeen:
                    if len(retReplList) > 0:
                        retReplList[(-1)].merge(theArgMap[myTtt.t][0])
                        retReplList += theArgMap[myTtt.t][1:]
                    else:
                        retReplList += theArgMap[myTtt.t]
                    flagConcatSeen = False
                else:
                    replaceTokens = copy.deepcopy(theArgMap[myTtt.t])
                    if len(replaceTokens):
                        _avoidTokenPasting(retReplList, replaceTokens[0])
                    retReplList += replaceTokens
            elif myTtt.t == self.CPP_STRINGIZE_OP:
                flagStringize = True
                if flagConcatSeen:
                    self.__logWarningHashHashHash()
            elif myTtt.t == self.CPP_CONCAT_OP:
                flagConcatSeen = True
                if flagStringize:
                    self.__logWarningHashHashHash()
                while len(retReplList) and retReplList[(-1)].isWs():
                    retReplList.pop()

            elif self._isVariadic and myTtt.t == self.VARIABLE_ARGUMENT_SUBSTITUTE:
                if self.VARIABLE_ARGUMENT_IDENTIFIER in theArgMap:
                    if flagStringize:
                        retReplList.append(self._cppStringize(theArgMap[self.VARIABLE_ARGUMENT_IDENTIFIER]))
                        flagStringize = False
                    else:
                        retReplList.extend(theArgMap[self.VARIABLE_ARGUMENT_IDENTIFIER])
                flagConcatSeen = False
            elif flagConcatSeen:
                if not myTtt.isWs():
                    retReplList[(-1)].merge(myTtt)
                    flagConcatSeen = False
            else:
                retReplList.append(myTtt)

        return retReplList

    def __logWarningHashHashHash(self):
        """Emit a warning to the log that # and ## are dangerous together."""
        logging.warning("Using both '#' and '##' gives rise to unspecified behaviour.")

    def _cppStringize(self, theArgTokens):
        """Applies the '#' operator to function style macros
        ISO/IEC ISO/IEC 14882:1998(E) 16.3.2 The # operator [cpp.stringize]"""
        assert self.isCurrentlyDefined
        assert not self.isObjectTypeMacro, '_cppStringize called but # character not significant in a object like macro.'
        tempList = []
        for aTtt in theArgTokens:
            if aTtt.isWs():
                if len(tempList) > 0 and tempList[(-1)] != self.STRINGIZE_WHITESPACE_CHAR:
                    tempList.append(self.STRINGIZE_WHITESPACE_CHAR)
            else:
                tempList.append(aTtt.t)

        if len(tempList) > 0 and tempList[(-1)] == self.STRINGIZE_WHITESPACE_CHAR:
            tempList.pop()
        return PpToken.PpToken('"%s"' % ('').join(tempList).replace('"', '\\"'), 'string-literal', isReplacement=True)

    @property
    def isObjectTypeMacro(self):
        """True if this is an object type macro and
        False if it is a function type macro."""
        return self._paramS is None

    @property
    def identifier(self):
        """The macro identifier i.e. the name as a string."""
        return self._identifier.t

    @property
    def tokenCounter(self):
        """The PpTokenCount object that counts tokens that have been consumed
        from the input."""
        return self._tokenCount

    @property
    def tokensConsumed(self):
        """The total number of tokens consumed by the class."""
        return self._tokenCount.totalAll

    @property
    def replacements(self):
        """The list of zero or more replacement tokens as strings."""
        return [ t.t for t in self._replaceTokTypesS ]

    @property
    def replacementTokens(self):
        """The list of zero or more replacement token as a list of
        :py:class:`.PpToken.PpToken`
        """
        return self._replaceTokTypesS

    @property
    def parameters(self):
        """The list of parameter names as strings for a function like macros
        or None if this is an object type Macro."""
        return self._paramS

    @property
    def expandArguments(self):
        """The flag that says whether arguments should be expanded.
        For object like macros this will be False. For function like macros
        this will be False if there is a stringize (``#``) or a token pasting
        operator (``##``). True otherwise."""
        return self._expandArguments

    @property
    def fileId(self):
        """The file ID given as an argument in the constructor."""
        return self._fileLine.fileId

    @property
    def line(self):
        """The line number given as an argument in the constructor."""
        return self._fileLine.lineNum

    @property
    def refCount(self):
        """Returns the current reference count as an integer less its initial
        value on construction."""
        return self._refCount - self.INITIAL_REF_COUNT

    @property
    def isReferenced(self):
        """Returns True if the reference count has been incremented since
        construction."""
        return self._refCount > self.INITIAL_REF_COUNT

    @property
    def isCurrentlyDefined(self):
        """Returns True if the current instance is a valid definition
        i.e. it has not been #undef'd."""
        return self._undefFileLine is None

    @property
    def undefFileId(self):
        """The file ID where this macro was undef'd or None."""
        if self._undefFileLine is not None:
            return self._undefFileLine.fileId
        else:
            return

    @property
    def undefLine(self):
        """The line number where this macro was undef'd or None."""
        if self._undefFileLine is not None:
            return self._undefFileLine.lineNum
        else:
            return

    @property
    def refFileLineColS(self):
        """Returns the list of FileLineCol objects where this macro was referenced."""
        return self._refFileLineColS

    def __eq__(self, other):
        return self.isSame(other) == 0

    def isSame(self, other):
        """Tests 'sameness'. Returns:
        -1 if the identifiers are different.
        1 if the identifiers are the same but redefinition is NOT allowed.
        0 if the identifiers are the same but redefinition is allowed i.e. the
        macros are equivelent."""
        if not self.isCurrentlyDefined:
            raise ExceptionCpipDefine("#undef on already #undef'd instance of self macro")
        if not other.isCurrentlyDefined:
            raise ExceptionCpipDefine("#undef on already #undef'd instance of other macro")
        if self.identifier != other.identifier:
            return -1
        if self.isValidRefefinition(other):
            return 0
        return 1

    def isValidRefefinition(self, other):
        """Returns True if this is a valid redefinition of *other*, False otherwise.
        Will raise an :py:class:`ExceptionCpipDefineInvalidCmp` if the identifiers are
        different.
        Will raise an :py:class:`ExceptionCpipDefine` if either is not currently defined.
        
        From: **ISO/IEC 9899:1999 (E) 6.10.3:**
        
        #. Two replacement lists are identical if and only if the preprocessing
            tokens in both have the same number, ordering, spelling, and white-space
            separation, where all white-space separations are considered identical.
        #. An identifier currently defined as a macro without use of lparen
            (an object-like macro) may be redefined by another #define preprocessing
            directive provided that the second definition is an object-like macro
            definition and the two replacement lists are identical, otherwise the
            program is ill-formed.
        #. An identifier currently defined as a macro using lparen (a
            function-like macro) may be redefined by another #define preprocessing
            directive provided that the second definition is a function-like macro
            definition that has the same number and spelling of parameters, and the
            two replacement lists are identical, otherwise the program is
            ill-formed.

        See also: **ISO/IEC 14882:1998(E) 16.3 Macro replacement [cpp.replace]**"""
        if not self.isCurrentlyDefined:
            raise ExceptionCpipDefine("isValidRefefinition() on already #undef'd macro instance of self.")
        if not other.isCurrentlyDefined:
            raise ExceptionCpipDefine("isValidRefefinition() on already #undef'd macro instance of other.")
        if self.identifier != other.identifier:
            raise ExceptionCpipDefineInvalidCmp('isValidRefefinition() "%s" != "%s"' % (
             self.identifier, other.identifier))
        if self.isObjectTypeMacro and not other.isObjectTypeMacro or not self.isObjectTypeMacro and other.isObjectTypeMacro:
            return False
        assert self.isObjectTypeMacro or not other.isObjectTypeMacro
        assert self._paramS is not None
        if not other.parameters is not None:
            raise AssertionError
            if self._paramS != other.parameters:
                return False
        if len(self.replacements) != len(other.replacements):
            return False
        else:
            for s, o in zip(self.replacements, other.replacements):
                if self._wsHandler.isAllWhitespace(s):
                    if not self._wsHandler.isAllWhitespace(o):
                        return False
                elif self._wsHandler.isAllWhitespace(o):
                    if not self._wsHandler.isAllWhitespace(s):
                        return False
                elif s != o:
                    return False

            return True

    def undef(self, theFileId, theLineNum):
        """Records this instance of a macro ``#undef``'d at a particular file
        and line number. May raise an :py:class:`ExceptionCpipDefine` if already
        undefined or the line number is bad."""
        if not self.isCurrentlyDefined:
            raise ExceptionCpipDefine("#undef on already #undef'd instance of macro")
        if theLineNum < FileLocation.START_LINE:
            raise ExceptionCpipDefine('Irresponsible line number: %s' % theLineNum)
        self._undefFileLine = FileLocation.FileLine(theFileId, theLineNum)