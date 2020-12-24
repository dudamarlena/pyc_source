# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/twaugh/devel/journal-brief/build/lib/tests/format/test_reboot.py
# Compiled at: 2015-10-28 06:34:24
# Size of source mod 2**32: 1226 bytes
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
from journal_brief.format import get_formatter
import journal_brief.format.reboot

class TestRebootEntryFormatter(object):

    def test_reboot(self):
        formatter = get_formatter('reboot')
        @py_assert1 = formatter.format
        @py_assert3 = {'_BOOT_ID': '1'}
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = ''
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.format\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(formatter) if 'formatter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(formatter) else 'formatter',  'py2': @pytest_ar._saferepr(@py_assert1),  'py4': @pytest_ar._saferepr(@py_assert3),  'py9': @pytest_ar._saferepr(@py_assert8),  'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        @py_assert1 = formatter.format
        @py_assert3 = {'_BOOT_ID': '2'}
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = '-- Reboot --\n'
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.format\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(formatter) if 'formatter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(formatter) else 'formatter',  'py2': @pytest_ar._saferepr(@py_assert1),  'py4': @pytest_ar._saferepr(@py_assert3),  'py9': @pytest_ar._saferepr(@py_assert8),  'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        @py_assert1 = formatter.format
        @py_assert3 = {'_BOOT_ID': '2'}
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = ''
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.format\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(formatter) if 'formatter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(formatter) else 'formatter',  'py2': @pytest_ar._saferepr(@py_assert1),  'py4': @pytest_ar._saferepr(@py_assert3),  'py9': @pytest_ar._saferepr(@py_assert8),  'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        @py_assert1 = formatter.flush
        @py_assert3 = @py_assert1()
        @py_assert6 = ''
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.flush\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(formatter) if 'formatter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(formatter) else 'formatter',  'py2': @pytest_ar._saferepr(@py_assert1),  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None