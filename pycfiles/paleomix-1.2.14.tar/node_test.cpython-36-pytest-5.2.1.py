# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/node_test.py
# Compiled at: 2019-10-16 12:05:38
# Size of source mod 2**32: 19652 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, random
from unittest.mock import call, Mock
import pytest
from paleomix.atomiccmd.command import AtomicCmd
from paleomix.node import Node, CommandNode, NodeError, NodeUnhandledException, CmdNodeError
from paleomix.common.utilities import safe_coerce_to_frozenset

def test_dir():
    return os.path.dirname(__file__)


def test_file(*args):
    return (os.path.join)(test_dir(), 'data', *args)


def first(values):
    return random.choice(tuple(values))


def _CommandNodeWrap(**kwargs):
    return CommandNode(command=AtomicCmd('true'), **kwargs)


_NODE_TYPES = (
 Node, _CommandNodeWrap)
_DESCRIPTION = 'My description of a node'
_IN_FILES = frozenset((test_file('empty_file_1'), test_file('empty_file_2')))
_OUT_FILES = frozenset((
 test_file('missing_out_file_1'), test_file('missing_out_file_2')))
_EXEC_FILES = frozenset(('ls', 'sh'))
_AUX_FILES = frozenset((test_file('rCRS.fasta'), test_file('rCRS.fasta.fai')))
_REQUIREMENTS = frozenset((id, str))
_EMPTY_FILE = test_file('empty_file_1')

def _build_cmd_mock(input_files=_IN_FILES, output_files=(), executables=(), auxiliary_files=(), requirements=(), optional_temp_files=(), return_codes=(0, )):
    cmd = Mock(input_files=(frozenset(input_files)),
      output_files=(frozenset(output_files)),
      executables=(frozenset(executables)),
      auxiliary_files=(frozenset(auxiliary_files)),
      requirements=(frozenset(requirements)),
      expected_temp_files=(frozenset(map(os.path.basename, output_files))),
      optional_temp_files=(frozenset(optional_temp_files)))
    cmd.join.return_value = return_codes
    return cmd


_CONSTUCTOR_SINGLE_VALUES = (
 (
  'input_files', first(_IN_FILES)),
 (
  'output_files', first(_OUT_FILES)),
 (
  'executables', first(_EXEC_FILES)),
 (
  'auxiliary_files', first(_AUX_FILES)),
 (
  'input_files', [first(_IN_FILES)]),
 (
  'output_files', [first(_OUT_FILES)]),
 (
  'executables', [first(_EXEC_FILES)]),
 (
  'auxiliary_files', [first(_AUX_FILES)]),
 (
  'input_files', _IN_FILES),
 (
  'output_files', _OUT_FILES),
 (
  'executables', _EXEC_FILES),
 (
  'auxiliary_files', _AUX_FILES))

@pytest.mark.parametrize('key, value', _CONSTUCTOR_SINGLE_VALUES)
def test_constructor(key, value):
    defaults = {'input_files': _EMPTY_FILE}
    defaults[key] = value
    node = Node(**defaults)
    expected = safe_coerce_to_frozenset(value)
    @py_assert3 = getattr(node, key)
    @py_assert5 = @py_assert3 == expected
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=124)
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(getattr) if 'getattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getattr) else 'getattr',  'py1':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py2':@pytest_ar._saferepr(key) if 'key' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(key) else 'key',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert3 = @py_assert5 = None


_CONSTUCTOR_INVALID_VALUES = (
 (
  'input_files', [id]),
 (
  'output_files', [-1]),
 (
  'executables', [{}]),
 (
  'auxiliary_files', [1.3]))

@pytest.mark.parametrize('key, value', _CONSTUCTOR_INVALID_VALUES)
def test_constructor__invalid_values(key, value):
    with pytest.raises(TypeError):
        Node(**{key: value})


def test_constructor__requirements():
    node = Node(requirements=id)
    @py_assert1 = node.requirements
    @py_assert5 = [
     id]
    @py_assert7 = frozenset(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=148)
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.requirements\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    node = Node(requirements=[id])
    @py_assert1 = node.requirements
    @py_assert5 = [
     id]
    @py_assert7 = frozenset(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=150)
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.requirements\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    node = Node(requirements=[id, str])
    @py_assert1 = node.requirements
    @py_assert5 = [
     id, str]
    @py_assert7 = frozenset(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=152)
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.requirements\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


