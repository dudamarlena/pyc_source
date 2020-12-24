# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.form/test/test_post_error.py
# Compiled at: 2014-05-21 17:45:45
"""
tests to ensure that the appropriate error codes are sent back when something
goes wrong
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from setup_test import setup_store, setup_web
from tiddlyweb.config import config
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
from tiddlyweb.store import NoTiddlerError
import httplib2, cgi
config['system_plugins'] = [
 'tiddlywebplugins.form']

def test_bad_input_error():
    """
    if the form cannot be read, then a 400 should be returned
    """
    store = setup_store()
    setup_web()
    http = httplib2.Http()
    response = http.request('http://test_domain:8001/bags/foo/tiddlers', method='POST', headers={'Content-type': 'multipart/form-data'}, body='title=HelloWorld&text=Hi%20There')[0]
    @py_assert0 = response['status']
    @py_assert3 = '400'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return