# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sushi/Projects/CTU/MI-PYT_B171/labelord/tests/tests_cli/test_list_labels.py
# Compiled at: 2017-11-22 03:33:06
# Size of source mod 2**32: 3243 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar

def test_list_normal(invoker, utils):
    invocation = invoker('--config', (utils.config('config_token')), 'list_labels',
      'MarekSuchanek/repo1', session_expectations={'get': 1})
    lines = invocation.result.output.split('\n')
    labels01 = ['#ee0701 bug',
     '#b495a9 core idea',
     '#cccccc duplicate',
     '#84b6eb enhancement',
     '#bfdadc experience',
     '#b495a9 extension idea',
     '#128A0C help wanted',
     '#cccccc invalid',
     '#cccccc on hold',
     '#84b6eb optimization',
     '#cc317c question',
     '#cccccc wontfix']
    @py_assert1 = invocation.result
    @py_assert3 = @py_assert1.exit_code
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.result\n}.exit_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(invocation) if 'invocation' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(invocation) else 'invocation',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = []
    @py_assert4 = len(lines)
    @py_assert7 = 13
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
    for label in labels01:
        @py_assert1 = label in lines
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (label, lines)) % {'py0':@pytest_ar._saferepr(label) if 'label' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(label) else 'label',  'py2':@pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None


def test_list_no_token(invoker_norec):
    invocation = invoker_norec('list_labels', 'MarekSuchanek/repo1', isolated=True)
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


def test_list_bad_credentials(invoker, utils):
    invocation = invoker('-c', (utils.config('config_token')), 'list_labels',
      'MarekSuchanek/repo1', session_expectations={'get': 1})
    lines = invocation.result.output.split('\n')
    @py_assert1 = invocation.result
    @py_assert3 = @py_assert1.exit_code
    @py_assert6 = 4
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
    @py_assert3 = 'GitHub: ERROR 401 - Bad credentials'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_list_unexisting_repo(invoker, utils):
    invocation = invoker('--config', (utils.config('config_token')), 'list_labels',
      'MarekSuchanek/repo2', session_expectations={'get': 1})
    lines = invocation.result.output.split('\n')
    @py_assert1 = invocation.result
    @py_assert3 = @py_assert1.exit_code
    @py_assert6 = 5
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
    @py_assert3 = 'GitHub: ERROR 404 - Not Found'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_list_more_than_hundred(invoker, utils):
    invocation = invoker('-c', (utils.config('config_token')), 'list_labels',
      'MarekSuchanek/repo3', session_expectations={'get': 2})
    lines = invocation.result.output.split('\n')
    @py_assert1 = invocation.result
    @py_assert3 = @py_assert1.exit_code
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.result\n}.exit_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(invocation) if 'invocation' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(invocation) else 'invocation',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = []
    @py_assert4 = len(lines)
    @py_assert7 = 155
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
    for i in range(154):
        @py_assert0 = '#ABC{} label{}'
        @py_assert2 = @py_assert0.format
        @py_assert5 = 100
        @py_assert7 = i + @py_assert5
        @py_assert9 = @py_assert2(@py_assert7, i)
        @py_assert11 = @py_assert9 in lines
        if not @py_assert11:
            @py_format13 = @pytest_ar._call_reprcompare(('in', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py3)s\n{%(py3)s = %(py1)s.format\n}((%(py4)s + %(py6)s), %(py8)s)\n} in %(py12)s', ), (@py_assert9, lines)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines'}
            @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
            raise AssertionError(@pytest_ar._format_explanation(@py_format15))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None