@pytest.mark.parametrize('value', (17, {}, '867-5309'))
def test_constructor__requirements__wrong_type(value):
    with pytest.raises(TypeError):
        Node(requirements=value)


def test_constructor__nodes_is_none():
    my_node = Node(dependencies=None)
    @py_assert1 = my_node.dependencies
    @py_assert5 = frozenset()
    @py_assert3 = @py_assert1 == @py_assert5
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=168)
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.dependencies\n} == %(py6)s\n{%(py6)s = %(py4)s()\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(my_node) if 'my_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_node) else 'my_node',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_constructor__single_node():
    sub_node = Node()
    my_node = Node(dependencies=sub_node)
    @py_assert1 = my_node.dependencies
    @py_assert5 = [
     sub_node]
    @py_assert7 = frozenset(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=174)
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.dependencies\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(my_node) if 'my_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_node) else 'my_node',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_constructor__iterable():
    sub_nodes = [
     Node(), Node()]
    my_node = Node(dependencies=(iter(sub_nodes)))
    @py_assert1 = my_node.dependencies
    @py_assert6 = frozenset(sub_nodes)
    @py_assert3 = @py_assert1 == @py_assert6
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=180)
    if not @py_assert3:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.dependencies\n} == %(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n}', ), (@py_assert1, @py_assert6)) % {'py0':@pytest_ar._saferepr(my_node) if 'my_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_node) else 'my_node',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py5':@pytest_ar._saferepr(sub_nodes) if 'sub_nodes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sub_nodes) else 'sub_nodes',  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert6 = None


def test_constructor__not_a_node():
    with pytest.raises(TypeError):
        Node(dependencies=(1, ))


@pytest.mark.parametrize('cls', _NODE_TYPES)
def test_constructor__description(cls):
    my_node = cls(description=_DESCRIPTION)
    @py_assert2 = str(my_node)
    @py_assert4 = @py_assert2 == _DESCRIPTION
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=196)
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, _DESCRIPTION)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(my_node) if 'my_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_node) else 'my_node',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(_DESCRIPTION) if '_DESCRIPTION' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_DESCRIPTION) else '_DESCRIPTION'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


@pytest.mark.parametrize('cls', _NODE_TYPES)
def test_constructor__description__default(cls):
    my_node = cls()
    @py_assert2 = str(my_node)
    @py_assert7 = repr(my_node)
    @py_assert4 = @py_assert2 == @py_assert7
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=202)
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}', ), (@py_assert2, @py_assert7)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(my_node) if 'my_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_node) else 'my_node',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr',  'py6':@pytest_ar._saferepr(my_node) if 'my_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_node) else 'my_node',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None


@pytest.mark.parametrize('cls', _NODE_TYPES)
@pytest.mark.parametrize('value', (1, {}))
def test_constructor__description__non_string(cls, value):
    with pytest.raises(TypeError):
        cls(description=value)


@pytest.mark.parametrize('cls', _NODE_TYPES)
@pytest.mark.parametrize('nthreads', (1, 3))
def test_constructor__threads(cls, nthreads):
    node = cls(threads=nthreads)
    @py_assert1 = node.threads
    @py_assert3 = @py_assert1 == nthreads
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=221)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.threads\n} == %(py4)s', ), (@py_assert1, nthreads)) % {'py0':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(nthreads) if 'nthreads' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(nthreads) else 'nthreads'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


@pytest.mark.parametrize('cls', _NODE_TYPES)
@pytest.mark.parametrize('nthreads', (-1, 0))
def test_constructor__threads_invalid_range(cls, nthreads):
    with pytest.raises(ValueError):
        cls(threads=nthreads)


@pytest.mark.parametrize('cls', _NODE_TYPES)
@pytest.mark.parametrize('nthreads', ('1', {}, 2.7))
def test_constructor__threads_invalid_type(cls, nthreads):
    with pytest.raises(TypeError):
        cls(threads=nthreads)


