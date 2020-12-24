# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/nodegraph_test.py
# Compiled at: 2019-10-16 12:05:38
# Size of source mod 2**32: 4911 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from unittest.mock import Mock
from paleomix.nodegraph import NodeGraph, FileStatusCache

def test_dir():
    return os.path.dirname(__file__)


def test_file(*args):
    return (os.path.join)(test_dir(), 'data', *args)


_DESCRIPTION = 'My description of a node'
_IN_FILES = frozenset((test_file('empty_file_1'), test_file('empty_file_2')))
_OUT_FILES = frozenset((
 test_file('missing_out_file_1'), test_file('missing_out_file_2')))
_EXEC_FILES = frozenset(('ls', 'sh'))
_AUX_FILES = frozenset((test_file('rCRS.fasta'), test_file('rCRS.fasta.fai')))
_REQUIREMENTS = frozenset((id, str))

def setup_module():
    timestamps = {test_file('timestamp_a_older'): 1000190760, 
     test_file('timestamp_b_older'): 1000190760, 
     test_file('timestamp_a_younger'): 1120719000, 
     test_file('timestamp_b_younger'): 1120719000}
    for filename, timestamp in timestamps.items():
        os.utime(filename, (timestamp, timestamp))


def test_nodegraph_is_done__no_output():
    cache = FileStatusCache()
    node = Mock(output_files=())
    @py_assert1 = NodeGraph.is_done
    @py_assert5 = @py_assert1(node, cache)
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/nodegraph_test.py', lineno=76)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_done\n}(%(py3)s, %(py4)s)\n}' % {'py0':@pytest_ar._saferepr(NodeGraph) if 'NodeGraph' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NodeGraph) else 'NodeGraph',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py4':@pytest_ar._saferepr(cache) if 'cache' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cache) else 'cache',  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert5 = None


def test_nodegraph_is_done__output_changes(tmp_path):
    temp_file_1 = tmp_path / 'file_1.txt'
    temp_file_2 = tmp_path / 'file_2.txt'
    my_node = Mock(output_files=(temp_file_1, temp_file_2))
    @py_assert1 = NodeGraph.is_done
    @py_assert5 = FileStatusCache()
    @py_assert7 = @py_assert1(my_node, @py_assert5)
    @py_assert9 = not @py_assert7
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/nodegraph_test.py', lineno=83)
    if not @py_assert9:
        @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_done\n}(%(py3)s, %(py6)s\n{%(py6)s = %(py4)s()\n})\n}' % {'py0':@pytest_ar._saferepr(NodeGraph) if 'NodeGraph' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NodeGraph) else 'NodeGraph',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(my_node) if 'my_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_node) else 'my_node',  'py4':@pytest_ar._saferepr(FileStatusCache) if 'FileStatusCache' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FileStatusCache) else 'FileStatusCache',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = None
    temp_file_1.write_text('foo')
    @py_assert1 = NodeGraph.is_done
    @py_assert5 = FileStatusCache()
    @py_assert7 = @py_assert1(my_node, @py_assert5)
    @py_assert9 = not @py_assert7
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/nodegraph_test.py', lineno=85)
    if not @py_assert9:
        @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_done\n}(%(py3)s, %(py6)s\n{%(py6)s = %(py4)s()\n})\n}' % {'py0':@pytest_ar._saferepr(NodeGraph) if 'NodeGraph' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NodeGraph) else 'NodeGraph',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(my_node) if 'my_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_node) else 'my_node',  'py4':@pytest_ar._saferepr(FileStatusCache) if 'FileStatusCache' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FileStatusCache) else 'FileStatusCache',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = None
    temp_file_2.write_text('bar')
    @py_assert1 = NodeGraph.is_done
    @py_assert5 = FileStatusCache()
    @py_assert7 = @py_assert1(my_node, @py_assert5)
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/nodegraph_test.py', lineno=87)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_done\n}(%(py3)s, %(py6)s\n{%(py6)s = %(py4)s()\n})\n}' % {'py0':@pytest_ar._saferepr(NodeGraph) if 'NodeGraph' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NodeGraph) else 'NodeGraph',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(my_node) if 'my_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_node) else 'my_node',  'py4':@pytest_ar._saferepr(FileStatusCache) if 'FileStatusCache' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FileStatusCache) else 'FileStatusCache',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert5 = @py_assert7 = None


def test_nodegraph_is_done__subnode_not_considered(tmp_path):
    temp_file = os.path.join(tmp_path, 'file.txt')
    subnode = Mock(output_files=(temp_file,))
    my_node = Mock(output_files=(), subnodes=(subnode,))
    @py_assert1 = NodeGraph.is_done
    @py_assert5 = FileStatusCache()
    @py_assert7 = @py_assert1(my_node, @py_assert5)
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/nodegraph_test.py', lineno=94)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_done\n}(%(py3)s, %(py6)s\n{%(py6)s = %(py4)s()\n})\n}' % {'py0':@pytest_ar._saferepr(NodeGraph) if 'NodeGraph' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NodeGraph) else 'NodeGraph',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(my_node) if 'my_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_node) else 'my_node',  'py4':@pytest_ar._saferepr(FileStatusCache) if 'FileStatusCache' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FileStatusCache) else 'FileStatusCache',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert5 = @py_assert7 = None


