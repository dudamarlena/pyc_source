# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/haoxun/Data/Project/pyenv-mirror/tests/test_misc.py
# Compiled at: 2016-04-12 06:51:46
# Size of source mod 2**32: 1971 bytes
from __future__ import division, absolute_import, print_function, unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from pyenv_mirror.locate_scripts import check_directory, check_script
from pyenv_mirror.parse_script import extract_filename, extract_urls
from tests.env import TEST_DIR_PATH
TARGET_DIR_PATH = os.path.join(TEST_DIR_PATH, 'test_pyenv_root/plugins/python-build/share/python-build')

def test_missing_path():
    os.environ['PYENV_ROOT'] = os.path.join(TEST_DIR_PATH, 'test_pyenv_root')
    @py_assert3 = check_directory()
    @py_assert1 = TARGET_DIR_PATH == @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py4)s\n{%(py4)s = %(py2)s()\n}', ), (TARGET_DIR_PATH, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(TARGET_DIR_PATH) if 'TARGET_DIR_PATH' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TARGET_DIR_PATH) else 'TARGET_DIR_PATH', 'py2': @pytest_ar._saferepr(check_directory) if 'check_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_directory) else 'check_directory'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_normal_path():
    @py_assert4 = check_directory(TARGET_DIR_PATH)
    @py_assert1 = TARGET_DIR_PATH == @py_assert4
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}', ), (TARGET_DIR_PATH, @py_assert4)) % {'py3': @pytest_ar._saferepr(TARGET_DIR_PATH) if 'TARGET_DIR_PATH' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TARGET_DIR_PATH) else 'TARGET_DIR_PATH', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(TARGET_DIR_PATH) if 'TARGET_DIR_PATH' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TARGET_DIR_PATH) else 'TARGET_DIR_PATH', 'py2': @pytest_ar._saferepr(check_directory) if 'check_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_directory) else 'check_directory'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = None
    @py_assert2 = check_directory(TEST_DIR_PATH)
    @py_assert5 = None
    @py_assert4 = @py_assert2 is @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} is %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(TEST_DIR_PATH) if 'TEST_DIR_PATH' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TEST_DIR_PATH) else 'TEST_DIR_PATH', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5), 'py0': @pytest_ar._saferepr(check_directory) if 'check_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_directory) else 'check_directory'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_check_script():
    @py_assert2 = '2.7'
    @py_assert4 = check_script(TARGET_DIR_PATH, @py_assert2)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py1': @pytest_ar._saferepr(TARGET_DIR_PATH) if 'TARGET_DIR_PATH' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TARGET_DIR_PATH) else 'TARGET_DIR_PATH', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(check_script) if 'check_script' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_script) else 'check_script'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert2 = '2.7.11'
    @py_assert4 = check_script(TARGET_DIR_PATH, @py_assert2)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py1': @pytest_ar._saferepr(TARGET_DIR_PATH) if 'TARGET_DIR_PATH' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TARGET_DIR_PATH) else 'TARGET_DIR_PATH', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(check_script) if 'check_script' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_script) else 'check_script'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert2 = 'not-exists'
    @py_assert4 = check_script(TARGET_DIR_PATH, @py_assert2)
    @py_assert6 = not @py_assert4
    if not @py_assert6:
        @py_format7 = ('' + 'assert not %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py1': @pytest_ar._saferepr(TARGET_DIR_PATH) if 'TARGET_DIR_PATH' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TARGET_DIR_PATH) else 'TARGET_DIR_PATH', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(check_script) if 'check_script' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_script) else 'check_script'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert4 = @py_assert6 = None


def test_extract_filename():
    from urllib.parse import urlparse
    url = 'http://www.python.org/ftp/python/2.7/Python-2.7.tgz#5670dd6c0c93b0b529781d070852f7b51ce6855615b16afcd318341af2910fb5'
    parsed_url = urlparse(url)
    @py_assert0 = 'Python-2.7.tgz'
    @py_assert5 = extract_filename(parsed_url)
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(extract_filename) if 'extract_filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(extract_filename) else 'extract_filename', 'py4': @pytest_ar._saferepr(parsed_url) if 'parsed_url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parsed_url) else 'parsed_url', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert5 = None


def test_extract_2_7():
    path = os.path.join(TARGET_DIR_PATH, '2.7')
    url_filename = extract_urls(path)
    @py_assert0 = [('https://www.openssl.org/source/openssl-1.0.2g.tar.gz#b784b1b3907ce39abf4098702dade6365522a253ad1552e267a9a0e89594aa33',
 'openssl-1.0.2g.tar.gz'), ('http://ftpmirror.gnu.org/readline/readline-6.3.tar.gz#56ba6071b9462f980c5a72ab0023893b65ba6debb4eeb475d7a563dc65cafd43',
 'readline-6.3.tar.gz'), ('http://www.python.org/ftp/python/2.7/Python-2.7.tgz#5670dd6c0c93b0b529781d070852f7b51ce6855615b16afcd318341af2910fb5',
 'Python-2.7.tgz')]
    @py_assert2 = @py_assert0 == url_filename
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, url_filename)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(url_filename) if 'url_filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url_filename) else 'url_filename'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None