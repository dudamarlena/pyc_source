# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/tests/test_errors.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 724 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from cms_qe_test.cms import create_page

def test_page_found(client):
    create_page('Test page', page_params={'slug': 'test'})
    html = client.get('/en/test/').content
    @py_assert0 = b'<h1>Generic error</h1>'
    @py_assert2 = @py_assert0 not in html
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, html)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(html) if 'html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(html) else 'html'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = b'<title>Test page</title>'
    @py_assert2 = @py_assert0 in html
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, html)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(html) if 'html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(html) else 'html'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_page_not_found(client):
    html = client.get('/en/non-existing-page/').content
    @py_assert0 = b'<h1>Generic error</h1>'
    @py_assert2 = @py_assert0 in html
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, html)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(html) if 'html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(html) else 'html'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = b'error404'
    @py_assert2 = @py_assert0 in html
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, html)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(html) if 'html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(html) else 'html'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_page_not_found_custom_by_cms(client):
    create_page('custom page not found', page_params={'slug': 'error404'})
    html = client.get('/en/non-existing-page/').content
    @py_assert0 = b'<h1>Generic error</h1>'
    @py_assert2 = @py_assert0 not in html
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, html)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(html) if 'html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(html) else 'html'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = b'<title>custom page not found</title>'
    @py_assert2 = @py_assert0 in html
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, html)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(html) if 'html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(html) else 'html'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None