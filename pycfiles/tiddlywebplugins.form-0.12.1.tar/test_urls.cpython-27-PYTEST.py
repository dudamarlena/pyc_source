# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.form/test/test_urls.py
# Compiled at: 2014-05-21 17:45:45
"""
checks to ensure that all urls have been set up properly 
and POST has been added to all the correct places
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from tiddlyweb.config import config
from setup_test import setup_store, setup_web
from tiddlywebplugins import form
import httplib2

def reset_config():
    """
    reset the plugin and prefix info in config
    ready for next call
    """
    config['system_plugins'] = []
    config['server_prefix'] = ''


def test_override_bag_url():
    """
    check that the /bags/bagname/tiddlers url has been found
    and POST support added
    """
    reset_config()
    setup_store()
    setup_web()
    http = httplib2.Http()
    response = http.request('http://test_domain:8001/bags/foo/tiddlers', method='POST')[0]
    @py_assert1 = response.status
    @py_assert4 = 405
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    config['system_plugins'] = [
     'tiddlywebplugins.form']
    setup_web()
    response = http.request('http://test_domain:8001/bags/foo/tiddlers', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body='title=HelloWorld&text=Hi%20There')[0]
    @py_assert1 = response.status
    @py_assert4 = 204
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_override_recipe_url():
    """
    check that the /recipes/recipename/tidlers url has been found
    and POST support added
    """
    reset_config()
    setup_store()
    setup_web()
    http = httplib2.Http()
    response = http.request('http://test_domain:8001/recipes/foobar/tiddlers', method='POST')[0]
    @py_assert1 = response.status
    @py_assert4 = 405
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    config['system_plugins'] = [
     'tiddlywebplugins.form']
    setup_web()
    response = http.request('http://test_domain:8001/recipes/foobar/tiddlers', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body='title=HelloWorld&text=Hi%20There')[0]
    @py_assert1 = response.status
    @py_assert4 = 204
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_override_server_prefix():
    """
    test that the overriding works when a server prefix is present
    """
    reset_config()
    config['server_prefix'] = '/prefix'
    setup_store()
    setup_web()
    http = httplib2.Http()
    response = http.request('http://test_domain:8001/prefix/bags/foo/tiddlers', method='POST')[0]
    @py_assert1 = response.status
    @py_assert4 = 405
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    config['system_plugins'] = [
     'tiddlywebplugins.form']
    setup_web()
    response = http.request('http://test_domain:8001/prefix/bags/foo/tiddlers', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body='title=HelloWorld&text=Hi%20There')[0]
    @py_assert1 = response.status
    @py_assert4 = 204
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return