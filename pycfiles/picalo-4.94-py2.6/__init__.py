# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/__init__.py
# Compiled at: 2011-03-14 13:51:33
"""
Picalo is a Python library to help anyone who works with data files, 
especially those who work with data in relational/spreadsheet format.  
It is primarily created for investigators and auditors search through 
data sets for anomalies, trends, ond other information, but it is 
generally useful for any type of data or text files.

Picalo is different from NumPy/Numarray in that it is meant for
heterogeneous data rather than homogenous data.  In NumPy, you
have an array (table) of the same type--all ints, for example.
In Picalo, you have a table made up of different column types,
very similar to a database.

One of Picalo's primary purposes is making relational
databases easier to work with.  Once you have a Picalo table, 
you can add, move, or delete columns; work with records (horizontal
slices of the data); select and group records in various ways;
and run analyses on tables.  Picalo includes adapters for popular
databases, and it provides a Query object that make queries seem
just like regular Tables (except they are live from the database).

If you work with relational databases, delimited (CSV/TSV) files, 
EBCDIC files, MS Excel files, log files, text files, or other 
heterogeneous datasets, Picalo might make your life easier.

Picalo is programmed to be as Pythonic as possible.  It's core objects--
tables, columns, records--they act like lists.  A column is a list of cells.
A record is a list of cells.  A table is a list of records.  Tables can be 
sorted via the sort function, just like the Sorting HowTo shows.  The return
values of almost all functions are new tables, so functions can be chained
together like pipes in Unix.

Picalo includes an optional Project object that stores tables in
Zope Object DB files.  When Projects are used, Picalo automatically
swaps records in and out of memory as needed to ensure efficient use of 
resources.  Projects allow Picalo to work with essentially an unlimited
amount of data.

The project was started in 2003 by Conan C. Albrecht, a professor
in Information Systems at Brigham Young University.  Conan remains
the primary developer of Picalo.

Picalo is released in two formats.  First, as a pure-Python library that is used 
by simply "import picalo" or "from picalo import *" in any Python script.  
Python programmers will be primarily interested in the library
version.  This format is installed in the typical Python fashion, either
as an .egg via setuptools, or via "python setup.py install" from
the source.

Second, Picalo is released as a standalone, wx-Python-based GUI environment that allow
end users to access the Picalo libraries. This version is packaged as a Windows setup.exe file, Mac
application bundle, and Linux rpm and deb files.  The user
may not realize Python is even being used when running the
full application environment.
</ol>

Enjoy!  Please report any bugs to me.  I also welcome additions to the toolkit.
  
Dr. Conan C. Albrecht
conan@warp.byu.edu
http://www.picalo.org/
"""
import sys, types, re, inspect, os, os.path, threading, decimal
format_cache = {}
format_parser = re.compile('^([^#0]*?)([#0]*?),{0,1}([0#]*)\\.{0,1}(0*)(%{0,1})(e\\+(0+)){0,1}$', re.IGNORECASE)

