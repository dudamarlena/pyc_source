# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/core/FileLocation.py
# Compiled at: 2017-10-03 13:07:16
__doc__ = "Various classes for use by the preprocessor for keeping track of the\nlocation in a set of files.\n\nThis consists of three related classes:\n\nLogicalPhysicalLineMap\n----------------------\nThis low-level class maintains and internal theoretical relationship between\nthe logical position in a string and the physical position. These differ when\nphysical characters are replaced by logical ones.\n\nThis is not usually used directly by other modules.\n\nFileLocation\n------------\nThis consists of a stack of one or more LogicalPhysicalLineMap objects each\nof which represents a phase of translation. This understands what it means to\nreplace a trigraph or encounter a line continuation phrase.\n\nTypically this is used by a PpTokeniser.\n\nCppFileLocation\n---------------\nThis consists of a stack of one or more FileLocation objects each\nof which represents an ITU or included file. Conceptually this is a table of\ncolumns (each a FileLocation object) and cells (each a LogicalPhysicalLineMap).\nThe public API gives access to the 'current' LogicalPhysicalLineMap i.e. the top\nright one in the table. The public API allows pushing (adding a column when a\nfile is #include'd) and popping (removing the last column at the end of\n#include processing).\n\nTypically this is used by a PpLexer.\n\n\nUsing line continuation in LogicalPhysicalLineMap\n=================================================\nclass FileLocation needs to poke the underlying LogicalPhysicalLineMap\nin the right way...\n\nThis is accomplished by calling from class FileLocation the underlying\nLogicalPhysicalLineMap._addToIr()\nThis makes calls occur in N pairs.\nN = The number of '\\\n' phrases.\nL(n) is the length of the physical line n (0 <= n < N) not including the '\\\n'\nMake N calls to _addIr(...)\nNOTE: The use of 1+ and -1* here\n_addToIr(theLogicalLine=a, theLogicalCol=1+b, dLine=c, dColumn=-1*d)\nWhere:\na(n) = The current logical line number (starting at 1), constant for the group\nb(n) = Sigma[L(n) for 0...n)]\nc(n) = 1\nd(n) = L(n)\n\nExamples:\nmyPstrS = ['abc\\\n', '\\\n', 'd\\\n', 'ef\n',]\nN = 3\nL(n) -> (3, 0, 1)\na = 1, c = 1\n(b, d)\n(3, 3)\n(3, 0)\n(4, 1)\n\nmyPstrS = ['abc\\\n', 'd\\\n', '\\\n', 'ef\n',]\nN = 3\nL(n) -> (3, 1, 0)\na = 1, c = 1\n(b, d)\n(3, 3)\n(4, 1)\n(4, 0)\n\nmyPstrS = ['ab\\\n', 'c\\\n', 'd\\\n', 'ef\n',]\nN = 3\nL(n) -> (2, 1, 1)\na = 1, c = 1\n(b, d)\n(2, 2)\n(3, 1)\n(4, 1)\n\nThe second call of the pair is as follows, this needs to know N so has\nto be done after all first-of-pair calls:\n_addToIr(theLogicalLine=d, theLogicalCol=1, dLine=e, dColumn=f)\nWhere:\nd = n+2 where n is the number of the '\\\n' in the group starting at 0\ne = N-n-1 where N is the total number of '\\\n' in the group.\nf = Length of the last physical line spliced, not including the '\n'\n\nProgramatically:\nfor n in range(N):\n    myLplm._addToIr(theLogicalLine=n+2, theLogicalCol=1, dLine=N-n-1, dColumn=f)\n\nIn all the examples above f = 2\n"
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import collections
from cpip import ExceptionCpip

class ExceptionFileLocation(ExceptionCpip):
    """Simple specialisation of an exception class for the FileLocation classes."""


START_LINE = 1
START_COLUMN = 1
FileLine = collections.namedtuple('FileLine', 'fileId lineNum', verbose=False)
FileLineCol = collections.namedtuple('FileLineCol', FileLine._fields + ('colNum', ), verbose=False)

