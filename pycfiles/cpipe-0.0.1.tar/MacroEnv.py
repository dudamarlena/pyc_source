# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/core/MacroEnv.py
# Compiled at: 2017-10-03 13:07:16
__doc__ = "This an environment of macro declarations\n\nIt implements :title-reference:`ISO/IEC 9899:1999(E) section 6 (aka 'C')`\nand :title-reference:`ISO/IEC 14882:1998(E) section 16 (aka 'C++')`\n"
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import io, logging, traceback
from cpip import ExceptionCpip
from cpip.core import PpDefine
from cpip.core import PpToken
from cpip.core import PpTokeniser
from cpip.core import PpWhitespace
from cpip.util.ListGen import ListAsGenerator
from cpip.util.Tree import DuplexAdjacencyList

class ExceptionMacroEnv(ExceptionCpip):
    """Exception when handling MacroEnv object."""


class ExceptionMacroEnvInvalidRedefinition(ExceptionMacroEnv):
    """Exception for a invalid redefinition of a macro.
    NOTE: Under C rules (C Rationale 6.10.3) callers should merely issue a
    suitable diagnostic."""


class ExceptionMacroReplacementInit(ExceptionMacroEnv):
    """Exception in the constructor."""


class ExceptionMacroReplacementPredefinedRedefintion(ExceptionMacroEnv):
    """Exception for a redefinition of a macro id that is predefined."""


class ExceptionMacroEnvNoMacroDefined(ExceptionMacroEnv):
    """Exception when trying to access a PpDefine that is not currently defined."""


class ExceptionMacroIndexError(ExceptionMacroEnv):
    """Exception when an access to a PpDefine that generates a IndexError."""


KEYWORD_DEFINED = 'defined'