class NumberFormat:

    def __init__(self, format):
        """Initializes the NumberFormat from the given format"""
        self.prefix = None
        self.decimalplaces = None
        self.commapos = None
        self.percent = False
        self.sciplaces = None
        result = format_parser.search(format.strip())
        assert result != None, 'Invalid number format: %s' % format
        if result.group(1):
            self.prefix = result.group(1)
        if result.group(2) and result.group(3):
            self.commapos = len(result.group(3))
        if result.group(3) and result.group(3)[(-1)] == '0':
            self.decimalplaces = 0
        if result.group(4):
            self.decimalplaces = len(result.group(4))
        if result.group(5):
            self.percent = True
        if result.group(6):
            self.sciplaces = len(result.group(7))
        return

    def format_value(self, value, typ):
        """Returns the value as a formatted string"""
        if self.sciplaces != None:
            val = float(value)
            exp = 0
            if abs(val) >= 1:
                while abs(val) >= 10:
                    val = val / 10
                    exp += 1

                return ('%0.' + unicode(self.sciplaces) + 'fE+%i') % (val, exp)
            while abs(val) < 1:
                val = val * 10
                exp += 1

            return ('%0.' + unicode(self.sciplaces) + 'fE-%i') % (val, exp)
        value2 = decimal.Decimal(unicode(value))
        if self.percent:
            value2 = value2 * 100
        if self.decimalplaces != None:
            value2 = decimal.Decimal(unicode(round(value2, self.decimalplaces)))
        parts = value2.as_tuple()
        if parts[2] == 0:
            intpart = [ unicode(s) for s in parts[1] ]
            decpart = []
        else:
            intpart = [ unicode(s) for s in parts[1][:parts[2]] ]
            decpart = [ unicode(s) for s in parts[1][parts[2]:] ]
        if self.commapos:
            i = len(intpart) - 1
            x = 0
            while i > 0:
                x += 1
                if x % self.commapos == 0:
                    intpart.insert(i, ',')
                i -= 1

            ret = ('').join(intpart)
        else:
            ret = unicode(int(value))
        if self.decimalplaces == None and typ not in (int, long):
            ret += '.' + ('').join([ unicode(s) for s in decpart ])
        elif self.decimalplaces > 0:
            while len(decpart) < self.decimalplaces:
                decpart.append('0')

            ret += '.' + ('').join([ unicode(s) for s in decpart ])
        if self.percent:
            ret += '%'
        if self.prefix:
            ret = self.prefix + ret
        return ret


def format_value_from_type(value, typ, format=None):
    """Utility method that does the actual formatting.  See the Column.set_format method
     for a description of the format used here."""
    if isinstance(value, error):
        return unicode(value)
    else:
        if value == None:
            return '<N>'
        if typ in (Date, DateTime):
            if format != None:
                return value.strftime(format)
            if typ == Date:
                return value.strftime('%Y-%m-%d')
            if typ == DateTime:
                return value.strftime('%Y-%m-%d %H:%M:%S')
        if typ in (int, long, float, number, currency):
            if format:
                if format_cache.has_key(format):
                    fmt = format_cache[format]
                else:
                    fmt = NumberFormat(format)
                    format_cache[format] = fmt
                return fmt.format_value(value, typ)
            else:
                return unicode(value)
        return unicode(value)


number_parser_main = re.compile('[^-0-9.]', re.DOTALL)
number_parser_dot_remover = re.compile('^(.*?\\..*?)\\.', re.DOTALL)
number_parser_percent = re.compile('^(.*?)%', re.DOTALL)
number_parser_sci_note = re.compile('^(.*?)E([-+])([0-9]+)', re.IGNORECASE | re.DOTALL)

def parse_value_to_type(value, typ, format=None):
    """Utility method that does the actual parsing.  See the Column.set_format method
     for a description of the format used here."""
    if value == None or isinstance(value, typ) or typ == None:
        return value
    else:
        if typ == Date:
            if format != None:
                return Date(value, format)
            return Date(value)
        if typ == DateTime:
            if format != None:
                return DateTime(value, format)
            return DateTime(value)
        if typ in (int, long, float, number, currency):
            num = unicode(value)
            result_scinote = number_parser_sci_note.search(num)
            if result_scinote != None:
                num = result_scinote.group(1)
            result_perc = number_parser_percent.search(num)
            if result_perc:
                num = result_perc.group(1)
            num = number_parser_main.sub('', num)
            result = number_parser_dot_remover.search(num)
            if result:
                num = result.group(1)
            if num == '':
                num = 0
            conv = typ(number(num))
            if result_scinote != None and result_scinote.group(2) == '-':
                conv = typ(conv / 10 ** int(result_scinote.group(3)))
            if result_scinote != None and result_scinote.group(2) == '+':
                conv = typ(conv * 10 ** int(result_scinote.group(3)))
            if result_perc != None:
                conv = typ(conv / 100.0)
            return conv
        if isinstance(value, str) and typ == unicode:
            return unicode(value, 'utf-8')
        return typ(value)


