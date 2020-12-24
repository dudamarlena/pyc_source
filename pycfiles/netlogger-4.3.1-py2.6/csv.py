# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/modules/csv.py
# Compiled at: 2010-09-20 14:05:31
"""
'Load' input as CSV records to a file.
"""
__author__ = 'Dan Gunter'
__rcsid__ = '$Id: csv.py 25224 2010-09-20 18:05:30Z dang $'
import sys
from netlogger.analysis.modules._base import Analyzer as BaseAnalyzer
from netlogger.nlapi import TS_FIELD, EVENT_FIELD
from netlogger import util
COL_SEP = ','
LINE_SEP = '\n'

class Analyzer(BaseAnalyzer):
    """Write CSV version of records to a file.

    Parameters:
      - ostrm {filename,standard output*}: Output stream
      - standard {yes,no,yes*}: Include standard timestamp (ts) and event name
         (event) columns.
      - columns {name,name,...,none*}: Names of columns to extract, 
         in addition to the timestamp (ts) and event name (event).
      - defaults {value,value,..,""*}: Default value to use if values 
          are missing. Must be either one value, which will be substituted 
          for any missing value, or one value for each column.
      - header {yes,no,yes*}: If 'yes' print a header row first
    """
    COLUMN_NULL_DEFAULT = ''

    def __init__(self, ostrm=sys.stdout, columns=[], defaults=None, header=True, standard=True, **kw):
        """Ctor."""
        BaseAnalyzer.__init__(self, **kw)
        self.ostrm = ostrm
        self._first = True
        self._header = util.as_bool(header)
        self.columns = util.as_list(columns, sep=',')
        self._stdcol = util.as_bool(standard)
        ncol = len(self.columns)
        if defaults:
            self._defaults = util.as_list(defaults, sep=',')
        else:
            self._defaults = [
             self.COLUMN_NULL_DEFAULT] * ncol
        if len(self._defaults) not in (1, ncol):
            raise ValueError("'defaults' should have length 1 or %d, not %d"(ncol, len(self._defaults)))
        if len(self._defaults) == 1:
            self._defaults = [
             self._defaults[0]] * len(self.columns)

    def process(self, data):
        if self._dbg:
            self.log.debug('process_data.start')
        ts, event = '%f' % data[TS_FIELD], data[EVENT_FIELD]
        if self._first:
            if self._header:
                if self._stdcol:
                    names = [
                     'timestamp', 'event'] + list(self.columns)
                else:
                    names = list(self.columns)
                self.ostrm.write(COL_SEP.join(names) + LINE_SEP)
            self._first = False
        if self._stdcol:
            col_values = [
             ts, event]
        else:
            col_values = []
        for (i, col) in enumerate(self.columns):
            value = util.stringize(data.get(col, self._defaults[i]))
            col_values.append(value)

        self.ostrm.write(COL_SEP.join(col_values) + LINE_SEP)
        if self._dbg:
            self.log.debug('process_data.end')


def __test(*args):
    import sys
    from netlogger.parsers.base import NLSimpleParser
    parser = NLSimpleParser(None)
    loader = Analyzer(sys.stdout, [])
    for line in sys.stdin:
        data = parser.parseLine(line)
        loader.process(data)

    return


if __name__ == '__main__':
    import sys
    __test()