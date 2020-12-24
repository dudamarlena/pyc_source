# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/twaugh/devel/journal-brief/build/lib/tests/format/test_short.py
# Compiled at: 2015-10-28 06:34:24
# Size of source mod 2**32: 2602 bytes
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
from datetime import datetime, timezone, timedelta
from journal_brief.format import get_formatter
import journal_brief.format.short, pytest

class TestShortEntryFormatter(object):

    def test_timestamp(self):
        dt = datetime.fromtimestamp(0, tz=timezone(timedelta(hours=1)))
        entry = {'__REALTIME_TIMESTAMP': dt, 
         'MESSAGE': 'epoch'}
        formatter = get_formatter('short')
        expected = 'Jan 01 01:00:00'
        @py_assert3 = formatter.format
        @py_assert6 = @py_assert3(entry)
        @py_assert1 = expected in @py_assert6
        if not @py_assert1:
            @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s.format\n}(%(py5)s)\n}', ), (expected, @py_assert6)) % {'py5': @pytest_ar._saferepr(entry) if 'entry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(entry) else 'entry', 'py0': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected', 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(formatter) if 'formatter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(formatter) else 'formatter'}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert6 = None

    @pytest.mark.parametrize(('entry', 'expected'), [
     (
      {'MESSAGE': 'message'},
      'localhost ?: message\n'),
     (
      {'_HOSTNAME': 'host', 
       'MESSAGE': 'message'},
      'host ?: message\n'),
     (
      {'_HOSTNAME': 'host', 
       '_COMM': 'comm', 
       'MESSAGE': 'message'},
      'host comm: message\n'),
     (
      {'_HOSTNAME': 'host', 
       '_COMM': 'comm', 
       '_PID': '1', 
       'MESSAGE': 'message'},
      'host comm[1]: message\n'),
     (
      {'_HOSTNAME': 'host', 
       'SYSLOG_IDENTIFIER': 'syslogid', 
       '_COMM': 'comm', 
       'MESSAGE': 'message'},
      'host syslogid: message\n'),
     (
      {'_HOSTNAME': 'host', 
       'SYSLOG_IDENTIFIER': 'syslogid', 
       '_PID': '1', 
       'MESSAGE': 'message'},
      'host syslogid[1]: message\n')])
    def test_format(self, entry, expected):
        entry['__REALTIME_TIMESTAMP'] = datetime.fromtimestamp(0, tz=timezone.utc)
        formatter = get_formatter('short')
        formatted = formatter.format(entry)
        date = 'Jan 01 00:00:00 '
        @py_assert1 = formatted.startswith
        @py_assert4 = @py_assert1(date)
        if not @py_assert4:
            @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}(%(py3)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(formatted) if 'formatted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(formatted) else 'formatted', 'py3': @pytest_ar._saferepr(date) if 'date' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(date) else 'date', 'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None
        @py_assert0 = formatted[len(date):]
        @py_assert2 = @py_assert0 == expected
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, expected)) % {'py3': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected', 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None