from Calendar import RE_DATE_FORMATS, RE_DATETIME_FORMATS, DateTime, Date
from Number import number
from Currency import currency
from Boolean import boolean
from picalo.lib import stats
from picalo.lib import progressbar
from Error import error
VARIABLE_TYPES_RE = []
VARIABLE_TYPES_RE.append([re.compile('^-{0,1}\\d+$'), int])
VARIABLE_TYPES_RE.append([re.compile('^-{0,1}\\d+$'), long])
VARIABLE_TYPES_RE.append([re.compile('^-{0,1}\\d+(\\.\\d+){0,1}$'), float])
VARIABLE_TYPES_RE.append([re.compile('^TRUE|FALSE$', re.IGNORECASE), boolean])
VARIABLE_TYPES_RE.append([re.compile('^T|F$', re.IGNORECASE), boolean])
VARIABLE_TYPES_RE.append([re.compile('^YES|NO$', re.IGNORECASE), boolean])
for item in RE_DATE_FORMATS:
    VARIABLE_TYPES_RE.append([item.regex, Date])

for item in RE_DATETIME_FORMATS:
    VARIABLE_TYPES_RE.append([item.regex, DateTime])

TYPE_TO_DB = {DateTime: 'TIMESTAMP', 
   Date: 'DATE', 
   int: 'INTEGER', 
   long: 'BIGINT', 
   float: 'FLOAT', 
   boolean: 'BOOLEAN'}
VARIABLE_RE = re.compile('^[A-Za-z_][A-Za-z0-9_]*$')
FIRST_LETTER_RE = re.compile('[A-Za-z_]')
LETTER_RE = re.compile('[A-Za-z0-9_]')
RESERVED_COLUMN_NAMES = {'record': None, 
   'recordindex': None, 
   'startrecord': None, 
   'record1': None, 
   'record1index': None, 
   'record2index': None, 
   'record2': None, 
   'value': None, 
   'group': None}
_builtinsum = sum

def sum(sequence, start=0):
    """Returns the sum of the given sequence of numbers
     plus the value of start.  When the sequence is empty,
     returns start.
     
     @param sequence:   A sequence of numbers
     @type  sequence:   list
     @param start:      The starting value, usually 0
     @type  start:      int
     @return:           The sum of the sequence, plus the start value
     @rtype:            int
  """
    return _builtinsum(sequence, start)


def mean(sequence, default=0):
    """Returns the average of the given sequence,
     or the default if the sequence is empty.
     More advanced statistical routines can be found in the picalo.lib.stats
     module.
  
     @param sequence:    A sequence of numbers
     @type  sequence:    list
     @param default:     The default value to return when the list is empty
     @type  default:     int
     @return:            The average of the numbers
     @rtype:             float
  """
    if len(sequence) == 0:
        return default
    else:
        if len(sequence) == 1:
            return sequence[0]
        return stats.mean(sequence)


def count(sequence):
    """Returns the number of items in the sequence.
     The built in function "len" also gives this value.
     
     @param sequence:    A sequence of items of any type.  If not a sequence, returns 1.
     @type  sequence:    list
     @return:              The number of items in the sequence
     @rtype:               float
  """
    try:
        return len(sequence)
    except:
        return 1


_builtinmax = max

def max(*args, **kargs):
    """With a single sequence argument, return its largest item.
     With two or more arguments, return the largest argument.
     
     @param args:   A sequence of items.
     @return:       The largest item in the sequence
     @rtype:        object
  """
    return _builtinmax(*args, **kargs)


_builtinmin = min

def min(*args, **kargs):
    """With a single sequence argument, return its smallest item.
     With two or more arguments, return the smallest argument.
     
     @param args:       A sequence of items.
     @return:           The smallest item in the sequence
     @rtype:            object
  """
    return _builtinmin(*args, **kargs)


