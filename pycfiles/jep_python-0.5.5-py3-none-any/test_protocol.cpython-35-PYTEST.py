# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Work\jep\src\jep-python\build\lib\test\test_protocol.py
# Compiled at: 2016-01-04 11:09:40
# Size of source mod 2**32: 10435 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from unittest import mock
import umsgpack, pytest
from test.logconfig import configure_test_logger
from jep_py.protocol import MessageSerializer
from jep_py.schema import Shutdown, BackendAlive, ContentSync, OutOfSync, CompletionRequest, CompletionResponse, CompletionOption, SemanticType, ProblemUpdate, Problem, Severity, FileProblems, CompletionInvocation, StaticSyntaxRequest, SyntaxFormatType, StaticSyntaxList, StaticSyntax

def setup_function(function):
    configure_test_logger()


def test_message_serializer_serialize_chain():
    mock_packer = mock.MagicMock()
    mock_packer.dumps = mock.MagicMock(return_value=mock.sentinel.PACKER_RESULT)
    serializer = MessageSerializer(mock_packer)
    @py_assert1 = serializer.serialize
    @py_assert4 = Shutdown()
    @py_assert6 = @py_assert1(@py_assert4)
    @py_assert10 = mock.sentinel
    @py_assert12 = @py_assert10.PACKER_RESULT
    @py_assert8 = @py_assert6 == @py_assert12
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.serialize\n}(%(py5)s\n{%(py5)s = %(py3)s()\n})\n} == %(py13)s\n{%(py13)s = %(py11)s\n{%(py11)s = %(py9)s.sentinel\n}.PACKER_RESULT\n}',), (@py_assert6, @py_assert12)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py13': @pytest_ar._saferepr(@py_assert12), 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py0': @pytest_ar._saferepr(serializer) if 'serializer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(serializer) else 'serializer', 'py3': @pytest_ar._saferepr(Shutdown) if 'Shutdown' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Shutdown) else 'Shutdown'}
        @py_format16 = ('' + 'assert %(py15)s') % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    mock_packer.dumps.assert_called_once_with(dict(_message='Shutdown'))


def test_message_serializer_deserialize_chain():
    mock_packer = mock.MagicMock()
    mock_packer.load = mock.MagicMock(return_value=dict(_message=mock.sentinel.MESSAGE_NAME))
    buffer = bytes(b'bytes')
    with mock.patch('jep_py.protocol.Message.class_by_name', lambda name: Shutdown) as (mock_class_by_msgname):
        serializer = MessageSerializer(mock_packer)
        @py_assert2 = serializer.deserialize
        @py_assert5 = @py_assert2(buffer)
        @py_assert8 = isinstance(@py_assert5, Shutdown)
        if not @py_assert8:
            @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py0)s(%(py6)s\n{%(py6)s = %(py3)s\n{%(py3)s = %(py1)s.deserialize\n}(%(py4)s)\n}, %(py7)s)\n}') % {'py7': @pytest_ar._saferepr(Shutdown) if 'Shutdown' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Shutdown) else 'Shutdown', 'py4': @pytest_ar._saferepr(buffer) if 'buffer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(buffer) else 'buffer', 'py1': @pytest_ar._saferepr(serializer) if 'serializer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(serializer) else 'serializer', 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert2 = @py_assert5 = @py_assert8 = None
        @py_assert1 = mock_packer.load
        @py_assert3 = @py_assert1.called
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.load\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_packer) if 'mock_packer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_packer) else 'mock_packer', 'py4': @pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None


@pytest.fixture
def observable_serializer():
    """Provides message serializer to test with msgpack installed via observable mocks."""
    mock_packer = mock.MagicMock()
    mock_packer.loads = mock.MagicMock(side_effect=lambda bindata: umsgpack.loads(bindata))
    mock_packer.dumps = mock.MagicMock(side_effect=lambda pydict: umsgpack.dumps(pydict))
    return MessageSerializer(mock_packer)


def test_message_serializer_serialize_shutdown(observable_serializer):
    packed = observable_serializer.serialize(Shutdown())
    observable_serializer.packer.dumps.assert_called_once_with(dict(_message='Shutdown'))


