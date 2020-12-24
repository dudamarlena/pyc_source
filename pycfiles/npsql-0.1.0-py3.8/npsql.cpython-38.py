# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/npsql/npsql.py
# Compiled at: 2020-03-13 15:13:35
# Size of source mod 2**32: 34397 bytes
"""
.. module:: npsql.npsql
.. moduleauthor:: Bastiaan Bergman <Bastiaan.Bergman@gmail.com>

"""
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
from .numpy_types import *
from .hashjoin import HashJoinMixin
from .util import ImpError, isstring
try:
    from tabulate import tabulate
except ImpError:

    def tabulate(npsql, columns=None, tablefmt=None):
        """Alt tabulate
        """
        outp = ''
        outp += ' '.join(columns) + '\n'
        for r in npsql:
            outp += str(r) + '\n'
        else:
            return outp


try:
    import os
except ImpError as e:
    try:
        import warnings
        warnings.warn('Dependencies could not be loaded: {}'.format(e))
    finally:
        e = None
        del e

try:
    import csv
except ImpError as e:
    try:
        import warnings
        warnings.warn('Dependencies could not be loaded: {}'.format(e))
    finally:
        e = None
        del e

try:
    import gzip
except ImpError as e:
    try:
        import warnings
        warnings.warn('Dependencies could not be loaded: {}'.format(e))
    finally:
        e = None
        del e