class LogicalPhysicalLineMap(object):
    """Class that can map logical positions (i.e. after text substitution) back
    to the original physical line columns.
    The effect of various substitutions is as follows:
    
    Phase 1: Trigraph replacement - logical is same or smaller than physical.
    Phase 1: Mapping non lex.charset to universal-character-name - logical is larger than physical.
    Phase 2: Line splicing - if done logical is smaller that physical.
    Phase 3: Digraph replacement - logical is same or smaller that physical.
    """

    def __init__(self):
        self._ir = {}

    def __str__(self):
        prefix = '    '
        retList = ['{line_num: [(col, line_increment, col_increment)], ...}']
        if len(self._ir) == 0:
            retList.append('%s%s' % (prefix, 'Empty'))
        else:
            for aK in sorted(self._ir.keys()):
                retList.append('%s:' % aK)
                for t in self._ir[aK]:
                    retList.append('%s%s' % (prefix, str(t)))

        return ('\n').join(retList)

    def _addToIr(self, theLogicalLine, theLogicalCol, dLine, dColumn):
        """Adds, or updates a record to the internal representation."""
        addTup = (
         theLogicalCol, dLine, dColumn)
        if theLogicalLine not in self._ir:
            self._ir[theLogicalLine] = [
             addTup]
        else:
            for i, tup in enumerate(self._ir[theLogicalLine]):
                c, dl, dc = tup
                if c == theLogicalCol:
                    dl += dLine
                    dc += dColumn
                    self._ir[theLogicalLine][i] = (c, dl, dc)
                    break
            else:
                for i, tup in enumerate(self._ir[theLogicalLine]):
                    c, dl, dc = tup
                    if c > theLogicalCol:
                        self._ir[theLogicalLine].insert(i, addTup)
                        break
                else:
                    self._ir[theLogicalLine].append(addTup)

    def substString(self, theLogicalLine, theLogicalCol, lenPhysical, lenLogical):
        """Records a string substitution."""
        self._addToIr(theLogicalLine, theLogicalCol, 0, lenPhysical - lenLogical)

    def pLineCol(self, lLine, lCol):
        """Returns the (physical line number, physical column number) from
        a logical line and logical column."""
        pLine = lLine
        pCol = lCol
        if lLine in self._ir:
            for lc, dl, dc in self._ir[lLine]:
                if lCol >= lc:
                    pLine += dl
                    pCol += dc
                else:
                    break

        return (
         pLine, pCol)

    def offsetAbsolute(self, theLineCol):
        """Given a pair of integers that represent line/column starting at
        zero this returns a tuple pair of the absolute line/column."""
        return (
         theLineCol[0] + START_LINE, theLineCol[1] + START_COLUMN)

    def offsetRelative(self, theLineCol):
        """Given a pair of integers that represent line/column starting at
        START_LINE, START_COLUMN this returns a tuple pair of the relative
        line/column i.e. starting at (0, 0)."""
        return (
         theLineCol[0] - START_LINE, theLineCol[1] - START_COLUMN)