def test_message_serializer_serialize_backend_alive(observable_serializer):
    packed = observable_serializer.serialize(BackendAlive())
    observable_serializer.packer.dumps.assert_called_once_with(dict(_message='BackendAlive'))


def test_message_serializer_serialize_content_sync(observable_serializer):
    packed = observable_serializer.serialize(ContentSync('thefile', bytes('thedata', 'utf-8'), 9, 11))
    observable_serializer.packer.dumps.assert_called_once_with(dict(_message='ContentSync', start=9, end=11, data=bytes('thedata', 'utf-8'), file='thefile'))


def test_message_serializer_serialize_out_of_sync(observable_serializer):
    packed = observable_serializer.serialize(OutOfSync('thefile'))
    observable_serializer.packer.dumps.assert_called_once_with(dict(_message='OutOfSync', file='thefile'))


def test_message_serializer_serialize_static_syntax_request(observable_serializer):
    packed = observable_serializer.serialize(StaticSyntaxRequest(SyntaxFormatType.textmate, ['c', 'h', 'cpp']))
    observable_serializer.packer.dumps.assert_called_once_with(dict(_message='StaticSyntaxRequest', format='textmate', fileExtensions=['c', 'h', 'cpp']))


def test_message_serializer_serialize_static_syntax_list(observable_serializer):
    packed = observable_serializer.serialize(StaticSyntaxList(SyntaxFormatType.textmate, [StaticSyntax('some.syntax', ['c', 'h', 'cpp'], 'DEFINITION')]))
    observable_serializer.packer.dumps.assert_called_once_with(dict(_message='StaticSyntaxList', format='textmate', syntaxes=[
     {'name': 'some.syntax', 'fileExtensions': ['c', 'h', 'cpp'], 'definition': 'DEFINITION'}]))


def test_message_serializer_serialize_completion_request(observable_serializer):
    packed = observable_serializer.serialize(CompletionRequest('thefile', 10, 17, 'thetoken'))
    observable_serializer.packer.dumps.assert_called_once_with(dict(_message='CompletionRequest', file='thefile', token='thetoken', pos=10, limit=17))


def test_message_serializer_serialize_completion_invocation(observable_serializer):
    packed = observable_serializer.serialize(CompletionInvocation('id'))
    observable_serializer.packer.dumps.assert_called_once_with(dict(_message='CompletionInvocation', extensionId='id'))


def test_message_serializer_serialize_problem_update(observable_serializer):
    msg = ProblemUpdate([FileProblems('thefile', [Problem('themsg', Severity.info, 99)], 50, 10, 20)], True)
    packed = observable_serializer.serialize(msg)
    observable_serializer.packer.dumps.assert_called_once_with(dict(_message='ProblemUpdate', partial=True, fileProblems=[
     dict(file='thefile', total=50, start=10, end=20, problems=[
      dict(message='themsg', severity='info', line=99)])]))


def test_message_serializer_serialize_completion_response(observable_serializer):
    msg = CompletionResponse(11, 12, True, [CompletionOption('display', 'thedescription', semantics=SemanticType.string, extensionId='theExtId'),
     CompletionOption('display2', 'thedescription2', semantics=SemanticType.identifier, extensionId='theExtId2')], 'thetoken')
    packed = observable_serializer.serialize(msg)
    expected = {'_message': 'CompletionResponse', 
     'token': 'thetoken', 
     'start': 11, 
     'end': 12, 
     'limitExceeded': True, 
     'options': [
                 {'insert': 'display', 'desc': 'thedescription', 'semantics': 'string', 'extensionId': 'theExtId'},
                 {'insert': 'display2', 'desc': 'thedescription2', 'semantics': 'identifier', 'extensionId': 'theExtId2'}]}
    observable_serializer.packer.dumps.assert_called_once_with(expected)


