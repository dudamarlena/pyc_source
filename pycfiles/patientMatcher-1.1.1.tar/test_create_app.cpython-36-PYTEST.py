# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chiararasi/Documents/work/GITs/patientMatcher/tests/server/test_create_app.py
# Compiled at: 2019-04-23 03:57:58
# Size of source mod 2**32: 157 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar

def test_create_app(mock_app):
    """Tests the function that creates the app"""
    @py_assert1 = mock_app.client
    if not @py_assert1:
        @py_format3 = 'assert %(py2)s\n{%(py2)s = %(py0)s.client\n}' % {'py0':@pytest_ar._saferepr(mock_app) if 'mock_app' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_app) else 'mock_app',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert1 = mock_app.db
    if not @py_assert1:
        @py_format3 = 'assert %(py2)s\n{%(py2)s = %(py0)s.db\n}' % {'py0':@pytest_ar._saferepr(mock_app) if 'mock_app' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_app) else 'mock_app',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None