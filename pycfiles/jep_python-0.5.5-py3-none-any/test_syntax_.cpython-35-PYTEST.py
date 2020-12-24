# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Work\jep\src\jep-python\build\lib\test\test_syntax_.py
# Compiled at: 2016-01-04 11:02:19
# Size of source mod 2**32: 4098 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from unittest import mock
from jep_py.schema import SyntaxFormatType
from jep_py.syntax import SyntaxFileSet, SyntaxFile

def setup_function(function):
    os.chdir(os.path.join(os.path.dirname(__file__), 'input'))


def test_syntax_file():
    s = SyntaxFile(mock.sentinel.NAME, mock.sentinel.PATH, mock.sentinel.FORMAT, ('ext1',
                                                                                  'ext2'))
    @py_assert1 = s.name
    @py_assert5 = mock.sentinel
    @py_assert7 = @py_assert5.NAME
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.sentinel\n}.NAME\n}', ), (@py_assert1, @py_assert7)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py4': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = s.path
    @py_assert5 = mock.sentinel
    @py_assert7 = @py_assert5.PATH
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.sentinel\n}.PATH\n}', ), (@py_assert1, @py_assert7)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py4': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = s.fileformat
    @py_assert5 = mock.sentinel
    @py_assert7 = @py_assert5.FORMAT
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.fileformat\n} == %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.sentinel\n}.FORMAT\n}', ), (@py_assert1, @py_assert7)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py4': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert2 = s.extensions
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 2
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.extensions\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert0 = 'ext1'
    @py_assert4 = s.extensions
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.extensions\n}', ), (@py_assert0, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'ext2'
    @py_assert4 = s.extensions
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.extensions\n}', ), (@py_assert0, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


def test_syntax_file_definition():
    s = SyntaxFile('mcmake.tmLanguage', 'syntax/mcmake.tmLanguage', SyntaxFormatType.textmate, ('cmake', ))
    d = s.definition
    @py_assert0 = 'string.quoted.double.mcmake'
    @py_assert2 = @py_assert0 in d
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, d)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert2 = len(d)
    @py_assert5 = 2837
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_syntax_file_normalized_extension():
    @py_assert1 = SyntaxFile.normalized_extension
    @py_assert3 = None
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = None
    @py_assert7 = @py_assert5 is @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.normalized_extension\n}(%(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(SyntaxFile) if 'SyntaxFile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SyntaxFile) else 'SyntaxFile', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = SyntaxFile.normalized_extension
    @py_assert3 = '.ext'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 'ext'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.normalized_extension\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(SyntaxFile) if 'SyntaxFile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SyntaxFile) else 'SyntaxFile', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = SyntaxFile.normalized_extension
    @py_assert3 = '.Ext'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 'ext'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.normalized_extension\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(SyntaxFile) if 'SyntaxFile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SyntaxFile) else 'SyntaxFile', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = SyntaxFile.normalized_extension
    @py_assert3 = '.EXT'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 'ext'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.normalized_extension\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(SyntaxFile) if 'SyntaxFile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SyntaxFile) else 'SyntaxFile', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = SyntaxFile.normalized_extension
    @py_assert3 = 'ext'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 'ext'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.normalized_extension\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(SyntaxFile) if 'SyntaxFile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SyntaxFile) else 'SyntaxFile', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = SyntaxFile.normalized_extension
    @py_assert3 = 'Ext'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 'ext'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.normalized_extension\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(SyntaxFile) if 'SyntaxFile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SyntaxFile) else 'SyntaxFile', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = SyntaxFile.normalized_extension
    @py_assert3 = 'EXT'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 'ext'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.normalized_extension\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(SyntaxFile) if 'SyntaxFile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SyntaxFile) else 'SyntaxFile', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_syntax_file_set_empty():
    sfiles = SyntaxFileSet()
    @py_assert1 = not sfiles
    if not @py_assert1:
        @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(sfiles) if 'sfiles' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sfiles) else 'sfiles'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert1 = None
    @py_assert2 = len(sfiles)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(sfiles) if 'sfiles' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sfiles) else 'sfiles', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = sfiles.extension_map
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.extension_map\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(sfiles) if 'sfiles' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sfiles) else 'sfiles'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None


