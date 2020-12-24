# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/twaugh/devel/journal-brief/build/lib/tests/format/test_config.py
# Compiled at: 2015-11-09 10:35:57
# Size of source mod 2**32: 3791 bytes
"""
Copyright (c) 2015 Tim Waugh <tim@cyberelk.net>

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from tests.util import maybe_mock_systemd
maybe_mock_systemd()
from journal_brief.format import get_formatter
from journal_brief.format.config import EntryCounter
import logging
from uuid import uuid1
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class TestEntryCounter(object):

    def test_get_counts(self):
        reader = [
         {'MESSAGE': 'message 1', 
          'KEY': 'multiple'},
         {'MESSAGE': 'message 1', 
          'KEY': 'multiple'},
         {'MESSAGE': 'message 1'},
         {'MESSAGE': 'message 1'},
         {'MESSAGE': 'message 2', 
          'KEY': 'multiple'},
         {'MESSAGE': 'message 2', 
          'KEY': 'single'}]
        counter = EntryCounter(reader)
        counts = counter.get_counts()
        @py_assert1 = counter.total_entries
        @py_assert6 = len(reader)
        @py_assert3 = @py_assert1 == @py_assert6
        if not @py_assert3:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.total_entries\n} == %(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n}', ), (@py_assert1, @py_assert6)) % {'py5': @pytest_ar._saferepr(reader) if 'reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reader) else 'reader', 'py0': @pytest_ar._saferepr(counter) if 'counter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(counter) else 'counter', 'py4': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert6 = None
        expected = [
         ('MESSAGE', 'message 1', 4),
         ('KEY', 'multiple', 3),
         ('MESSAGE', 'message 2', 2),
         ('KEY', 'single', 1)]
        for exp_field, exp_value, exp_count in expected:
            count = counts.pop(0)
            log.debug('%r: expect %s=%r x %s', count, exp_field, exp_value, exp_count)
            @py_assert1 = count.field
            @py_assert3 = @py_assert1 == exp_field
            if not @py_assert3:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.field\n} == %(py4)s', ), (@py_assert1, exp_field)) % {'py0': @pytest_ar._saferepr(count) if 'count' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(count) else 'count', 'py4': @pytest_ar._saferepr(exp_field) if 'exp_field' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exp_field) else 'exp_field', 'py2': @pytest_ar._saferepr(@py_assert1)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert1 = @py_assert3 = None
            @py_assert2 = count.entries
            @py_assert4 = len(@py_assert2)
            @py_assert6 = @py_assert4 == exp_count
            if not @py_assert6:
                @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.entries\n})\n} == %(py7)s', ), (@py_assert4, exp_count)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(count) if 'count' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(count) else 'count', 'py7': @pytest_ar._saferepr(exp_count) if 'exp_count' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exp_count) else 'exp_count'}
                @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                raise AssertionError(@pytest_ar._format_explanation(@py_format10))
            @py_assert2 = @py_assert4 = @py_assert6 = None
            values = set([entry[exp_field] for entry in count.entries])
            @py_assert2 = len(values)
            @py_assert5 = 1
            @py_assert4 = @py_assert2 == @py_assert5
            if not @py_assert4:
                @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(values) if 'values' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(values) else 'values'}
                @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert2 = @py_assert4 = @py_assert5 = None


class TestDebriefer(object):

    def test_get_exclusions(self):
        reader = [
         {'MESSAGE': 'message 1', 
          'MESSAGE1': 'x', 
          'KEY': 'multiple'},
         {'MESSAGE': 'message 1', 
          'MESSAGE1': 'x', 
          'KEY': 'multiple'},
         {'MESSAGE': 'message 1', 
          'MESSAGE1': 'x'},
         {'MESSAGE': 'message 1', 
          'MESSAGE1': 'x'},
         {'MESSAGE': 'message 2', 
          'KEY': 'multiple'},
         {'MESSAGE': 'message 2', 
          'KEY': 'single'}]
        dbr = get_formatter('config')
        formatted = ''
        for entry in reader:
            formatted += dbr.format(entry)

        formatted += dbr.flush()
        @py_assert2 = '\n'
        @py_assert4 = @py_assert2.join
        @py_assert6 = [
         'exclusions:', '  # 4 occurrences (out of 6)', '  - MESSAGE:', '    - message 1', '    MESSAGE1:', '    - x', '  # 2 occurrences (out of 2)', '  - MESSAGE:', '    - message 2', '']
        @py_assert8 = @py_assert4(@py_assert6)
        @py_assert1 = formatted == @py_assert8
        if not @py_assert1:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.join\n}(%(py7)s)\n}', ), (formatted, @py_assert8)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(formatted) if 'formatted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(formatted) else 'formatted', 'py3': @pytest_ar._saferepr(@py_assert2), 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None

    def test_uuid(self):
        dbr = get_formatter('config')
        message_id = uuid1()
        formatted = dbr.format({'MESSAGE_ID': message_id})
        formatted += dbr.flush()
        @py_assert2 = '\n'
        @py_assert4 = @py_assert2.join
        @py_assert6 = [
         'exclusions:', '  # 1 occurrences (out of 1)', '  - MESSAGE_ID:', '    - {0}'.format(str(message_id)), '']
        @py_assert8 = @py_assert4(@py_assert6)
        @py_assert1 = formatted == @py_assert8
        if not @py_assert1:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.join\n}(%(py7)s)\n}', ), (formatted, @py_assert8)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(formatted) if 'formatted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(formatted) else 'formatted', 'py3': @pytest_ar._saferepr(@py_assert2), 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None