class MacroEnv(object):
    r"""Represents a set of #define directives that represent a macro processing
    environment. This provides support for #define and #undef directives.
    It also provides support for macro replacement see:
    :title-reference:`ISO/IEC 9899:1999 (E) 6.10.3 Macro replacement.`
    
    *enableTrace*
        Allows calls to ``_debugTokenStream()`` that may or may not
        produce log output (depending on logging level).
        If True this makes this code run slower, typically 3x slower
        
    *stdPredefMacros*
        If present should be a dictionary of:
        ``{identifier : replacement_string_\n_terminated, ...}``
        For example: ::
        
            {
                '__DATE__' : 'First of June\n',
                '__TIME__' : 'Just before lunchtime.\n',
            }
            
        Each identifier must be in ``STD_PREDEFINED_NAMES``
    """
    NAMES_NO_REDEFINITION = set((
     KEYWORD_DEFINED,))
    STD_PREDEFINED_NEVER_REDEFINED = set([
     '__LINE__', '__FILE__', '__DATE__', '__TIME__']) | NAMES_NO_REDEFINITION

    def __init__(self, enableTrace=False, stdPredefMacros=None):
        """Constructor.
        enableTrace allows calls to _debugTokenStream() that may or may not
        produce log output (depending on logging level).
        stdPredefMacros, if present should be a dictionary of:
        {identifier : replacement_string_
_terminated, ...}
        These identifiers are not permitted to be redefined.
        This also increments the count is the number of times that the
        identifier has been referenced in the lifetime of me.
        A 'reference' is defined as: replacement or if defined.
        So:
        - Count set to zero on self.define()
        - Increment on:
            self.isDefined()
            self.defined()
            self._expand()
        """
        self._enableTrace = enableTrace
        self._wsHandler = PpWhitespace.PpWhitespace()
        self._stdPredefMacros = stdPredefMacros
        self._reset()

    def _reset(self):
        """Initialises the dynamic values."""
        self._defineMap = {}
        self._undefS = []
        self._expandedSet = set()
        self.debugMarker = None
        self._noDefineIdentifiers = set(self.STD_PREDEFINED_NEVER_REDEFINED)
        if self._stdPredefMacros is not None:
            for k in self._stdPredefMacros.keys():
                if k in self.NAMES_NO_REDEFINITION:
                    raise ExceptionMacroReplacementInit('"%s" is not a predefined identifier' % k)

            self._noDefineIdentifiers |= set(self._stdPredefMacros.keys())
            for k in self._stdPredefMacros.keys():
                self.__setString('%s %s' % (k, self._stdPredefMacros[k]))

        self._ifDefAbsentMacros = {}
        return

    def clear(self):
        """Clears the macro environment."""
        self._reset()

    def __str__(self):
        retStr = []
        for k in sorted(self._defineMap.keys()):
            retStr.append('%s' % str(self._defineMap[k]))

        return ('\n').join(retStr)

    def __len__(self):
        return len(self._defineMap)

    def _assertDefineMapIntegrity(self):
        """Returns True if dynamic tests on self._defineMap and
        self._expandedSet pass. i.e. every entry in self._expandedSet
        must be in self._defineMap.keys()."""
        return self._expandedSet.issubset(set(self._defineMap.keys()))

    def _debugTokenStream(self, thePrefix, theArg=''):
        """Writes to logging.debug() an interpretation of the token stream
        provided by theList. It will be preceded by the debugMarker value
        (if set) and that will always be cleared."""
        assert self._enableTrace
        if type(theArg) == list:
            debugStr = '[%d] %s' % (
             len(theArg), PpToken.tokensStr(theArg, shortForm=True))
        elif type(theArg) == str:
            debugStr = theArg
        elif theArg is None:
            debugStr = 'None'
        else:
            raise ExceptionMacroEnv('Unknown argument type %s, %s passed to _debugTokenStream()' % (
             type(theArg), theArg))
        if self.debugMarker is not None:
            logging.debug(self.debugMarker)
        self.debugMarker = None
        stackPrefix = ' ' * len(traceback.extract_stack())
        logging.debug('[%2d]%s%s: %s' % (
         len(stackPrefix), stackPrefix, thePrefix, debugStr))
        return

    def define(self, theGen, theFile, theLine):
        """Defines a macro. theGen should be in the state immediately after the
        ``#define`` i.e. this will consume leading whitespace and the trailing
        newline.
        
        Will raise a :py:class:`ExceptionMacroEnvInvalidRedefinition` if the redefinition
        is not valid. May raise a :py:class:`.PpDefine.ExceptionCpipDefineInit` (or sub class) on failure.
        
        On success it returns the identifier of the macro as a string..
        The insertion is stable i.e. a valid re-definition does not replace
        the existing definition so that the existing state of the macro
        definition (file, line, reference count etc. are preserved."""
        try:
            myDef = PpDefine.PpDefine(theGen, theFile, theLine)
        except PpDefine.ExceptionCpipDefineInit as err:
            raise ExceptionMacroReplacementInit(str(err))

        if myDef.identifier in self._noDefineIdentifiers:
            raise ExceptionMacroReplacementPredefinedRedefintion('Attempting to redefine predefined identifier "%s"' % myDef.identifier)
        return self.__define(myDef)

    def __define(self, ppD):
        """Takes a PpDefine.PpDefine object and adds it to
        the map of objects. Does NOT check if it is a redefinition of
        a predefined macro. Does check if it is a valid redefinition.
        On success it returns the identifier of the macro.
        The insertion is stable i.e. a valid re-definition does not replace
        the existing definition so that the definition file, line and reference
        count are preserved."""
        if ppD.identifier in self._defineMap:
            if not ppD.isValidRefefinition(self._defineMap[ppD.identifier]):
                raise ExceptionMacroEnvInvalidRedefinition('Ignoring invalid redefinition of "%s" as "%s"' % (
                 self._defineMap[ppD.identifier], ppD))
        else:
            self._defineMap[ppD.identifier] = ppD
        return ppD.identifier

    def undef(self, theGen, theFile, theLine):
        """Removes a definition from the map and adds the PpDefine to
        self._undefS. It returns None.
        If no definition exists this has no side-effects on the internal
        representation."""
        myDef = PpDefine.PpDefine(theGen, '', 1)
        try:
            myMacro = self._defineMap.pop(myDef.identifier)
            myMacro.undef(theFile, theLine)
            self._undefS.append(myMacro)
        except KeyError:
            pass

    def set__LINE__(self, theStr):
        """This sets the ``__LINE__`` macro directly."""
        self.__setString('__LINE__ %s\n' % theStr)

    def set__FILE__(self, theStr):
        """This sets the ``__FILE__`` macro directly."""
        self.__setString('__FILE__ %s\n' % theStr)

    def __setString(self, theStr):
        """Takes a string 'identifier replacement
' and sets the macro map.
        This uses __defien(...) so only a redefinition exception is raised."""
        myCpp = PpTokeniser.PpTokeniser(theFileObj=io.StringIO(theStr))
        myGen = myCpp.next()
        myDef = PpDefine.PpDefine(myGen, '', 1)
        self.__define(myDef)

    def isDefined(self, theTtt, theFileLineCol=None):
        """Returns True theTtt is an identifier that is currently defined,
        False otherwise. If True this increments the macro reference.
        
        *theFileLineCol*
            Is a :py:class:`.FileLocation.FileLineCol object`.
        
        See: :title-reference:`ISO/IEC 9899:1999 (E) 6.10.1.`
        """
        if theTtt.isIdentifier():
            try:
                self._defineMap[theTtt.t].incRefCount(theFileLineCol)
                return True
            except KeyError:
                try:
                    self._ifDefAbsentMacros[theTtt.t].append(theFileLineCol)
                except KeyError:
                    self._ifDefAbsentMacros[theTtt.t] = [
                     theFileLineCol]

        return False

    def defined(self, theTtt, flagInvert, theFileLineCol=None):
        """If the PpToken theTtt is an identifier that is currently defined
        then this returns 1 as a PpToken, 0 as a PpToken otherwise.
        If the macro exists in the environment its reference count is
        incremented.
        
        *theFileLineCol*
            Is a :py:class:`.FileLocation.FileLineCol object`.
        
        See: :title-reference:`ISO/IEC 9899:1999 (E) 6.10.1.`
        """
        if not theTtt.isIdentifier():
            raise ExceptionMacroEnv('defined() on non-identifier but: %s' % theTtt)
        try:
            self._defineMap[theTtt.t].incRefCount(theFileLineCol)
            if flagInvert:
                return PpToken.PpToken('0', 'pp-number')
            return PpToken.PpToken('1', 'pp-number')
        except KeyError:
            try:
                self._ifDefAbsentMacros[theTtt.t].append(theFileLineCol)
            except KeyError:
                self._ifDefAbsentMacros[theTtt.t] = [
                 theFileLineCol]

        if flagInvert:
            return PpToken.PpToken('1', 'pp-number')
        return PpToken.PpToken('0', 'pp-number')

    def mightReplace(self, theTtt):
        """Returns True if theTok might be able to be expanded.
        'Might' is not 'can' or 'will' because of this: ::
        
            #define FUNC(a,b) a-b
            FUNC FUNC(45,3)
        
        Becomes: ::
            
            FUNC 45 -3
        
        Thus ``mightReplace('FUNC', ...)`` is True in both cases but actual
        replacement only occurs once for the second ``FUNC``."""
        assert self._assertDefineMapIntegrity()
        return theTtt.canReplace and theTtt.t in self._defineMap

    def _hasExpanded(self, theTtt):
        """Returns True if theTok represents a macro name that has already
        been expanded."""
        assert self._assertDefineMapIntegrity()
        return theTtt.t in self._expandedSet

    def replace(self, theTtt, theGen, theFileLineCol=None):
        """Given a PpToken this returns the replacement as a list of
        ``[class PpToken, ...]`` that is the result of the substitution of
        macro definitions.
        
        *theGen*
            Is a generator that might be used in the case of function-like
            macros to consume their argument lists.
        
        *theFileLineCol*
            Is a :py:class:`.FileLocation.FileLineCol object`.
        """
        assert len(self._expandedSet) == 0
        try:
            retVal = self._expand(theTtt, theGen, theFileLineCol)
        finally:
            self._expandedSet = set()

        assert len(self._expandedSet) == 0
        return retVal

    def _expand(self, theTtt, theGen, theFileLineCol):
        """Recursive call to expand macro symbols.
        
        *theFileLineCol*
            Is a :py:class:`.FileLocation.FileLineCol object`.
        """
        if self._enableTrace:
            self._debugTokenStream('_expand("%s")' % theTtt)
        if not self.mightReplace(theTtt):
            if self._enableTrace:
                self._debugTokenStream('_expand("%s") nothing to do' % theTtt)
            return [theTtt]
        else:
            if self._hasExpanded(theTtt):
                if self._enableTrace:
                    self._debugTokenStream('_expand("%s") already expanded' % theTtt)
                theTtt.canReplace = False
                return [
                 theTtt]
            if self._enableTrace:
                self._debugTokenStream('_expand() examining "%s"' % theTtt.t)
            hasReplaced = False
            myMacro = self._defineMap[theTtt.t]
            if myMacro.isObjectTypeMacro:
                rTokS = myMacro.replaceObjectStyleMacro()
                if self._enableTrace:
                    self._debugTokenStream('_expand("%s") object replacement' % theTtt, rTokS)
                hasReplaced = True
            else:
                myPreamble = myMacro.consumeFunctionPreamble(theGen)
                if self._enableTrace:
                    self._debugTokenStream('_expand() func preamble', myPreamble)
                if myPreamble is not None:
                    rTokS = [
                     theTtt] + myPreamble
                    hasReplaced = False
                    if self._enableTrace:
                        self._debugTokenStream('_expand("%s") function preamble failed' % theTtt, rTokS)
                else:
                    if self._enableTrace:
                        self._debugTokenStream('_expand() extracting arguments')
                    myArgS = myMacro.retArgumentListTokens(theGen)
                    if self._enableTrace:
                        self._debugTokenStream('_expand() arguments %s' % myArgS)
                    if myMacro.expandArguments:
                        myExpandedArgS = []
                        for argTokS in myArgS:
                            if self._enableTrace:
                                self._debugTokenStream('_expand("%s") function argument was' % theTtt, argTokS)
                            if argTokS != myMacro.PLACEMARKER:
                                myGen = next(ListAsGenerator(argTokS, None))
                                myExpArgTokS = []
                                while 1:
                                    try:
                                        myExpArgTokS += self._expand(next(myGen), myGen, theFileLineCol)
                                    except StopIteration:
                                        break

                                if self._enableTrace:
                                    self._debugTokenStream('_expand("%s") function argument now' % theTtt, myExpArgTokS)
                                myExpandedArgS.append(myExpArgTokS)
                            else:
                                myExpandedArgS.append(myMacro.PLACEMARKER)

                        rTokS = myMacro.replaceArgumentList(myExpandedArgS)
                    else:
                        rTokS = myMacro.replaceArgumentList(myArgS)
                    if self._enableTrace:
                        self._debugTokenStream('_expand("%s") function now' % theTtt, rTokS)
                    hasReplaced = True
                if hasReplaced:
                    myMacro.incRefCount(theFileLineCol)
                else:
                    if self._enableTrace:
                        self._debugTokenStream('_expand("%s") not hasReplaced.' % theTtt, rTokS)
                    return rTokS
                reexTokS = []
                if self._enableTrace:
                    self._debugTokenStream('_expand("%s") reexamine' % theTtt, rTokS)
                self._expandedSet.add(theTtt.t)
                myListAsGen = ListAsGenerator(rTokS, theGen)
                myGen = next(myListAsGen)
                while not myListAsGen.listIsEmpty:
                    reexTokS += self._expand(next(myGen), myGen, theFileLineCol)

            self._expandedSet.remove(theTtt.t)
            if self._enableTrace:
                self._debugTokenStream('_expand("%s") reexamined' % theTtt, reexTokS)
            return reexTokS

    def genMacrosOutOfScope(self, theIdent=None):
        """Generates PpDefine objects encountered during my existence but then
        undefined in the order of un-definition.
        
        If theIdent is not None then only that named macros will be yielded."""
        for aM in self._undefS:
            if theIdent is None or aM.identifier == theIdent:
                yield aM

        return

    def genMacrosInScope(self, theIdent=None):
        """Generates PpDefine objects encountered during my existence and still
        in scope i.e. not yet un-defined.
        
        If theIdent is not None then only that named macros will be yielded."""
        if theIdent is None:
            for anId in sorted(self._defineMap.keys()):
                yield self._defineMap[anId]

        else:
            try:
                yield self._defineMap[theIdent]
            except KeyError:
                pass

        return

    def genMacros(self, theIdentifier=None):
        """Generates PpDefine objects encountered during my existence.
        Macros that have been undefined will be generated first in order of
        un-definition followed by the currently defined macros in identifier
        order.
        
        Macros that have been #undef'd will have the attribute 
        isCurrentlyDefined as False."""
        for aM in self.genMacrosOutOfScope(theIdentifier):
            yield aM

        for aM in self.genMacrosInScope(theIdentifier):
            yield aM

    def hasMacro(self, theIdentifier):
        """Returns True if the environment has the macro.
        
        NOTE: This does _not_ increment the reference count so should not be
        used when processing #ifdef ..., #if defined ... or #if !defined ...
        for those use isDefined() and defined() instead."""
        return theIdentifier in self._defineMap

    def macros(self):
        """Returns and unsorted list of strings of current macro identifiers."""
        return list(self._defineMap.keys())

    def macro(self, theIdentifier):
        """Returns the macro identified by the identifier.
        Will raise a :py:class:`ExceptionMacroEnvNoMacroDefined` is undefined."""
        try:
            return self._defineMap[theIdentifier]
        except KeyError:
            raise ExceptionMacroEnvNoMacroDefined('Macro %s is not currently defined' % theIdentifier)

    def allStaticMacroDependencies(self):
        """Returns a DuplexAdjacencyList() of macro dependencies for the
        Macro environment. All objects in the :py:class:`cpip.util.Tree.DuplexAdjacencyList` are macro
        identifiers as strings.
        
        A :py:class:`cpip.util.Tree.DuplexAdjacencyList` can be converted to a
        :py:class:`cpip.util.Tree.Tree` and that can be converted to a
        :py:class:`cpip.util.DictTree.DictTree`"""
        ret = DuplexAdjacencyList()
        for macroIdentifier in self.macros():
            for depMacro in self._staticMacroDependencies(macroIdentifier):
                ret.add(macroIdentifier, depMacro)

        return ret

    def _staticMacroDependencies(self, theIdentifier):
        """Returns the immediate dependencies as a list of strings for a macro
        identified by the string."""
        ret = []
        macro = self.macro(theIdentifier)
        for tok in macro.replacementTokens:
            if tok.tt == 'identifier' and self.hasMacro(tok.t) and tok.t not in ret:
                ret.append(tok.t)

        return ret

    def getUndefMacro(self, theIdx):
        """Returns the PpDefine object from the undef list for the given index.
        Will raise an :py:class:`ExceptionMacroIndexError` if the index is out of range."""
        try:
            return self._undefS[theIdx]
        except IndexError:
            raise ExceptionMacroIndexError('Index %d is not in range 0-%d' % (
             theIdx, len(self._undefS) - 1))

    def referencedMacroIdentifiers(self, sortedByRefcount=False):
        """Returns an unsorted list of macro identifiers that have a reference
        count > 0. If sortedByRefcount is True the list will be in increasing
        order of reference count then by name. Use reverse() on the result to get decreasing
        order.
        If sortedByRefcount is False the return value is unsorted."""
        if sortedByRefcount:
            myPairs = []
            for k in sorted(self._defineMap.keys()):
                rc = self._defineMap[k].refCount
                if rc > 0:
                    myPairs.append((k, rc))

            listD = [ (x[1], x) for x in myPairs ]
            listD.sort()
            myPairs = [ v[1] for v in listD ]
            return [ x[0] for x in myPairs ]
        return [ mId for mId in self._defineMap.keys() if self._defineMap[mId].refCount > 0 ]

    def macroHistory(self, incEnv=True, onlyRef=True):
        """Returns the macro history as a multi-line string"""
        retList = []
        if incEnv:
            retList.append('Macro Environment:')
            retList.append(str(self))
            retList.append('')
        if onlyRef:
            retList.append('Macro History (referenced macros only):')
        else:
            retList.append('Macro History (all macros):')
        doneTitle = False
        for aMacro in self.genMacrosOutOfScope(None):
            if not doneTitle:
                retList.append('Out-of-scope:')
                doneTitle = True
            if not onlyRef or aMacro.refCount > 0:
                retList.append(str(aMacro))
                for aFlc in aMacro.refFileLineColS:
                    retList.append('    %s %s %s' % (aFlc.fileId, aFlc.lineNum, aFlc.colNum))

        doneTitle = False
        for aMacro in self.genMacrosInScope(None):
            if not doneTitle:
                retList.append('In scope:')
                doneTitle = True
            if not onlyRef or aMacro.refCount > 0:
                retList.append(str(aMacro))
                for aFlc in aMacro.refFileLineColS:
                    retList.append('    %s %s %s' % (aFlc.fileId, aFlc.lineNum, aFlc.colNum))

        return ('\n').join(retList)

    def macroHistoryMap(self):
        """Returns a map of ``{ident : ([ints, ...], True/False), ...}``
        Where the macro identifier is mapped to a pair where:
        pair[0] is a list of indexes into :py:meth:`getUndefMacro()`.
        pair[1] is boolean, True if the identifier is currently defined
        i.e. it is the value ofself.hasMacro(ident).
        The macro can be obtained by self.macro()."""
        undefMap = {}
        for i, aMacro in enumerate(self.genMacrosOutOfScope(None)):
            try:
                undefMap[aMacro.identifier].append(i)
            except KeyError:
                undefMap[aMacro.identifier] = [
                 i]

        retMap = {}
        for aMacro in self.genMacrosInScope(None):
            try:
                retMap[aMacro.identifier] = (
                 undefMap[aMacro.identifier],
                 True)
            except KeyError:
                retMap[aMacro.identifier] = ([], True)

        for k in undefMap.keys():
            if k not in retMap:
                retMap[k] = (undefMap[k],
                 False)

        return retMap

    def macroNotDefinedDependencies(self):
        """Returns a map of ``{identifier : [class FileLineColumn, ...], ...}``
        where there has been an ``#ifdef`` and nothing is defined.
        Thus these macros, if present, could alter the outcome
        i.e. it is dependency on them NOT being defined."""
        return self._ifDefAbsentMacros

    def macroNotDefinedDependencyNames(self):
        """Returns an unsorted list of identifies
        where there has been an ``#ifdef`` and nothing is defined.
        Thus these macros, if present, could alter the outcome
        i.e. it is dependency on them NOT being defined."""
        return list(self._ifDefAbsentMacros.keys())

    def macroNotDefinedDependencyReferences(self, theIdentifier):
        """Returns an ordered list of class FileLineColumn for an identifier
        where there has been an ``#ifdef`` and nothing is defined.
        Thus these macros, if present, could alter the outcome
        i.e. it is dependency on them NOT being defined."""
        try:
            return self._ifDefAbsentMacros[theIdentifier][:]
        except KeyError:
            raise ExceptionMacroEnvNoMacroDefined('Macro %s is not currently present in the macroNotDefinedDependancies.' % theIdentifier)