def test_syntax_file_set_add():
    sfiles = SyntaxFileSet()
    sfiles.add(SyntaxFile(mock.sentinel.NAMEA, mock.sentinel.PATHA, mock.sentinel.FORMATA, ('extA1',
                                                                                            'extA2')))
    sfiles.add(SyntaxFile(mock.sentinel.NAMEB, mock.sentinel.PATHB, mock.sentinel.FORMATB, ('extB1',
                                                                                            'extB2')))
    @py_assert2 = len(sfiles)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(sfiles) if 'sfiles' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sfiles) else 'sfiles', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    s = SyntaxFile(mock.sentinel.NAMEB, mock.sentinel.PATHB, mock.sentinel.FORMATB, ('extB1',
                                                                                     'extB2'))
    @py_assert1 = s in sfiles
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (s, sfiles)) % {'py2': @pytest_ar._saferepr(sfiles) if 'sfiles' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sfiles) else 'sfiles', 'py0': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert0 = sfiles.extension_map['exta1']
    @py_assert2 = @py_assert0.path
    @py_assert6 = mock.sentinel
    @py_assert8 = @py_assert6.PATHA
    @py_assert4 = @py_assert2 == @py_assert8
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.path\n} == %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.sentinel\n}.PATHA\n}', ), (@py_assert2, @py_assert8)) % {'py5': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert0 = sfiles.extension_map['exta2']
    @py_assert2 = @py_assert0.path
    @py_assert6 = mock.sentinel
    @py_assert8 = @py_assert6.PATHA
    @py_assert4 = @py_assert2 == @py_assert8
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.path\n} == %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.sentinel\n}.PATHA\n}', ), (@py_assert2, @py_assert8)) % {'py5': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert0 = sfiles.extension_map['extb1']
    @py_assert2 = @py_assert0.path
    @py_assert6 = mock.sentinel
    @py_assert8 = @py_assert6.PATHB
    @py_assert4 = @py_assert2 == @py_assert8
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.path\n} == %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.sentinel\n}.PATHB\n}', ), (@py_assert2, @py_assert8)) % {'py5': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert0 = sfiles.extension_map['extb2']
    @py_assert2 = @py_assert0.path
    @py_assert6 = mock.sentinel
    @py_assert8 = @py_assert6.PATHB
    @py_assert4 = @py_assert2 == @py_assert8
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.path\n} == %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.sentinel\n}.PATHB\n}', ), (@py_assert2, @py_assert8)) % {'py5': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None


def test_syntax_file_set_add_syntax_file():
    sfiles = SyntaxFileSet()
    sfiles.add_syntax_file(mock.sentinel.NAME1, mock.sentinel.PATHA, mock.sentinel.FORMATA, ('extA1',
                                                                                             'extA2'))
    @py_assert2 = len(sfiles)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(sfiles) if 'sfiles' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sfiles) else 'sfiles', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    s = SyntaxFile(mock.sentinel.NAME1, mock.sentinel.PATHA, mock.sentinel.FORMATA, ('extA1',
                                                                                     'extA2'))
    @py_assert1 = s in sfiles
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (s, sfiles)) % {'py2': @pytest_ar._saferepr(sfiles) if 'sfiles' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sfiles) else 'sfiles', 'py0': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_syntax_file_set_remove():
    sfiles = SyntaxFileSet()
    sfiles.add(SyntaxFile(mock.sentinel.NAMEA, mock.sentinel.PATHA, mock.sentinel.FORMATA, ('extA1', 'extA2')))
    sfiles.add(SyntaxFile(mock.sentinel.NAMEB, mock.sentinel.PATHB, mock.sentinel.FORMATB, ('extB1', 'extB2')))
    sfiles.remove(SyntaxFile(mock.sentinel.NAMEB, mock.sentinel.PATHB, mock.sentinel.FORMATB, ('extB1', 'extB2')))
    @py_assert2 = len(sfiles)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(sfiles) if 'sfiles' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sfiles) else 'sfiles', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = mock.sentinel
    @py_assert4 = @py_assert2.NAMEA
    @py_assert7 = mock.sentinel
    @py_assert9 = @py_assert7.PATHA
    @py_assert12 = mock.sentinel
    @py_assert14 = @py_assert12.FORMATA
    @py_assert16 = (
     'extA1', 'extA2')
    @py_assert18 = SyntaxFile(@py_assert4, @py_assert9, @py_assert14, @py_assert16)
    @py_assert20 = @py_assert18 in sfiles
    if not @py_assert20:
        @py_format22 = @pytest_ar._call_reprcompare(('in',), (@py_assert20,), ('%(py19)s\n{%(py19)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.sentinel\n}.NAMEA\n}, %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.sentinel\n}.PATHA\n}, %(py15)s\n{%(py15)s = %(py13)s\n{%(py13)s = %(py11)s.sentinel\n}.FORMATA\n}, %(py17)s)\n} in %(py21)s',), (@py_assert18, sfiles)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py13': @pytest_ar._saferepr(@py_assert12), 'py1': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py10': @pytest_ar._saferepr(@py_assert9), 'py17': @pytest_ar._saferepr(@py_assert16), 'py11': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py8': @pytest_ar._saferepr(@py_assert7), 'py3': @pytest_ar._saferepr(@py_assert2), 'py15': @pytest_ar._saferepr(@py_assert14), 'py21': @pytest_ar._saferepr(sfiles) if 'sfiles' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sfiles) else 'sfiles', 
         'py19': @pytest_ar._saferepr(@py_assert18), 'py0': @pytest_ar._saferepr(SyntaxFile) if 'SyntaxFile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SyntaxFile) else 'SyntaxFile', 'py6': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock'}
        @py_format24 = ('' + 'assert %(py23)s') % {'py23': @py_format22}
        raise AssertionError(@pytest_ar._format_explanation(@py_format24))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = @py_assert20 = None
    @py_assert2 = sfiles.extension_map
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 2
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.extension_map\n})\n} == %(py8)s',), (@py_assert4, @py_assert7)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(sfiles) if 'sfiles' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sfiles) else 'sfiles', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert0 = sfiles.extension_map['exta1']
    @py_assert2 = @py_assert0.path
    @py_assert6 = mock.sentinel
    @py_assert8 = @py_assert6.PATHA
    @py_assert4 = @py_assert2 == @py_assert8
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.path\n} == %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.sentinel\n}.PATHA\n}',), (@py_assert2, @py_assert8)) % {'py5': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert0 = sfiles.extension_map['exta2']
    @py_assert2 = @py_assert0.path
    @py_assert6 = mock.sentinel
    @py_assert8 = @py_assert6.PATHA
    @py_assert4 = @py_assert2 == @py_assert8
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.path\n} == %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.sentinel\n}.PATHA\n}',), (@py_assert2, @py_assert8)) % {'py5': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None