class FileLocation(object):
    """Class that persists the line/column location in a source file.
    This also handles various passes of the same file for the PpTokeniser."""

    def __init__(self, theFileName):
        """Initialise with a file name (actually an ID)
        NOTE: We do not check for it's existence as we are not allied to the
        file system (we could get the files from a database instead."""
        self._fileName = theFileName
        self._lineNum = START_LINE
        self._colNum = START_COLUMN
        self._logicalPhysMapStack = [
         LogicalPhysicalLineMap()]
        self._lineSpliceCount = 0
        self._lineSpliceColInc = 0

    def __str__(self):
        retList = [
         'FileLocation with %d maps:' % len(self._logicalPhysMapStack)]
        for i in range(len(self._logicalPhysMapStack) - 1, -1, -1):
            retList.append('Map [%d]:' % i)
            retList.append(str(self._logicalPhysMapStack[i]))

        return ('\n').join(retList)

    def startNewPhase(self):
        """Starts a new processing phase e.g. a translation phase.
        This adds a new LogicalPhysicalLineMap() to the stack."""
        assert len(self._logicalPhysMapStack) > 0
        self._lineNum = START_LINE
        self._colNum = START_COLUMN
        self._logicalPhysMapStack.append(LogicalPhysicalLineMap())

    def retPredefinedMacro(self, theName):
        """Returns the value of __FILE__ or __LINE__.
        Applies ISO/IEC 14882:1998(E) 16 Predefined macro names [cpp.predefined] note 2
        May raise ExceptionFileLocation if theName is something else."""
        if theName == '__FILE__':
            return self.fileName
        if theName == '__LINE__':
            return '%d' % self.lineNum
        raise ExceptionFileLocation('Unknown predefined macro name "%s"' % theName)

    def logicalToPhysical(self, theLline, theLcol):
        """Returns the physical line and column number for a
        logical line and column."""
        assert len(self._logicalPhysMapStack) > 0
        retL = theLline
        retC = theLcol
        for i in range(len(self._logicalPhysMapStack) - 1, -1, -1):
            retL, retC = self._logicalPhysMapStack[i].pLineCol(retL, retC)

        return (retL, retC)

    def retLineNum(self):
        return self._lineNum

    def setLineNum(self, theNum):
        self._lineNum = theNum

    lineNum = property(retLineNum, setLineNum)

    def retColNum(self):
        return self._colNum

    def setColNum(self, theNum):
        self._colNum = theNum

    colNum = property(retColNum, setColNum)

    @property
    def fileName(self):
        return self._fileName

    @property
    def pLineCol(self):
        """Returns the current physical line and column number."""
        assert len(self._logicalPhysMapStack) > 0
        return self.logicalToPhysical(self._lineNum, self._colNum)

    @property
    def lineCol(self):
        """Returns the current line and column number as a pair."""
        assert len(self._logicalPhysMapStack) > 0
        return (
         self._lineNum, self._colNum)

    @property
    def lineSpliceCount(self):
        """The number of line splices in the current splice group."""
        return self._lineSpliceCount

    def fileLineCol(self):
        """Return an instance of FileLineCol from the current settings."""
        pLine, pCol = self.pLineCol
        return FileLineCol(self.fileName, pLine, pCol)

    def incCol(self, num=1):
        """Increment the column by num. There is no range check on num."""
        self._colNum += num

    def incLine(self, num=1):
        """Increment the line by num. There is no range check on num."""
        self._lineNum += num
        if num:
            self._colNum = START_COLUMN

    def update(self, theString):
        """Increment line and column counters from a string."""
        self.incLine(theString.count('\n'))
        self.incCol(len(theString) - theString.rfind('\n') - 1)

    @property
    def logicalPhysicalLineMap(self):
        """Return the current top level LogicalPhysicalLineMap Read Only instance."""
        assert len(self._logicalPhysMapStack) > 0
        return self._logicalPhysMapStack[(-1)]

    def substString(self, lenPhysical, lenLogical):
        """Records a string substitution at the current logical location.
        This does NOT update the current line or column, use update(...) to do that."""
        self._logicalPhysMapStack[(-1)].substString(self.lineNum, self.colNum, lenPhysical, lenLogical)

    def setTrigraph(self):
        """Records that a trigraph has be substituted at the current place."""
        myTriLen = 3
        self._logicalPhysMapStack[(-1)].substString(self.lineNum, self.colNum + 1, myTriLen, 1)

    def spliceLine(self, thePhysicalLine):
        """Update the line/column mapping to record a line splice."""
        assert thePhysicalLine.endswith('\\\n')
        lP = len(thePhysicalLine) - len('\\\n')
        if self._lineSpliceCount == 0:
            self._lineSpliceColInc = lP
        else:
            self._lineSpliceColInc += lP
        self.logicalPhysicalLineMap._addToIr(theLogicalLine=self.lineNum, theLogicalCol=1 + self._lineSpliceColInc, dLine=1, dColumn=-1 * lP)
        self._lineSpliceCount += 1
        self._colNum += lP

    def pformatLogicalToPhysical(self, theLfile, thePfile):
        """Given a logical and a physical representation this goes through
        character by both character, pretty formats the comparison and
        returns the formatted string."""
        strList = [
         'Logical -> Physical']
        for rLl in range(len(theLfile)):
            for rLc in range(len(theLfile[rLl])):
                absLogPair = self.logicalPhysicalLineMap.offsetAbsolute((rLl, rLc))
                pLine, pCol = self.logicalPhysicalLineMap.pLineCol(absLogPair[0], absLogPair[1])
                rPl, rPc = self.logicalPhysicalLineMap.offsetRelative((pLine, pCol))
                if rLc == 0 and theLfile[rLl][rLc] == '\n':
                    myPchar = '\n'
                else:
                    myPchar = thePfile[rPl][rPc]
                if myPchar == '\n':
                    myPchar = '\\n'
                myLchar = theLfile[rLl][rLc]
                if myLchar == '\n':
                    myLchar = '\\n'
                if myLchar != myPchar:
                    theMsg = '%s != %s' % (myLchar, myPchar)
                else:
                    theMsg = '%s == %s' % (myLchar, myPchar)
                strList.append('%s -> %s %s' % (str(absLogPair), str((pLine, pCol)), theMsg))

        return ('\n').join(strList)