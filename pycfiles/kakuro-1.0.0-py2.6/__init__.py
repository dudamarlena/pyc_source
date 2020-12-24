# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/kakuro/__init__.py
# Compiled at: 2010-05-20 14:13:05
"""This library provides functionality to represent and solve Kakuro boards.

A board is represented by a two dimensional array of KakuroEntry objects,
either Brick or Blank:

* Brick(v=None, h=None):
A greyed out brick, possibly specifying a vertical (v) and / or horizontal
(h) sum.

* Blank(value=None):
An entry to be filled in, possibly with a value already specified.

The two dimensional array is passed to the constructor of a KakuroBoard:

* KakuroBoard(array)
Uses the two dimensional array to represent internal data structures
necessary to solve the Kakuro board. Provides the solve() method to solve a
board, which functions as a generator in the case of no or multiple solutions.

The board is solved using an iterative refinement process by eliminating
possible values from entries and candidate values for semirows or semicolumns
used in sums. When pure refinement yields no more improvement, the algorithm
uses backtracking, branching on an entry of fewest possible values.

Here is an example of the use of this class to solve a Kokuro board:

board = [[Brick(), Brick(v=14), Brick(v=5), Brick(v=28), Brick(v=3), Brick(), Brick(), Brick(v=26), Brick(v=5), Brick(v=22)],
         [Brick(h=12), Blank(), Blank(), Blank(), Blank(), Brick(v=12,h=24), Blank(), Blank(), Blank(), Blank()],
         [Brick(h=23), Blank(), Blank(), Blank(), Blank(), Blank(), Brick(v=32,h=21), Blank(), Blank(), Blank()],
         [Brick(), Brick(v=7), Brick(v=39), Blank(), Brick(h=6), Blank(), Blank(), Blank(), Brick(v=24), Blank()],
         [Brick(h=20), Blank(), Blank(), Blank(), Brick(v=19,h=27), Blank(), Blank(), Blank(), Blank(), Brick(v=34)],
         [Brick(h=6), Blank(), Blank(), Brick(v=22,h=23), Blank(), Blank(), Blank(), Brick(v=13,h=15), Blank(), Blank()],
         [Brick(h=14), Blank(), Blank(), Blank(), Blank(), Brick(h=14), Blank(), Blank(), Blank(), Blank()],
         [Brick(), Brick(v=6,h=22), Blank(), Blank(), Blank(), Brick(v=4,h=16), Blank(), Blank(), Brick(v=17), Blank()],
         [Brick(h=21), Blank(), Blank(), Blank(), Brick(h=24), Blank(), Blank(), Blank(), Blank(), Blank()],
         [Brick(h=15), Blank(), Blank(), Blank(), Blank(), Blank(), Brick(h=20), Blank(), Blank(), Blank()]]

k = KakuroBoard(board)

for entries in k.solve():
    print '*** SOLUTION ***'
    str = ''
    for row in board:
        for col in row:
            if isinstance(col, Brick):
                str += '_ '
            else:
                str += '%s ' % entries[col.myID].possibleValues[0]
        str += '
'
    print str
"""
import operator

def _findAssignments(val, blankList, exclude=[]):
    """_findAssignments(val, blankList, exclude=[])

    Given a value and a list of blanks, find all possible assignments of values
    to entries that satisfies this value. Exclude can be used to exclude certain
    possible values. In this case, it is used recursively to make sure that each
    possible number appears at most once in each sum."""
    if val == 0 and len(blankList) == 0:
        yield []
    if len(blankList) == 0:
        return
    if not reduce(lambda x, y: x and y, [ filter(lambda x: x not in exclude, blank.possibleValues)
     for blank in blankList ], True):
        return
    if sum([ max([ i for i in blank.possibleValues if i not in exclude ]) for blank in blankList ]) < val:
        return
    if sum([ min([ i for i in blank.possibleValues if i not in exclude ]) for blank in blankList ]) > val:
        return
    for candidate in [ i for i in blankList[0].possibleValues if i not in exclude ]:
        for s in _findAssignments(val - candidate, blankList[1:], exclude + [candidate]):
            yield [
             candidate] + s