_DUMMY_TEMP_ROOT = '/xyz/tmp'
_DUMMY_TEMP = os.path.join(_DUMMY_TEMP_ROOT, 'xTMPx')

def test_run__order():
    cfg_mock = Mock(temp_root=_DUMMY_TEMP_ROOT)
    node_mock = Mock()
    node = Node()
    node._create_temp_dir = node_mock._create_temp_dir
    node._create_temp_dir.return_value = _DUMMY_TEMP
    node._setup = node_mock._setup
    node._run = node_mock._run
    node._teardown = node_mock._teardown
    node._remove_temp_dir = node_mock._remove_temp_dir
    node.run(cfg_mock)
    node_mock.mock_calls == [
     call._create_temp_dir(cfg_mock),
     call._setup(cfg_mock, _DUMMY_TEMP),
     call._run(cfg_mock, _DUMMY_TEMP),
     call._teardown(cfg_mock, _DUMMY_TEMP),
     call._remove_temp_dir(_DUMMY_TEMP)]


_EXCEPTIONS = (
 (
  TypeError('The castle AAARGH!'), NodeUnhandledException),
 (
  NodeError("He's a very naughty boy!"), NodeError))

@pytest.mark.parametrize('key', ('_setup', '_run', '_teardown'))
@pytest.mark.parametrize('exception, expectation', _EXCEPTIONS)
def test_run__exceptions(key, exception, expectation):
    mock = Mock()
    node = Node()
    node._create_temp_dir = mock._create_temp_dir
    node._create_temp_dir.return_value = _DUMMY_TEMP
    setattr(node, key, getattr(mock, key))
    getattr(node, key).side_effect = exception
    cfg_mock = Mock(temp_root=_DUMMY_TEMP_ROOT)
    with pytest.raises(expectation):
        node.run(cfg_mock)
    @py_assert1 = mock.mock_calls
    @py_assert4 = [
     call._create_temp_dir(cfg_mock), getattr(call, key)(cfg_mock, _DUMMY_TEMP)]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=290)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_run__exception__create_temp_dir():
    cfg_mock = Mock(temp_root=_DUMMY_TEMP_ROOT)
    node_mock = Node()
    node_mock._create_temp_dir = Mock()
    node_mock._create_temp_dir.side_effect = OSError()
    with pytest.raises(NodeUnhandledException):
        node_mock.run(cfg_mock)
    @py_assert1 = node_mock._create_temp_dir
    @py_assert3 = @py_assert1.mock_calls
    @py_assert6 = [
     call(cfg_mock)]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=304)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s._create_temp_dir\n}.mock_calls\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(node_mock) if 'node_mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_mock) else 'node_mock',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_run__exception__remove_temp_dir():
    cfg_mock = Mock(temp_root=_DUMMY_TEMP_ROOT)
    mock = Mock()
    node_mock = Node()
    node_mock._create_temp_dir = mock._create_temp_dir
    node_mock._create_temp_dir.return_value = _DUMMY_TEMP
    node_mock._remove_temp_dir = mock._remove_temp_dir
    node_mock._remove_temp_dir.side_effect = OSError()
    with pytest.raises(NodeUnhandledException):
        node_mock.run(cfg_mock)
    @py_assert1 = mock.mock_calls
    @py_assert4 = [
     call._create_temp_dir(cfg_mock), call._remove_temp_dir(_DUMMY_TEMP)]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=318)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


@pytest.mark.parametrize('exception', (NodeError, OSError))
def test_run__error_log__node_error(tmp_path, exception):
    temp = tmp_path / 'xTMPx'
    mock = Mock()
    cfg_mock = Mock(temp_root=tmp_path)
    node_mock = Node()
    node_mock._create_temp_dir = mock._create_temp_dir
    node_mock._create_temp_dir.return_value = temp
    node_mock._run = mock._run
    node_mock._run.side_effect = exception('ARGH!')
    os.mkdir(temp)
    with pytest.raises(NodeError):
        node_mock.run(cfg_mock)
    log_file = tmp_path / 'xTMPx' / 'pipe.errors'
    @py_assert1 = log_file.exists
    @py_assert3 = @py_assert1()
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=339)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}' % {'py0':@pytest_ar._saferepr(log_file) if 'log_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(log_file) else 'log_file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = 'Errors ='
    @py_assert4 = log_file.read_text
    @py_assert6 = @py_assert4()
    @py_assert2 = @py_assert0 in @py_assert6
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=340)
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.read_text\n}()\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(log_file) if 'log_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(log_file) else 'log_file',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert1 = mock.mock_calls
    @py_assert4 = [
     call._create_temp_dir(cfg_mock), call._run(cfg_mock, temp)]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=342)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