def test_nodegraph_is_outdated__no_output():
    my_node = Mock(input_files=(), output_files=())
    @py_assert1 = NodeGraph.is_outdated
    @py_assert5 = FileStatusCache()
    @py_assert7 = @py_assert1(my_node, @py_assert5)
    @py_assert9 = not @py_assert7
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/nodegraph_test.py', lineno=99)
    if not @py_assert9:
        @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_outdated\n}(%(py3)s, %(py6)s\n{%(py6)s = %(py4)s()\n})\n}' % {'py0':@pytest_ar._saferepr(NodeGraph) if 'NodeGraph' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NodeGraph) else 'NodeGraph',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(my_node) if 'my_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_node) else 'my_node',  'py4':@pytest_ar._saferepr(FileStatusCache) if 'FileStatusCache' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FileStatusCache) else 'FileStatusCache',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_nodegraph_is_outdated__input_but_no_output():
    my_node = Mock(input_files=_IN_FILES, output_files=())
    @py_assert1 = NodeGraph.is_outdated
    @py_assert5 = FileStatusCache()
    @py_assert7 = @py_assert1(my_node, @py_assert5)
    @py_assert9 = not @py_assert7
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/nodegraph_test.py', lineno=104)
    if not @py_assert9:
        @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_outdated\n}(%(py3)s, %(py6)s\n{%(py6)s = %(py4)s()\n})\n}' % {'py0':@pytest_ar._saferepr(NodeGraph) if 'NodeGraph' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NodeGraph) else 'NodeGraph',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(my_node) if 'my_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_node) else 'my_node',  'py4':@pytest_ar._saferepr(FileStatusCache) if 'FileStatusCache' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FileStatusCache) else 'FileStatusCache',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_nodegraph_is_outdated__output_but_no_input():
    my_node = Mock(input_files=(), output_files=_OUT_FILES)
    @py_assert1 = NodeGraph.is_outdated
    @py_assert5 = FileStatusCache()
    @py_assert7 = @py_assert1(my_node, @py_assert5)
    @py_assert9 = not @py_assert7
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/nodegraph_test.py', lineno=109)
    if not @py_assert9:
        @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_outdated\n}(%(py3)s, %(py6)s\n{%(py6)s = %(py4)s()\n})\n}' % {'py0':@pytest_ar._saferepr(NodeGraph) if 'NodeGraph' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NodeGraph) else 'NodeGraph',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(my_node) if 'my_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_node) else 'my_node',  'py4':@pytest_ar._saferepr(FileStatusCache) if 'FileStatusCache' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FileStatusCache) else 'FileStatusCache',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_nodegraph_is_outdated__not_outdated():
    my_node = Mock(input_files=(
     test_file('timestamp_a_older'),),
      output_files=(
     test_file('timestamp_a_younger'),))
    @py_assert1 = NodeGraph.is_outdated
    @py_assert5 = FileStatusCache()
    @py_assert7 = @py_assert1(my_node, @py_assert5)
    @py_assert9 = not @py_assert7
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/nodegraph_test.py', lineno=117)
    if not @py_assert9:
        @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_outdated\n}(%(py3)s, %(py6)s\n{%(py6)s = %(py4)s()\n})\n}' % {'py0':@pytest_ar._saferepr(NodeGraph) if 'NodeGraph' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NodeGraph) else 'NodeGraph',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(my_node) if 'my_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_node) else 'my_node',  'py4':@pytest_ar._saferepr(FileStatusCache) if 'FileStatusCache' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FileStatusCache) else 'FileStatusCache',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_nodegraph_is_outdated__outdated():
    my_node = Mock(input_files=(
     test_file('timestamp_a_younger'),),
      output_files=(
     test_file('timestamp_a_older'),))
    @py_assert1 = NodeGraph.is_outdated
    @py_assert5 = FileStatusCache()
    @py_assert7 = @py_assert1(my_node, @py_assert5)
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/nodegraph_test.py', lineno=125)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_outdated\n}(%(py3)s, %(py6)s\n{%(py6)s = %(py4)s()\n})\n}' % {'py0':@pytest_ar._saferepr(NodeGraph) if 'NodeGraph' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NodeGraph) else 'NodeGraph',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(my_node) if 'my_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_node) else 'my_node',  'py4':@pytest_ar._saferepr(FileStatusCache) if 'FileStatusCache' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FileStatusCache) else 'FileStatusCache',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert5 = @py_assert7 = None


def test_nodegraph_is_outdated__updates():
    my_node = Mock(input_files=(
     test_file('timestamp_a_older'),),
      output_files=(
     test_file('timestamp_a_younger'),))
    @py_assert1 = NodeGraph.is_outdated
    @py_assert5 = FileStatusCache()
    @py_assert7 = @py_assert1(my_node, @py_assert5)
    @py_assert9 = not @py_assert7
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/nodegraph_test.py', lineno=133)
    if not @py_assert9:
        @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_outdated\n}(%(py3)s, %(py6)s\n{%(py6)s = %(py4)s()\n})\n}' % {'py0':@pytest_ar._saferepr(NodeGraph) if 'NodeGraph' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NodeGraph) else 'NodeGraph',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(my_node) if 'my_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_node) else 'my_node',  'py4':@pytest_ar._saferepr(FileStatusCache) if 'FileStatusCache' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FileStatusCache) else 'FileStatusCache',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = None
    my_node = Mock(input_files=(
     test_file('timestamp_a_younger'),),
      output_files=(
     test_file('timestamp_a_older'),))
    @py_assert1 = NodeGraph.is_outdated
    @py_assert5 = FileStatusCache()
    @py_assert7 = @py_assert1(my_node, @py_assert5)
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/nodegraph_test.py', lineno=138)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_outdated\n}(%(py3)s, %(py6)s\n{%(py6)s = %(py4)s()\n})\n}' % {'py0':@pytest_ar._saferepr(NodeGraph) if 'NodeGraph' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NodeGraph) else 'NodeGraph',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(my_node) if 'my_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_node) else 'my_node',  'py4':@pytest_ar._saferepr(FileStatusCache) if 'FileStatusCache' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FileStatusCache) else 'FileStatusCache',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert5 = @py_assert7 = None