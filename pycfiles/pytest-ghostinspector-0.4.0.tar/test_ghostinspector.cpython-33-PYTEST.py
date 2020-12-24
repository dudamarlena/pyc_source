# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jluker/projects/pytest-ghostinspector/tests/test_ghostinspector.py
# Compiled at: 2016-05-17 11:50:55
# Size of source mod 2**32: 5602 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from pytest_httpretty import stub_get

def test_help_message(testdir):
    result = testdir.runpytest('--help')
    result.stdout.fnmatch_lines([
     'ghostinspector:'])


def test_key_option(testdir):
    config = testdir.parseconfig('--gi_key=foo')
    @py_assert1 = config.option
    @py_assert3 = @py_assert1.gi_key
    @py_assert6 = 'foo'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.option\n}.gi_key\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    return


def test_start_url_option(testdir):
    config = testdir.parseconfig('--gi_start_url=bar')
    @py_assert1 = config.option
    @py_assert3 = @py_assert1.gi_start_url
    @py_assert6 = 'bar'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.option\n}.gi_start_url\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    return


def test_suite_option(testdir):
    config = testdir.parseconfig()
    @py_assert1 = config.option
    @py_assert3 = @py_assert1.gi_suite
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.option\n}.gi_suite\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    config = testdir.parseconfig('--gi_suite=abc123', '--gi_suite=def456')
    @py_assert1 = config.option
    @py_assert3 = @py_assert1.gi_suite
    @py_assert6 = [
     'abc123', 'def456']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.option\n}.gi_suite\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    return


def test_test_option(testdir):
    config = testdir.parseconfig()
    @py_assert1 = config.option
    @py_assert3 = @py_assert1.gi_test
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.option\n}.gi_test\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    config = testdir.parseconfig('--gi_test=xyz789')
    @py_assert1 = config.option
    @py_assert3 = @py_assert1.gi_test
    @py_assert6 = [
     'xyz789']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.option\n}.gi_test\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    return


def test_param_option(testdir):
    config = testdir.parseconfig()
    @py_assert1 = config.option
    @py_assert3 = @py_assert1.gi_param
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.option\n}.gi_param\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    config = testdir.parseconfig('--gi_param=foo=bar', '--gi_param=baz=blerg')
    @py_assert1 = config.option
    @py_assert3 = @py_assert1.gi_param
    @py_assert6 = [
     'foo=bar', 'baz=blerg']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.option\n}.gi_param\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    return


@pytest.mark.httpretty
def test_cmdline_empty_suite(testdir, gi_api_suite_tests_re):
    stub_get(gi_api_suite_tests_re, body='{ "data": [] }', content_type='application/json')
    result = testdir.runpytest('--gi_key=foo', '--gi_suite=abc123')
    result.stdout.fnmatch_lines([
     'collected 0 items'])


@pytest.mark.httpretty
def test_cmdline_404_suite(testdir, gi_api_suite_tests_re):
    stub_get(gi_api_suite_tests_re, body='{ "errorType": "VALIDATION_ERROR", "message": "Suite not found" }', content_type='application/json')
    result = testdir.runpytest('--gi_key=foo', '--gi_suite=abc123')
    result.stdout.fnmatch_lines([
     'Ghost Inspector API returned error: Suite not found'])


@pytest.mark.httpretty
def test_cmdline_collect_suite(testdir, suite_resp, gi_api_suite_tests_re):
    stub_get(gi_api_suite_tests_re, body=suite_resp, content_type='application/json')
    result = testdir.runpytest('--collect-only', '--gi_key=foo', '--gi_suite=abc123')
    result.stdout.fnmatch_lines([
     'collected 2 items',
     "*GITestItem*'test 1'*",
     "*GITestItem*'test 2'*"])


@pytest.mark.httpretty
def test_cmdline_collect_test(testdir, test_resp, gi_api_test_re):
    stub_get(gi_api_test_re, body=test_resp, content_type='application/json')
    result = testdir.runpytest('--collect-only', '--gi_key=foo', '--gi_test=xyz789')
    result.stdout.fnmatch_lines([
     'collected 1 items',
     "*GITestItem*'test xyz789'*"])


@pytest.mark.httpretty
def test_cmdline_exec_test(testdir, test_resp, gi_api_test_re, gi_api_test_exec_re):

    def req_callback(request, uri, headers):
        return (
         200,
         headers,
         '{ "data": { "passing": true } }')

    stub_get(gi_api_test_re, content_type='application/json', body=test_resp)
    stub_get(gi_api_test_exec_re, content_type='application/json', body=req_callback)
    result = testdir.runpytest('--gi_key=foo', '--gi_test=xyz789')
    result.stdout.fnmatch_lines([
     'collected 1 items',
     '*1 passed*'])


def test_collect_mode_files(testdir):
    testdir.makepyfile('def test_fail(): assert 0')
    result = testdir.runpytest('--collect-only', '--gi_key=foo', '--gi_test=xyz789')
    result.stdout.fnmatch_lines([
     '*Test not found*'])
    result = testdir.runpytest('--collect-only', '--gi_key=foo', '--gi_test=xyz789', '--gi_collect_mode=files')
    result.stdout.fnmatch_lines([
     'collected 1 items',
     '*test_fail*'])


@pytest.mark.httpretty
def test_collect_mode_all(testdir, test_resp, gi_api_test_re):
    testdir.makepyfile('def test_fail(): assert 0')
    stub_get(gi_api_test_re, body=test_resp, content_type='application/json')
    result = testdir.runpytest('--collect-only', '--gi_key=foo', '--gi_test=xyz789', '--gi_collect_mode=all')
    result.stdout.fnmatch_lines([
     'collected 2 items',
     '*test_fail*',
     "*GITestItem*'test xyz789'*"])


@pytest.mark.httpretty
def test_collect_mode_ids(testdir, test_resp, gi_api_test_re):
    testdir.makepyfile('def test_fail(): assert 0')
    stub_get(gi_api_test_re, body=test_resp, content_type='application/json')
    result = testdir.runpytest('--collect-only', '--gi_key=foo', '--gi_test=xyz789')
    result.stdout.fnmatch_lines([
     'collected 1 items',
     "*GITestItem*'test xyz789'*"])