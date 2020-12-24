# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py
# Compiled at: 2019-10-16 12:05:38
# Size of source mod 2**32: 10004 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, io, os, pytest
from paleomix.common.formats.fasta import FASTA, FASTAError
_SEQ_FRAG = 'AAGTCC'

def test_dir():
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def test_file(*args):
    return (os.path.join)(test_dir(), 'data', *args)


def _simple_fasta_record():
    return FASTA('Dummy', 'Meta-inf', 'ACGT')


def test_fasta__constructor__name():
    record = _simple_fasta_record()
    @py_assert1 = record.name
    @py_assert4 = 'Dummy'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=55)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(record) if 'record' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(record) else 'record',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_fasta__constructor__meta():
    record = _simple_fasta_record()
    @py_assert1 = record.meta
    @py_assert4 = 'Meta-inf'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=60)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.meta\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(record) if 'record' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(record) else 'record',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_fasta__constructor__sequence():
    record = _simple_fasta_record()
    @py_assert1 = record.sequence
    @py_assert4 = 'ACGT'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=65)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.sequence\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(record) if 'record' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(record) else 'record',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_fasta__constructor__name_must_be_non_empty():
    with pytest.raises(FASTAError):
        FASTA('', None, 'ACGT')


def test_fasta__constructor__name_must_be_string_type():
    with pytest.raises(FASTAError):
        FASTA(1, None, 'ACGT')


def test_fasta__constructor__name_must_be_string_type_or_none():
    with pytest.raises(FASTAError):
        FASTA('Seq1', 1, 'ACGT')


def test_fasta__constructor__sequence_must_be_string_type():
    with pytest.raises(FASTAError):
        FASTA('Seq1', None, 1)


def test_fasta__repr__partial_line_test():
    expected = '>foobar\n%s\n' % (_SEQ_FRAG,)
    result = repr(FASTA('foobar', None, _SEQ_FRAG))
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=96)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_fasta__repr__complete_line_test():
    expected = '>barfoo\n%s\n' % (_SEQ_FRAG * 10,)
    result = repr(FASTA('barfoo', None, _SEQ_FRAG * 10))
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=102)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_fasta__repr__multiple_lines():
    expected = '>foobar\n%s\n%s\n' % (_SEQ_FRAG * 10, _SEQ_FRAG * 5)
    result = repr(FASTA('foobar', None, _SEQ_FRAG * 15))
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=108)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_fasta__repr__partial_line_test_with_meta_information():
    expected = '>foobar my Meta-Info\n%s\n' % (_SEQ_FRAG,)
    result = repr(FASTA('foobar', 'my Meta-Info', _SEQ_FRAG))
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=114)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_fasta__write__partial_line():
    expected = '>foobar\n%s\n' % (_SEQ_FRAG,)
    stringf = io.StringIO()
    FASTA('foobar', None, _SEQ_FRAG).write(stringf)
    @py_assert1 = stringf.getvalue
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == expected
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=126)
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.getvalue\n}()\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(stringf) if 'stringf' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stringf) else 'stringf',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_fasta__write__complete_line_test():
    expected = '>barfoo\n%s\n' % (_SEQ_FRAG * 10,)
    stringf = io.StringIO()
    FASTA('barfoo', None, _SEQ_FRAG * 10).write(stringf)
    @py_assert1 = stringf.getvalue
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == expected
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=133)
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.getvalue\n}()\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(stringf) if 'stringf' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stringf) else 'stringf',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_fasta__write__multiple_lines():
    expected = '>foobar\n%s\n%s\n' % (_SEQ_FRAG * 10, _SEQ_FRAG * 5)
    stringf = io.StringIO()
    FASTA('foobar', None, _SEQ_FRAG * 15).write(stringf)
    @py_assert1 = stringf.getvalue
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == expected
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=140)
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.getvalue\n}()\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(stringf) if 'stringf' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stringf) else 'stringf',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_fasta__from_lines__no_records():
    @py_assert2 = FASTA.from_lines
    @py_assert4 = []
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = list(@py_assert6)
    @py_assert12 = []
    @py_assert14 = list(@py_assert12)
    @py_assert10 = @py_assert8 == @py_assert14
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=149)
    if not @py_assert10:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.from_lines\n}(%(py5)s)\n})\n} == %(py15)s\n{%(py15)s = %(py11)s(%(py13)s)\n}', ), (@py_assert8, @py_assert14)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_fasta__from_lines_single_record():
    lines = [
     '>single\n', 'TGTTCTCCACCGTGCACAAC\n', 'CCTTCATCCA\n']
    expected = [FASTA('single', None, 'TGTTCTCCACCGTGCACAACCCTTCATCCA')]
    @py_assert2 = FASTA.from_lines
    @py_assert5 = @py_assert2(lines)
    @py_assert7 = list(@py_assert5)
    @py_assert12 = list(expected)
    @py_assert9 = @py_assert7 == @py_assert12
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=155)
    if not @py_assert9:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py3)s\n{%(py3)s = %(py1)s.from_lines\n}(%(py4)s)\n})\n} == %(py13)s\n{%(py13)s = %(py10)s(%(py11)s)\n}', ), (@py_assert7, @py_assert12)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py11':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = None