def test_message_serializer_deserialize_completion_response():
    unpacked = {'_message': 'CompletionResponse', 
     'token': 'thetoken', 
     'start': 11, 
     'end': 12, 
     'limitExceeded': True, 
     'options': [
                 {'insert': 'insert', 'desc': 'thedescription', 'semantics': 'string', 'extensionId': 'theExtId'},
                 {'insert': 'insert2', 'desc': 'thedescription2', 'semantics': 'identifier', 'extensionId': 'theExtId2'}]}
    packed = umsgpack.packb(unpacked)
    serializer = MessageSerializer()
    msg = serializer.deserialize(packed)
    expected = CompletionResponse(11, 12, True, [CompletionOption('insert', 'thedescription', semantics=SemanticType.string, extensionId='theExtId'),
     CompletionOption('insert2', 'thedescription2', semantics=SemanticType.identifier, extensionId='theExtId2')], 'thetoken')
    @py_assert1 = serializer.serialize
    @py_assert4 = @py_assert1(msg)
    @py_assert8 = serializer.serialize
    @py_assert11 = @py_assert8(expected)
    @py_assert6 = @py_assert4 == @py_assert11
    if not @py_assert6:
        @py_format13 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.serialize\n}(%(py3)s)\n} == %(py12)s\n{%(py12)s = %(py9)s\n{%(py9)s = %(py7)s.serialize\n}(%(py10)s)\n}',), (@py_assert4, @py_assert11)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(serializer) if 'serializer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(serializer) else 'serializer', 'py10': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected', 'py12': @pytest_ar._saferepr(@py_assert11), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(serializer) if 'serializer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(serializer) else 'serializer', 
         'py3': @pytest_ar._saferepr(msg) if 'msg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg) else 'msg'}
        @py_format15 = ('' + 'assert %(py14)s') % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert11 = None


def test_message_serializer_enqueue_dequeue():
    serializer = MessageSerializer()
    serializer.enque_data(serializer.serialize(CompletionResponse(1, 2, False, (), 'token')))
    serializer.enque_data(serializer.serialize(CompletionResponse(3, 4, True, (), 'token2')))
    @py_assert1 = serializer.buffer
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.buffer\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(serializer) if 'serializer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(serializer) else 'serializer'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    msg1 = serializer.dequeue_message()
    msg2 = serializer.dequeue_message()
    msg3 = serializer.dequeue_message()
    msg4 = serializer.dequeue_message()
    @py_assert3 = isinstance(msg1, CompletionResponse)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py2': @pytest_ar._saferepr(CompletionResponse) if 'CompletionResponse' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(CompletionResponse) else 'CompletionResponse', 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(msg1) if 'msg1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg1) else 'msg1'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert1 = msg1.token
    @py_assert4 = 'token'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.token\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(msg1) if 'msg1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg1) else 'msg1'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = msg1.start
    @py_assert4 = 1
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.start\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(msg1) if 'msg1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg1) else 'msg1'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = msg1.end
    @py_assert4 = 2
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.end\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(msg1) if 'msg1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg1) else 'msg1'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = msg1.limitExceeded
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.limitExceeded\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(msg1) if 'msg1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg1) else 'msg1'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = isinstance(msg2, CompletionResponse)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py2': @pytest_ar._saferepr(CompletionResponse) if 'CompletionResponse' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(CompletionResponse) else 'CompletionResponse', 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(msg2) if 'msg2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg2) else 'msg2'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert1 = msg2.token
    @py_assert4 = 'token2'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.token\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(msg2) if 'msg2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg2) else 'msg2'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = msg2.start
    @py_assert4 = 3
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.start\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(msg2) if 'msg2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg2) else 'msg2'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = msg2.end
    @py_assert4 = 4
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.end\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(msg2) if 'msg2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg2) else 'msg2'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = msg2.limitExceeded
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.limitExceeded\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(msg2) if 'msg2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg2) else 'msg2'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert1 = not msg3
    if not @py_assert1:
        @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(msg3) if 'msg3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg3) else 'msg3'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert1 = None
    @py_assert1 = not msg4
    if not @py_assert1:
        @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(msg4) if 'msg4' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg4) else 'msg4'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert1 = None


