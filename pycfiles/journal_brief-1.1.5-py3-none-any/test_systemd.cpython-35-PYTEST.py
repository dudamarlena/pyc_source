# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/twaugh/devel/journal-brief/build/lib/tests/format/test_systemd.py
# Compiled at: 2015-11-03 12:06:59
# Size of source mod 2**32: 1831 bytes
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
import journal_brief.format.systemd
from locale import setlocale, LC_ALL

class TestSystemdEntryFormatter(object):

    def test_no_failed_units(self):
        formatter = get_formatter('systemd')
        @py_assert1 = formatter.flush
        @py_assert3 = @py_assert1()
        @py_assert6 = ''
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.flush\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(formatter) if 'formatter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(formatter) else 'formatter', 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None

    def test_systemd(self):
        setlocale(LC_ALL, 'en_US.UTF-8')
        formatter = get_formatter('systemd')
        base = formatter.FILTER_INCLUSIONS[0].copy()
        for unit in ['unit1', 'unit2', 'unit1', 'Unit3']:
            entry = base.copy()
            entry.update({'MESSAGE': 'Unit %s.service entered failed state.' % unit, 
             'UNIT': '%s.service' % unit})
            @py_assert1 = formatter.format
            @py_assert4 = @py_assert1(entry)
            @py_assert7 = ''
            @py_assert6 = @py_assert4 == @py_assert7
            if not @py_assert6:
                @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.format\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(formatter) if 'formatter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(formatter) else 'formatter', 'py3': @pytest_ar._saferepr(entry) if 'entry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(entry) else 'entry', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1)}
                @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
                raise AssertionError(@pytest_ar._format_explanation(@py_format11))
            @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

        @py_assert1 = formatter.flush
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3.splitlines
        @py_assert7 = @py_assert5()
        @py_assert10 = [
         '', 'Failed systemd units:', '', '    2 x unit1.service', '    1 x unit2.service', '    1 x Unit3.service']
        @py_assert9 = @py_assert7 == @py_assert10
        if not @py_assert9:
            @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.flush\n}()\n}.splitlines\n}()\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py0': @pytest_ar._saferepr(formatter) if 'formatter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(formatter) else 'formatter', 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None