def stdev(sequence, default=0):
    """Returns the standard deviation of the given sequence,
     or the default if the sequence contains zero or one items.
     More advanced statistical routines can be found in the picalo.lib.stats
     module.
     
     @param sequence:   A sequence of items.
     @type  sequence:   list
     @param default:    The default if a standard deviation cannot be calculated.
     @type  default:    float
     @return:           The standard deviation of the sequence, or the default if len(sequence) < 2.
     @rtype:            float
  """
    if len(sequence) < 2:
        return default
    return stats.stdev(sequence)


def variance(sequence, default=0):
    """Returns the variance of the given sequence,
     or the default if the sequence contains zero or one items.
     More advanced statistical routines can be found in the picalo.lib.stats
     module.
     
     @param sequence:   A sequence of items.
     @type  sequence:   list
     @param default:    The default if a variance cannot be calculated.
     @type  default:    float
     @return:           The variance of the sequence, or the default if len(sequence) < 2.
     @rtype:            float
  """
    if len(sequence) < 2:
        return default
    return stats.var(sequence)


mainframe = None
guiUpdateProgressDialog = None
useProgress = False
lastcaller = None
lastprogress = 0.0
progress_lock = threading.RLock()

def _updateProgress(msg='', progress=1, title='Progress', force=False):
    """Initializes the progress bar if it's being used.  Progress should be from 0 to 1.
     This function SHOULD NOT be called directly.  Instead, call the show_progress()
     method global to Picalo (imported when you "from picalo import *").
     
     See the documentation for show_progress for information on the parameters.
  """
    global lastcaller
    global lastprogress
    global useProgress
    progress_lock.acquire()
    try:
        if not useProgress:
            return
        caller = id(inspect.currentframe().f_back.f_back.f_code)
        if caller != None and lastcaller != None and caller != lastcaller and force == False:
            if mainframe == None:
                _updateProgressDialog(progress=lastprogress)
            else:
                guiUpdateProgressDialog(progress=lastprogress, parent=mainframe)
            return
        lastcaller = caller
        if not msg or progress >= 1.0 or progress < 0.0:
            lastcaller = None
        lastprogress = progress
        if mainframe == None:
            _updateProgressDialog(msg=msg, progress=progress)
        else:
            guiUpdateProgressDialog(msg=msg, progress=progress, title=title, parent=mainframe)
    finally:
        progress_lock.release()

    return


def use_progress_indicators(show):
    """Sets whether Picalo shows progress dialogs in text or GUI mode.
     Send False into this method to make Picalo quiet.  Send True
     to see progress bars for operations.
  """
    global useProgress
    useProgress = show


def show_progress(msg='', progress=1.0, title='Progress', force=False):
    """Updates the progress bar with a message and
     a percentage progress between 0 and 1. To remove the progress
     bar, call clear_progress().
     
     This function is important because it gives feedback to the user.
     In addition, and perhaps more importantly, it gives the user a 
     cancel button (in GUI mode) that allows the user to cancel
     your script.  Be sure to call show_progress throughout your
     script.
     
     Sometimes multiple functions try to show or clear a progress bar.
     For example, a top-level script might show a master progress bar
     and then call load().  The load() function tries to show another
     progress bar, which Picalo normally circumvents or the load() function
     would take over the top-level script's progress bar.  In other words,
     the first script to show a progress bar is the only one that can update
     and/or clear the dialog.  By setting force to True, you can override this
     default behavior.  This should not normally be used as it takes control 
     when the top-level script should keep control.

     @param msg:        The message to show the user.
     @type  msg:        str
     @param progress:   A value between 0 and 1 indicating the percentage finished.
     @type  progress:   float
     @param title:      The title of the progress bar.  Defaults to 'Progress'.
     @type  title:      str
     @param force:      Whether to force control of the dialog to the calling code.  
     @type  force:      boolean
  """
    _updateProgress(msg=msg, progress=progress, title=title, force=force)