def test_message_serializer_enqueue_dequeue_incomplete():
    serializer = MessageSerializer()
    packed = serializer.serialize(CompletionResponse(1, 2, False))
    @py_assert2 = len(packed)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 > @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('>', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} > %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(packed) if 'packed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(packed) else 'packed', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    for b in packed:
        @py_assert1 = serializer.dequeue_message
        @py_assert3 = @py_assert1()
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.dequeue_message\n}()\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(serializer) if 'serializer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(serializer) else 'serializer', 'py4': @pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        serializer.enque_data([b])

    @py_assert2 = serializer.dequeue_message
    @py_assert4 = @py_assert2()
    @py_assert7 = isinstance(@py_assert4, CompletionResponse)
    if not @py_assert7:
        @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.dequeue_message\n}()\n}, %(py6)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(serializer) if 'serializer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(serializer) else 'serializer', 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(CompletionResponse) if 'CompletionResponse' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(CompletionResponse) else 'CompletionResponse'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert1 = serializer.dequeue_message
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.dequeue_message\n}()\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(serializer) if 'serializer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(serializer) else 'serializer', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_message_serializer_message_iterator():
    serializer = MessageSerializer()
    serializer.enque_data(serializer.serialize(CompletionResponse(1, 2, False)))
    serializer.enque_data(serializer.serialize(CompletionResponse(3, 4, True)))
    count = 0
    for msg in serializer:
        @py_assert3 = isinstance(msg, CompletionResponse)
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py2': @pytest_ar._saferepr(CompletionResponse) if 'CompletionResponse' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(CompletionResponse) else 'CompletionResponse', 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(msg) if 'msg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg) else 'msg'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert3 = None
        count += 1

    @py_assert2 = 2
    @py_assert1 = count == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (count, @py_assert2)) % {'py0': @pytest_ar._saferepr(count) if 'count' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(count) else 'count', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_deserialize_problem_update_ruby_backend():
    serialized = b'\x82\xacfileProblems\x91\x82\xa4file\xda\x001C:\\Users\\mthiede\\gitrepos\\jep-ruby\\demo\\test.demo\xa8problems\x91\x83\xa7message\xb5unexpected token kEND\xa8severity\xa5error\xa4line\x04\xa8_message\xadProblemUpdate'
    serializer = MessageSerializer()
    serializer.enque_data(serialized)
    message = next(iter(serializer))
    @py_assert3 = isinstance(message, ProblemUpdate)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py2': @pytest_ar._saferepr(ProblemUpdate) if 'ProblemUpdate' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ProblemUpdate) else 'ProblemUpdate', 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(message) if 'message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message) else 'message'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert0 = message.fileProblems[0].problems[0]
    @py_assert2 = @py_assert0.severity
    @py_assert6 = Severity.error
    @py_assert4 = @py_assert2 is @py_assert6
    if not @py_assert4:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.severity\n} is %(py7)s\n{%(py7)s = %(py5)s.error\n}', ), (@py_assert2, @py_assert6)) % {'py5': @pytest_ar._saferepr(Severity) if 'Severity' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Severity) else 'Severity', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_regression_009_string_argument_without_encoding():
    serialized = b'\x83\xa8_message\xabContentSync\xa4file\xd9!D:\\Work\\jep\\test\\my.requestlogger\xa4data\xa40sdf,smndfsdf M s df jhsdkashdk  sjhdjhsjdkakdhsj'
    serializer = MessageSerializer()
    serializer.enque_data(serialized)
    message = next(iter(serializer))
    @py_assert3 = isinstance(message, ContentSync)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py2': @pytest_ar._saferepr(ContentSync) if 'ContentSync' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ContentSync) else 'ContentSync', 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(message) if 'message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message) else 'message'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None


def test_descode_static_syntax_request():
    serialized = b'\x82\xa6format\xa8textmate\xa8_message\xb3StaticSyntaxRequest'
    serializer = MessageSerializer()
    serializer.enque_data(serialized)
    message = next(iter(serializer))
    @py_assert3 = isinstance(message, StaticSyntaxRequest)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py2': @pytest_ar._saferepr(StaticSyntaxRequest) if 'StaticSyntaxRequest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(StaticSyntaxRequest) else 'StaticSyntaxRequest', 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(message) if 'message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message) else 'message'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None