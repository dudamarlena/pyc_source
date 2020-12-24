# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sushi/Projects/CTU/MI-PYT_B171/labelord/tests/tests_web/test_usage_flask.py
# Compiled at: 2017-11-22 03:33:06
# Size of source mod 2**32: 740 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse
import os

def test_flask_run(utils):
    os.environ['LABELORD_CONFIG'] = utils.config('config_3repos_web')
    from labelord import app
    client = Client(app, BaseResponse)
    result = client.get('/')
    @py_assert1 = result.status_code
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = 'master-to-master'
    @py_assert4 = result.data
    @py_assert6 = @py_assert4.decode
    @py_assert8 = 'utf-8'
    @py_assert10 = @py_assert6(@py_assert8)
    @py_assert2 = @py_assert0 in @py_assert10
    if not @py_assert2:
        @py_format12 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.data\n}.decode\n}(%(py9)s)\n}', ), (@py_assert0, @py_assert10)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
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