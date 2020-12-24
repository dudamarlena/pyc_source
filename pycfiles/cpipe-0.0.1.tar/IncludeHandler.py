# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/core/IncludeHandler.py
# Compiled at: 2017-10-03 13:07:16
__doc__ = 'Provides handlers for #including files.'
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import os, sys, collections, io
from cpip import ExceptionCpip

class ExceptionCppInclude(ExceptionCpip):
    """Simple specialisation of an exception class for the CppInclude."""


FilePathOrigin = collections.namedtuple('FilePathOrigin', 'fileObj filePath currentPlace origin')

class CppIncludeStd(object):
    """Class that applies search rules for #include statements.
    
    Search tactics based on RVCT and Berkeley UNIX search rules: ::
    
        I is the usr includes.
        J is the sys includes.
        Size of I Size of J   #include <...>      #include "..."
        0         0           None                CP
    
        0         >0          SYSTEMINCLUDEdirs   CP, SYSTEMINCLUDEdirs
    
        >0        0           USERINCLUDEdirs     CP, USERINCLUDEdirs
    
        >0        >0          SYSTEMINCLUDEdirs,  CP, USERINCLUDEdirs,
                              USERINCLUDEdirs      SYSTEMINCLUDEdirs

    ISO/IEC 9899:1999 (E) 6.10.2-3 means that a failure of q-char must be
    retried as if it was a h-char. i.e. A failure of a q-char-sequence thus: ``#include "..."``
    
    Is to be retried as if it was written as a h-char-sequence thus: ``#include <...>``
    
    See: _includeQcharseq()
    """
    INCLUDE_ORIGIN_CODES = {None: 'Not found', 
       'comp': 'Compiler specific directories', 
       'sys': 'System include directories', 
       'usr': 'User include directories', 
       'CP': 'Current Place', 
       'TU': 'Translation unit'}

    def __init__(self, theUsrDirs, theSysDirs):
        self._usr = theUsrDirs[:]
        self._sys = theSysDirs[:]
        self._cpStack = []
        self._findLogic = []

    def clearHistory(self):
        """Clears the CP stack. This needed if you use this class as a
        persistent one and it encounters an exception. You need to call this
        function before you can reuse it."""
        self._cpStack = []
        self.clearFindLogic()

    def clearFindLogic(self):
        """Clears the list of find results for a single #include statement."""
        self._findLogic = []

    def cpStackPush(self, theFpo):
        """Appends the CP from the FilePathOrigin to the current place stack.
        This is public so that the PpLexer can use it when processing
        pre-include files that might themselves include other files."""
        if theFpo is None:
            self._cpStack.append(None)
        else:
            self._cpStack.append(theFpo.currentPlace)
        return

    def cpStackPop(self):
        """Pops and returns the CP string off the current place stack.
        This is public so that the PpLexer can use it when processing
        pre-include files that might themselves include other files."""
        return self.endInclude()

    def validateCpStack(self):
        """Tests the coherence of the CP stack. A None can not be followed by
        a non-None."""
        for i in range(len(self._cpStack)):
            if self._cpStack[i] is None and i != len(self._cpStack) - 1:
                return False

        return True

    def canInclude(self):
        """Returns True if the last include succeeded."""
        if not self.validateCpStack():
            return False
        else:
            if len(self._cpStack) == 0:
                return False
            if self._cpStack[(-1)] is None:
                return False
            return True

    @property
    def currentPlace(self):
        """Returns the last current place or None if #include failed."""
        if len(self._cpStack) < 1:
            raise ExceptionCppInclude('currentPlace() on empty stack')
        if not self.validateCpStack():
            raise ExceptionCppInclude('currentPlace() on invalid stack')
        return self._cpStack[(-1)]

    @property
    def cpStack(self):
        """Returns the current stack of current places."""
        return self._cpStack[:]

    @property
    def cpStackSize(self):
        """Returns the size of the current stack of current places."""
        return len(self._cpStack)

    @property
    def findLogic(self):
        """Returns a list of strings that describe _how_ the file was found
        For example:
        
        ``['<foo.h>', 'CP=None', 'sys=None', 'usr=include/foo.h']``
        
        Each string after [0] is of the form: ``key=value`` Where:        
        
        #. key is a key in ``self.INCLUDE_ORIGIN_CODES``
        
        #. = is the ``'='`` character.
        
        #. value is the result, or 'None' if not found.
        
        #. Item [0] is the invocation
        
        #. Item [-1] is the final resolution.
        
        The intermediate ones are various tries in order.
        So:
        
        ``['<foo.h>', 'CP=None', 'sys=None', 'usr=include/foo.h']``
        
        Wwould mean:
        
        * [0]: ``'<foo.h>'`` the include directive was: ``#include <foo.h>``
        
        * [1]: ``'CP=None'`` the Current place was searched and nothing found.
        
        * [2]: ``'sys=None'`` the system include(s) were searched and nothing found.
        
        * [3]: ``'usr=include/foo.h'`` the user include(s) were searched and include/foo.h was found.
        """
        return self._findLogic[:]

    def _includeHcharseq(self, theHstr, include_next=False):
        """Return the file location of a #include <...> as a FilePathOrigin
        object or None on failure.
        If not None this also records the CP for the file."""
        if not self.canInclude():
            raise ExceptionCppInclude('_includeHcharseq() with CP stack: %s' % self._cpStack)
        foundFile = None
        pathS = self._sys[1:] if include_next else self._sys
        for aSearchPath in pathS:
            foundFile = self._searchFile(theHstr, aSearchPath)
            if foundFile is not None:
                foundFile = foundFile._replace(origin='sys')
                self._findLogic.append('sys=%s' % aSearchPath)
                break

        if foundFile is not None:
            self.cpStackPush(foundFile)
        elif not include_next:
            self.cpStackPush(None)
            self._findLogic.append('sys=None')
        return foundFile

    def _includeQcharseq(self, theQstr, include_next=False):
        """Return the file location of a #include "..." as a FilePathOrigin
        object or None on failure.
        If not None this also records the CP for the file."""
        if not self.canInclude():
            raise ExceptionCppInclude('_includeQcharseq() with CP stack: %s' % self._cpStack)
        if include_next:
            foundFile = None
        else:
            foundFile = self._searchFile(theQstr, self._cpStack[(-1)])
        if foundFile is not None:
            foundFile = foundFile._replace(origin='CP')
            self._findLogic.append('CP=%s' % self._cpStack[(-1)])
        else:
            self._findLogic.append('CP=None')
            pathS = self._usr[1:] if include_next else self._usr
            for aSearchPath in pathS:
                foundFile = self._searchFile(theQstr, aSearchPath)
                if foundFile is not None:
                    foundFile = foundFile._replace(origin='usr')
                    self._findLogic.append('usr=%s' % aSearchPath)
                    break

        if foundFile is not None:
            self.cpStackPush(foundFile)
        elif not include_next:
            self._findLogic.append('usr=None')
            foundFile = self._includeHcharseq(theQstr)
        return foundFile

    def includeHeaderName(self, theStr):
        """Return the file location of a #include header-name where the
        header-name is a pp-token either a <h-char-sequence> or a
        "q-char-sequence" (including delimiters).
        If not None return value this also records the CP for the file."""
        self._findLogic = [
         theStr]
        if theStr.startswith('<') and theStr.endswith('>'):
            return self._includeHcharseq(theStr[1:-1])
        if theStr.startswith('"') and theStr.endswith('"'):
            return self._includeQcharseq(theStr[1:-1])
        raise ExceptionCppInclude('includeHeaderName() unrecognised string %s with CP stack: %s' % (
         theStr, self._cpStack))

    def includeNextHeaderName(self, theStr):
        """Return the file location of a #include_next header-name where the
        header-name is a pp-token either a <h-char-sequence> or a
        "q-char-sequence" (including delimiters).
        
        This is a GCC extension, see: https://gcc.gnu.org/onlinedocs/cpp/Wrapper-Headers.html
        
        This never records the CP for the found file (if any)."""
        self._findLogic = [
         theStr]
        if theStr.startswith('<') and theStr.endswith('>'):
            return self._includeHcharseq(theStr[1:-1], include_next=True)
        if theStr.startswith('"') and theStr.endswith('"'):
            return self._includeQcharseq(theStr[1:-1], include_next=True)
        raise ExceptionCppInclude('includeNextHeaderName() unrecognised string %s with CP stack: %s' % (
         theStr, self._cpStack))

    def endInclude(self):
        """Notify end of #include'd file. This pops the CP stack."""
        if len(self._cpStack) == 0:
            raise ExceptionCppInclude('endInclude() on empty stack.')
        self._cpStack.pop()

    def finalise(self):
        """Finalise at the end of the translation unit.
        Might raise a ExceptionCppInclude."""
        if len(self._cpStack) != 0:
            raise ExceptionCppInclude('finalise() with CP stack: %s' % self._cpStack)

    def _currentPlaceFromFile(self, theFilePath):
        """Helper method that returns the enclosing directory of the file as
        the current place."""
        return os.path.dirname(theFilePath)

    def _fixDirsep(self, theCharSeq):
        """Returns a character sequence with the allowable directory seperator
        repalced by that the OS will recognise."""
        return theCharSeq.replace('/', os.sep)

    def _searchFile(self, theCharSeq, theSearchPath):
        """Given an HcharSeq/Qcharseq and a searchpath this should return a
        class FilePathOrigin or None"""
        raise NotImplementedError('_searchFile() not implemented.')

    def initialTu(self, theTuIdentifier):
        """Given an Translation Unit Identifier this should return a
        class FilePathOrigin or None for the initial translation unit.
        As a precaution this should include code to check that the stack
        of current places is empty. For example: ::
        
            if len(self._cpStack) != 0:
                raise ExceptionCppInclude('setTu() with CP stack: %s' % self._cpStack)
        """
        raise NotImplementedError('initialTu() not implemented.')


