# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/Record.py
# Compiled at: 2011-03-14 13:31:39
from picalo import check_valid_table
from Error import error
import types, ZODB.DB, persistent
from persistent.dict import PersistentDict
from persistent.list import PersistentList

class Record(persistent.Persistent):
    """An individual record of a Table. Individual fields in a record can be accessed 
     via column number or name.  In the table above, this is done with the following:
       >>> rec1 = mytable3[0]
       >>> print rec1[1]
       'Bart'
       >>> print rec1['Name'] 
       'Bart'
  """

    def __init__(self, table):
        """Called by Table's append or insert method.  Do not create Records directly.
       table         => The Picalo table that owns this record
    """
        assert table != None, 'The table cannot be None when creating a record.'
        self.__dict__['_table'] = table
        self.__dict__['_rowdata'] = PersistentList()
        return

    def __repr__(self):
        """Returns a quick view of this record.  Provide mostly for debugging purposes."""
        return '<Record: [%s]>' % (', ').join([ str(self[i]) for i in range(len(self.__dict__['_table'].columns)) ])

    def __str__(self):
        """Returns a quick view of this record.  Provide mostly for debugging purposes."""
        return '<Record: [%s]>' % (', ').join([ str(self[i]) for i in range(len(self.__dict__['_table'].columns)) ])

    def __iter__(self):
        """Returns an iterator to this record (using the table's column order)"""
        return RecordIterator(self)

    def __contains__(self, item):
        """Returns whether the given item is in the record"""
        for value in self:
            try:
                if item in value:
                    return True
            except TypeError:
                if item == value:
                    return True

        return False

    def __eq__(self, other):
        """Returns whether this record is equal to a list/tuple/record of values.
       The other parameter can be a record of this table, a record of another table,
       or any list-like object.  Only the values are compared -- the column names
       don't have to match (but the number of columns must be the same).
    """
        if other != None and len(self) == len(other):
            for i in range(len(self)):
                if self[i] != other[i]:
                    return False

            return True
        else:
            return False

    def __ne__(self, other):
        """Returns whether this record is not equal to a list/tuple/record of values.
       The other parameter can be a record of this table, a record of another table,
       or any list-like object.  Only the values are compared -- the column names
       don't have to match (but the number of columns must be the same).
    """
        return not self.__eq__(other)

    def __len__(self):
        """Returns the length of this record"""
        return self._table.column_count()

    def has_key(self, key):
        """Returns whether the record has the given column name"""
        return self._table.columns_map_names.has_key(key)

    def __getattribute__(self, col):
        """Retrieves the value of a field in the record.  This method allows
       record.colname type of access to values.  
       
       @param col: The column name or index
       @type  col: str
       @return:    The value in the given field
       @rtype:     returns
    """
        if object.__getattribute__(self, '__dict__').has_key('_table') and object.__getattribute__(self, '_table').columns_map_names.has_key(col):
            return object.__getattribute__(self, '__get_value__')(col, [])
        try:
            return persistent.Persistent.__getattribute__(self, col)
        except AttributeError:
            raise AttributeError('This table has no column named "%s"' % col)

    def __getitem__(self, col):
        """Retrieves the value of a field in the record.  This method allows
       record['colname'] type of access to values.
       
       @param col: The column name or index
       @type  col: str
       @return:    The value in the given field
       @rtype:     returns
    """
        return self.__get_value__(col, [])

    def __get_value__(self, col, expression_backtrack):
        """Internal method to retrieve the value of a cell.
       col                  => The column name or index
       expression_backtrack => A list of expression ids that have been run so far, to catch circular formulas
    """
        if isinstance(col, types.SliceType):
            return [ self.__getitem__(col.name) for col in self._table.columns[col] ]
        else:
            if not isinstance(col, int):
                if col not in self._table.columns_map_names:
                    raise AttributeError('This table has no column named "%s"' % col)
                col = self._table.columns_map_names[col]
            else:
                origcol = col
                if col < 0:
                    col += self._table.num_columns
                if col >= self._table.num_columns or col < 0:
                    raise IndexError('Column index [%s] is out of range.  The table only has %s columns, referenced with [0] to [%s] or [-1] to [-%s].' % (origcol, self._table.num_columns, self._table.num_columns - 1, self._table.num_columns))
                col = self._table.columns_map_virtual[col]
            coldef = self._table.columns[col]
            if coldef.expression:
                return coldef.expression.evaluate([{'record': self}, self], expression_backtrack)
            if col < len(self.__dict__['_rowdata']):
                return self.__dict__['_rowdata'][col]
            return
            return

    def __setattr__(self, col, value):
        """Sets the value of a field in the record.
      
       @param col:   The column name or index
       @type  col:   str/int
       @param value: The value to save in the field
       @type  value: value
    """
        if isinstance(col, (int, long)) or self._table.columns_map_names.has_key(col):
            self.__setitem__(col, value)
        persistent.Persistent.__setattr__(self, col, value)

    def __setitem__(self, col, value):
        """Sets the value of a field in the record.
      
       @param col:   The column name or index
       @type  col:   str/int
       @param value: The value to save in the field
       @type  value: value
    """
        assert not self._table.is_readonly(), 'This table is set as read-only and cannot be modified.'
        if isinstance(col, types.SliceType):
            for i in range(self._table.deref_column(col.start), self._table.deref_column(col.stop)):
                valueidx = i - self._table.deref_column(col.start)
                if valueidx >= 0 and valueidx < len(value):
                    self.__setitem__(i, value[valueidx])

            return
        else:
            if not isinstance(col, int):
                if col not in self._table.columns_map_names:
                    raise IndexError('This table has no column named %s' % col)
                col = self._table.columns_map_names[col]
            else:
                origcol = col
                if col < 0:
                    col += self._table.num_columns
                if col >= self._table.num_columns or col < 0:
                    raise IndexError('Column index [%s] is out of range.  The table only has %s columns, referenced with [0] to [%s] or [-1] to [-%s].' % (origcol, self._table.num_columns, self._table.num_columns - 1, self._table.num_columns))
                col = self._table.columns_map_virtual[col]
            coldef = self._table.columns[col]
            if value != None and not isinstance(value, coldef.column_type):
                try:
                    value = coldef.parse_value(value)
                except Exception, e:
                    value = error(e)

            self._table._invalidate_indexes()
            while len(self.__dict__['_rowdata']) <= col:
                self.__dict__['_rowdata'].append(None)

            self.__dict__['_rowdata'][col] = value
            self._table._notify_listeners()
            return

    def __setslice__(self, i, j, values):
        """Sets the value of several items in this record.  Use slice notation:
       table[rec][0:2] = [ 1, 2 ]   # sets first two items
       
       @param i:  The starting index (inclusive)
       @type  i:  int
       @param j:  The ending index (exclusive)
       @type  j:  int
       @param values: A sequence of values to set
       @type  values: list or tuple
    """
        self.__setitem__(slice(i, j), values)


def RecordIterator(record):
    """Returns a generator object to iterate over the columns of a record"""
    index = 0
    numcols = len(record._table.columns)
    while index < numcols:
        yield record[index]
        index += 1