def test_fasta__from_lines__multiple_records():
    lines = [
     '>first\n',
     'TGTTCTCCACCGTGCACAAC\n',
     'CCTTCATCCA\n',
     '>Second XT:1:0\n',
     'GAGAGCTCAGCTAAC\n',
     '>Third\n',
     'CGCTGACCAAAAACGGACAG\n',
     'GGCATTCGGC\n']
    expected = [
     FASTA('first', None, 'TGTTCTCCACCGTGCACAACCCTTCATCCA'),
     FASTA('Second', 'XT:1:0', 'GAGAGCTCAGCTAAC'),
     FASTA('Third', None, 'CGCTGACCAAAAACGGACAGGGCATTCGGC')]
    @py_assert2 = FASTA.from_lines
    @py_assert5 = @py_assert2(lines)
    @py_assert7 = list(@py_assert5)
    @py_assert12 = list(expected)
    @py_assert9 = @py_assert7 == @py_assert12
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=174)
    if not @py_assert9:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py3)s\n{%(py3)s = %(py1)s.from_lines\n}(%(py4)s)\n})\n} == %(py13)s\n{%(py13)s = %(py10)s(%(py11)s)\n}', ), (@py_assert7, @py_assert12)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py11':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = None


def test_fasta__from_lines__empty_record_name_only__nothing_else():
    with pytest.raises(FASTAError):
        list(FASTA.from_lines(['>fasta1\n']))


def test_fasta__from_lines__empty_record_name_only__first():
    with pytest.raises(FASTAError):
        list(FASTA.from_lines(['>fasta1\n', '>fasta2\n', 'AGTC\n']))


def test_fasta__from_lines__empty_record__middle():
    lines = [
     '>fasta0\n', 'ACGT\n', '>fasta1\n', '>fasta2\n', 'AGTC\n']
    with pytest.raises(FASTAError):
        list(FASTA.from_lines(lines))


def test_fasta__from_lines__empty_record_last():
    lines = [
     '>fasta1\n', 'ACGT\n', '>fasta2\n']
    with pytest.raises(FASTAError):
        list(FASTA.from_lines(lines))


def test_fasta__from_lines__missing_name__alone():
    with pytest.raises(FASTAError):
        list(FASTA.from_lines(['ACGT\n']))


def test_fasta__from_lines__missing_name__with_others():
    with pytest.raises(FASTAError):
        list(FASTA.from_lines(['ACGT\n', '>Foo\n', 'ACGGTA\n']))


def test_fasta__from_lines__empty_name__alone():
    with pytest.raises(FASTAError):
        list(FASTA.from_lines(['>\n', 'ACGT\n']))


def test_fasta__from_lines__empty_name__with_others():
    with pytest.raises(FASTAError):
        list(FASTA.from_lines(['>\n', 'ACGT\n', '>Foo\n', 'ACGGTA\n']))


def test_fasta__from_file__uncompressed():
    expected = [
     FASTA('This_is_FASTA!', None, 'ACGTN'),
     FASTA('This_is_ALSO_FASTA!', None, 'CGTNA')]
    results = list(FASTA.from_file(test_file('fasta_file.fasta')))
    @py_assert1 = results == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=230)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_fasta__from_file__compressed_gz():
    expected = [
     FASTA('This_is_GZipped_FASTA!', None, 'ACGTN'),
     FASTA('This_is_ALSO_GZipped_FASTA!', None, 'CGTNA')]
    results = list(FASTA.from_file(test_file('fasta_file.fasta.gz')))
    @py_assert1 = results == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=239)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_fasta__from_file__compressed_bz2():
    expected = [
     FASTA('This_is_BZ_FASTA!', None, 'CGTNA'),
     FASTA('This_is_ALSO_BZ_FASTA!', None, 'ACGTN')]
    results = list(FASTA.from_file(test_file('fasta_file.fasta.bz2')))
    @py_assert1 = results == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=248)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_fasta__equality():
    @py_assert1 = 'A'
    @py_assert3 = 'B'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'A'
    @py_assert13 = 'B'
    @py_assert15 = 'C'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 == @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=256)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} == %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None


