# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/core/PragmaHandler.py
# Compiled at: 2017-10-03 13:07:16
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
from cpip import ExceptionCpip

class ExceptionPragmaHandler(ExceptionCpip):
    """Simple specialisation of an exception class for the PragmaHandler.
    If raised this will cause the PpLexer to register undefined behaviour."""


class ExceptionPragmaHandlerStopParsing(ExceptionPragmaHandler):
    """Exception class for the PragmaHandler to stop parsing token stream."""


class PragmaHandlerABC(object):
    """Abstract base class for a pragma handler."""

    @property
    def replaceTokens(self):
        """An boolean attribute that says whether the supplied tokens should
        be macro replaced before being passed to self."""
        raise NotImplementedError('replaceTokens attribute not implemented.')

    def pragma(self, theTokS):
        """Takes a list of PpTokens, processes then and should return a newline
        terminated string that will be preprocessed in the current environment."""
        raise NotImplementedError('pragma() not implemented.')

    @property
    def isLiteral(self):
        """Treat the result of pragma() literally so no further processing required."""
        return False


class PragmaHandlerNull(PragmaHandlerABC):
    """A pragma handler that does nothing."""

    @property
    def replaceTokens(self):
        """Tokens do not require macro replacement."""
        return False

    def pragma(self, theTokS):
        """Consume and return."""
        return ''


class PragmaHandlerSTDC(PragmaHandlerABC):
    """Base class for a pragma handler that implements ISO/IEC 9899:1999 (E)
    6.10.5 Error directive para. 2."""
    STDC = 'STDC'
    DIRECTIVES = ('FP_CONTRACT', 'FENV_ACCESS', 'CX_LIMITED_RANGE')
    ON_OFF_SWITCH_STATES = ('ON', 'OFF', 'DEFAULT')

    @property
    def replaceTokens(self):
        """STDC lines do not require macro replacement."""
        return False

    def _consumeWs(self, theTokS, i):
        retVal = 0
        while theTokS[i].isWs():
            i += 1
            retVal += 1

        return retVal

    def pragma(self, theTokS):
        """Inject a macro declaration into the environment.
        
        See ISO/IEC 9899:1999 (E) 6.10.5 Error directive para. 2."""
        myTokS = []
        try:
            i = self._consumeWs(theTokS, 0)
            if theTokS[i].t == self.STDC:
                i += 1
            else:
                raise ExceptionPragmaHandlerStopParsing()
            i += self._consumeWs(theTokS, i)
            if theTokS[i].t in self.DIRECTIVES:
                myTokS.append(theTokS[i].t)
                i += 1
            else:
                raise ExceptionPragmaHandlerStopParsing()
            i += self._consumeWs(theTokS, i)
            if theTokS[i].t in self.ON_OFF_SWITCH_STATES:
                myTokS.append(' ')
                myTokS.append(theTokS[i].t)
                i += 1
            else:
                raise ExceptionPragmaHandlerStopParsing()
        except (IndexError, ExceptionPragmaHandlerStopParsing):
            myTokS = []

        if len(myTokS) > 0:
            return '#define %s\n' % ('').join([ s for s in myTokS ])
        return ''


class PragmaHandlerEcho(PragmaHandlerABC):
    """A pragma handler that retains the #pragma line verbatim."""

    @property
    def isLiteral(self):
        """This class is just going to echo the line back complete with
        the '#pragma' prefix. If the PpLexer re-interpreted this it would
        be an infinite loop."""
        return True

    @property
    def replaceTokens(self):
        """Tokens do not require macro replacement."""
        return False

    def pragma(self, theTokS):
        """Consume and return."""
        return '#pragma%s' % ('').join([ t.t for t in theTokS ])