def clear_progress(force=False):
    """Clears the progress bar from the screen.  
  
     Sometimes multiple functions try to show or clear a progress bar.
     For example, a top-level script might show a master progress bar
     and then call load().  The load() function tries to show another
     progress bar, which Picalo normally circumvents or the load() function
     would take over the top-level script's progress bar.  In other words,
     the first script to show a progress bar is the only one that can update
     and/or clear the dialog.  By setting force to True, you can override this
     default behavior.  This should not normally be used as it takes control 
     when the top-level script should keep control.

     @param force:      Whether to force control of the dialog to the calling code.  
     @type  force:      boolean
  """
    _updateProgress(force=force)


class MessageProgressBarWidget(progressbar.ProgressBarWidget):
    """Extension to display a message"""

    def __init__(self):
        self.msg = ''

    def update(self, pbar):
        return self.msg


message_widget = MessageProgressBarWidget()
widgets = (
 message_widget,
 '  ',
 progressbar.Percentage(),
 ' ',
 progressbar.Bar(marker='#', left='|', right='|'),
 ' ',
 progressbar.ETA())
progressDialog = None

def _updateProgressDialog(msg='', progress=1):
    """Initializes the progress bar.  This should not be called directly.
     Call show_progress() instead, which gets imported when you run
     "from picalo import *".
     """
    global progressDialog
    if progress >= 1.0 or progress < 0.0:
        if progressDialog:
            progressDialog.finish()
        progressDialog = None
        return
    else:
        if not progressDialog:
            progressDialog = progressbar.ProgressBar(maxval=100, widgets=widgets, fd=sys.stdout)
            progressDialog.start()
        if msg:
            message_widget.msg = msg
        progressDialog.update(int(progress * 100.0))
        sys.stdout.flush()
        return


def check_valid_table(table, *columns):
    """Checks to ensure the table is a valid table object, and that the columns
     are valid columns in the table.  Throws an AssertionError if anything is
     wrong."""
    assert isinstance(table, Table), 'Please specify a valid table for this function.'
    for column in columns:
        if isinstance(column, (list, tuple)):
            check_valid_table(table, *column)
        else:
            table.deref_column(column)


def is_valid_variable(varname):
    """Returns whether the given varname is a valid python variablename"""
    return VARIABLE_RE.match(varname) != None


def make_valid_variable(varname, repl='_'):
    """Makes the given variable a valid variable name"""
    if not isinstance(varname, types.StringTypes):
        varname = unicode(varname)
    if len(varname) == 0:
        varname = repl
    if not FIRST_LETTER_RE.match(varname[0]):
        if LETTER_RE.match(varname[0]):
            varname = repl + varname
        else:
            varname = repl + varname[1:]
    for i in range(1, len(varname)):
        if not LETTER_RE.match(varname[i]):
            varname = varname[:i] + repl + varname[i + 1:]

    return varname


def ensure_valid_variables(lst, repl='_'):
    """Ensures the strings in the list are valid Picalo/Python variables.
     This is used to create column names during loading picalo tables.
     
     This method modifies the lst directly.  It also returns the lst for
     convenience reasons.
  """
    for i in range(len(lst)):
        lst[i] = make_valid_variable(lst[i], repl)

    return lst


def make_unique_colnames(columns):
    """Takes a list of names and adds the appropriate values to
     each value to ensure each is unique"""
    unique = []
    for i in range(len(columns)):
        unique.append(ensure_unique_list_value(unique, columns[i]))

    return unique


def ensure_unique_colname(table, name):
    """Ensures the name is unique for the columns in the table.  It
     adds _1, _2, _3, and so forth if needed to the name.
  """
    colnames = [ col.name for col in table.get_columns() ]
    return ensure_unique_list_value(colnames, name)