def test_syntax_file_set_filtered():
    s = SyntaxFileSet()
    s1 = SyntaxFile(mock.sentinel.NAME1, mock.sentinel.PATH1, mock.sentinel.FORMATA, ['ext1a', 'ext1b'])
    s2 = SyntaxFile(mock.sentinel.NAME2, mock.sentinel.PATH2, mock.sentinel.FORMATA, ['ext2a', 'ext2b'])
    s.add(s1)
    s.add(s2)
    s.add(SyntaxFile(mock.sentinel.NAME3, mock.sentinel.PATH3, mock.sentinel.FORMATB, ['ext3a', 'ext3b']))
    @py_assert2 = s.filtered
    @py_assert5 = mock.sentinel
    @py_assert7 = @py_assert5.FORMATC
    @py_assert9 = [
     'ext1a', 'ext2a', 'ext3a']
    @py_assert11 = @py_assert2(@py_assert7, @py_assert9)
    @py_assert13 = list(@py_assert11)
    @py_assert15 = not @py_assert13
    if not @py_assert15:
        @py_format16 = ('' + 'assert not %(py14)s\n{%(py14)s = %(py0)s(%(py12)s\n{%(py12)s = %(py3)s\n{%(py3)s = %(py1)s.filtered\n}(%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.sentinel\n}.FORMATC\n}, %(py10)s)\n})\n}') % {'py14': @pytest_ar._saferepr(@py_assert13), 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py1': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py10': @pytest_ar._saferepr(@py_assert9), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert2 = s.filtered
    @py_assert5 = mock.sentinel
    @py_assert7 = @py_assert5.FORMATA
    @py_assert9 = [
     'ext4', 'ext3a', 'ext3b']
    @py_assert11 = @py_assert2(@py_assert7, @py_assert9)
    @py_assert13 = list(@py_assert11)
    @py_assert15 = not @py_assert13
    if not @py_assert15:
        @py_format16 = ('' + 'assert not %(py14)s\n{%(py14)s = %(py0)s(%(py12)s\n{%(py12)s = %(py3)s\n{%(py3)s = %(py1)s.filtered\n}(%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.sentinel\n}.FORMATA\n}, %(py10)s)\n})\n}') % {'py14': @pytest_ar._saferepr(@py_assert13), 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py1': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py10': @pytest_ar._saferepr(@py_assert9), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    f = list(s.filtered(mock.sentinel.FORMATA, ['ext4', 'ext1a', 'ext2b']))
    @py_assert2 = len(f)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = s1 in f
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('in',), (@py_assert1,), ('%(py0)s in %(py2)s',), (s1, f)) % {'py2': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f', 'py0': @pytest_ar._saferepr(s1) if 's1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s1) else 's1'}
        @py_format5 = ('' + 'assert %(py4)s') % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = s2 in f
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('in',), (@py_assert1,), ('%(py0)s in %(py2)s',), (s2, f)) % {'py2': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f', 'py0': @pytest_ar._saferepr(s2) if 's2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s2) else 's2'}
        @py_format5 = ('' + 'assert %(py4)s') % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None