else:
    try:
        import pandas as pd
        PD_PRESENT = True
    except ImpError:
        PD_PRESENT = False
    else:

        def transpose(datastruct):
            """Transpose rows and columns.

    Convenience function. Usually DB connectors return data as a list of
    records, Nptab takes and internally stores data as a list of columns (column
    store). This function will transpose the list of records into a list of
    columns without a priori assuming anything about the datatype of each
    individual element.

    Arguments:
        datastruct (list):
            list or tuple containing lists or tuples with the data for each row.

    Returns:

        transposed datastruct, list containing lists with the data for each
        column.
    """
            shape = (
             len(datastruct), len(datastruct[0]))
            datastruct_out = [[] for i in range(shape[1])]
            for row in datastruct:
                assert len(row) == shape[1]
                for col, c in zip(datastruct_out, row):
                    col.append(c)
                else:
                    return datastruct_out


        T = transpose

        class Nptab(HashJoinMixin):
            __doc__ = 'Nptab datastructure\n\n    Data table with rows and columns, rows are numbered columns are named. Each\n    column has its own datatype. Data is stored by columns (column store), fixed\n    datatype per column, varyiable datatypes from column to column.\n\n    Parameters:\n        datastruct (object) :\n            list, tuple, ndarray or dict of lists, tuples, ndarrays or elements;\n            or a `pandas.DataFrame`. List of columns of data. See :mod:`npsql.T` for\n            a convenience function to transpose a list of records.\n        columns (list of strings) :\n            Column names, ignored when keys are part of the datastruct (dict and\n            `pandas.DataFrame`). Automatic names are generated, if omitted, as\n            strings of column number.\n        copy (boolean) :\n            Wether to make a copy of the data or to reference to the current\n            memory location (when possible), default: True\n\n    Notes:\n\n        1. It is possible to create an empty Nptab instance and later add data\n           using the :mod:`npsql.Nptab.append` and/or\n           :mod:`npsql.Nptab.__setitem__` methods.\n\n        2. It is possibe to add or manipulate data directly through the instance\n           attributes :mod:`npsql.Nptab.columns` and :mod:`npsql.Nptab.data`. One\n           could use the :mod:`npsql.Nptab.valid` method to check wether the\n           manipulated structure is still valid.\n\n        4. If one or more (but not all) of the columns contain a single element\n           this element is repeated to match the length of the other columns.\n\n    Examples:\n\n        To initialize a Nptab, call the constructor with the data in column\n        lists:\n\n            >>> from npsql import Nptab\n            >>> Nptab( [ ["John", "Joe", "Jane"],\n            ...          [1.82, 1.65, 2.15],\n            ...          [False, False, True] ],\n            ...       columns = ["Name", "Height", "Married"])\n             Name   |   Height |   Married\n            --------+----------+-----------\n             John   |     1.82 |         0\n             Joe    |     1.65 |         0\n             Jane   |     2.15 |         1\n            3 rows [\'<U4\', \'<f8\', \'|b1\']\n\n    '
            max_repr_rows = 20
            repr_layout = 'presto'
            join_fill_value = {'float':np.nan, 
             'integer':999999,  'string':''}

            def __init__(self, datastruct=None, columns=None, copy=True):
                self.data = list()
                self.columns = list()
                if datastruct is not None:
                    if hasattr(datastruct, 'items'):
                        datastruct_iter = datastruct.items()
                elif columns is not None:
                    datastruct_iter = zip(columns, datastruct)
                else:
                    if len(datastruct):
                        columns = [str(i) for i in range(len(datastruct))]
                        datastruct_iter = zip(columns, datastruct)
                    else:
                        raise NotImplementedError('datastruct structure could not be resolved')
                stack = []
                for k, v in datastruct_iter:
                    column = self._columnize(v, copy)
                    self.columns.append(k)
                    if len(column) == 1:
                        stack += [(k, v)]
                        self.data.append([])
                    else:
                        self.data.append(column)
                else:
                    for k, v in stack:
                        column = self._columnize(v, copy)
                        c = self.columns.index(k)
                        self.data[c] = column
                    else:
                        if not self.valid:
                            raise ValueError('Invalid Table created.')

            def _columnize(self, value, copy=True):
                if not (isstring(value) or hasattr(value, '__iter__')):
                    value = [
                     value] * max(1, len(self))
                return np.array(value, copy=copy)

            def row_append(self, row):
                """Append a row reccord at the end of the Nptab.

        Appending a single row at the end of the Nptab.

        Arguments:
            row (dict, list, tuple) :
                The row to be appended to the Nptab. If a dict is provided the
                keys should match the column names of the Nptab. If a list or
                tuple is provided the length and order should match the columns
                of the Nptab. columns do not need to match if the current Nptab
                has zero length.
        Returns:
            self. I like chaining/fluent api's and don't care about being pythonic
        """
                if len(self) == 0:
                    self.__init__(row)
                else:
                    if hasattr(row, 'items'):
                        assert set(self.columns) == set(row), 'Not the same columns in Nptab: {} {}'.format(self.columns, row.keys())
                        for col, dta in row.items():
                            ci = self.columns.index(col)
                            self.data[ci] = np.concatenate([self.data[ci], np.array([dta])])

                    else:
                        if len(row) == len(self.columns):
                            for ci, dta in enumerate(row):
                                self.data[ci] = np.concatenate([self.data[ci], np.array([dta])])

                        else:
                            raise ValueError('Number of elements in {row} not equal '.format(row=row), 'to number of columns in Nptab.')
                if not self.valid:
                    raise ValueError('Invalid datastructure.')
                return self

            def append(self, npsql):
                """Append new Nptab to the current Nptab.

        Append a Nptab or pandas.DataFrame to the end of this Nptab. Each column
        is appended to each column of the instance invoking the method.

        Arguments:
            npsql (Nptab) :
                Nptab with the same columns as the current Nptab, order of
                columns does not need to match. Columns do not need to match if
                the current Nptab has zero length. Besides Nptab onjects
                pandas.DataFrame objects are also allowed.

        Returns:
            self. I like chaining/fluent api's and don't care about being pythonic
        """
                if len(self) == 0 and isinstance(npsql, Nptab):
                    self.__init__((npsql.data), columns=(npsql.columns))
                else:
                    if len(self) == 0:
                        self.__init__(npsql)
                    else:
                        if isinstance(npsql, Nptab):
                            assert set(self.columns) == set(npsql.columns), 'Not the same columns in Nptab: {} {}'.format(self.columns, npsql.columns)
                            for col, dta in zip(npsql.columns, npsql.data):
                                ci = self.columns.index(col)
                                self.data[ci] = np.concatenate([self.data[ci], dta])

                        else:
                            if isinstance(npsql, pd.DataFrame):
                                assert set(self.columns) == set(npsql), 'Not the same columns in Nptab: {} {}'.format(self.columns, npsql.keys())
                                for col, dta in npsql.items():
                                    ci = self.columns.index(col)
                                    self.data[ci] = np.concatenate([self.data[ci], dta])

                            else:
                                raise ValueError('Nptab type not recognized.')
                if not self.valid:
                    raise ValueError('Invalid datastructure.')
                return self

            def __iadd__(self, other):
                self.append(other)
                return self

            def _column_index(self, c):
                if not isinstance(c, np.ndarray):
                    try:
                        return self.columns.index(c)
                                    except (TypeError, ValueError) as e:
                        try:
                            pass
                        finally:
                            e = None
                            del e

                    try:
                        c = int(c)
                        assert c < len(self.columns)
                        return c
                                    except (TypeError, ValueError, AssertionError) as e:
                        try:
                            pass
                        finally:
                            e = None
                            del e

                raise ValueError('Not a single, existing column: {}'.format(c))

            def _column_indices(self, c):
                if isinstance(c, (slice, np.ndarray)):
                    try:
                        c = np.arange(len(self.columns))[c]
                        assert np.all(c < len(self.columns))
                        return c
                                    except (ValueError, TypeError,
                 IndexError, AssertionError) as e:
                        try:
                            pass
                        finally:
                            e = None
                            del e

                try:
                    return [self._column_index(ci) for ci in c]
                            except (ValueError, TypeError) as e:
                    try:
                        raise ValueError('Not iterable or existing columns: {}'.format(c))
                    finally:
                        e = None
                        del e

            def __getitem__(self, key):
                """Indexing and slicing parts of a Nptab.

        Slicing and indexing mostly follows Numpy array and Python list
        conventions.

        Arguments:

            key (r, c):
                r can be a single integer, a boolean array, an integer itereable
                or a slice object. c can be a single integer or string, a
                boolean array, an integer or string itereable or a slice object.

            key (int or string) :
                When only a single int is supplied, it is considered to
                point to a whole single row.

                When only a single string is supplied, it is considered to
                point to a whole single column.

        Returns:

            Depending on key, four different types can be returned.

            element ():
                If both the row place and the column place are a single integer
                (or string for the column place), adressing a single element in
                the Nptab, wich could be of any datatype supported by
                Numpy.ndarray.
            column (ndarray):
                If the column place is a single string or integer, adressing a
                single column and the row place is either abscent or not an
                integer.
            row (tuple) :
                If the row place is a single integer, adressing a single row and
                the coumn place is either abscent or not a single integer/string.
            Nptab (Nptab) :
                If a tuple key (r, c) is provided with anything other than an
                integer for the row place and anything other than a single
                integer/string type for the column place.

    Notes:

        Returned Nptab objects from slicing are referenced to the original Nptab
        object unless row indexing was with a boolean list/array or the returned
        type was not a Nptab or np.ndarray object. Changes made to the slice
        will be reflected in the original Nptab. Appending or joining Tabls or
        adding/renaming columns will never be reflected in the original Nptab
        object. Use the `py:copy` function to make a full copy of the object.

    Raises:

        KeyError :
            When a key is referencing an invallid or not existing part of the data.

    Examples:

        >>> npsql[:, 1:3]
           Height |   Married
        ----------+-----------
             1.82 |         0
             1.65 |         0
             2.15 |         1
        3 rows ['<f8', '|b1']

        >>> npsql[0, 0]
        'John'
        >>> npsql["Name"]
        array(['John', 'Joe', 'Jane'], dtype='<U4')
        >>> npsql[0]
        ('John', 1.82, False)
        """
                try:
                    c = self.columns.index(key)
                    return self.data[c]
                            except ValueError as e:
                    try:
                        pass
                    finally:
                        e = None
                        del e

                try:
                    r, c = key
                    return self._getitem(r, c)
                            except (ValueError, TypeError) as e:
                    try:
                        pass
                    finally:
                        e = None
                        del e

                try:
                    r = int(key)
                    return tuple((dt[r] for dt in self.data))
                            except (ValueError, TypeError) as e:
                    try:
                        raise KeyError('Invalid key: {}'.format(key))
                    finally:
                        e = None
                        del e

            def _getitem(self, r, c):
                """Get item from row r and column c

        Arguments:
            r (int, iterable, slice) :
                The row number or numbers to be getting
            c (int, string, iterable, slice)
                The column to be getting
        Returns :

        """
                if not isinstance(r, np.ndarray):
                    try:
                        r = int(r)
                        c = self._column_index(c)
                        return self.data[c][r]
                                    except (ValueError, TypeError) as e:
                        try:
                            pass
                        finally:
                            e = None
                            del e

                try:
                    c = self._column_index(c)
                    return self.data[c][r]
                            except (ValueError, TypeError) as e:
                    try:
                        pass
                    finally:
                        e = None
                        del e

                if not isinstance(r, np.ndarray):
                    try:
                        r = int(r)
                        c = self._column_indices(c)
                        return tuple((self.data[ci][r] for ci in c))
                                    except (ValueError, TypeError) as e:
                        try:
                            pass
                        finally:
                            e = None
                            del e

                try:
                    c = self._column_indices(c)
                    columns = [self.columns[ci] for ci in c]
                    data = [self.data[ci][r] for ci in c]
                    return Nptab(data, columns, copy=False)
                            except (ValueError, TypeError, KeyError) as e:
                    try:
                        raise KeyError('Invalid key provided: ({}, {})'.format(r, c))
                    finally:
                        e = None
                        del e

            def __setitem__(self, key, value):
                """Setting a slice of a Nptab

        Setting, like getting, slices mostly follows numpy conventions.
        Specifically the rules for the key are the same as for
        :mod:`npsql.Nptab.__getitem__` with the same relation between key and
        expected type for the value. In adition this method can also be used to
        add new columns.

        Arguments:

            key (r, c):
                r can be a single integer, a boolean array, an integer
                itereable or a slice object.

                c can be a single integer or string, a boolean array, an integer
                or string itereable or a slice object.

                To adress a single element in the Nptab object the key should be
                a tuple of (r, c) with r a single integer adressing the row and
                c a single integer or string addressing the column of the
                element to be changed.

            key (int or string):
                When only a single int is supplied, it is considered to
                point to a whole single row.

                When only a single string is supplied, it is considered to
                point to a whole single column.

            value (object):
                The type the value needs to have depends on the key provided.

                element:
                    A single element of the same type, or a type convertable to
                    the same, as the column targeted as a destination. See
                    :mod:`npsql.Nptab.dtype` to get the type of the columns.

                column :
                    An array or list of elements, each element of of the same
                    type, or a type convertable to the same, as the column
                    targeted as a destination. If a new column is targeted a
                    single element could be provided, in which case it will be
                    replicated along all rows.

                row :
                    A tuple of elements, each of the same type or a type
                    convertable to the same, as the column targeted as a
                    destination. Length of the tuple should match the number of
                    columns addressed.

                Nptab :
                    Not currently implemented.

        Returns:
            self. I like chaining/fluent api's and don't care about being pythonic

        Notes:

            When changing a column two syntaxes give approximately the same
            result, with, however, a noteable difference. Using a slice object
            ":" will change all elements of the column with the new element(s)
            provided. If just the colum name is provided, with no indication for row,
            than the whole column is replaced with the column provided.

                >>> npsql = Nptab( [ ["John", "Joe", "Jane"], [1.82, 1.65, 2.15],
                ...              [False, False, True] ], columns = ["Name", "Height", "Married"])
                >>> npsql[:, "Name"] = [1, 2, 3]
                >>> npsql
                   Name |   Height |   Married
                --------+----------+-----------
                      1 |     1.82 |         0
                      2 |     1.65 |         0
                      3 |     2.15 |         1
                3 rows ['<U4', '<f8', '|b1']
                >>> npsql["Name"] = [1, 2, 3]
                >>> npsql
                   Name |   Height |   Married
                --------+----------+-----------
                      1 |     1.82 |         0
                      2 |     1.65 |         0
                      3 |     2.15 |         1
                3 rows ['<i8', '<f8', '|b1']

            Note how in the first case the type of the name column stays "<U8"
            while seccond case the type of the Name column changes to "<i8".
        """
                try:
                    c = self.columns.index(key)
                    self.data[c] = self._columnize(value)
                    return self
                            except ValueError as e:
                    try:
                        pass
                    finally:
                        e = None
                        del e

                if isstring(key):
                    self.columns.append(key)
                    self.data.append(self._columnize(value))
                    return self
                try:
                    r, c = key
                    self._setitem(r, c, value)
                    return self
                            except (ValueError, TypeError) as e:
                    try:
                        pass
                    finally:
                        e = None
                        del e

                try:
                    r = int(key)
                    assert len(value) == len(self.columns), 'Value iterable does not match number of columns.'
                    for i, v in enumerate(value):
                        self.data[i][r] = v
                    else:
                        return self

                            except (ValueError, TypeError) as e:
                    try:
                        raise KeyError('Invalid key: {}'.format(key))
                    finally:
                        e = None
                        del e

            def _setitem(self, r, c, value):
                """Set item on row r and column c.

        Arguments:
            r (int, iterable, slice) :
                The row number or numbers to be getting
            c (int, string, iterable, slice)
                The column to be getting
        Returns:
            self. I like chaining/fluent api's and don't care about being pythonic
        """
                try:
                    r = int(r)
                    c = self._column_index(c)
                    self.data[c][r] = value
                    return self
                            except (ValueError, TypeError) as e:
                    try:
                        pass
                    finally:
                        e = None
                        del e

                try:
                    c = self._column_index(c)
                    self.data[c][r] = value
                    return self
                            except (ValueError, TypeError) as e:
                    try:
                        pass
                    finally:
                        e = None
                        del e

                try:
                    r = int(r)
                    c = self._column_indices(c)
                    assert len(c) == len(value), 'Data does not match the addressed row: {}, {}'.format(c, value)
                    for ci, v in zip(c, value):
                        self.data[ci][r] = v
                    else:
                        return self

                            except (ValueError, TypeError) as e:
                    try:
                        pass
                    finally:
                        e = None
                        del e

                try:
                    self[(r, c)]
                    NotImplementedError(('Setting Nptab slices with Nptab ', 'slice is not yet implemented.'))
                except (ValueError, TypeError, KeyError) as e:
                    try:
                        pass
                    finally:
                        e = None
                        del e

                else:
                    raise KeyError('Invalid key provided: ({}, {})'.format(r, c))

            def __delitem__(self, key):
                """Deleting rows or columns from a Nptab.

        Deleting rows or columns can be done using the del keyword.

        Arguments:
            key (int, list of ints, slice or string):

                If the key is a single integer, a list of integers or a slice
                object, then the specified rows will be removed from the Nptab.

                If the key is a single string, then the specified column will be
                removed from the Nptab.

        Returns:
            self. I like chaining/fluent api's and don't care about being pythonic

        Raises:

            IndexError:
                When key is an integer or list of integers that references an
                invalid row.

                Note that no exception is thrown if key is a slice object that
                refers to one or more invalid rows.

            ValueError:
                When key is a string that references an invalid column.

        Notes:

            Because Nptab stores data by columns, this operation requires
            creating new numpy arrays for all columns in the Nptab.

            Examples:
        >>> npsql = Nptab( [ ["John", "Joe", "Jane"], [1.82, 1.65, 2.15],
        ...              [False, False, True] ], columns = ["Name", "Height", "Married"])
        >>> del npsql["Name"]
        >>> del npsql[0]
        >>> npsql
           Height |   Married
        ----------+-----------
             1.65 |         0
             2.15 |         1
        2 rows ['<f8', '|b1']
        >>> del npsql[0:2]
        >>> npsql
         Height   | Married
        ----------+-----------
        0 rows ['<f8', '|b1']
        >>> del npsql['Married']
        >>> npsql
         Height
        ----------
        0 rows ['<f8']
        """
                if isstring(key):
                    c = self.columns.index(key)
                    self.columns.pop(c)
                    self.data.pop(c)
                else:
                    for i in range(len(self.data)):
                        self.data[i] = np.delete(self.data[i], key)
                    else:
                        return self

            def __len__(self):
                if self.data:
                    return max([len(dt) for dt in self.data])
                return 0

            @property
            def shape(self):
                """Nptab shape.

        Returns:

            tuple (r, c) with r the number of rows and c the number of columns.
        """
                if self.data:
                    return (
                     len(self.data[0]), len(self.data))
                return (0, 0)

            def __repr__(self):
                """Pretty print using tabulate.

        Examples:
            >>> npsql = Nptab( [ ["John", "Joe", "Jane"], [1.82, 1.65, 2.15],
            ...          [False, False, True] ], columns = ["Name", "Height", "Married"])
            >>> npsql
             Name   |   Height |   Married
            --------+----------+-----------
             John   |     1.82 |         0
             Joe    |     1.65 |         0
             Jane   |     2.15 |         1
            3 rows ['<U4', '<f8', '|b1']

        """
                npsql = tabulate([[c[r] for c in self.data] for r in range(min(len(self), self.max_repr_rows))],
                  (self.columns),
                  tablefmt=(self.repr_layout))
                len_str = '\n{} rows'.format(len(self))
                typ_str = ' {}'.format([dt.dtype.descr[0][1] for dt in self.data])
                return npsql + len_str + typ_str

            @property
            def dtype(self):
                """List of dtypes of the data columns.
        """
                return np.dtype([(c, dt.dtype) for c, dt in zip(self.columns, self.data)])

            def astype(self, dtypes):
                """Returns a type-converted npsql.

        Converts the npsql according to the provided list of dtypes and returns
        a new Nptab instance.

        Arguments:

            dtypes (list) :
                list of valid numpy dtypes in the order of the columns. List
                should have same length as number of columns present (see
                `Nptab.shape`) See Nptab.dtype for the current types of the
                Nptab.

        Returns:

            Nptab object with the columns converted to the new dtype.

        Examples:

        """
                return Nptab({v.astype(dty):k for k, v, dty in zip(self.columns, self.data, dtypes)})

            @property
            def dict(self):
                """Dump all data as a dict of columns.

        Keywords are the column names and values are the column Numpy.ndarrays.
        Usefull when transferring to a pandas DataFrame.
        """
                return {v:k for k, v in zip(self.columns, self.data)}

            @property
            def valid(self):
                """Check wether the current datastructure is legit.

        Returns:
            (bool) True if the Nptab internal structure is valid.

        Notes:
            This is currently checking for the length of the columns to be the
            same and the number of the columns to be the same as the number of
            column names.
        """
                wid_chk = len(self.columns) == len(self.data)
                len_chk = np.all([len(d) == len(self.data[0]) for d in self.data])
                return wid_chk and len_chk

            def sort(self, columns):
                """Sort the Nptab.

        Sorting in-place the Nptab according to columns provided. Rows always stay together,
        just the order of rows is affectd.

        Arguments:
            columns (string or list) :
                column name or column names to be sorted, listed in-order.

        Returns:
            self. I like chaining/fluent api's and don't care about being pythonic

        Examples:
            >>> npsql = Nptab({'a':['b', 'g', 'd'], 'b':list(range(3))})
            >>> npsql.sort('a')
            >>> npsql
             a   |   b
            -----+-----
             b   |   0
             d   |   2
             g   |   1
            3 rows ['<U1', '<i8']
        """
                columns = columns if hasattr(columns, '__iter__') and not isstring(columns) else [columns]
                ind = np.lexsort([self.data[self.columns.index(c)] for c in columns])
                for i in range(len(self.columns)):
                    self.data[i] = self.data[i][ind]
                else:
                    return self

            def save(self, filename, fmt='auto', header=True):
                """Save to file

        Saves the Nptab data including a header with the column names to a file
        of the specified name in the current directory or the directory
        specified.

        Arguments:
            filename (str) :
                filename, should include path

            fmt (str) :
                formatting, valid values are: 'auto', 'csv', 'npz', 'gz'

                ``auto`` :
                    Determine the filetype from the fiel extension.
                ``csv`` :
                    Write to csv file using pythons `csv` module.
                ``gz`` :
                    Write to csv using pythons `csv` module and zip using
                    standard `gzip` module.
                ``npz`` :
                    Write to compressed `numpy` native binary format.

            header (bool) :
                whether to write a header line with the column names, only used for
                csv and gz

        Returns:
            self. I like chaining/fluent api's and don't care about being pythonic
        """
                if fmt == 'auto':
                    fmt = os.path.splitext(filename)[1].replace('.', '')
                elif fmt == 'csv':
                    with open(filename, 'w') as (f):
                        self._write_csv(f, header)
                else:
                    if fmt == 'gz':
                        with gzip.open(filename, 'wt') as (f):
                            self._write_csv(f, header)
                    else:
                        if fmt == 'npz':
                            (np.savez_compressed)(filename, **)
                        else:
                            raise ValueError('Only formats supported: csv, npz, gz')
                return self

            def _write_csv(self, f, header=True):
                """Writing csv filesself.

        Arguments:
            f (object) :
                file handle
            header (bool) :
                whether to write the columns header
        """
                writer = csv.writer(f)
                if header:
                    writer.writerow(self.columns)
                writer.writerows(zip(*self.data))
                return self


        def read_tabl(filename, fmt='auto', header=True):
            """Read data from disk

    Read data from disk and return a Nptab object.

    Arguments:
        filename (str) :
            filename sring, including path and extension.
        fmt (str) :
            format specifier, supports: 'csv', 'npz', 'gz'.
        header (bool) :
            whether to expect a header (True) or not (False) or try to sniff
            (None), only used for csv and gz

    Returns:
        Nptab object containing the data.
    """
            if fmt == 'auto':
                fmt = os.path.splitext(filename)[1].replace('.', '')
            elif fmt == 'csv':
                with open(filename, 'r') as (f):
                    data = _read_csv(f, header)
            else:
                if fmt == 'gz':
                    with gzip.open(filename, 'rt') as (f):
                        data = _read_csv(f, header)
                else:
                    if fmt == 'npz':
                        reader = np.load(filename)
                        columns = reader.keys()
                        datastruct = [reader[k] for k in columns]
                        data = dict(datastruct=datastruct, columns=columns)
                    else:
                        raise ValueError('Only formats supported: csv, npz, gz')
            return Nptab(**data)


        def _read_csv--- This code section failed: ---

 L. 913         0  LOAD_GLOBAL              _csv_sniff
                2  LOAD_FAST                'f'
                4  CALL_FUNCTION_1       1  ''
                6  UNPACK_SEQUENCE_2     2 
                8  STORE_FAST               'dialect'
               10  STORE_FAST               'sniff_header'

 L. 914        12  LOAD_GLOBAL              csv
               14  LOAD_METHOD              reader
               16  LOAD_FAST                'f'
               18  LOAD_FAST                'dialect'
               20  CALL_METHOD_2         2  ''
               22  STORE_FAST               'reader'

 L. 915        24  LOAD_GLOBAL              next
               26  LOAD_FAST                'reader'
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'columns'

 L. 916        32  LOAD_FAST                'header'
               34  LOAD_CONST               None
               36  COMPARE_OP               is
               38  POP_JUMP_IF_FALSE    44  'to 44'

 L. 917        40  LOAD_FAST                'sniff_header'
               42  STORE_FAST               'header'
             44_0  COME_FROM            38  '38'

 L. 918        44  LOAD_FAST                'header'
               46  POP_JUMP_IF_TRUE     80  'to 80'

 L. 919        48  LOAD_LISTCOMP            '<code_object <listcomp>>'
               50  LOAD_STR                 '_read_csv.<locals>.<listcomp>'
               52  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               54  LOAD_GLOBAL              range
               56  LOAD_GLOBAL              len
               58  LOAD_FAST                'columns'
               60  CALL_FUNCTION_1       1  ''
               62  CALL_FUNCTION_1       1  ''
               64  GET_ITER         
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'columns'

 L. 920        70  LOAD_FAST                'f'
               72  LOAD_METHOD              seek
               74  LOAD_CONST               0
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
             80_0  COME_FROM            46  '46'

 L. 921        80  LOAD_LISTCOMP            '<code_object <listcomp>>'
               82  LOAD_STR                 '_read_csv.<locals>.<listcomp>'
               84  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               86  LOAD_GLOBAL              range
               88  LOAD_GLOBAL              len
               90  LOAD_FAST                'columns'
               92  CALL_FUNCTION_1       1  ''
               94  CALL_FUNCTION_1       1  ''
               96  GET_ITER         
               98  CALL_FUNCTION_1       1  ''
              100  STORE_FAST               'datastruct'

 L. 922       102  LOAD_FAST                'reader'
              104  GET_ITER         
              106  FOR_ITER            142  'to 142'
              108  STORE_FAST               'row'

 L. 923       110  LOAD_GLOBAL              zip
              112  LOAD_FAST                'datastruct'
              114  LOAD_FAST                'row'
              116  CALL_FUNCTION_2       2  ''
              118  GET_ITER         
              120  FOR_ITER            140  'to 140'
              122  UNPACK_SEQUENCE_2     2 
              124  STORE_FAST               'data_col'
              126  STORE_FAST               'c'

 L. 924       128  LOAD_FAST                'data_col'
              130  LOAD_METHOD              append
              132  LOAD_FAST                'c'
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
              138  JUMP_BACK           120  'to 120'
              140  JUMP_BACK           106  'to 106'

 L. 925       142  LOAD_GLOBAL              NP_INT_TYPES
              144  LOAD_GLOBAL              NP_FLOAT_TYPES
              146  BINARY_ADD       
              148  STORE_FAST               'np_types'

 L. 926       150  LOAD_GLOBAL              list
              152  LOAD_GLOBAL              map
              154  LOAD_GLOBAL              np
              156  LOAD_ATTR                array
              158  LOAD_FAST                'datastruct'
              160  CALL_FUNCTION_2       2  ''
              162  CALL_FUNCTION_1       1  ''
              164  STORE_FAST               'datastruct'

 L. 927       166  LOAD_GLOBAL              enumerate
              168  LOAD_FAST                'datastruct'
              170  CALL_FUNCTION_1       1  ''
              172  GET_ITER         
              174  FOR_ITER            242  'to 242'
              176  UNPACK_SEQUENCE_2     2 
              178  STORE_FAST               'i'
              180  STORE_FAST               'data_col'

 L. 928       182  LOAD_FAST                'np_types'
              184  GET_ITER         
              186  FOR_ITER            240  'to 240'
              188  STORE_FAST               'np_type'

 L. 929       190  SETUP_FINALLY       210  'to 210'

 L. 930       192  LOAD_FAST                'data_col'
              194  LOAD_METHOD              astype
              196  LOAD_FAST                'np_type'
              198  CALL_METHOD_1         1  ''
              200  LOAD_FAST                'datastruct'
              202  LOAD_FAST                'i'
              204  STORE_SUBSCR     
              206  POP_BLOCK        
              208  JUMP_FORWARD        234  'to 234'
            210_0  COME_FROM_FINALLY   190  '190'

 L. 931       210  DUP_TOP          
              212  LOAD_GLOBAL              ValueError
              214  COMPARE_OP               exception-match
              216  POP_JUMP_IF_FALSE   232  'to 232'
              218  POP_TOP          
              220  POP_TOP          
              222  POP_TOP          

 L. 932       224  POP_EXCEPT       
              226  JUMP_BACK           186  'to 186'
              228  POP_EXCEPT       
              230  JUMP_FORWARD        234  'to 234'
            232_0  COME_FROM           216  '216'
              232  END_FINALLY      
            234_0  COME_FROM           230  '230'
            234_1  COME_FROM           208  '208'

 L. 933       234  POP_TOP          
              236  CONTINUE            174  'to 174'
              238  JUMP_BACK           186  'to 186'
              240  JUMP_BACK           174  'to 174'

 L. 934       242  LOAD_GLOBAL              dict
              244  LOAD_FAST                'datastruct'
              246  LOAD_FAST                'columns'
              248  LOAD_CONST               ('datastruct', 'columns')
              250  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              252  STORE_FAST               'data'

 L. 935       254  LOAD_FAST                'data'
              256  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 228


        def _csv_sniff(f):
            """
    Sniff using csv module whether or not a csv file (csv or gz) has a header.

    Arguments:
        f (filehandle) :
            filehandle of the file to be read
    """
            sniff_size = 1048575
            dialect = csv.Sniffer().sniff(f.read(sniff_size))
            f.seek(0)
            has_header = csv.Sniffer().has_header(f.read(sniff_size))
            f.seek(0)
            return (dialect, has_header)