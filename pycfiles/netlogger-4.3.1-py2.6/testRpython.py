# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/unit/testRpython.py
# Compiled at: 2010-09-27 20:23:24
"""
Unittests for netlogger.analysis.datamining.rpython
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testRpython.py 26522 2010-09-27 21:34:04Z dang $'
import datetime, math, time, unittest
from netlogger.tests import shared
from netlogger.analysis.datamining import rpython
from netlogger.analysis.datamining.rpython import COLTYPE

class TestCase(shared.BaseTestCase):
    """Unit test cases.
    """

    def testMakeDataFrame(self):
        """make_data_frame function
        """
        dtnow = datetime.datetime.now()
        data = [[1, 1.5, 'a', dtnow, 1.0, False, 'a-1'],
         [
          2, 2.5, 'b', dtnow, 2.0, True, 'b-2']]
        df = rpython.make_data_frame(data, ('count', 'val', 'letter', 'date1', 'date2',
                                            'bool', 'fact'), (
         COLTYPE.INT, COLTYPE.FLOAT, COLTYPE.STR, COLTYPE.DATE,
         COLTYPE.DATE, COLTYPE.BOOL, COLTYPE.FACTOR))
        col = {}
        for (i, name) in enumerate(df.names):
            col[name] = i

        for row in (0, 1):
            if self.DEBUG:
                for c in col:
                    self.debug_('ROW %d COL %s = %s' % (row, c, df[col[c]][row]))

            colidx, exval = col['count'], row + 1
            self.assert_(df[colidx][row] == exval, 'Bad count')
            colidx, exval = col['val'], row + 1.5
            self.assert_(df[colidx][row] == exval, 'Bad val')
            colidx, exval = col['letter'], ('a', 'b')[row]
            self.assert_(df[colidx][row] == exval, "Bad letter '%s', expected '%s'" % (
             df[colidx][row], exval))
            colidx, exval = col['fact'], row + 1
            self.assert_(df[colidx][row] == exval, "Bad factor val '%s', expected '%s'" % (
             df[colidx][row], exval))
            colidx, exval = col['date1'], time.mktime(dtnow.timetuple()) + dtnow.microsecond / 1000000.0
            self.assert_(df[colidx][row] == exval, "Bad time1 '%f', expected '%f'" % (
             df[colidx][row], exval))
            colidx, exval = col['date2'], row + 1.0
            self.assert_(df[colidx][row] == exval, "Bad time1 '%f', expected '%f'" % (
             df[colidx][row], exval))


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()