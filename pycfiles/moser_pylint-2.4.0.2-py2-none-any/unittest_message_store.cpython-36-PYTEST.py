# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/message/unittest_message_store.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 4136 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from contextlib import redirect_stdout
from io import StringIO
import pytest
from pylint.checkers import BaseChecker
from pylint.exceptions import InvalidMessageError, UnknownMessageError
from pylint.message import MessageDefinition, MessagesStore

@pytest.fixture
def store():
    store = MessagesStore()

    class Checker(BaseChecker):
        name = 'achecker'
        msgs = {'W1234':(
          'message',
          'msg-symbol',
          'msg description.',
          {'old_names': [('W0001', 'old-symbol')]}), 
         'E1234':(
          'Duplicate keyword argument %r in %s call',
          'duplicate-keyword-arg',
          'Used when a function call passes the same keyword argument multiple times.',
          {'maxversion': (2, 6)})}

    store.register_messages_from_checker(Checker())
    return store


class TestMessagesStore(object):

    def _compare_messages(self, desc, msg, checkerref=False):
        @py_assert3 = msg.format_help
        @py_assert6 = @py_assert3(checkerref=checkerref)
        @py_assert1 = desc == @py_assert6
        if @py_assert1 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/message/unittest_message_store.py', lineno=43)
        if not @py_assert1:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s.format_help\n}(checkerref=%(py5)s)\n}', ), (desc, @py_assert6)) % {'py0':@pytest_ar._saferepr(desc) if 'desc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(desc) else 'desc',  'py2':@pytest_ar._saferepr(msg) if 'msg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg) else 'msg',  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(checkerref) if 'checkerref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checkerref) else 'checkerref',  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert6 = None

    def test_check_message_id(self, store):
        @py_assert1 = store.get_message_definitions('W1234')[0]
        @py_assert4 = isinstance(@py_assert1, MessageDefinition)
        if @py_assert4 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/message/unittest_message_store.py', lineno=46)
        if not @py_assert4:
            @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(MessageDefinition) if 'MessageDefinition' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(MessageDefinition) else 'MessageDefinition',  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None
        with pytest.raises(UnknownMessageError):
            store.get_message_definitions('YB12')

    def test_message_help(self, store):
        message_definition = store.get_message_definitions('W1234')[0]
        self._compare_messages(':msg-symbol (W1234): *message*\n  msg description. This message belongs to the achecker checker.',
          message_definition,
          checkerref=True)
        self._compare_messages(':msg-symbol (W1234): *message*\n  msg description.',
          message_definition,
          checkerref=False)

    def test_message_help_minmax(self, store):
        message_definition = store.get_message_definitions('E1234')[0]
        self._compare_messages(":duplicate-keyword-arg (E1234): *Duplicate keyword argument %r in %s call*\n  Used when a function call passes the same keyword argument multiple times.\n  This message belongs to the achecker checker. It can't be emitted when using\n  Python >= 2.6.",
          message_definition,
          checkerref=True)
        self._compare_messages(":duplicate-keyword-arg (E1234): *Duplicate keyword argument %r in %s call*\n  Used when a function call passes the same keyword argument multiple times.\n  This message can't be emitted when using Python >= 2.6.",
          message_definition,
          checkerref=False)

    def test_list_messages(self, store):
        output = StringIO()
        with redirect_stdout(output):
            store.list_messages()
        @py_assert0 = ':msg-symbol (W1234): *message*'
        @py_assert4 = output.getvalue
        @py_assert6 = @py_assert4()
        @py_assert2 = @py_assert0 in @py_assert6
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/message/unittest_message_store.py', lineno=89)
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.getvalue\n}()\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None

    def test_add_renamed_message(self, store):
        store.add_renamed_message('W1234', 'old-bad-name', 'msg-symbol')
        @py_assert0 = 'msg-symbol'
        @py_assert3 = store.get_message_definitions('W1234')[0]
        @py_assert5 = @py_assert3.symbol
        @py_assert2 = @py_assert0 == @py_assert5
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/message/unittest_message_store.py', lineno=93)
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.symbol\n}', ), (@py_assert0, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'msg-symbol'
        @py_assert3 = store.get_message_definitions('old-bad-name')[0]
        @py_assert5 = @py_assert3.symbol
        @py_assert2 = @py_assert0 == @py_assert5
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/message/unittest_message_store.py', lineno=94)
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.symbol\n}', ), (@py_assert0, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None

    def test_add_renamed_message_invalid(self, store):
        with pytest.raises(InvalidMessageError) as (cm):
            store.add_renamed_message('W1234', 'old-msg-symbol', 'duplicate-keyword-arg')
        expected = "Message id 'W1234' cannot have both 'msg-symbol' and 'old-msg-symbol' as symbolic name."
        @py_assert2 = cm.value
        @py_assert4 = str(@py_assert2)
        @py_assert6 = @py_assert4 == expected
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/message/unittest_message_store.py', lineno=106)
        if not @py_assert6:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.value\n})\n} == %(py7)s', ), (@py_assert4, expected)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(cm) if 'cm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cm) else 'cm',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert2 = @py_assert4 = @py_assert6 = None

    def test_renamed_message_register(self, store):
        @py_assert0 = 'msg-symbol'
        @py_assert3 = store.get_message_definitions('W0001')[0]
        @py_assert5 = @py_assert3.symbol
        @py_assert2 = @py_assert0 == @py_assert5
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/message/unittest_message_store.py', lineno=109)
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.symbol\n}', ), (@py_assert0, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'msg-symbol'
        @py_assert3 = store.get_message_definitions('old-symbol')[0]
        @py_assert5 = @py_assert3.symbol
        @py_assert2 = @py_assert0 == @py_assert5
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/message/unittest_message_store.py', lineno=110)
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.symbol\n}', ), (@py_assert0, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None