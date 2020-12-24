# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/TableList.py
# Compiled at: 2011-02-17 12:03:59
import os, sys, time, types, codecs, gzip, re, inspect, linecache, csv, xml.dom.minidom
from Table import Table
from TableArray import TableArray
import ZODB.DB, persistent
from persistent.list import PersistentList
__all__ = [
 'TableList']

class TableList(persistent.Persistent):

    def __init__(self, *args, **kargs):
        """A list of picalo tables.  Some functions in Picalo return a set
       of tables.  Sets of tables are returned as TableList objects.  
       
       Users do not normally create TableLists.  They are created automatically
       by Picalo functions.
       
       TableLists are a weaker form of TableArrays.  While TableArrays
       must have compatible tables, TableLists can hold tables of
       different schema.  TableLists can be viewed in the Picalo GUI,
       but they cannot be sent into most Picalo functions.
    """
        self.changed = False
        if len(args) == 0:
            self._tables = PersistentList()
        else:
            self._tables = PersistentList(args[0])
        for value in self:
            if not isinstance(value, (Table, TableArray, TableList)):
                raise TypeError, 'This type of list can only hold Picalo Tables, TableArrays, and TableLists.'

    def view(self):
        """Opens the table list for viewing in the Picalo user interface.
       The resulting view allows you to page through the tables in the
       list.  See the first example.
       
       You can view individual tables in the list by using the [n]
       notation.  See the second example for this notation.
       
       Example:
        >>> data = Table([
        ...   ('id', int),
        ...   ('name', unicode),
        ... ],[
        ...   [ 1, 'Benny' ],
        ...   [ 2, 'Vijay' ],
        ... ])
        >>> tables = Grouping.stratify_by_value(data, 'id')
        >>> tables.view()
         
       Example:
        >>> data = Table([
        ...   ('id', int),
        ...   ('name', unicode),
        ... ],[
        ...   [ 1, 'Benny' ],
        ...   [ 2, 'Vijay' ],
        ... ])
        >>> tables = Grouping.stratify_by_value(data, 'id')
        >>> tables[0].view()
         
    """
        from picalo import mainframe
        if mainframe != None:
            f = inspect.currentframe().f_back
            locals = f.f_locals
            for name in f.f_code.co_names:
                if locals.has_key(name) and locals[name] == self:
                    mainframe.openTable(name)
                    return

        print self
        return

    def __repr__(self):
        """For debugging.
       @return:   The number of tables in this TableList.
       @rtype:    str
    """
        return '<TableList of %s: %s>' % (len(self), (', ').join([ repr(t) for t in self._tables ]))

    def __str__(self):
        """For debugging.
       @return:   The number of tables in this TableList.
       @rtype:    str
    """
        return '<TableList of %s: %s>' % (len(self), (', ').join([ str(t) for t in self._tables ]))

    def __iter__(self):
        """Returns an iterator to this TableList"""
        return TableListIterator(self)

    def __contains__(self, table):
        """Returns whether the given table is in this TableArray"""
        if isinstance(table, (Table, TableArray)):
            for item in self:
                if item.get_columns() == table.get_columns() and item == table:
                    return true

        return False

    def __eq__(self, other):
        """Returns whether this TableArray is equal to a list/tuple/TableArray of tables."""
        if other != None and len(self) == len(other):
            for i in range(len(self)):
                if self[i] != other[i]:
                    return False

            return True
        else:
            return False

    def __ne__(self, other):
        """Returns whether this TableArray is not equal to a list/tuple/TableArray of tables."""
        return not self.__eq__(other)

    def __len__(self):
        return len(self._tables)

    def __getitem__(self, index):
        return self._tables[index]

    def __setitem__(self, index, table):
        if not isinstance(table, Table):
            raise TypeError, 'This type of list can only hold Picalo tables.'
        self.changed = True
        self._tables[index] = table

    def __setslice__(self, i, j, sequence):
        for value in sequence:
            if not isinstance(value, Table):
                raise TypeError, 'This type of list can only hold Picalo tables.'

        self.changed = True
        self._table.__setslice__(i, j, sequence)

    def __getslice__(self, i, j):
        return self._table.__getslice__(i, j)

    def append(self, table):
        if not isinstance(table, (Table, TableList, TableArray)):
            raise TypeError, 'This type of list can only hold Picalo tables.'
        self.changed = True
        self._tables.append(table)

    def is_changed(self):
        """Returns whether the table has been changed since loading"""
        if self.changed:
            return True
        for table in self:
            if table.is_changed():
                return True

        return False

    def set_changed(self, changed):
        """Sets whether the class has been changed since loading.  This is not normally
       called by users."""
        self.changed = True

    def set_readonly(self, readonly_flag=False):
        """Sets the read only status of this table.  Tables that are read only cannot
       be modified.  Normally, tables are initially not read only (i.e. can be modified).
       The only exception is tables loaded from databases, which are read only.
       
       @param readonly_flag: True or False, depending upon whether the table should be read only or not.
       @type  readonly_flag: bool
    """
        for table in self:
            table.set_readonly(readonly_flag)

    def is_readonly(self):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def filter(self, expression=None):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def clear_filter(self):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def is_filtered(self):
        """Returns whether the first table in this list is filtered."""
        return False

    def column(self, col):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def get_columns(self):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def get_column_names(self):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def column_count(self):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def set_name(self, column, name):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def set_type(self, column, column_type=None, format=None, expression=None):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def set_format(self, column, format=None):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def append_column(self, name, column_type, values=None):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def insert_column(self, index, name, column_type, values=None):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def append_calculated(self, name, expression):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def insert_calculated(self, index, name, expression):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def append_calculated_static(self, name, column_type, expression):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def insert_calculated_static(self, index, name, column_type, expression):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def move_column(self, column, new_index):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def delete_column(self, column):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def structure(self):
        """This method is not supported in TableLists.  Use TableArrays if this method is required."""
        raise AssertionError, 'This method is not supported in TableLists.'

    def save(self, filename, respect_filter=False):
        """Saves this TableList in native Picalo format.  This is the preferred
       format to save TableLists in because all column types, formulas, and so
       forth are saved.
    
       @param filename: The filename to save to.  This can also be an open stream.
       @type  filename: str
       @param respect_filter Whether to save the entire file or only those rows available through any current filters.
       @type  respect_filter bool
    """
        from Table import save as table_save
        table_save(self, filename, respect_filter)

    def save_delimited(self, filename, delimiter=',', qualifier='"', line_ending='\n', none='', encoding='utf-8', respect_filter=False):
        """Saves this TableList in delimited format.  Since the table list probably has multiple tables
       in it, one delimited file per table is created by prepending 1, 2, 3 to the filename.

       @param filename:     A file name or a file pointer to an open file.  Using the file name string directly is suggested since it ensures the file is opened correctly for reading in CSV.
       @type  filename:     str
       @param delimiter:    An optional field delimiter character
       @type  delimiter:    str
       @param qualifier:    An optional qualifier to use when delimiters exist in field values
       @type  qualifier:    str
       @param line_ending:  An optional line ending to separate rows with
       @type  line_ending:  str
       @param none:         An optional parameter specifying what to write for cells that have the None value.
       @type  none:         str
       @param encoding:     The unicode encoding to use for international or special characters.  For example, Microsoft applications like to use special characters for double quotes rather than the standard characters.  Unicode (the default) handles these nicely.
       @type  encoding:     str
       @param respect_filter Whether to save the entire file or only those rows available through any current filter.
       @type  respect_filter bool
    """
        for (i, table) in enumerate(self):
            table.save_delimited('%05i-' % i + filename, delimiter, qualifier, line_ending, none, encoding, respect_filter)

    def save_csv(self, filename, line_ending='\n', none='', encoding='utf-8', respect_filter=False):
        """Saves this TableList in CSV format.  Since the table list probably has multiple tables
       in it, one CSV per table is created by prepending 1, 2, 3 to the filename.

       @param filename:     A file name or a file pointer to an open file.  Using the file name string directly is suggested since it ensures the file is opened correctly for reading in CSV.
       @type  filename:     str
       @param line_ending:  An optional line ending to separate rows with
       @type  line_ending:  str
       @param none:         An optional parameter specifying what to write for cells that have the None value.
       @type  none:         str
       @param encoding:     The unicode encoding to use for international or special characters.  For example, Microsoft applications like to use special characters for double quotes rather than the standard characters.  Unicode (the default) handles these nicely.
       @type  encoding:     str
       @param respect_filter Whether to save the entire file or only those rows available through any current filter.
       @type  respect_filter bool
    """
        for (i, table) in enumerate(self):
            table.save_csv('%05i-' % i + filename, line_ending, none, encoding, respect_filter)

    def save_tsv(self, filename, line_ending='\n', none='', encoding='utf-8', respect_filter=False):
        """Saves this TableList in tsv format.  Since the table list probably has multiple tables
       in it, one tsv file per table is created by prepending 1, 2, 3 to the filename.

       @param filename:     A file name or a file pointer to an open file.  Using the file name string directly is suggested since it ensures the file is opened correctly for reading in CSV.
       @type  filename:     str
       @param line_ending:  An optional line ending to separate rows with
       @type  line_ending:  str
       @param none:         An optional parameter specifying what to write for cells that have the None value.
       @type  none:         str
       @param encoding:     The unicode encoding to use for international or special characters.  For example, Microsoft applications like to use special characters for double quotes rather than the standard characters.  Unicode (the default) handles these nicely.
       @type  encoding:     str
    """
        for (i, table) in enumerate(self):
            table.save_tsv('%05i-' % i + filename, line_ending, none, encoding, respect_filter)

    def save_fixed(self, filename, line_ending='\n', none='', respect_filter=False):
        """Saves this TableList in fixed format.  Since the table list probably has multiple tables
       in it, one fixed file per table is created by prepending 1, 2, 3 to the filename.

       @param filename:     A file name or a file pointer to an open file.  Using the file name string directly is suggested since it ensures the file is opened correctly for reading in CSV.
       @type  filename:     str
       @param line_ending:  An optional line ending to separate rows with
       @type  line_ending:  str
       @param none:         An optional parameter specifying what to write for cells that have the None value.
       @type  none:         str
       @param respect_filter Whether to save the entire file or only those rows available through any current filter.
       @type  respect_filter bool
    """
        for (i, table) in enumerate(self):
            table.save_fixed('%05i-' % i + filename, line_ending, none, respect_filter)

    def save_xml(self, filename, line_ending='\n', indent='\t', compact=False, none='', respect_filter=False):
        """Saves this TableList in xml format.  Since the table list probably has multiple tables
       in it, one xml file per table is created by prepending 1, 2, 3 to the filename.

       @param filename:     A file name or a file pointer to an open file.  Using the file name string directly is suggested since it ensures the file is opened correctly for reading in CSV.
       @type  filename:     str
       @param line_ending:  An optional line ending to separate rows with (when compact is False)
       @type  line_ending:  str
       @param indent:       The character(s) to use for indenting (when compact is False)
       @type  indent:       str
       @param compact:      Whether to compact the XML or make it "pretty" with whitespace
       @type  compact:      bool
       @param none:         An optional parameter specifying what to write for cells that have the None value.
       @type  none:         str
       @param respect_filter Whether to save the entire file or only those rows available through any current filter.
       @type  respect_filter bool
    """
        for (i, table) in enumerate(self):
            table.save_xml('%05i-' % i + filename, line_ending, indent, compact, none, respect_filter)


def TableListIterator(ta):
    """Returns a generator object to iterate over the tables in a TableList"""
    index = 0
    numcols = len(ta)
    while index < numcols:
        yield ta[index]
        index += 1