def ensure_unique_list_value(lst, name):
    """Ensures that the name is unique for the names
     already in the list.  It adds _1, _2, _3, and so forth
     if needed to the name.  This function is split out
     because functions like Crosstable need to create the
     column name list before creating the table.
  """
    ret = name
    i = 1
    while ret in lst:
        ret = name + '_' + str(i)
        i += 1

    return ret


def make_unicode(value):
    """Makes a value (of any type) into unicode using utf_8"""
    if isinstance(value, unicode):
        return value
    else:
        if isinstance(value, str):
            return unicode(value, 'utf_8')
        return unicode(repr(value), 'utf_8')


def run_tablearray(msg, func, tablearray, *args, **kargs):
    """Runs the given function on every table in the TableArray.  If the 
     function returns a Table, the results are collected into another
     TableList and returned.
     
     It assumes that the first parameter in the function is the table.
  """
    try:
        results = TableArray()
        return_results = False
        for (i, table) in enumerate(tablearray):
            show_progress(msg, float(i) / float(len(tablearray)))
            ret = func(table, *args, **kargs)
            if isinstance(ret, (Table, TableArray, TableList)):
                return_results = True
                results.append(ret)

        if return_results:
            return results
    finally:
        clear_progress()


def create_directory(directory):
    """Creates the given directory, including all required
     directories.  This works equally well on Windows 
     and Unix (the os.mkdirs doesn't seem to like c: in paths).
  """
    parts = []
    lastdir = None
    while not os.path.exists(directory) and lastdir != directory:
        lastdir = directory
        (directory, tail) = os.path.split(directory)
        if tail:
            parts.append(tail)

    parts.reverse()
    for part in parts:
        directory = os.path.join(directory, part)
        os.mkdir(directory)

    return


from Table import Table
from TableList import TableList
from TableArray import TableArray
from Record import Record
from Column import Column
table = Table(['id'], [[0]])
RESERVED_COLUMN_NAMES.update([ (name, None) for name in dir(table[0]) ])
assert stats.__version__ == 0.6, 'The picalo.lib.stats module has been upgraded.  The Picalo developers need to modify the picalo.lib.__init__ file to match it.'
for name in dir(stats):
    func = getattr(stats, name)
    if isinstance(func, stats.Dispatch):
        if types.ListType in func._dispatch:
            func._dispatch[Column] = func._dispatch[types.ListType]
            func._dispatch[Record] = func._dispatch[types.ListType]

import Boolean as BooleanModule
from Boolean import *
import Number as NumberModule
from Number import *
import Currency as CurrencyModule
from Currency import *
import Error as ErrorModule
from Error import *
import Calendar as CalendarModule
from Calendar import *
import Table as TableModule
from Table import *
import TableArray as TableArrayModule
from TableArray import *
import TableList as TableListModule
from TableList import *
import Project as ProjectModule
from Project import *
global_variables = BooleanModule.__all__ + NumberModule.__all__ + CurrencyModule.__all__ + ErrorModule.__all__ + CalendarModule.__all__ + TableModule.__all__ + TableArrayModule.__all__ + TableListModule.__all__ + ProjectModule.__all__
import Benfords, Crosstable, Database, Financial, Grouping, Trending, Simple
global_modules = [
 'Benfords',
 'Boolean',
 'Crosstable',
 'Currency',
 'Column',
 'Calendar',
 'Database',
 'Error',
 'Expression',
 'Financial',
 'Grouping',
 'Number',
 'Table',
 'Project',
 'Record',
 'Simple',
 'TableArray',
 'TableList',
 'Trending']
python_modules = [
 'string',
 'sys',
 're',
 'random',
 'os',
 'os.path',
 'urllib',
 'xml.etree.ElementTree']
global_functions = [
 'sum',
 'count',
 'mean',
 'max',
 'min',
 'stdev',
 'variance',
 'use_progress_indicators',
 'show_progress',
 'clear_progress',
 'check_valid_table',
 'format_value_from_type',
 'parse_value_to_type']
__all__ = global_variables + global_modules + global_functions
use_progress_indicators(True)