def test_fasta__inequality():
    @py_assert1 = 'A'
    @py_assert3 = 'B'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'A'
    @py_assert13 = 'B'
    @py_assert15 = 'D'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 != @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=260)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} != %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = 'A'
    @py_assert3 = 'B'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'A'
    @py_assert13 = None
    @py_assert15 = 'C'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 != @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=261)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} != %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = 'A'
    @py_assert3 = 'B'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'D'
    @py_assert13 = 'B'
    @py_assert15 = 'C'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 != @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=262)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} != %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None


def test_fasta__sorting_less_equal():
    @py_assert1 = 'A'
    @py_assert3 = 'B'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'A'
    @py_assert13 = 'B'
    @py_assert15 = 'C'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 < @py_assert17
    @py_assert21 = not @py_assert9
    if @py_assert21 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=266)
    if not @py_assert21:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} < %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format22 = 'assert not %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert21 = None
    @py_assert1 = 'A'
    @py_assert3 = 'B'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'B'
    @py_assert13 = 'B'
    @py_assert15 = 'C'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 < @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=267)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} < %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = 'A'
    @py_assert3 = 'B'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'A'
    @py_assert13 = 'C'
    @py_assert15 = 'C'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 < @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=268)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} < %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = 'A'
    @py_assert3 = 'B'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'A'
    @py_assert13 = 'B'
    @py_assert15 = 'D'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 < @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=269)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} < %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = 'A'
    @py_assert3 = 'B'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'A'
    @py_assert13 = 'B'
    @py_assert15 = 'C'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 <= @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=270)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('<=', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} <= %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = 'A'
    @py_assert3 = 'B'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'B'
    @py_assert13 = 'B'
    @py_assert15 = 'C'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 <= @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=271)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('<=', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} <= %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = 'A'
    @py_assert3 = 'B'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'A'
    @py_assert13 = 'C'
    @py_assert15 = 'C'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 <= @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=272)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('<=', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} <= %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = 'A'
    @py_assert3 = 'B'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'A'
    @py_assert13 = 'B'
    @py_assert15 = 'D'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 <= @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=273)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('<=', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} <= %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None


