# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/grmaster/tests/test_table.py
# Compiled at: 2015-05-28 11:03:40
# Size of source mod 2**32: 5015 bytes
"""Test for `grmaster.Table`."""
from pytest import raises
from grmaster.table import Table, is_empty
import itertools
TABLE_TUPLE = (('Name', 'Surname', 'City'), ('Alex', 'Brown', 'Moscow'), ('John', 'Smith', 'Moscow'),
               ('Эд', 'Wood', 'Hollywood'))
TABLE_STR = '| Name | Surname | City      |\n------------------------------\n| Alex | Brown   | Moscow    |\n| John | Smith   | Moscow    |\n| Эд   | Wood    | Hollywood |'
TABLE_CSV = 'Name,Surname,City\nAlex,Brown,Moscow\nJohn,Smith,Moscow\nЭд,Wood,Hollywood'
TABLE_PARTITION = ((('Alex', 'Brown', 'Moscow'), ('John', 'Smith', 'Moscow')), (('Эд', 'Wood', 'Hollywood'),))

def test_table_new():
    """Table is a tuple, so test `new`, not `init`."""
    table = Table(TABLE_TUPLE)
    assert table.header == TABLE_TUPLE[0]
    assert tuple(table) == TABLE_TUPLE[1:]


def test_table_new_two_tables():
    """Table is a tuple, so test `new`, not `init`."""
    two_tables = itertools.chain(TABLE_TUPLE, (
     ('', ) * len(TABLE_TUPLE[0]),), TABLE_TUPLE[:-1])
    table_one = Table(two_tables)
    assert table_one.header == TABLE_TUPLE[0]
    assert tuple(table_one) == TABLE_TUPLE[1:]
    table_two = Table(two_tables)
    assert table_two.header == TABLE_TUPLE[0]
    assert tuple(table_two) == TABLE_TUPLE[1:-1]


def test_is_empty():
    """Input is a list."""
    assert is_empty(tuple())
    assert is_empty(('', ))
    assert is_empty(('', ''))
    assert is_empty(('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                     '', '', '', ''))
    assert not is_empty(('aba', ''))
    assert not is_empty(('', 'aba'))
    assert is_empty([])
    assert is_empty([''])
    assert is_empty(['', ''])
    assert is_empty(['', ''] * 10)
    assert not is_empty(['aba', ''])
    assert not is_empty(['', 'aba'])


def test_table_from_csv_file(tmpdir):
    """Loading by filename."""
    table_file = tmpdir.join('table.csv')
    table_file.write(TABLE_CSV)
    table = Table.from_csv_file(str(table_file))
    assert table.header == TABLE_TUPLE[0]
    assert tuple(table) == TABLE_TUPLE[1:]


def test_from_csv_str():
    """Loading from string."""
    table = Table.from_csv_str(TABLE_CSV)
    assert table.header == TABLE_TUPLE[0]
    assert tuple(table) == TABLE_TUPLE[1:]


class TestTable:
    __doc__ = 'Test case for `grmaster.Table`.'
    table = None

    def setup(self):
        """Just set up."""
        self.table = Table(TABLE_TUPLE)

    def test_table_str(self):
        """Return markdown table."""
        assert str(self.table) == TABLE_STR

    def test_table_slice(self):
        """Return Table."""
        assert isinstance(self.table[:-1], Table)
        assert tuple(self.table[:-1]) == TABLE_TUPLE[1:-1]

    def test_table_repr(self):
        """Test repr."""
        table_repr = 'Table(' + str(TABLE_TUPLE) + ')'
        assert repr(self.table) == table_repr

    def test_table_immutable(self):
        """Table is immutable."""
        with raises(TypeError):
            self.table[0] = self.table[1]

    def test_table_len(self):
        """Len (without header)."""
        assert len(self.table) == len(TABLE_TUPLE) - 1

    def test_table_eq(self):
        """Two table equal <=> header and body are aequal."""
        other = Table(TABLE_TUPLE)
        assert self.table == other

    def test_table_split(self):
        """Split by column or header."""
        partition = self.table.split_by_column(2)
        sorted_partition = tuple(sorted(tuple(group) for group in partition))
        assert isinstance(partition, list)
        assert isinstance(partition[0], Table)
        assert sorted_partition == TABLE_PARTITION
        partition = self.table.split_by_header('City')
        sorted_partition = tuple(sorted(tuple(group) for group in partition))
        assert sorted_partition == TABLE_PARTITION

    def test_table_to_csv(self):
        """Csv is a string."""
        assert self.table.to_csv() == TABLE_CSV

    def test_table_get_by_column(self):
        """Full test."""
        for row in self.table:
            for j in range(len(row) - 1):
                if not self.table.get_by_column(j, row[j]) == row:
                    raise AssertionError