class CppIncludeStdOs(CppIncludeStd):
    """This implements _searchFile() based on an OS file system call."""

    def _searchFile(self, theCharSeq, theSearchPath):
        """Given an HcharSeq/Qcharseq and a searchpath this tries the
        file system for the file and returns a FilePathOrigin object or None
        on failure."""
        myPath = os.path.join(theSearchPath, self._fixDirsep(theCharSeq))
        try:
            return FilePathOrigin(open(myPath), myPath, self._currentPlaceFromFile(myPath), None)
        except Exception as _err:
            pass

        return

    def initialTu(self, theTuPath):
        """Given an path as a string this returns the
        class FilePathOrigin or None for the initial translation unit"""
        if len(self._cpStack) != 0:
            raise ExceptionCppInclude('setTu() with CP stack: %s' % self._cpStack)
        retVal = None
        try:
            retVal = FilePathOrigin(open(theTuPath), theTuPath, self._currentPlaceFromFile(theTuPath), 'TU')
            self.cpStackPush(retVal)
        except Exception as _err:
            pass

        return retVal


class CppIncludeStdin(CppIncludeStdOs):
    """This reads stdin for the ITU but delegates _searchFile() to the OS file system call."""

    def initialTu(self, theTuPath):
        """Given an path as a string this returns the
        class FilePathOrigin or None for the initial translation unit"""
        if len(self._cpStack) != 0:
            raise ExceptionCppInclude('setTu() with CP stack: %s' % self._cpStack)
        retVal = None
        try:
            retVal = FilePathOrigin(sys.stdin, theTuPath, self._currentPlaceFromFile(theTuPath), 'stdin')
            self.cpStackPush(retVal)
        except Exception as _err:
            pass

        return retVal


