# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/utils/unittest_utils.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 2085 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, io, re
from pylint.utils import utils

def test__basename_in_blacklist_re_match():
    patterns = [
     re.compile('.*enchilada.*'), re.compile('unittest_.*')]
    @py_assert1 = utils._basename_in_blacklist_re
    @py_assert3 = 'unittest_utils.py'
    @py_assert6 = @py_assert1(@py_assert3, patterns)
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/utils/unittest_utils.py', lineno=27)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s._basename_in_blacklist_re\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(patterns) if 'patterns' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(patterns) else 'patterns',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    @py_assert1 = utils._basename_in_blacklist_re
    @py_assert3 = 'cheese_enchiladas.xml'
    @py_assert6 = @py_assert1(@py_assert3, patterns)
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/utils/unittest_utils.py', lineno=28)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s._basename_in_blacklist_re\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(patterns) if 'patterns' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(patterns) else 'patterns',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None


def test__basename_in_blacklist_re_nomatch():
    patterns = [
     re.compile('.*enchilada.*'), re.compile('unittest_.*')]
    @py_assert1 = utils._basename_in_blacklist_re
    @py_assert3 = 'test_utils.py'
    @py_assert6 = @py_assert1(@py_assert3, patterns)
    @py_assert8 = not @py_assert6
    if @py_assert8 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/utils/unittest_utils.py', lineno=33)
    if not @py_assert8:
        @py_format9 = 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s._basename_in_blacklist_re\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(patterns) if 'patterns' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(patterns) else 'patterns',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    @py_assert1 = utils._basename_in_blacklist_re
    @py_assert3 = 'enchilad.py'
    @py_assert6 = @py_assert1(@py_assert3, patterns)
    @py_assert8 = not @py_assert6
    if @py_assert8 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/utils/unittest_utils.py', lineno=34)
    if not @py_assert8:
        @py_format9 = 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s._basename_in_blacklist_re\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(patterns) if 'patterns' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(patterns) else 'patterns',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None


def test_decoding_stream_unknown_encoding():
    """decoding_stream should fall back to *some* decoding when given an
    unknown encoding.
    """
    binary_io = io.BytesIO(b'foo\nbar')
    stream = utils.decoding_stream(binary_io, 'garbage-encoding')
    ret = stream.readlines()
    @py_assert2 = ['foo\n', 'bar']
    @py_assert1 = ret == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/utils/unittest_utils.py', lineno=45)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (ret, @py_assert2)) % {'py0':@pytest_ar._saferepr(ret) if 'ret' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ret) else 'ret',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_decoding_stream_known_encoding():
    binary_io = io.BytesIO('€'.encode('cp1252'))
    stream = utils.decoding_stream(binary_io, 'cp1252')
    @py_assert1 = stream.read
    @py_assert3 = @py_assert1()
    @py_assert6 = '€'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/utils/unittest_utils.py', lineno=51)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(stream) if 'stream' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stream) else 'stream',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None