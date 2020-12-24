# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/datamining/rpython.py
# Compiled at: 2011-03-01 07:02:13
"""
Provide a Python API for easy interfacing with R.

Depends on RPy2: http://rpy.sourceforge.net/rpy2.html

"""
__author__ = 'Dan Gunter <dkgunter@lbl.gov>'
__rcsid__ = '$Id: rpython.py 27256 2011-03-01 12:02:12Z dang $'
import datetime, gc, time, rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import rpy2.rlike.container as rlc
from netlogger.analysis.datamining import base as dmbase
base = importr('base')
R = robjects.r

class RDataSource(dmbase.DataSource):
    """Source of data for a plot or analysis.
    """

    def preprocess(self, data):
        return cursor_data_frame(data)


class COLTYPE:
    """Enumeration of column types.
    """
    INT = 1
    FLOAT = 2
    STR = 3
    DATE = 4
    FACTOR = 5
    BOOL = 6
    NONE = [
     None,
     0,
     0.0,
     '',
     datetime.datetime(1970, 1, 1),
     '',
     True]

    @staticmethod
    def from_value(value, factors=True):
        """Return an inferred column type.
        """
        if isinstance(value, int):
            return COLTYPE.INT
        if isinstance(value, float) or isinstance(value, long):
            return COLTYPE.FLOAT
        if isinstance(value, datetime.datetime):
            return COLTYPE.DATE
        if isinstance(value, bool):
            return COLTYPE.BOOL
        return (
         COLTYPE.STR, COLTYPE.FACTOR)[factors]


def _datetime_to_sec(dt):
    """Convert datetime object to number of seconds since 1/1/1970.

    Args:
      dt - Datetime object
      
    Return:
      Seconds (as a float) since the UNIX epoch.
    """
    return time.mktime(dt.timetuple()) + dt.microsecond / 1000000.0


def make_data_frame(rows, colnames, coltypes):
    """Make a data frame from a list of rows and definitions
    (name and type) of the columns found in each row.
    
    See COLTYPE documentation for a description of accepted input types
    for each column type.
    
    Args:
      - rows (object[][]): Rows of data, each of the same length and types
      - colnames (str[]): Name of each column
      - column_type (COLTYPE[]): Type of each column. 
         
    Return:
      - robjects.DataFrame: Data frame

    Exceptions:
      - TypeError: Column value does not match stated type
    """
    if len(rows) == 0:
        return robjects.DataFrame({})
    columns = rlc.TaggedList([])
    for i in range(len(rows[0])):
        col = []
        for row in rows:
            col.append(row[i])

        ct = coltypes[i]
        if ct == COLTYPE.INT:
            vec = robjects.IntVector(col)
        elif ct == COLTYPE.FLOAT:
            vec = robjects.FloatVector(col)
        elif ct == COLTYPE.STR:
            vec = base.I(robjects.StrVector(col))
        elif ct == COLTYPE.BOOL:
            vec = robjects.BoolVector(col)
        elif ct == COLTYPE.FACTOR:
            vec = robjects.StrVector(col)
        elif ct == COLTYPE.DATE:
            field = col[0]
            if isinstance(field, datetime.datetime):
                tcol = map(_datetime_to_sec, col)
            elif isinstance(field, float):
                tcol = col
            else:
                raise TypeError("Bad date type '%s' for column %d, '%s'. Expected time.struct_time, datetime.datetime, or float." % (
                 type(field), i, colnames[i]))
            vec = robjects.FloatVector(tcol)
        else:
            raise TypeError("Unknown type '%s' for column %d, '%s'." % (
             type(field), i, colnames[i]))
        columns.append(vec, tag=colnames[i].encode())

    df = robjects.DataFrame(columns)
    gc.collect()
    return df


def cursor_data_frame(cursor, column_types={}):
    """Iterate through cursor and return an R DataFrame object
    that represents its rows.
    
    It is assumed that all records have the same structure.
    If a record is missing any fields, it will be silently ignored.

    This is not a streaming algorithm. Temporary storage of 3x the
    original size is required. All records will be loaded
    into memory, then duplicated by make_data_frame(), and copied
    again by R into the DataFrame object itself.
    
    Args:
      - cursor (iterable): The 'cursor' is anything that supports the iterator
                 protocol. The expected datatype returned at each iteration is
                 a dictionary-like object that supports `keys()` and `get()`.
      - column_types (dict): Mapping of column names to values in COLTYPE

    Return:
      robject.DataFrame

    Exceptions:
      - StopIteration: If there is no data in the cursor.
    """
    table = []
    colnames, coltypes = [], []
    first = True
    for row in cursor:
        if first:
            for name in row.keys():
                coltypes.append(column_types.get(name, COLTYPE.from_value(row[name])))
                colnames.append(name)

            first = False
        table_row, ignore = [], False
        for (i, name) in enumerate(colnames):
            try:
                value = row[name]
            except KeyError:
                value = COLTYPE.NONE[coltypes[i]]

            table_row.append(value)

        if not ignore:
            table.append(table_row)

    df = make_data_frame(table, colnames, coltypes)
    return df