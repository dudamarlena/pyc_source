# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.form/test/test_post_binary.py
# Compiled at: 2014-05-21 17:45:45
"""
tests to ensure binary tiddlers are uploaded correctly
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from setup_test import setup_store, setup_web
from tiddlyweb.config import config
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.store import NoTiddlerError
import httplib2
config['system_plugins'] = [
 'tiddlywebplugins.form']

def test_upload_binary_file():
    """
    upload a binary file without any meta data
    """
    store = setup_store()
    setup_web()
    http = httplib2.Http()
    binary_data = open('test/test.bmp').read()
    post_data = [
     '-----------------------------984943658114410893',
     'Content-Disposition: form-data; name="file"; filename="test.bmp"',
     'Content-Type: image/bmp',
     '']
    post_data.append(binary_data)
    post_data.append('-----------------------------984943658114410893--')
    post_body = ('\n').join(post_data)
    response = http.request('http://test_domain:8001/bags/foo/tiddlers', method='POST', headers={'Content-type': 'multipart/form-data; boundary=---------------------------984943658114410893', 'Content-Length': '301'}, body=post_body)[0]
    @py_assert1 = response.status
    @py_assert4 = 204
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    tiddler = Tiddler('test.bmp', 'foo')
    try:
        tiddler = store.get(tiddler)
    except NoTiddlerError:
        raise AssertionError('tiddler not put into store')

    @py_assert1 = tiddler.title
    @py_assert4 = 'test.bmp'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.text
    @py_assert3 = @py_assert1 == binary_data
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, binary_data)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(binary_data) if 'binary_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(binary_data) else 'binary_data'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    return


def test_upload_binary_with_meta():
    """
    upload a binary file with some tags and an explicit title
    """
    store = setup_store()
    setup_web()
    http = httplib2.Http()
    binary_data = open('test/test.bmp').read()
    post_data = [
     '-----------------------------984943658114410893',
     'Content-Disposition: form-data; name="title"',
     '',
     'RGBSquare.bmp',
     '-----------------------------984943658114410893',
     'Content-Disposition: form-data; name="tags"',
     '',
     'image bitmap [[test data]]',
     '-----------------------------984943658114410893',
     'Content-Disposition: form-data; name="file"; filename="test.bmp"',
     'Content-Type: image/bmp',
     '']
    post_data.append(binary_data)
    post_data.append('-----------------------------984943658114410893--')
    post_body = ('\n').join(post_data)
    response = http.request('http://test_domain:8001/bags/foo/tiddlers', method='POST', headers={'Content-type': 'multipart/form-data; boundary=---------------------------984943658114410893', 'Content-Length': '301'}, body=post_body)[0]
    @py_assert1 = response.status
    @py_assert4 = 204
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    tiddler = Tiddler('RGBSquare.bmp', 'foo')
    try:
        tiddler = store.get(tiddler)
    except NoTiddlerError:
        raise AssertionError('tiddler not put into store')

    @py_assert1 = tiddler.title
    @py_assert4 = 'RGBSquare.bmp'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.text
    @py_assert3 = @py_assert1 == binary_data
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, binary_data)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(binary_data) if 'binary_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(binary_data) else 'binary_data'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert2 = tiddler.tags
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 3
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.tags\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py8': @pytest_ar._saferepr(@py_assert7), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    for tag in ['image', 'bitmap', 'test data']:
        @py_assert3 = tiddler.tags
        @py_assert1 = tag in @py_assert3
        if not @py_assert1:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py4)s\n{%(py4)s = %(py2)s.tags\n}', ), (tag, @py_assert3)) % {'py0': @pytest_ar._saferepr(tag) if 'tag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tag) else 'tag', 'py2': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None

    return