_INPUT_FILES_EXIST = (
 {'executables': ('ls', 'sh')},
 {'input_files': _IN_FILES},
 {'auxiliary_files': _IN_FILES})

@pytest.mark.parametrize('kwargs', _INPUT_FILES_EXIST)
def test__setup__input_files(kwargs):
    Node(**kwargs)._setup(None, None)


_INPUT_FILES_MISSING = (
 {'executables': ('ls', 'shxxxx')},
 {'input_files': _OUT_FILES},
 {'auxiliary_files': _OUT_FILES})

@pytest.mark.parametrize('kwargs', _INPUT_FILES_MISSING)
def test__setup__input_files_missing(kwargs):
    with pytest.raises(NodeError):
        Node(**kwargs)._setup(None, None)


def test__teardown__output_files():
    Node(input_files=_EMPTY_FILE, output_files=_IN_FILES)._teardown(None, None)


def test__teardown__output_files_missing():
    node = Node(input_files=_EMPTY_FILE, output_files=_OUT_FILES)
    with pytest.raises(NodeError):
        node._teardown(None, None)


_SIMPLE_DEPS = Node()
_SIMPLE_SUBS = Node()
_SIMPLE_CMD_MOCK = Mock(input_files=_IN_FILES,
  output_files=_OUT_FILES,
  executables=_EXEC_FILES,
  auxiliary_files=_AUX_FILES,
  requirements=_REQUIREMENTS)
_SIMPLE_CMD_NODE = CommandNode(command=_SIMPLE_CMD_MOCK, dependencies=_SIMPLE_DEPS)

