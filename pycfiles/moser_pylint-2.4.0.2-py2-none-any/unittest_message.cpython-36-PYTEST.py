# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/message/unittest_message.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 5425 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from pylint.checkers import BaseChecker
from pylint.exceptions import InvalidMessageError
from pylint.message import MessageDefinition, MessagesStore

@pytest.fixture
def store():
    return MessagesStore()


@pytest.mark.parametrize('messages,expected', [
 (
  {'W1234':('message one', 'msg-symbol-one', 'msg description'), 
   'W4321':('message two', 'msg-symbol-two', 'msg description')},
  "Inconsistent checker part in message id 'W4321' (expected 'x12xx' because we already had ['W1234'])."),
 (
  {'W1233':(
    'message two',
    'msg-symbol-two',
    'msg description',
    {'old_names': [('W1234', 'old-symbol')]}), 
   'W1234':('message one', 'msg-symbol-one', 'msg description')},
  "Message id 'W1234' cannot have both 'msg-symbol-one' and 'old-symbol' as symbolic name."),
 (
  {'W1234':('message one', 'msg-symbol-one', 'msg description'), 
   'W1235':(
    'message two',
    'msg-symbol-two',
    'msg description',
    {'old_names': [('W1234', 'old-symbol')]})},
  "Message id 'W1234' cannot have both 'msg-symbol-one' and 'old-symbol' as symbolic name."),
 (
  {'W1234':(
    'message one',
    'msg-symbol-one',
    'msg description',
    {'old_names': [('W1201', 'old-symbol-one')]}), 
   'W1235':(
    'message two',
    'msg-symbol-two',
    'msg description',
    {'old_names': [('W1201', 'old-symbol-two')]})},
  "Message id 'W1201' cannot have both 'old-symbol-one' and 'old-symbol-two' as symbolic name."),
 (
  {'W1234':('message one', 'msg-symbol', 'msg description'), 
   'W1235':('message two', 'msg-symbol', 'msg description')},
  "Message symbol 'msg-symbol' cannot be used for 'W1234' and 'W1235' at the same time."),
 (
  {'W1233':(
    'message two',
    'msg-symbol-two',
    'msg description',
    {'old_names': [('W1230', 'msg-symbol-one')]}), 
   'W1234':('message one', 'msg-symbol-one', 'msg description')},
  "Message symbol 'msg-symbol-one' cannot be used for 'W1230' and 'W1234' at the same time."),
 (
  {'W1234':('message one', 'msg-symbol-one', 'msg description'), 
   'W1235':(
    'message two',
    'msg-symbol-two',
    'msg description',
    {'old_names': [('W1230', 'msg-symbol-one')]})},
  "Message symbol 'msg-symbol-one' cannot be used for 'W1234' and 'W1235' at the same time."),
 (
  {'W1234':(
    'message one',
    'msg-symbol-one',
    'msg description',
    {'old_names': [('W1230', 'old-symbol-one')]}), 
   'W1235':(
    'message two',
    'msg-symbol-two',
    'msg description',
    {'old_names': [('W1231', 'old-symbol-one')]})},
  "Message symbol 'old-symbol-one' cannot be used for 'W1230' and 'W1235' at the same time.")])
def test_register_error(store, messages, expected):

    class Checker(BaseChecker):
        name = 'checker'
        msgs = messages

    with pytest.raises(InvalidMessageError) as (cm):
        store.register_messages_from_checker(Checker())
    @py_assert2 = cm.value
    @py_assert4 = str(@py_assert2)
    @py_assert6 = @py_assert4 == expected
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/message/unittest_message.py', lineno=126)
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.value\n})\n} == %(py7)s', ), (@py_assert4, expected)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(cm) if 'cm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cm) else 'cm',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None


def test_register_error_new_id_duplicate_of_new(store):

    class CheckerOne(BaseChecker):
        name = 'checker_one'
        msgs = {'W1234': ('message one', 'msg-symbol-one', 'msg description.')}

    class CheckerTwo(BaseChecker):
        name = 'checker_two'
        msgs = {'W1234': ('message two', 'msg-symbol-two', 'another msg description.')}

    store.register_messages_from_checker(CheckerOne())
    test_register_error(store, {'W1234': ('message two', 'msg-symbol-two', 'another msg description.')}, "Message id 'W1234' cannot have both 'msg-symbol-one' and 'msg-symbol-two' as symbolic name.")


@pytest.mark.parametrize('msgid,expected', [
 ('Q1234', "Bad message type Q in 'Q1234'"),
 ('W12345', "Invalid message id 'W12345'")])
def test_create_invalid_message_type(msgid, expected):
    with pytest.raises(InvalidMessageError) as (cm):
        MessageDefinition('checker', msgid, 'msg', 'descr', 'symbol', 'scope')
    @py_assert2 = cm.value
    @py_assert4 = str(@py_assert2)
    @py_assert6 = @py_assert4 == expected
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/message/unittest_message.py', lineno=156)
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.value\n})\n} == %(py7)s', ), (@py_assert4, expected)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(cm) if 'cm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cm) else 'cm',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None