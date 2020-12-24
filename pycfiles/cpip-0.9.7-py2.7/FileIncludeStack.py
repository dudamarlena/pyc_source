# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/core/FileIncludeStack.py
# Compiled at: 2017-10-03 13:07:16
"""This module represents a stack of file includes as used by the
:py:class:`.PpLexer.PpLexer`
"""
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import logging
from cpip import ExceptionCpip
from cpip.core import PpTokeniser
from cpip.core import PpTokenCount
from cpip.core import FileIncludeGraph
from cpip.util import CommonPrefix

class ExceptionFileIncludeStack(ExceptionCpip):
    """Exception for FileIncludeStack object."""
    pass


class FileInclude(object):
    """Represents a single TU fragment with a PpTokeniser and a token counter.
    
    *theFpo*
        A FilePathOrigin object that identifies the file.
        
    *theDiag*
        A CppDiagnostic object to give to the PpTokeniser.
    """

    def __init__(self, theFpo, theDiag):
        self.fileName = theFpo.filePath
        self.ppt = PpTokeniser.PpTokeniser(theFileObj=theFpo.fileObj, theFileId=theFpo.filePath, theDiagnostic=theDiag)
        self.tokenCounter = PpTokenCount.PpTokenCount()

    def tokenCounterAdd(self, theC):
        """Add a token counter to my token counter (used when a macro is
        declared)."""
        self.tokenCounter += theC

    def tokenCountInc(self, tok, isUnCond, num=1):
        """Increment the token counter."""
        self.tokenCounter.inc(tok, isUnCond, num)


class FileIncludeStack(object):
    """This maintains information about the stack of file includes.
    This holds several stacks (or representations of them):
    
    *self._ppts*
        A stack of :py:class:`.PpTokeniser.PpTokeniser` objects.
        
    *self._figr*
        A :py:class:`.FileIncludeGraph.FileIncludeGraphRoot` for tracking the ``#include`` graph.
        
    *self._fns*
        A stack of file IDs as strings (e.g. the file path).
        
    *self._tcs*
        A :py:class:`.PpTokenCount.PpTokenCountStack` object for counting tokens.
    """

    def __init__(self, theDiagnostic):
        """Constructor, takes a CppDiagnostic object to give to the PpTokeniser."""
        self._diagnostic = theDiagnostic
        self._fincS = []
        self._figr = FileIncludeGraph.FileIncludeGraphRoot()

    @property
    def depth(self):
        """Returns the current include depth as an integer."""
        return len(self._fincS)

    @property
    def currentFile(self):
        """Returns the file ID from the top of the stack."""
        if self.depth < 1:
            raise ExceptionFileIncludeStack('FileIncludeStack.currentFile on zero length stack.')
        return self._fincS[(-1)].fileName

    @property
    def fileStack(self):
        """Returns a copy of the stack of file IDs."""
        return [ fi.fileName for fi in self._fincS ]

    @property
    def ppt(self):
        """Returns the PpTokeniser from the top of the stack."""
        if self.depth < 1:
            raise ExceptionFileIncludeStack('FileIncludeStack.ppt on zero length stack.')
        return self._fincS[(-1)].ppt

    @property
    def fileIncludeGraphRoot(self):
        """The :py:class:`.FileIncludeGraph.FileIncludeGraphRoot` object."""
        return self._figr

    @property
    def fileLineCol(self):
        """Return an instance of FileLineCol from the current physical line column."""
        return self.ppt.fileLineCol

    def finalise(self):
        """Finalisation, may raise an ExceptionFileIncludeStack."""
        if self.depth != 0:
            raise ExceptionFileIncludeStack('FileIncludeStack.finalise(): Non-zero length stack: %s' % str(self.fileStack))

    def _printFileList(self, thePref, theL):
        l = CommonPrefix.lenCommonPrefix(theL)
        print (thePref, [ f[l + 1:] for f in theL ])

    def includeStart(self, theFpo, theLineNum, isUncond, condStr, incLogic):
        """Start an ``#include`` file.
        
        *theFpo*
            A :py:class:`.FileLocation.FilePathOrigin` object that identifies the file.
            
        *theLineNum*
            The integer line number of the file that includes (None if Root).
        
        *isUncond*
            A boolean that is the conditional compilation state.
            
        *condStr*
            A string of the conditional compilation stack.
            
        *incLogic*
            A string that describes the find include logic.
        """
        logging.debug('FileIncludeStack.includeStart(): %s line=%d', theFpo.filePath, theLineNum)
        assert len(self._fincS) == 0 and theLineNum is None or theLineNum == self._fincS[(-1)].ppt.pLineCol[0]
        self._fincS.append(FileInclude(theFpo, self._diagnostic))
        if self.depth == 1:
            assert theLineNum is None
            self._figr.addGraph(FileIncludeGraph.FileIncludeGraph(theFpo.filePath, True, '', ''))
        else:
            assert self._figr.numTrees() > 0
            myFileStack = self.fileStack
            self._figr.graph.addBranch(myFileStack[:-1], theLineNum - 1, myFileStack[(-1)], isUncond, condStr, incLogic)
        return

    def includeFinish(self):
        """End an ``#include`` file, returns the file ID that has been finished."""
        if self.depth < 1:
            raise ExceptionFileIncludeStack('FileIncludeStack.includeFinish() on zero length stack.')
        myFileStack = [ fi.fileName for fi in self._fincS ]
        logging.debug('FileIncludeStack.includeFinish(): %s', self._fincS[(-1)].fileName)
        myFinc = self._fincS.pop()
        self._figr.graph.retLatestNode(myFileStack).setTokenCounter(myFinc.tokenCounter)
        if self.depth > 0:
            logging.debug('FileIncludeStack.includeFinish(): passing control back to %s', self._fincS[(-1)].fileName)
        else:
            logging.debug('FileIncludeStack.includeFinish(): passing control back to NONE')
        return myFinc.fileName

    def tokenCounter(self):
        """Returns the Token Counter object at the tip of the stack."""
        if self.depth < 1:
            raise ExceptionFileIncludeStack('FileIncludeStack.tokenCounter on zero length stack.')
        return self._fincS[(-1)].tokenCounter

    def tokenCounterAdd(self, theC):
        """Add a token counter to my token counter (used when a macro is
        declared)."""
        if self.depth < 1:
            raise ExceptionFileIncludeStack('FileIncludeStack.tokenCounterAdd() on zero length stack.')
        self._fincS[(-1)].tokenCounterAdd(theC)

    def tokenCountInc(self, tok, isUnCond, num=1):
        """Increment the token counter."""
        self._fincS[(-1)].tokenCountInc(tok, isUnCond, num)