def test_commandnode_constructor__input_files():
    @py_assert1 = _SIMPLE_CMD_NODE.input_files
    @py_assert3 = @py_assert1 == _IN_FILES
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=404)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.input_files\n} == %(py4)s', ), (@py_assert1, _IN_FILES)) % {'py0':@pytest_ar._saferepr(_SIMPLE_CMD_NODE) if '_SIMPLE_CMD_NODE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_SIMPLE_CMD_NODE) else '_SIMPLE_CMD_NODE',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(_IN_FILES) if '_IN_FILES' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_IN_FILES) else '_IN_FILES'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_commandnode_constructor__output_files():
    @py_assert1 = _SIMPLE_CMD_NODE.output_files
    @py_assert3 = @py_assert1 == _OUT_FILES
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=408)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.output_files\n} == %(py4)s', ), (@py_assert1, _OUT_FILES)) % {'py0':@pytest_ar._saferepr(_SIMPLE_CMD_NODE) if '_SIMPLE_CMD_NODE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_SIMPLE_CMD_NODE) else '_SIMPLE_CMD_NODE',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(_OUT_FILES) if '_OUT_FILES' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_OUT_FILES) else '_OUT_FILES'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_commandnode_constructor__auxiliary_files():
    @py_assert1 = _SIMPLE_CMD_NODE.auxiliary_files
    @py_assert3 = @py_assert1 == _AUX_FILES
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=412)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.auxiliary_files\n} == %(py4)s', ), (@py_assert1, _AUX_FILES)) % {'py0':@pytest_ar._saferepr(_SIMPLE_CMD_NODE) if '_SIMPLE_CMD_NODE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_SIMPLE_CMD_NODE) else '_SIMPLE_CMD_NODE',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(_AUX_FILES) if '_AUX_FILES' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_AUX_FILES) else '_AUX_FILES'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_commandnode_constructor__executables():
    @py_assert1 = _SIMPLE_CMD_NODE.executables
    @py_assert3 = @py_assert1 == _EXEC_FILES
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=416)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.executables\n} == %(py4)s', ), (@py_assert1, _EXEC_FILES)) % {'py0':@pytest_ar._saferepr(_SIMPLE_CMD_NODE) if '_SIMPLE_CMD_NODE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_SIMPLE_CMD_NODE) else '_SIMPLE_CMD_NODE',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(_EXEC_FILES) if '_EXEC_FILES' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_EXEC_FILES) else '_EXEC_FILES'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_commandnode_constructor__requirements():
    @py_assert1 = _SIMPLE_CMD_NODE.requirements
    @py_assert3 = @py_assert1 == _REQUIREMENTS
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=420)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.requirements\n} == %(py4)s', ), (@py_assert1, _REQUIREMENTS)) % {'py0':@pytest_ar._saferepr(_SIMPLE_CMD_NODE) if '_SIMPLE_CMD_NODE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_SIMPLE_CMD_NODE) else '_SIMPLE_CMD_NODE',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(_REQUIREMENTS) if '_REQUIREMENTS' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_REQUIREMENTS) else '_REQUIREMENTS'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_commandnode_constructor__dependencies():
    @py_assert1 = _SIMPLE_CMD_NODE.dependencies
    @py_assert5 = [
     _SIMPLE_DEPS]
    @py_assert7 = frozenset(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=424)
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.dependencies\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(_SIMPLE_CMD_NODE) if '_SIMPLE_CMD_NODE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_SIMPLE_CMD_NODE) else '_SIMPLE_CMD_NODE',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_commandnode_constructor__dependencies__default():
    cmd_mock = CommandNode(command=_SIMPLE_CMD_MOCK)
    @py_assert1 = cmd_mock.dependencies
    @py_assert5 = frozenset()
    @py_assert3 = @py_assert1 == @py_assert5
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=429)
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.dependencies\n} == %(py6)s\n{%(py6)s = %(py4)s()\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(cmd_mock) if 'cmd_mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_mock) else 'cmd_mock',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_command_node__run():
    cfg_mock = Mock(temp_root=_DUMMY_TEMP_ROOT)
    mock = _build_cmd_mock()
    node_mock = CommandNode(mock)
    node_mock._create_temp_dir = mock._test_node_._create_temp_dir
    node_mock._create_temp_dir.return_value = _DUMMY_TEMP
    node_mock._setup = mock._test_node_._setup
    node_mock._teardown = mock._test_node_._teardown
    node_mock._remove_temp_dir = mock._test_node_._remove_temp_dir
    node_mock.run(cfg_mock)
    @py_assert1 = mock.mock_calls
    @py_assert4 = [
     call._test_node_._create_temp_dir(cfg_mock), call._test_node_._setup(cfg_mock, _DUMMY_TEMP), call.run(_DUMMY_TEMP), call.join(), call._test_node_._teardown(cfg_mock, _DUMMY_TEMP), call._test_node_._remove_temp_dir(_DUMMY_TEMP)]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=450)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


_SETUP_FILES_EXIST = (
 {'executables': ('ls', 'sh')},
 {'input_files': _IN_FILES},
 {'auxiliary_files': _IN_FILES})

@pytest.mark.parametrize('kwargs', _INPUT_FILES_EXIST)
def test_commandnode_setup__files_exist(kwargs):
    cmd_mock = _build_cmd_mock(**kwargs)
    node = CommandNode(cmd_mock)
    node._setup(None, None)


_SETUP_FILES_MISSING = (
 {'executables': ('ls', 'shxxxxxxxxxxx')},
 {'input_files': _OUT_FILES},
 {'auxiliary_files': _OUT_FILES})

@pytest.mark.parametrize('kwargs', _INPUT_FILES_MISSING)
def test_commandnode_setup__files_missing(kwargs):
    cmd_mock = _build_cmd_mock(**kwargs)
    node = CommandNode(cmd_mock)
    with pytest.raises(NodeError):
        node._setup(None, None)


