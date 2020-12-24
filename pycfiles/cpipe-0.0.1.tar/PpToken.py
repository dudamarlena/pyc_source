# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/core/PpToken.py
# Compiled at: 2017-10-03 13:07:16
__doc__ = 'Represents a preprocessing Token in C/C++ source code.\n'
import copy, sys
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
from cpip import ExceptionCpip

class ExceptionCpipToken(ExceptionCpip):
    """Used by :py:class:`PpToken`."""


class ExceptionCpipTokenUnknownType(ExceptionCpipToken):
    """Used by :py:class:`PpToken` when the token type is out of range."""


class ExceptionCpipTokenIllegalOperation(ExceptionCpipToken):
    """Used by :py:class:`PpToken` when an illegal operation is performed."""


class ExceptionCpipTokenReopenForExpansion(ExceptionCpipTokenIllegalOperation):
    """Used by :py:class:`PpToken` when a non-expandable token is
    made available for expansion."""


class ExceptionCpipTokenIllegalMerge(ExceptionCpipTokenIllegalOperation):
    """Used by :py:class:`PpToken` when :py:meth:`PpToken.merge()` is called illegally."""


LEX_PPTOKEN_TYPES = [
 'header-name',
 'identifier',
 'pp-number',
 'character-literal',
 'string-literal',
 'preprocessing-op-or-punc',
 'non-whitespace',
 'whitespace',
 'concat']
NAME_ENUM = {}
ENUM_NAME = {}
LEX_PPTOKEN_TYPE_ENUM_RANGE = range(len(LEX_PPTOKEN_TYPES))

def __initPptokenMaps():
    """Initialise the reverse map on module load."""
    for i in LEX_PPTOKEN_TYPE_ENUM_RANGE:
        NAME_ENUM[LEX_PPTOKEN_TYPES[i]] = i
        ENUM_NAME[i] = LEX_PPTOKEN_TYPES[i]


__initPptokenMaps()

def tokensStr(theTokens, shortForm=True):
    """Given a list of tokens this returns them as a string.
    If shortForm is True then the lexical string is returned.
    If False then the :py:class:`PpToken` representations separated by ' | ' is returned.
    e.g. ``PpToken(t="f", tt=identifier, line=True, prev=False, ?=False) | ...``
    """
    assert theTokens is not None
    if shortForm:
        strList = [ t.t for t in theTokens ]
        return ('').join(strList)
    else:
        strList = [ str(t) for t in theTokens ]
        return (' | ').join(strList)


