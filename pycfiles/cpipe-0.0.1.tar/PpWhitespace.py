# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/core/PpWhitespace.py
# Compiled at: 2017-10-03 13:07:16
__doc__ = 'Understands whitespacey things about source code character streams.\n'
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
LEX_WHITESPACE = set('\t\x0b\x0c\n ')
LEN_WHITESPACE_CHARACTER_SET = 5
LEX_NEWLINE = '\n'
DEFINE_WHITESPACE = set('\n\t ')

class PpWhitespace(object):
    """A class that does whitespacey type things in accordance with
    ISO/IEC 9899:1999(E) Section 6 and ISO/IEC 14882:1998(E)."""

    def sliceWhitespace(self, theBuf, theOfs=0):
        """Returns the length of whitespace characters that are in theBuf from
        position theOfs."""
        i = theOfs
        try:
            while theBuf[i] in LEX_WHITESPACE:
                i += 1

        except IndexError:
            pass

        return i - theOfs

    def sliceNonWhitespace(self, theBuf, theOfs=0):
        """Returns the length of non-whitespace characters that are in
        theBuf from position theOfs."""
        i = theOfs
        try:
            while theBuf[i] not in LEX_WHITESPACE:
                i += 1

        except IndexError:
            pass

        return i - theOfs

    def hasLeadingWhitespace(self, theCharS):
        """Returns True if any leading whitespace, False if zero length or
        starts with non-whitespace."""
        return len(theCharS) > 0 and theCharS[0] in LEX_WHITESPACE

    def isAllWhitespace(self, theCharS):
        """Returns True if the supplied string is all whitespace."""
        return len(theCharS) > 0 and self.sliceWhitespace(theCharS) == len(theCharS)

    def isBreakingWhitespace(self, theCharS):
        """Returns True if whitespace leads theChars and that whitespace
        contains a newline."""
        i = 0
        while i < len(theCharS) and theCharS[i] in LEX_WHITESPACE:
            if theCharS[i] == LEX_NEWLINE:
                return True
            i += 1

        return False

    def isAllMacroWhitespace(self, theCharS):
        """"Return True if theCharS is zero length or only has allowable
        whitespace for preprocesing macros.
        
        ISO/IEC 14882:1998(E) 16-2 only ' ' and '       ' as whitespace."""
        for c in theCharS:
            if c not in DEFINE_WHITESPACE:
                return False

        return True

    def preceedsNewline(self, theCharS):
        """Returns True if theChars ends with a newline. i.e. this immediately
        precedes a new line."""
        return theCharS.endswith(LEX_NEWLINE)