def test_commandnode_run__call_order():
    cmd_mock = _build_cmd_mock()
    node = CommandNode(cmd_mock)
    node._run(None, 'xTMPx')
    @py_assert1 = cmd_mock.mock_calls
    @py_assert4 = [
     call.run('xTMPx'), call.join()]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=503)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(cmd_mock) if 'cmd_mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_mock) else 'cmd_mock',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_commandnode_run__exception_on_error():
    cmd_mock = _build_cmd_mock(return_codes=(1, ))
    node = CommandNode(cmd_mock)
    with pytest.raises(CmdNodeError):
        node._run(None, 'xTMPx')
    @py_assert1 = cmd_mock.mock_calls
    @py_assert4 = [
     call.run('xTMPx'), call.join()]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=512)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(cmd_mock) if 'cmd_mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_mock) else 'cmd_mock',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def _setup_temp_folders(tmp_path):
    destination = tmp_path / 'dst'
    tmp_path = tmp_path / 'tmp'
    os.makedirs(tmp_path)
    os.makedirs(destination)
    return (destination, tmp_path)


def test_commandnode_teardown__commit(tmp_path):
    cmd_mock = _build_cmd_mock()
    node = CommandNode(cmd_mock)
    node._teardown(None, tmp_path)
    @py_assert1 = cmd_mock.mock_calls
    @py_assert4 = [
     call.commit(tmp_path)]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=533)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(cmd_mock) if 'cmd_mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_mock) else 'cmd_mock',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_commandnode_teardown(tmp_path):
    destination, tmp_path = _setup_temp_folders(tmp_path)
    cmd = AtomicCmd(('echo', '-n', '1 2 3'),
      IN_DUMMY=_EMPTY_FILE,
      OUT_STDOUT=(os.path.join(destination, 'foo.txt')))
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=546)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    node = CommandNode(cmd)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = 'foo.txt'
    @py_assert13 = @py_assert8(tmp_path, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=548)
    if not @py_assert15:
        @py_format17 = 'assert %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = 'foo.txt'
    @py_assert13 = @py_assert8(destination, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    @py_assert17 = not @py_assert15
    if @py_assert17 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=549)
    if not @py_assert17:
        @py_format18 = 'assert not %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(destination) if 'destination' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(destination) else 'destination',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    node._teardown(None, tmp_path)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = 'foo.txt'
    @py_assert13 = @py_assert8(tmp_path, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    @py_assert17 = not @py_assert15
    if @py_assert17 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=551)
    if not @py_assert17:
        @py_format18 = 'assert not %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = 'foo.txt'
    @py_assert13 = @py_assert8(destination, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=552)
    if not @py_assert15:
        @py_format17 = 'assert %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(destination) if 'destination' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(destination) else 'destination',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = None


def test_commandnode_teardown__missing_files_in_temp(tmp_path):
    destination, tmp_path = _setup_temp_folders(tmp_path)
    cmd = AtomicCmd(('echo', '-n', '1 2 3'),
      IN_DUMMY=_EMPTY_FILE,
      OUT_BAR=(os.path.join(destination, 'bar.txt')),
      OUT_STDOUT=(os.path.join(destination, 'foo.txt')))
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=566)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    node = CommandNode(cmd)
    temp_files_before = set(os.listdir(tmp_path))
    dest_files_before = set(os.listdir(destination))
    with pytest.raises(CmdNodeError):
        node._teardown(None, tmp_path)
    @py_assert4 = os.listdir
    @py_assert7 = @py_assert4(tmp_path)
    @py_assert9 = set(@py_assert7)
    @py_assert1 = temp_files_before == @py_assert9
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=573)
    if not @py_assert1:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py10)s\n{%(py10)s = %(py2)s(%(py8)s\n{%(py8)s = %(py5)s\n{%(py5)s = %(py3)s.listdir\n}(%(py6)s)\n})\n}', ), (temp_files_before, @py_assert9)) % {'py0':@pytest_ar._saferepr(temp_files_before) if 'temp_files_before' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_files_before) else 'temp_files_before',  'py2':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py3':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert7 = @py_assert9 = None
    @py_assert4 = os.listdir
    @py_assert7 = @py_assert4(destination)
    @py_assert9 = set(@py_assert7)
    @py_assert1 = dest_files_before == @py_assert9
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=574)
    if not @py_assert1:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py10)s\n{%(py10)s = %(py2)s(%(py8)s\n{%(py8)s = %(py5)s\n{%(py5)s = %(py3)s.listdir\n}(%(py6)s)\n})\n}', ), (dest_files_before, @py_assert9)) % {'py0':@pytest_ar._saferepr(dest_files_before) if 'dest_files_before' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest_files_before) else 'dest_files_before',  'py2':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py3':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(destination) if 'destination' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(destination) else 'destination',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert7 = @py_assert9 = None


