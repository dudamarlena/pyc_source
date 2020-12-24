# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/twaugh/devel/journal-brief/build/lib/tests/format/test_json.py
# Compiled at: 2015-10-28 06:34:24
# Size of source mod 2**32: 3051 bytes
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
from io import StringIO
from journal_brief.format import get_formatter
import journal_brief.format.json, json, pytest, uuid
from tests.util import maybe_mock_systemd
maybe_mock_systemd()
from systemd import journal

class TestJSONEntryFormatter(object):

    def test_uuid(self):
        """
        Should be string representation of UUID
        """
        entry = {'_BOOT_ID': uuid.uuid1()}
        formatter = get_formatter('json')
        out = json.loads(formatter.format(entry))
        @py_assert0 = out['_BOOT_ID']
        @py_assert4 = entry['_BOOT_ID']
        @py_assert6 = str(@py_assert4)
        @py_assert2 = @py_assert0 == @py_assert6
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None

    def test_timestamp(self):
        """
        Should output microseconds since the epoch
        """
        dt = datetime.fromtimestamp(5, tz=timezone(timedelta(hours=1)))
        entry = {'__REALTIME_TIMESTAMP': dt}
        formatter = get_formatter('json')
        out = json.loads(formatter.format(entry))
        @py_assert0 = out['__REALTIME_TIMESTAMP']
        @py_assert3 = 5000000
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_monotonic(self):
        """
        Should be in microseconds
        """
        us = 700
        elapsed = timedelta(microseconds=us)
        boot_id = uuid.uuid1()
        timestamp = journal.Monotonic((elapsed, boot_id))
        entry = {'__MONOTONIC_TIMESTAMP': timestamp}
        formatter = get_formatter('json')
        out = json.loads(formatter.format(entry))
        @py_assert0 = out['__MONOTONIC_TIMESTAMP']
        @py_assert2 = @py_assert0 == us
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, us)) % {'py3': @pytest_ar._saferepr(us) if 'us' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(us) else 'us',  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None

    @pytest.mark.parametrize(('bdata', 'brepr'), [
     (b'abc', 'abc'),
     (
      b'\x82\xac', [130, 172])])
    def test_bytes(self, bdata, brepr):
        """
        Should decode to unicode or a number array
        """
        entry = {'BDATA': bdata}
        formatter = get_formatter('json')
        out = json.loads(formatter.format(entry))
        @py_assert0 = out['BDATA']
        @py_assert2 = @py_assert0 == brepr
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, brepr)) % {'py3': @pytest_ar._saferepr(brepr) if 'brepr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(brepr) else 'brepr',  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None

    def test_multiline(self):
        """
        Check each entry is formatted as a single output line
        """
        count = 5
        output = StringIO()
        formatter = get_formatter('json')
        for n in range(count):
            output.write(formatter.format({'MESSAGE': 'entry'}))

        output.write(formatter.flush())
        output.seek(0)
        @py_assert2 = output.read
        @py_assert4 = @py_assert2()
        @py_assert6 = @py_assert4.splitlines
        @py_assert8 = @py_assert6()
        @py_assert10 = len(@py_assert8)
        @py_assert12 = @py_assert10 == count
        if not @py_assert12:
            @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.read\n}()\n}.splitlines\n}()\n})\n} == %(py13)s',), (@py_assert10, count)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py11': @pytest_ar._saferepr(@py_assert10),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6),  'py3': @pytest_ar._saferepr(@py_assert2),  'py9': @pytest_ar._saferepr(@py_assert8),  'py13': @pytest_ar._saferepr(count) if 'count' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(count) else 'count',  'py1': @pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output'}
            @py_format16 = ('' + 'assert %(py15)s') % {'py15': @py_format14}
            raise AssertionError(@pytest_ar._format_explanation(@py_format16))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None