class Sum:
    """Represents a sum in the board, i.e. the value of the sum and the iist of
    Blank objects contributing to that sum."""

    def __init__(self, value, blankList, isCopy=False):
        self.value = value
        self.blankList = blankList
        if not isCopy:
            self.configurations = list(_findAssignments(self.value, self.blankList))
        for blank in blankList:
            blank._recordSum(self)

        self.flag = False

    def isComplete(self):
        """Return True if this sum is completely defined and has been processed.
        and False otherwise."""
        return self.flag

    def _copy(self, entries):
        """Make a copy of this sum, using the entries in entries instead of the
        original entries. (The entries in entries should be copies.)"""
        s = Sum(self.value, [ entries[i.myID] for i in self.blankList ], isCopy=True)
        s.configurations = self.configurations[:]
        return s

    def _filterBasedOnEntry(self, entry):
        """For a given entry, filter out all configurations that are not valid
        based on the possible values for the entry."""
        if self.flag:
            return False
        idx = self.blankList.index(entry)
        newConfigurations = [ config for config in self.configurations if config[idx] in entry.possibleValues ]
        changed = newConfigurations != self.configurations
        self.configurations = newConfigurations
        return changed

    def _banExistingConfiguration(self, config):
        """We only allow each sum to appear once in the table, e.g. if we have
        twos sum of value 10 over three entries and one of them is 1, 3, 6, then
        the other one cannot be any permutation of 1, 3, 6.

        This method accepts a configuration (a list of values) that has already
        been used, and filters all permutations of it out of the configuration
        for this row."""
        if self.flag:
            return False
        newConfigurations = [ c for c in self.configurations if set(c) != set(config) ]
        changed = newConfigurations != self.configurations
        self.configurations = newConfigurations
        return changed

    def _getValuesForEntry(self, entry):
        """Given an entry appearing in the sum, determine all the possible
        values it can have in the sum."""
        idx = self.blankList.index(entry)
        return [ config[idx] for config in self.configurations ]

    def _checkCompleteAndProcess(self):
        """Check if this sum is defined, i.e. if only one configuration remains.
        If this is the case, mark it as such and set all of the entries to their
        value in the configuration."""
        if self.flag:
            return False
        changed = False
        if len(self.configurations) == 1:
            self.flag = True
            for (entry, value) in zip(self.blankList, self.configurations[0]):
                changed |= entry._setValue(value)

        return changed


class KakuroEntry:
    """The superclass for entries in a Kakuro board."""
    pass


class Blank(KakuroEntry):
    """A blank square to be filled in."""
    id = 0

    def __init__(self, value=None, specificID=None):
        self.possibleValues = [value] if value else range(1, 10)
        if specificID == None:
            self.myID = Blank.id
            Blank.id += 1
        else:
            self.myID = specificID
        self.sums = []
        return

    def _copy(self):
        """Create a copy of this entry.

        NOTE: We do not populate sums, as this will be done when the sums are
        duplicated."""
        blank = Blank(specificID=self.myID)
        blank.possibleValues = self.possibleValues[:]
        return blank

    def __str__(self):
        """Return a string identifying this blank."""
        return 'E%2s' % self.myID

    def _recordSum(self, s):
        """Record this entry as appearing in the specified Sum object."""
        if s not in self.sums:
            self.sums.append(s)

    def _filterSumConfigurations(self):
        """Iterate over all the sums containing this blank, and filter out
        all of the configurations over those sums that contain an invalid
        entry for this blank."""
        changed = False
        for s in self.sums:
            changed |= s._filterBasedOnEntry(self)

        return changed

    def _filterValuesFromSums(self):
        """This entry can only have certain values in each sum it appears in.
        The possible values that it can have overall is the intersection of
        its current possible values with the possible values in each of the
        sums in which it appears."""
        newPossibleValues = reduce(lambda x, y: [ i for i in x if i in y ], [ set(s._getValuesForEntry(self)) for s in self.sums ], self.possibleValues)
        changed = newPossibleValues != self.possibleValues
        self.possibleValues = newPossibleValues
        return changed

    def _setValue(self, value):
        """Set the value for this entry. This triggers a reaction where we then
        iterate over the sums containing this entry and modify them
        accordingly."""
        self.flag = True
        self.possibleValues = [value]
        return self._filterSumConfigurations()


class Brick(KakuroEntry):
    """A brick, i.e. solid space."""

    def __init__(self, v=None, h=None):
        self.verticalSum = v
        self.horizontalSum = h

    def __str__(self):
        return '_'


