# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/date/_daterange.py
# Compiled at: 2019-02-02 17:02:31
# Size of source mod 2**32: 7941 bytes
import datetime
from six import string_types
from ._generalslice import OPEN_OPEN, CLOSED_CLOSED, OPEN_CLOSED, CLOSED_OPEN, GeneralSlice
from ._parse import parse
INTERVAL_LOOKUP = {(True, True):OPEN_OPEN, 
 (False, False):CLOSED_CLOSED, 
 (True, False):OPEN_CLOSED, 
 (False, True):CLOSED_OPEN}

class DateRange(GeneralSlice):
    __doc__ = '\n    Represents a bounded datetime range.\n\n    Ranges may be bounded on either end if a date is\n    specified for the start or end of the range, or unbounded\n    if None is specified for either value. Unbounded ranges will allow\n    all available data to pass through when used as a filter argument\n    on function or method.\n\n    =====  ====  ============================  ===============================\n    start  end  interval                      Meaning\n    -----  ----  ----------------------------  -------------------------------\n    None   None                                any date\n    a      None  CLOSED_CLOSED or CLOSED_OPEN  date >= a\n    a      None  OPEN_CLOSED or OPEN_OPEN      date > a\n    None   b     CLOSED_CLOSED or OPEN_CLOSED  date <= b\n    None   b     CLOSED_OPEN or OPEN_OPEN      date < b\n    a      b     CLOSED_CLOSED                 date >= a and date <= b\n    a      b     OPEN_CLOSED                   date > a and date <= b\n    a      b     CLOSED_OPEN                   date >= a and date < b\n    a      b     OPEN_OPEN                     date > a and date < b\n    =====  ====  ============================  ===============================\n\n    Parameters\n    ----------\n    start : `int`, `str` or `datetime.datetime`\n        lower bound date value as an integer, string or datetime object.\n\n    end : `int`, `str` or `datetime.datetime`\n        upper bound date value as an integer, string or datetime object.\n\n    interval : `int`\n               CLOSED_CLOSED, OPEN_CLOSED, CLOSED_OPEN or OPEN_OPEN.\n               **Default is CLOSED_CLOSED**.\n    '

    def __init__(self, start=None, end=None, interval=CLOSED_CLOSED):

        def _is_dt_type(x):
            return isinstance(x, (datetime.datetime, datetime.date))

        def _compute_bound(value, desc):
            if isinstance(value, bytes):
                return parse(value.decode('ascii'))
            if isinstance(value, (int, string_types)):
                return parse(str(value))
            if _is_dt_type(value):
                return value
            if value is None:
                return
            raise TypeError('unsupported type for %s: %s' % (desc, type(value)))

        super(DateRange, self).__init__(_compute_bound(start, 'start'), _compute_bound(end, 'end'), 1, interval)
        if _is_dt_type(self.start):
            if _is_dt_type(self.end):
                if self.start > self.end:
                    raise ValueError('start date (%s) cannot be greater than end date (%s)!' % (
                     self.start, self.end))

    @property
    def unbounded(self):
        """True if range is unbounded on either or both ends, False otherwise."""
        return self.start is None or self.end is None

    def intersection(self, other):
        """
        Create a new DateRange representing the maximal range enclosed by this range and other
        """
        startopen = other.startopen if self.start is None else self.startopen if other.start is None else other.startopen if self.start < other.start else self.startopen if self.start > other.start else self.startopen or other.startopen
        endopen = other.endopen if self.end is None else self.endopen if other.end is None else other.endopen if self.end > other.end else self.endopen if self.end < other.end else self.endopen or other.endopen
        new_start = self.start if other.start is None else other.start if self.start is None else max(self.start, other.start)
        new_end = self.end if other.end is None else other.end if self.end is None else min(self.end, other.end)
        interval = INTERVAL_LOOKUP[(startopen, endopen)]
        return DateRange(new_start, new_end, interval)

    def as_dates(self):
        """
        Create a new DateRange with the datetimes converted to dates and changing to CLOSED/CLOSED.
        """
        new_start = self.start.date() if (self.start and isinstance(self.start, datetime.datetime)) else (self.start)
        new_end = self.end.date() if (self.end and isinstance(self.end, datetime.datetime)) else (self.end)
        return DateRange(new_start, new_end, CLOSED_CLOSED)

    def mongo_query(self):
        """
        Convert a DateRange into a MongoDb query string. FIXME: Mongo can only handle
        datetimes in queries, so we should make this handle the case where start/end are
        datetime.date and extend accordingly (being careful about the interval logic).
        """
        comps = {OPEN_CLOSED: ('t', 'te'), OPEN_OPEN: ('t', 't'), 
         CLOSED_OPEN: ('te', 't'), CLOSED_CLOSED: ('te', 'te')}
        query = {}
        comp = comps[self.interval]
        if self.start:
            query['$g' + comp[0]] = self.start
        if self.end:
            query['$l' + comp[1]] = self.end
        return query

    def get_date_bounds(self):
        """
        Return the upper and lower bounds along
        with operators that are needed to do an 'in range' test.
        Useful for SQL commands.

        Returns
        -------
        tuple: (`str`, `date`, `str`, `date`)
                (date_gt, start, date_lt, end)
        e.g.:
                ('>=', start_date, '<', end_date)
        """
        start = end = None
        date_gt = '>='
        date_lt = '<='
        if self:
            if self.start:
                start = self.start
            if self.end:
                end = self.end
            if self.startopen:
                date_gt = '>'
            if self.endopen:
                date_lt = '<'
        return (
         date_gt, start, date_lt, end)

    def __contains__--- This code section failed: ---

 L. 159         0  LOAD_FAST                'self'
                2  LOAD_ATTR                interval
                4  LOAD_GLOBAL              CLOSED_CLOSED
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    50  'to 50'

 L. 160        10  LOAD_FAST                'self'
               12  LOAD_ATTR                start
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_TRUE     30  'to 30'
               20  LOAD_FAST                'd'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                start
               26  COMPARE_OP               >=
               28  JUMP_IF_FALSE_OR_POP    48  'to 48'
             30_0  COME_FROM            18  '18'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                end
               34  LOAD_CONST               None
               36  COMPARE_OP               is
               38  JUMP_IF_TRUE_OR_POP    48  'to 48'
               40  LOAD_FAST                'd'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                end
               46  COMPARE_OP               <=
             48_0  COME_FROM            38  '38'
             48_1  COME_FROM            28  '28'
               48  RETURN_VALUE     
             50_0  COME_FROM             8  '8'

 L. 161        50  LOAD_FAST                'self'
               52  LOAD_ATTR                interval
               54  LOAD_GLOBAL              CLOSED_OPEN
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE   100  'to 100'

 L. 162        60  LOAD_FAST                'self'
               62  LOAD_ATTR                start
               64  LOAD_CONST               None
               66  COMPARE_OP               is
               68  POP_JUMP_IF_TRUE     80  'to 80'
               70  LOAD_FAST                'd'
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                start
               76  COMPARE_OP               >=
               78  JUMP_IF_FALSE_OR_POP    98  'to 98'
             80_0  COME_FROM            68  '68'
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                end
               84  LOAD_CONST               None
               86  COMPARE_OP               is
               88  JUMP_IF_TRUE_OR_POP    98  'to 98'
               90  LOAD_FAST                'd'
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                end
               96  COMPARE_OP               <
             98_0  COME_FROM            88  '88'
             98_1  COME_FROM            78  '78'
               98  RETURN_VALUE     
            100_0  COME_FROM            58  '58'

 L. 163       100  LOAD_FAST                'self'
              102  LOAD_ATTR                interval
              104  LOAD_GLOBAL              OPEN_CLOSED
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   150  'to 150'

 L. 164       110  LOAD_FAST                'self'
              112  LOAD_ATTR                start
              114  LOAD_CONST               None
              116  COMPARE_OP               is
              118  POP_JUMP_IF_TRUE    130  'to 130'
              120  LOAD_FAST                'd'
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                start
              126  COMPARE_OP               >
              128  JUMP_IF_FALSE_OR_POP   148  'to 148'
            130_0  COME_FROM           118  '118'
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                end
              134  LOAD_CONST               None
              136  COMPARE_OP               is
              138  JUMP_IF_TRUE_OR_POP   148  'to 148'
              140  LOAD_FAST                'd'
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                end
              146  COMPARE_OP               <=
            148_0  COME_FROM           138  '138'
            148_1  COME_FROM           128  '128'
              148  RETURN_VALUE     
            150_0  COME_FROM           108  '108'

 L. 166       150  LOAD_FAST                'self'
              152  LOAD_ATTR                start
              154  LOAD_CONST               None
              156  COMPARE_OP               is
              158  POP_JUMP_IF_TRUE    170  'to 170'
              160  LOAD_FAST                'd'
              162  LOAD_FAST                'self'
              164  LOAD_ATTR                start
              166  COMPARE_OP               >
              168  JUMP_IF_FALSE_OR_POP   188  'to 188'
            170_0  COME_FROM           158  '158'
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                end
              174  LOAD_CONST               None
              176  COMPARE_OP               is
              178  JUMP_IF_TRUE_OR_POP   188  'to 188'
              180  LOAD_FAST                'd'
              182  LOAD_FAST                'self'
              184  LOAD_ATTR                end
              186  COMPARE_OP               <
            188_0  COME_FROM           178  '178'
            188_1  COME_FROM           168  '168'
              188  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 48

    def __repr__(self):
        return 'DateRange(start=%r, end=%r)' % (self.start, self.end)

    def __eq__(self, rhs):
        if not ((rhs is None or hasattr)(rhs, 'end') and hasattr(rhs, 'start')):
            return False
        return self.end == rhs.end and self.start == rhs.start

    def __lt__(self, other):
        if self.start is None:
            return True
        if other.start is None:
            return False
        return self.start < other.start

    def __hash__(self):
        return hash((self.start, self.end, self.step, self.interval))

    def __getitem__(self, key):
        if key == 0:
            return self.start
        if key == 1:
            return self.end
        raise IndexError('Index %s not in range (0:1)' % key)

    def __str__(self):
        return '%s%s, %s%s' % (
         '(' if self.startopen else '[',
         self.start,
         self.end,
         ')' if self.endopen else ']')

    def __setstate__(self, state):
        """Called by pickle, PyYAML etc to set state."""
        self.start = state['start']
        self.end = state['end']
        self.interval = state.get('interval') or CLOSED_CLOSED
        self.step = 1