# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sushi/Projects/CTU/MI-PYT_B171/labelord/tests/tests_web/test_usage_click.py
# Compiled at: 2017-11-22 03:33:06
# Size of source mod 2**32: 2181 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest

def test_click_run_server(invoker, utils):
    from labelord import app

    def mock_run(host, port, debug, *opts):
        print('Host:', host)
        print('Port:', port)
        print('Debug:', debug)
        print('Opts:', opts)

    app.run = mock_run
    invocation = invoker('--config', utils.config('config_3repos_web'), 'run_server', '--debug', '--host', '127.66.66.66', '--port', '5666')
    lines = invocation.result.output.split('\n')
    @py_assert0 = 'Host: 127.66.66.66'
    @py_assert2 = @py_assert0 in lines
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, lines)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'Port: 5666'
    @py_assert2 = @py_assert0 in lines
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, lines)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'Debug: True'
    @py_assert2 = @py_assert0 in lines
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, lines)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    client = app.test_client()
    result = client.get('/')
    @py_assert1 = result.status_code
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    page = result.data.decode('utf-8')
    @py_assert0 = 'master-to-master'
    @py_assert2 = @py_assert0 in page
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, page)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'MarekSuchanek/pyplayground'
    @py_assert2 = @py_assert0 in page
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, page)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'MarekSuchanek/repocribro'
    @py_assert2 = @py_assert0 in page
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, page)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'MarekSuchanek/labelord'
    @py_assert2 = @py_assert0 not in page
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, page)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'MarekSuchanek/maze'
    @py_assert2 = @py_assert0 in page
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, page)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


@pytest.mark.parametrize('isolated', [True, False])
def test_click_run_server_help(invoker_norec, isolated):
    invocation = invoker_norec('run_server', '--help', isolated=isolated)
    @py_assert1 = invocation.result
    @py_assert3 = @py_assert1.exit_code
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.result\n}.exit_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(invocation) if 'invocation' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(invocation) else 'invocation',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert0 = '-h, --host'
    @py_assert4 = invocation.result
    @py_assert6 = @py_assert4.output
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.result\n}.output\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(invocation) if 'invocation' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(invocation) else 'invocation',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = '-p, --port'
    @py_assert4 = invocation.result
    @py_assert6 = @py_assert4.output
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.result\n}.output\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(invocation) if 'invocation' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(invocation) else 'invocation',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = '-d, --debug'
    @py_assert4 = invocation.result
    @py_assert6 = @py_assert4.output
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.result\n}.output\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(invocation) if 'invocation' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(invocation) else 'invocation',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = '--help'
    @py_assert4 = invocation.result
    @py_assert6 = @py_assert4.output
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.result\n}.output\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(invocation) if 'invocation' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(invocation) else 'invocation',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None