def test_commandnode_teardown__missing_optional_files(tmp_path):
    destination, tmp_path = _setup_temp_folders(tmp_path)
    cmd = AtomicCmd(('echo', '-n', '1 2 3'),
      IN_DUMMY=_EMPTY_FILE,
      TEMP_OUT_BAR='bar.txt',
      OUT_STDOUT=(os.path.join(destination, 'foo.txt')))
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=588)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    node = CommandNode(cmd)
    node._teardown(None, tmp_path)
    @py_assert1 = os.listdir
    @py_assert4 = @py_assert1(tmp_path)
    @py_assert7 = []
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=591)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = os.listdir
    @py_assert4 = @py_assert1(destination)
    @py_assert7 = [
     'foo.txt']
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=592)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(destination) if 'destination' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(destination) else 'destination',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_commandnode_teardown__missing_files_in_dest(tmp_path):
    destination, tmp_path = _setup_temp_folders(tmp_path)

    class _CmdMock(AtomicCmd):

        def commit(self, temp):
            AtomicCmd.commit(self, temp)
            os.remove(os.path.join(destination, 'foo.txt'))

    cmd = _CmdMock(('touch', '%(OUT_FOO)s', '%(OUT_BAR)s'),
      IN_DUMMY=_EMPTY_FILE,
      OUT_FOO=(os.path.join(destination, 'foo.txt')),
      OUT_BAR=(os.path.join(destination, 'bar.txt')))
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=611)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    node = CommandNode(cmd)
    with pytest.raises(NodeError):
        node._teardown(None, tmp_path)


def test_commandnode_teardown__extra_files_in_temp(tmp_path):
    destination, tmp_path = _setup_temp_folders(tmp_path)
    cmd = AtomicCmd(('echo', '-n', '1 2 3'),
      IN_DUMMY=_EMPTY_FILE,
      OUT_STDOUT=(os.path.join(destination, 'foo.txt')))
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=627)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    node = CommandNode(cmd)
    (tmp_path / 'bar.txt').write_text('1 2 3')
    temp_files_before = set(os.listdir(tmp_path))
    dest_files_before = set(os.listdir(destination))
    with pytest.raises(CmdNodeError):
        node._teardown(None, tmp_path)
    @py_assert4 = os.listdir
    @py_assert7 = @py_assert4(tmp_path)
    @py_assert9 = set(@py_assert7)
    @py_assert1 = temp_files_before == @py_assert9
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=635)
    if not @py_assert1:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py10)s\n{%(py10)s = %(py2)s(%(py8)s\n{%(py8)s = %(py5)s\n{%(py5)s = %(py3)s.listdir\n}(%(py6)s)\n})\n}', ), (temp_files_before, @py_assert9)) % {'py0':@pytest_ar._saferepr(temp_files_before) if 'temp_files_before' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_files_before) else 'temp_files_before',  'py2':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py3':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert7 = @py_assert9 = None
    @py_assert4 = os.listdir
    @py_assert7 = @py_assert4(destination)
    @py_assert9 = set(@py_assert7)
    @py_assert1 = dest_files_before == @py_assert9
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/node_test.py', lineno=636)
    if not @py_assert1:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py10)s\n{%(py10)s = %(py2)s(%(py8)s\n{%(py8)s = %(py5)s\n{%(py5)s = %(py3)s.listdir\n}(%(py6)s)\n})\n}', ), (dest_files_before, @py_assert9)) % {'py0':@pytest_ar._saferepr(dest_files_before) if 'dest_files_before' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest_files_before) else 'dest_files_before',  'py2':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py3':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(destination) if 'destination' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(destination) else 'destination',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert7 = @py_assert9 = None