def test_fasta__sorting_greater_equal():
    @py_assert1 = 'A'
    @py_assert3 = 'B'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'A'
    @py_assert13 = 'B'
    @py_assert15 = 'C'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 > @py_assert17
    @py_assert21 = not @py_assert9
    if @py_assert21 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=277)
    if not @py_assert21:
        @py_format19 = @pytest_ar._call_reprcompare(('>', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} > %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format22 = 'assert not %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert21 = None
    @py_assert1 = 'B'
    @py_assert3 = 'B'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'A'
    @py_assert13 = 'B'
    @py_assert15 = 'C'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 > @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=278)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('>', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} > %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = 'A'
    @py_assert3 = 'C'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'A'
    @py_assert13 = 'B'
    @py_assert15 = 'C'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 > @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=279)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('>', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} > %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = 'A'
    @py_assert3 = 'B'
    @py_assert5 = 'D'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'A'
    @py_assert13 = 'B'
    @py_assert15 = 'C'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 > @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=280)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('>', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} > %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = 'A'
    @py_assert3 = 'B'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'A'
    @py_assert13 = 'B'
    @py_assert15 = 'C'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 >= @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=281)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} >= %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = 'B'
    @py_assert3 = 'B'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'A'
    @py_assert13 = 'B'
    @py_assert15 = 'C'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 >= @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=282)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} >= %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = 'A'
    @py_assert3 = 'C'
    @py_assert5 = 'C'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'A'
    @py_assert13 = 'B'
    @py_assert15 = 'C'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 >= @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=283)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} >= %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = 'A'
    @py_assert3 = 'B'
    @py_assert5 = 'D'
    @py_assert7 = FASTA(@py_assert1, @py_assert3, @py_assert5)
    @py_assert11 = 'A'
    @py_assert13 = 'B'
    @py_assert15 = 'C'
    @py_assert17 = FASTA(@py_assert11, @py_assert13, @py_assert15)
    @py_assert9 = @py_assert7 >= @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=284)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} >= %(py18)s\n{%(py18)s = %(py10)s(%(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None


def test_fasta__hash():
    @py_assert2 = 'A'
    @py_assert4 = 'B'
    @py_assert6 = 'C'
    @py_assert8 = FASTA(@py_assert2, @py_assert4, @py_assert6)
    @py_assert10 = hash(@py_assert8)
    @py_assert15 = 'A'
    @py_assert17 = 'B'
    @py_assert19 = 'C'
    @py_assert21 = FASTA(@py_assert15, @py_assert17, @py_assert19)
    @py_assert23 = hash(@py_assert21)
    @py_assert12 = @py_assert10 == @py_assert23
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=288)
    if not @py_assert12:
        @py_format25 = @pytest_ar._call_reprcompare(('==',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py1)s(%(py3)s, %(py5)s, %(py7)s)\n})\n} == %(py24)s\n{%(py24)s = %(py13)s(%(py22)s\n{%(py22)s = %(py14)s(%(py16)s, %(py18)s, %(py20)s)\n})\n}',), (@py_assert10, @py_assert23)) % {'py0':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py1':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py14':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py22':@pytest_ar._saferepr(@py_assert21),  'py24':@pytest_ar._saferepr(@py_assert23)}
        @py_format27 = ('' + 'assert %(py26)s') % {'py26': @py_format25}
        raise AssertionError(@pytest_ar._format_explanation(@py_format27))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = None
    @py_assert2 = 'A'
    @py_assert4 = 'B'
    @py_assert6 = 'C'
    @py_assert8 = FASTA(@py_assert2, @py_assert4, @py_assert6)
    @py_assert10 = hash(@py_assert8)
    @py_assert15 = 'B'
    @py_assert17 = 'B'
    @py_assert19 = 'C'
    @py_assert21 = FASTA(@py_assert15, @py_assert17, @py_assert19)
    @py_assert23 = hash(@py_assert21)
    @py_assert12 = @py_assert10 != @py_assert23
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=289)
    if not @py_assert12:
        @py_format25 = @pytest_ar._call_reprcompare(('!=',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py1)s(%(py3)s, %(py5)s, %(py7)s)\n})\n} != %(py24)s\n{%(py24)s = %(py13)s(%(py22)s\n{%(py22)s = %(py14)s(%(py16)s, %(py18)s, %(py20)s)\n})\n}',), (@py_assert10, @py_assert23)) % {'py0':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py1':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py14':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py22':@pytest_ar._saferepr(@py_assert21),  'py24':@pytest_ar._saferepr(@py_assert23)}
        @py_format27 = ('' + 'assert %(py26)s') % {'py26': @py_format25}
        raise AssertionError(@pytest_ar._format_explanation(@py_format27))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = None
    @py_assert2 = 'A'
    @py_assert4 = 'B'
    @py_assert6 = 'C'
    @py_assert8 = FASTA(@py_assert2, @py_assert4, @py_assert6)
    @py_assert10 = hash(@py_assert8)
    @py_assert15 = 'A'
    @py_assert17 = 'C'
    @py_assert19 = 'C'
    @py_assert21 = FASTA(@py_assert15, @py_assert17, @py_assert19)
    @py_assert23 = hash(@py_assert21)
    @py_assert12 = @py_assert10 != @py_assert23
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=290)
    if not @py_assert12:
        @py_format25 = @pytest_ar._call_reprcompare(('!=',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py1)s(%(py3)s, %(py5)s, %(py7)s)\n})\n} != %(py24)s\n{%(py24)s = %(py13)s(%(py22)s\n{%(py22)s = %(py14)s(%(py16)s, %(py18)s, %(py20)s)\n})\n}',), (@py_assert10, @py_assert23)) % {'py0':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py1':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py14':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py22':@pytest_ar._saferepr(@py_assert21),  'py24':@pytest_ar._saferepr(@py_assert23)}
        @py_format27 = ('' + 'assert %(py26)s') % {'py26': @py_format25}
        raise AssertionError(@pytest_ar._format_explanation(@py_format27))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = None
    @py_assert2 = 'A'
    @py_assert4 = 'B'
    @py_assert6 = 'C'
    @py_assert8 = FASTA(@py_assert2, @py_assert4, @py_assert6)
    @py_assert10 = hash(@py_assert8)
    @py_assert15 = 'A'
    @py_assert17 = 'B'
    @py_assert19 = 'D'
    @py_assert21 = FASTA(@py_assert15, @py_assert17, @py_assert19)
    @py_assert23 = hash(@py_assert21)
    @py_assert12 = @py_assert10 != @py_assert23
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=291)
    if not @py_assert12:
        @py_format25 = @pytest_ar._call_reprcompare(('!=',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py1)s(%(py3)s, %(py5)s, %(py7)s)\n})\n} != %(py24)s\n{%(py24)s = %(py13)s(%(py22)s\n{%(py22)s = %(py14)s(%(py16)s, %(py18)s, %(py20)s)\n})\n}',), (@py_assert10, @py_assert23)) % {'py0':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py1':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py14':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py22':@pytest_ar._saferepr(@py_assert21),  'py24':@pytest_ar._saferepr(@py_assert23)}
        @py_format27 = ('' + 'assert %(py26)s') % {'py26': @py_format25}
        raise AssertionError(@pytest_ar._format_explanation(@py_format27))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = None