class PpToken(object):
    """Holds a preprocessor token, its type and whether the token can
    be replaced.
    
    t is the token (a string) and tt is either an enumerated integer or
    a string. Internally tt is stored as an enumerated integer.
    If the token is an identifier then it is eligible for replacement
    unless marked otherwise."""
    SINGLE_SPACE = ' '
    WORD_REPLACE_MAP = {'&&': ' and ', 
       '||': ' or ', 
       'true': 'True', 
       'false': 'False', 
       '/': '//'}
    CHARACTER_LITERAL_PREFIXES = {
     'L', 'u', 'U'}

    def __init__(self, t, tt, lineNum=0, colNum=0, isReplacement=False):
        """T is the token (a string) and tt is either an enumerated integer or
        a string. Internally tt is stored as an enumerated integer.
        If the token is an identifier then it is eligible for replacement
        unless marked otherwise."""
        self._t = t
        if tt in ENUM_NAME:
            self._tt = tt
        elif tt in NAME_ENUM:
            self._tt = NAME_ENUM[tt]
        else:
            raise ExceptionCpipTokenUnknownType('Unknown token enumeration: %s' % str(tt))
        self._lineNum = lineNum
        self._colNum = colNum
        self._canReplace = self.isIdentifier()
        self._prevWs = False
        self._isCond = False
        self._isReplacement = isReplacement

    def copy(self):
        """Returns a shallow copy of self. This is useful where the same token is
        added to multiple lists and then a merge() operation on one list will
        be seen by the others. To avoid this insert self.copy() in all but one
        of the lists."""
        return copy.copy(self)

    def subst(self, t, tt):
        """Substitutes token value and type."""
        self._t = t
        if tt in ENUM_NAME:
            self._tt = tt
        elif tt in NAME_ENUM:
            self._tt = NAME_ENUM[tt]
        else:
            raise ExceptionCpipTokenUnknownType('Unknown token enumeration: %s' % str(tt))

    def __str__(self):
        return 'PpToken(t="%s", tt=%s, line=%s, prev=%s, ?=%s)' % (
         self.t.replace('\n', '\\n'), self.tt, self._canReplace, self._prevWs, self._isCond)

    def __lt__(self, other):
        return self.t < other.t or self.tt < other.tt

    def __eq__(self, other):
        return self.t == other.t and self.tt == other.tt

    def __repr__(self):
        return '"%s"' % self.t

    def isIdentifier(self):
        """Returns True if the token type is 'identifier'."""
        return self._tt == NAME_ENUM['identifier']

    def isWs(self):
        """Returns True if the token type is 'whitespace'."""
        return self._tt == NAME_ENUM['whitespace']

    def replaceNewLine(self):
        """Replace any newline with a single whitespace character in-place.
        
        See:
        :title-reference:`ISO/IEC 9899:1999(E) 6.10-3 and C++ ISO/IEC 14882:1998(E) 16.3-9`
        
        This will raise a :py:class:`ExceptionCpipTokenIllegalOperation` if I am not
        a whitespace token."""
        if self.isWs():
            self._t = self._t.replace('\n', self.SINGLE_SPACE)
        else:
            raise ExceptionCpipTokenIllegalOperation('replaceNewLine() on non-whitespace token.')

    def shrinkWs(self):
        """Replace all whitespace with a single ' '
        
        This will raise a :py:class:`ExceptionCpipTokenIllegalOperation` if I am not
        a whitespace token."""
        if self.isWs():
            self._t = self.SINGLE_SPACE
        else:
            raise ExceptionCpipTokenIllegalOperation('replaceNewLine() on non-whitespace token.')

    def _isOctalInteger(self, value):
        """Returns True is value is an octal digit according to:
        ISO/IEC 14882:1998(E) 2.13.1 Integer literals [lex.icon] - octal-literal.
        Value must have been shorn of integer-suffix
        """
        if len(value) < 2:
            return False
        if value[0] != '0':
            return False
        i = 1
        chars = set('01234567')
        while i < len(value):
            if value[i] not in chars:
                return False
            i += 1

        return True

    def _convertOctalInteger(self, value):
        """If value is an octal integer then this converts it to a string
        suitable for eval().
        If not the value is returned unchanged."""
        assert self._tt == NAME_ENUM['pp-number'] or self._tt == NAME_ENUM['concat']
        assert '.' not in self._t, 'Floating point can not be octal.'
        if sys.version_info.major == 3 and self._isOctalInteger(value):
            value = '0o' + value[1:]
        return value

    def evalConstExpr(self):
        """Returns an string value suitable for eval'ing in a constant expression.
        For numbers this removes such tiresome trivia as 'u', 'L' etc. For others
        it replaces '&&' with 'and' and so on.
        
        See
        :title-reference:`ISO/IEC ISO/IEC 14882:1998(E) 16.1 Conditional inclusion sub-section 4`
        i.e. section 16.1-4
        
        and:
        :title-reference:`ISO/IEC 9899:1999 (E) 6.10.1 Conditional
        inclusion sub-section 3`
        i.e. section 6.10.1-3"""
        if self._tt == NAME_ENUM['pp-number'] or self._tt == NAME_ENUM['concat']:
            s = self._t.lower()
            endI = 0
            if '.' in s:
                for fSuffix in ('fl', 'lf', 'f', 'l'):
                    if s.endswith(fSuffix):
                        endI = -len(fSuffix)
                        break

                if endI != 0:
                    return self._t[:endI]
            else:
                for iSuffix in ('llu', 'ull', 'll', 'ul', 'lu', 'u', 'l'):
                    if s.endswith(iSuffix):
                        endI = -len(iSuffix)
                        break

                if endI != 0:
                    ret_val = self._t[:endI]
                else:
                    ret_val = self._t[:]
                return self._convertOctalInteger(ret_val)
            return self._t
        if self.isWs():
            self.shrinkWs()
            return self._t
        try:
            return self.WORD_REPLACE_MAP[self._t]
        except KeyError:
            pass

        if self.isIdentifier():
            return '0'
        if self._tt == NAME_ENUM['character-literal'] and len(self._t) and self._t[0] in self.CHARACTER_LITERAL_PREFIXES:
            return self._t[1:]
        return self._t

    def merge(self, other):
        """This will merge by appending the other token if they are different token
        types the type becomes 'concat'."""
        self._t += other.t
        if self.tt != other.tt:
            self._tt = NAME_ENUM['concat']

    @property
    def t(self):
        """Returns the token as a string."""
        return self._t

    @property
    def tt(self):
        """Returns the token type as a string."""
        return ENUM_NAME[self._tt]

    @property
    def tokEnumToktype(self):
        """Returns the token and the enumerated token type as a tuple."""
        return (
         self._t, self._tt)

    @property
    def tokToktype(self):
        """Returns the token and the token type (as a string) as a tuple."""
        return (
         self._t, ENUM_NAME[self._tt])

    @property
    def lineNum(self):
        """Returns the line number of the start of the token as an integer."""
        return self._lineNum

    @property
    def colNum(self):
        """Returns the column number of the start of the token as an integer."""
        return self._colNum

    def getReplace(self):
        """Gets the flag that controls whether this can be replaced."""
        return self._canReplace

    def setReplace(self, val):
        """Setter, will raise if I am not an identifier or val is True and
        if I am otherwise not expandable."""
        if not self.isIdentifier():
            raise ExceptionCpipTokenIllegalOperation('setReplace when token type is "%s"' % ENUM_NAME[self._tt])
        if val and not self._canReplace:
            raise ExceptionCpipTokenReopenForExpansion('setReplace(True) when canReplace is already False.')
        self._canReplace = val

    canReplace = property(getReplace, setReplace, None, 'Flag to control whether this token is eligible for replacement')

    def getPrevWs(self):
        """Gets the flag that records prior whitespace."""
        return self._prevWs

    def setPrevWs(self, val):
        """Sets the flag that records prior whitespace."""
        self._prevWs = val

    prevWs = property(getPrevWs, setPrevWs, None, 'Flag to indicate whether this token is preceded by whitespace')

    def getIsReplacement(self):
        """Gets the flag that records that this token is the result of macro replacement"""
        return self._isReplacement

    def setIsReplacement(self, val):
        """Sets the flag that records that this token is the result of macro replacement."""
        self._isReplacement = val

    isReplacement = property(getIsReplacement, setIsReplacement, None, 'Flag that records that this token is the result of macro replacement')

    @property
    def isCond(self):
        """Flag that if True indicates that the token appeared within a
        section that was conditionally compiled. This is False on construction
        and can only be set True by setIsCond()"""
        return self._isCond

    @property
    def isUnCond(self):
        """Flag that if True indicates that the token appeared within a
        section that was un-conditionally compiled. This is the negation of
        isCond."""
        return not self._isCond

    def setIsCond(self):
        """Sets self._isCond to be True."""
        self._isCond = True