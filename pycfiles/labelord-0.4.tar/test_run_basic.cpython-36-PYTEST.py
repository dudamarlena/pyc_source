# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sushi/Projects/CTU/MI-PYT_B171/labelord/tests/tests_cli/test_run_basic.py
# Compiled at: 2017-11-22 03:33:06
# Size of source mod 2**32: 1871 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, itertools
MODES = [
 'update', 'replace']
PRINTING = ['--verbose', '--quiet', '-q', '-v', None]

@pytest.mark.parametrize(('mode', 'printing'), itertools.product(MODES, PRINTING))
def test_run_no_token(invoker_norec, mode, printing):
    invocation = invoker_norec('run', mode, printing, isolated=True)
    lines = invocation.result.output.split('\n')
    @py_assert1 = invocation.result
    @py_assert3 = @py_assert1.exit_code
    @py_assert6 = 3
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.result\n}.exit_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(invocation) if 'invocation' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(invocation) else 'invocation',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = []
    @py_assert4 = len(lines)
    @py_assert7 = 2
    @py_assert6 = @py_assert4 == @py_assert7
    @py_assert0 = @py_assert6
    if @py_assert6:
        @py_assert12 = lines[(-1)]
        @py_assert15 = ''
        @py_assert14 = @py_assert12 == @py_assert15
        @py_assert0 = @py_assert14
    if not @py_assert0:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py2':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py3':@pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = '%(py10)s' % {'py10': @py_format9}
        @py_assert1.append(@py_format11)
        if @py_assert6:
            @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert14,), ('%(py13)s == %(py16)s', ), (@py_assert12, @py_assert15)) % {'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15)}
            @py_format19 = '%(py18)s' % {'py18': @py_format17}
            @py_assert1.append(@py_format19)
        @py_format20 = @pytest_ar._format_boolop(@py_assert1, 0) % {}
        @py_format22 = 'assert %(py21)s' % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert0 = @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert12 = @py_assert14 = @py_assert15 = None
    @py_assert0 = lines[0]
    @py_assert3 = 'No GitHub token has been provided'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


@pytest.mark.parametrize(('mode', 'printing'), itertools.product(MODES, PRINTING))
def test_run_no_labels(invoker_norec, utils, mode, printing):
    invocation = invoker_norec('--config', utils.config('config_nolabels'), 'run', mode, printing)
    lines = invocation.result.output.split('\n')
    @py_assert1 = invocation.result
    @py_assert3 = @py_assert1.exit_code
    @py_assert6 = 6
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.result\n}.exit_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(invocation) if 'invocation' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(invocation) else 'invocation',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = []
    @py_assert4 = len(lines)
    @py_assert7 = 2
    @py_assert6 = @py_assert4 == @py_assert7
    @py_assert0 = @py_assert6
    if @py_assert6:
        @py_assert12 = lines[(-1)]
        @py_assert15 = ''
        @py_assert14 = @py_assert12 == @py_assert15
        @py_assert0 = @py_assert14
    if not @py_assert0:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py2':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py3':@pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = '%(py10)s' % {'py10': @py_format9}
        @py_assert1.append(@py_format11)
        if @py_assert6:
            @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert14,), ('%(py13)s == %(py16)s', ), (@py_assert12, @py_assert15)) % {'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15)}
            @py_format19 = '%(py18)s' % {'py18': @py_format17}
            @py_assert1.append(@py_format19)
        @py_format20 = @pytest_ar._format_boolop(@py_assert1, 0) % {}
        @py_format22 = 'assert %(py21)s' % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert0 = @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert12 = @py_assert14 = @py_assert15 = None
    @py_assert0 = lines[0]
    @py_assert3 = 'No labels specification has been found'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


@pytest.mark.parametrize(('mode', 'printing'), itertools.product(MODES, PRINTING))
def test_run_no_repos(invoker_norec, utils, mode, printing):
    invocation = invoker_norec('-c', utils.config('config_norepos'), 'run', mode, printing)
    lines = invocation.result.output.split('\n')
    @py_assert1 = invocation.result
    @py_assert3 = @py_assert1.exit_code
    @py_assert6 = 7
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.result\n}.exit_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(invocation) if 'invocation' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(invocation) else 'invocation',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = []
    @py_assert4 = len(lines)
    @py_assert7 = 2
    @py_assert6 = @py_assert4 == @py_assert7
    @py_assert0 = @py_assert6
    if @py_assert6:
        @py_assert12 = lines[(-1)]
        @py_assert15 = ''
        @py_assert14 = @py_assert12 == @py_assert15
        @py_assert0 = @py_assert14
    if not @py_assert0:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py2':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py3':@pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = '%(py10)s' % {'py10': @py_format9}
        @py_assert1.append(@py_format11)
        if @py_assert6:
            @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert14,), ('%(py13)s == %(py16)s', ), (@py_assert12, @py_assert15)) % {'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15)}
            @py_format19 = '%(py18)s' % {'py18': @py_format17}
            @py_assert1.append(@py_format19)
        @py_format20 = @pytest_ar._format_boolop(@py_assert1, 0) % {}
        @py_format22 = 'assert %(py21)s' % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert0 = @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert12 = @py_assert14 = @py_assert15 = None
    @py_assert0 = lines[0]
    @py_assert3 = 'No repositories specification has been found'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None