def test_fasta__unimplemented_comparison():
    @py_assert3 = 'A'
    @py_assert5 = None
    @py_assert7 = 'C'
    @py_assert9 = FASTA(@py_assert3, @py_assert5, @py_assert7)
    @py_assert11 = @py_assert9.__eq__
    @py_assert13 = 10
    @py_assert15 = @py_assert11(@py_assert13)
    @py_assert1 = NotImplemented is @py_assert15
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=295)
    if not @py_assert1:
        @py_format17 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py16)s\n{%(py16)s = %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py2)s(%(py4)s, %(py6)s, %(py8)s)\n}.__eq__\n}(%(py14)s)\n}', ), (NotImplemented, @py_assert15)) % {'py0':@pytest_ar._saferepr(NotImplemented) if 'NotImplemented' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NotImplemented) else 'NotImplemented',  'py2':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert3 = 'A'
    @py_assert5 = None
    @py_assert7 = 'C'
    @py_assert9 = FASTA(@py_assert3, @py_assert5, @py_assert7)
    @py_assert11 = @py_assert9.__lt__
    @py_assert13 = 10
    @py_assert15 = @py_assert11(@py_assert13)
    @py_assert1 = NotImplemented is @py_assert15
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=296)
    if not @py_assert1:
        @py_format17 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py16)s\n{%(py16)s = %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py2)s(%(py4)s, %(py6)s, %(py8)s)\n}.__lt__\n}(%(py14)s)\n}', ), (NotImplemented, @py_assert15)) % {'py0':@pytest_ar._saferepr(NotImplemented) if 'NotImplemented' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NotImplemented) else 'NotImplemented',  'py2':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert3 = 'A'
    @py_assert5 = None
    @py_assert7 = 'C'
    @py_assert9 = FASTA(@py_assert3, @py_assert5, @py_assert7)
    @py_assert11 = @py_assert9.__le__
    @py_assert13 = 10
    @py_assert15 = @py_assert11(@py_assert13)
    @py_assert1 = NotImplemented is @py_assert15
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=297)
    if not @py_assert1:
        @py_format17 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py16)s\n{%(py16)s = %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py2)s(%(py4)s, %(py6)s, %(py8)s)\n}.__le__\n}(%(py14)s)\n}', ), (NotImplemented, @py_assert15)) % {'py0':@pytest_ar._saferepr(NotImplemented) if 'NotImplemented' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NotImplemented) else 'NotImplemented',  'py2':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert3 = 'A'
    @py_assert5 = None
    @py_assert7 = 'C'
    @py_assert9 = FASTA(@py_assert3, @py_assert5, @py_assert7)
    @py_assert11 = @py_assert9.__ge__
    @py_assert13 = 10
    @py_assert15 = @py_assert11(@py_assert13)
    @py_assert1 = NotImplemented is @py_assert15
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=298)
    if not @py_assert1:
        @py_format17 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py16)s\n{%(py16)s = %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py2)s(%(py4)s, %(py6)s, %(py8)s)\n}.__ge__\n}(%(py14)s)\n}', ), (NotImplemented, @py_assert15)) % {'py0':@pytest_ar._saferepr(NotImplemented) if 'NotImplemented' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NotImplemented) else 'NotImplemented',  'py2':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert3 = 'A'
    @py_assert5 = None
    @py_assert7 = 'C'
    @py_assert9 = FASTA(@py_assert3, @py_assert5, @py_assert7)
    @py_assert11 = @py_assert9.__gt__
    @py_assert13 = 10
    @py_assert15 = @py_assert11(@py_assert13)
    @py_assert1 = NotImplemented is @py_assert15
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/fasta_test.py', lineno=299)
    if not @py_assert1:
        @py_format17 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py16)s\n{%(py16)s = %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py2)s(%(py4)s, %(py6)s, %(py8)s)\n}.__gt__\n}(%(py14)s)\n}', ), (NotImplemented, @py_assert15)) % {'py0':@pytest_ar._saferepr(NotImplemented) if 'NotImplemented' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NotImplemented) else 'NotImplemented',  'py2':@pytest_ar._saferepr(FASTA) if 'FASTA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FASTA) else 'FASTA',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None