class KakuroBoard:
    """A Kakuro board is represented by a two dimensional array with entries of
    type KakuroEntry representing the data at position x,y."""

    def __init__(self, board):
        self.board = board
        self.entries = []
        sums = []
        for (x, row) in enumerate(board):
            for (y, entry) in enumerate(row):
                if isinstance(entry, Brick):
                    if entry.verticalSum:
                        blocks = []
                        posx = x + 1
                        col = [ board[i][y] for i in range(len(board)) ]
                        while posx < len(col) and isinstance(col[posx], Blank):
                            blocks.append(col[posx])
                            posx += 1

                        sums.append(Sum(entry.verticalSum, blocks))
                    if entry.horizontalSum:
                        blocks = []
                        posy = y + 1
                        while posy < len(row) and isinstance(row[posy], Blank):
                            blocks.append(row[posy])
                            posy += 1

                        sums.append(Sum(entry.horizontalSum, blocks))
                elif isinstance(entry, Blank):
                    self.entries.append(entry)

        self.sums = sums

    def _copyBoard(self, entries, sums):
        """Given a board, make a copy of it. This is used in backtracking.

        NOTE: We are not making a full copy of this object so much as we are
        simply copying the entries and sums lists."""
        cEntries = [ entry._copy() for entry in entries ]
        cSums = [ s._copy(cEntries) for s in sums ]
        return (
         cEntries, cSums)

    def solve(self):
        """Solve the board."""
        (cEntries, cSums) = self._copyBoard(self.entries, self.sums)
        return self._solve(cEntries, cSums)

    def _solve(self, entries, sums):
        """Solve the board on the data structures given.

        Go as far as we can computationally, and then branch on the entry of
        fewest choices."""
        changed = True
        while changed:
            changed = False
            for s in filter(lambda x: not x.isComplete(), sums):
                changed |= s._checkCompleteAndProcess()
                if s.isComplete():
                    for s2 in filter(lambda s2: s2.value == s.value and len(s2.blankList) == len(s.blankList), sums):
                        changed |= s2._banExistingConfiguration(s.configurations[0])

            for e in entries:
                changed |= e._filterValuesFromSums()

            for e in entries:
                changed |= e._filterSumConfigurations()

        if reduce(operator.or_, map(lambda x: len(x.possibleValues) == 0, entries), False):
            return
        if reduce(operator.and_, [ len(i.possibleValues) == 1 for i in entries ], True):
            yield entries
        else:
            branchingEntries = sorted([ (len(entry.possibleValues), entry.myID) for entry in entries if len(entry.possibleValues) > 1
                                      ])
            entryID = branchingEntries[0][1]
        for value in entries[entryID].possibleValues:
            (cEntries, cSums) = self._copyBoard(entries, sums)
            cEntries[entryID]._setValue(value)
            for solution in self._solve(cEntries, cSums):
                yield solution


if __name__ == '__main__':
    board = [
     [
      Brick(), Brick(v=14), Brick(v=5), Brick(v=28), Brick(v=3), Brick(), Brick(), Brick(v=26), Brick(v=5), Brick(v=22)],
     [
      Brick(h=12), Blank(), Blank(), Blank(), Blank(), Brick(v=12, h=24), Blank(), Blank(), Blank(), Blank()],
     [
      Brick(h=23), Blank(), Blank(), Blank(), Blank(), Blank(), Brick(v=32, h=21), Blank(), Blank(), Blank()],
     [
      Brick(), Brick(v=7), Brick(v=39), Blank(), Brick(h=6), Blank(), Blank(), Blank(), Brick(v=24), Blank()],
     [
      Brick(h=20), Blank(), Blank(), Blank(), Brick(v=19, h=27), Blank(), Blank(), Blank(), Blank(), Brick(v=34)],
     [
      Brick(h=6), Blank(), Blank(), Brick(v=22, h=23), Blank(), Blank(), Blank(), Brick(v=13, h=15), Blank(), Blank()],
     [
      Brick(h=14), Blank(), Blank(), Blank(), Blank(), Brick(h=14), Blank(), Blank(), Blank(), Blank()],
     [
      Brick(), Brick(v=6, h=22), Blank(), Blank(), Blank(), Brick(v=4, h=16), Blank(), Blank(), Brick(v=17), Blank()],
     [
      Brick(h=21), Blank(), Blank(), Blank(), Brick(h=24), Blank(), Blank(), Blank(), Blank(), Blank()],
     [
      Brick(h=15), Blank(), Blank(), Blank(), Blank(), Blank(), Brick(h=20), Blank(), Blank(), Blank()]]
    k = KakuroBoard(board)
    for entries in k.solve():
        print '*** SOLUTION ***'
        str = ''
        for row in board:
            for col in row:
                if isinstance(col, Brick):
                    str += '_ '
                else:
                    str += '%s ' % entries[col.myID].possibleValues[0]

            str += '\n'

        print str