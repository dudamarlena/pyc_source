# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/dlx/__init__.py
# Compiled at: 2011-01-17 15:11:09
"""An implementation of Donald Knuth's Dancing Links implementation:

http://lanl.arxiv.org/pdf/cs/0011047

By Sebastian Raaphorst, 2008.

Thanks to the following people for their testing efforts:
   * Winfried Plappert"""

class DLX():
    """The DLX data structure and relevant operations."""
    PRIMARY = 0
    SECONDARY = 1

    def __init__(self, columns, rows=None, rowNames=None):
        """Initialize the DLX problem with the specified columns and row data,
        if provided. Column data must be a list of pairs of the form
        (columnname, 0/1) where 0 represents a primary column (i.e. one that
        must be covered) and 1 represents a secondary column (i.e. one that is
        not essential to cover)."""
        self.nodect = len(columns) + 1
        self.U = [ i for i in range(self.nodect) ]
        self.D = [ i for i in range(self.nodect) ]
        self.L = [0] * self.nodect
        self.R = list(range(self.nodect))
        self.C = list(range(self.nodect))
        self.S = [0] * self.nodect
        self.N = [ colname for (colname, _) in columns ] + [None]
        prev = self.nodect - 1
        cur = 0
        for (_, columntype) in columns:
            if columntype == DLX.PRIMARY:
                self.L[cur] = prev
                prev = cur
            else:
                self.L[cur] = cur
            cur += 1

        self.L[self.nodect - 1] = prev
        prev = self.nodect - 1
        cur = self.L[prev]
        while cur != self.nodect - 1:
            self.R[cur] = prev
            prev = cur
            cur = self.L[cur]

        self.R[self.nodect - 1] = prev
        self.header = len(columns)
        self.partialsolution = []
        if rows:
            self.appendRows(rows, rowNames)
        return

    def appendRows(self, rows, rowNames=None):
        """Append the rows to the matrix. The row information should be provided
        as a list with each entry corresponding to a row, with row information
        stored as a list of column indices where the 1s appear.

        Returns a list containing row identifiers, which are the indices of the
        first nodes appearing in the row."""
        rowIdentifiers = []
        if rowNames == None:
            rowNames = [
             None] * len(rows)
        for i in range(len(rows)):
            rowIdentifiers.append(self.appendRow(rows[i], rowNames[i]))

        return rowIdentifiers

    def appendRow(self, row, rowName=None):
        """Given a set of row indices (e.g. column coordinates), append the
        necessary entries to the DLX matrix.

        Returns a row identifier, which is the index of the first node
        appearing in the row."""
        first = self.nodect
        prev = self.nodect
        for index in row:
            self.U.append(self.U[index])
            self.D.append(index)
            self.D[self.U[index]] = self.nodect
            self.U[index] = self.nodect
            self.S[index] += 1
            self.C.append(index)
            self.R.append(self.nodect)
            self.L.append(prev)
            self.R[self.nodect] = self.R[prev]
            self.R[prev] = self.nodect
            self.L[self.R[self.nodect]] = self.nodect
            self.N.append(rowName)
            self.prev = self.nodect
            self.nodect += 1

        return first

    def useRow(self, rowindex):
        """Given a row index, as returned by appendRows or appendRow, use this
        in the partial solution.

        ***NOTE:***
        To unuse rows, unuseRow() must be called with the appropriate rows in
        reverse order that calls were made to useRow(). For example, if we had:
             useRow(7)
             useRow(92)
             useRow(14)
        To undo this and restore the DLX matrix to its original form, we would
        need to perform:
             unuseRow(14)
             unuseRow(92)
             unuseRow(7)
        Failure to comply will result in unexpected behaviour.

        This can be used to force certain rows into the final solution, i.e. by
        executing the appropriate useRow calls prior to solving.

        This should NEVER be called during solving; failure to comply may result
        in unpredictable behaviour."""
        self.partialsolution.append(rowindex)
        i = rowindex
        while 1:
            self._cover(self.C[i])
            i = self.R[i]
            if i == rowindex:
                break

    def unuseRow(self, rowindex):
        """Given a row index, as returned by appendRows or appendRow, if
        useRow() was called to use this row, now unuse it.

        ***NOTE:***
        To unuse rows, unuseRow() must be called with the appropriate rows in
        reverse order that calls were made to useRow(). For example, if we had:
             useRow(7)
             useRow(92)
             useRow(14)
        To undo this and restore the DLX matrix to its original form, we would
        need to perform:
             unuseRow(14)
             unuseRow(92)
             unuseRow(7)
        Failure to comply will result in an AssertionError being raised.
        
        This should NEVER be called during solving, but only prior to and after;
        calling while solving will likely result in AssertionErrors as well."""
        assert self.partialsolution.pop() == rowindex
        i = self.L[rowindex]
        while 1:
            self._uncover(self.C[i])
            i = self.L[i]
            if i == self.L[rowindex]:
                break

    def leftmostColumnSelector(self, _):
        """Select the leftmost available column to cover.

        Note that the userdata (second parameter) is ignored."""
        return self.R[self.header]

    def smallestColumnSelector(self, _):
        """Select the column with the fewest rows covering it, i.e. minimize
        the branching factor.

        Note that the userdata (second parameter) is ignored."""
        smallest = self.R[self.header]
        j = self.R[self.R[self.header]]
        while j != self.header:
            if self.S[j] < self.S[smallest]:
                smallest = j
            j = self.R[j]

        return smallest

    def getRowList(self, row):
        """Get a list of the column names corresponding to the row."""
        names = []
        i = row
        while 1:
            names.append(self.N[self.C[i]])
            i = self.R[i]
            if i == row:
                break

        return names

    def printSolution(self, solution):
        """A convenience function, which simply writes out each of the chosen
        rows in the covering as a list of column names."""
        for i in solution:
            print self.getRowList(i)

    def solve(self, columnselector=smallestColumnSelector, columnselectoruserdata=None):
        """Solve the DLX problem.

        The function accepts two parameters, as follows:

        1. Function: columnselector(DLX, columnselectoruserdata)
        The columnselector function, given the header, and the partial solution
        (stored as a list of rows, with entries being the first DLXEntry in each
        row), should choose a column to process next. If header is returned,
        then it is assumed that no column can be selected and the problem
        backtracks. Default value is smallestColumnSelector.

        2. column selector userdata
        Data to be passed to the supplied column selector as a second parameter.
        Default value is None.

        It yields solutions to the DLX instance, serving as a generator. Thus,
        to process all solutions, one should execute:

        for solution in DLXinstance.solve():
           process solution here

        This call initializes and populated a DLXStatistics object, which may
        be accessed as self.statistics."""
        self.statistics = DLXStatistics()
        for sol in self._solve(0, columnselector, columnselectoruserdata, self.statistics):
            yield sol

    def _solve(self, depth, columnselector, columnselectoruserdata, statistics):
        """This is an internal function and should not be called directly."""
        result = None
        if self.R[self.header] == self.header:
            yield self.partialsolution[:]
            return
        else:
            if len(statistics.nodes) <= depth:
                statistics.nodes += [0] * (depth - len(statistics.nodes) + 1)
            if len(statistics.updates) <= depth:
                statistics.updates += [0] * (depth - len(statistics.updates) + 1)
            c = columnselector(self, columnselectoruserdata)
            if c == self.header or self.S[c] == 0:
                return
            statistics.updates[depth] += self._cover(c)
            r = self.D[c]
            while r != c:
                self.partialsolution.append(r)
                statistics.nodes[depth] += 1
                j = self.R[r]
                while j != r:
                    self._cover(self.C[j])
                    j = self.R[j]

                for sol in self._solve(depth + 1, columnselector, columnselectoruserdata, statistics):
                    yield sol

                self.partialsolution.pop()
                j = self.L[r]
                while j != r:
                    self._uncover(self.C[j])
                    j = self.L[j]

                if result != None:
                    break
                r = self.D[r]

            self._uncover(c)
            return

    def _cover(self, c):
        """This is an internal function and should not be called directly."""
        updates = 1
        self.L[self.R[c]] = self.L[c]
        self.R[self.L[c]] = self.R[c]
        i = self.D[c]
        while i != c:
            j = self.R[i]
            while j != i:
                self.U[self.D[j]] = self.U[j]
                self.D[self.U[j]] = self.D[j]
                self.S[self.C[j]] -= 1
                j = self.R[j]
                updates += 1

            i = self.D[i]

        return updates

    def _uncover(self, c):
        """This is an internal function and should not be called directly."""
        i = self.U[c]
        while i != c:
            j = self.L[i]
            while j != i:
                self.S[self.C[j]] += 1
                self.D[self.U[j]] = j
                self.U[self.D[j]] = j
                j = self.L[j]

            i = self.U[i]

        self.R[self.L[c]] = c
        self.L[self.R[c]] = c


class DLXStatistics():
    """Statistics collected from a run of solving a DLX problem.

    This object has two lists, nodes and updates, as fields.

    Nodes represents the number of nodes visited at each depth of the
    search tree.

    Updates represents the number of link updates performed at each
    depth of the search tree."""

    def __init__(self):
        """__init__(self)

        Create a new empty statistical object."""
        self.nodes = []
        self.updates = []


if __name__ == '__main__':
    columns = [
     (
      'a', DLX.PRIMARY), ('b', DLX.PRIMARY), ('c', DLX.PRIMARY), ('d', DLX.SECONDARY), ('e', DLX.PRIMARY)]
    d = DLX(columns)
    rows = [[1, 2, 4],
     [
      0, 1, 3],
     [
      0],
     [
      0, 1, 2, 3, 4]]
    rowNames = [ 'row%i' % i for i in range(len(rows)) ]
    d.appendRows(rows, rowNames)
    for sol in d.solve():
        d.printSolution(sol)