class CppIncludeStringIO(CppIncludeStd):
    """This implements _searchFile() based on a lookup of stings that
    returns StringIO file-like object."""

    def __init__(self, theUsrDirs, theSysDirs, theInitialTuContent, theFilePathToContent):
        """Acts like a IncludeHandler but looks up in theFilePathToContent
        map that is a {path_string : content_string, ...}.
        This will be used to simulate resolving a #include statement."""
        super(CppIncludeStringIO, self).__init__(theUsrDirs, theSysDirs)
        if sys.version_info.major == 2:
            self._initialTuContent = theInitialTuContent.decode('ascii')
            self._filePathToContent = {k:v.decode('ascii') for k, v in theFilePathToContent.items()}
        else:
            self._initialTuContent = theInitialTuContent
            self._filePathToContent = theFilePathToContent

    def _searchFile(self, theCharSeq, theSearchPath):
        """Given an HcharSeq/Qcharseq and a searchpath this tries the
        file system for the file."""
        myPath = os.path.join(theSearchPath, self._fixDirsep(theCharSeq))
        try:
            myContent = self._filePathToContent[myPath]
            return FilePathOrigin(io.StringIO(myContent), myPath, self._currentPlaceFromFile(myPath), None)
        except KeyError:
            pass

        return

    def initialTu(self, theTuIdentifier):
        """Given an path as a string this returns the
        class FilePathOrigin or None for the initial translation unit"""
        if len(self._cpStack) != 0:
            raise ExceptionCppInclude('setTu() with CP stack: %s' % self._cpStack)
        retVal = FilePathOrigin(io.StringIO(self._initialTuContent), theTuIdentifier, self._currentPlaceFromFile(theTuIdentifier), 'TU')
        self.cpStackPush(retVal)
        return retVal