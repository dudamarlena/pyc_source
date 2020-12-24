# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/charman/src/concrete-python/tests/test_redis_io.py
# Compiled at: 2017-08-05 16:54:39
# Size of source mod 2**32: 22549 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from itertools import product
from mock import Mock, sentinel, patch, call
from pytest import raises, mark
from concrete.util.redis_io import read_communication_from_redis_key, write_communication_to_redis_key, RedisCommunicationReader, RedisCommunicationWriter

@patch('concrete.util.redis_io.read_communication_from_buffer')
def test_read_communication_from_redis_key(mock_read_communication_from_buffer):
    redis = Mock(get=Mock(side_effect=[sentinel.buf]))
    mock_read_communication_from_buffer.side_effect = [sentinel.comm]
    @py_assert3 = sentinel.key
    @py_assert6 = sentinel.add_references
    @py_assert8 = read_communication_from_redis_key(redis, @py_assert3, @py_assert6)
    @py_assert12 = sentinel.comm
    @py_assert10 = @py_assert8 == @py_assert12
    if not @py_assert10:
        @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py1)s, %(py4)s\n{%(py4)s = %(py2)s.key\n}, %(py7)s\n{%(py7)s = %(py5)s.add_references\n})\n} == %(py13)s\n{%(py13)s = %(py11)s.comm\n}',), (@py_assert8, @py_assert12)) % {'py2': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py13': @pytest_ar._saferepr(@py_assert12), 'py0': @pytest_ar._saferepr(read_communication_from_redis_key) if 'read_communication_from_redis_key' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(read_communication_from_redis_key) else 'read_communication_from_redis_key', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis', 'py11': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel'}
        @py_format16 = ('' + 'assert %(py15)s') % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    redis.get.assert_called_once_with(sentinel.key)
    mock_read_communication_from_buffer.assert_called_once_with(sentinel.buf, add_references=sentinel.add_references)


@patch('concrete.util.redis_io.read_communication_from_buffer')
def test_read_communication_from_redis_key_empty(mock_read_communication_from_buffer):
    redis = Mock(get=Mock(side_effect=[None]))
    @py_assert3 = sentinel.key
    @py_assert6 = sentinel.add_references
    @py_assert8 = read_communication_from_redis_key(redis, @py_assert3, @py_assert6)
    @py_assert11 = None
    @py_assert10 = @py_assert8 is @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('is',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py1)s, %(py4)s\n{%(py4)s = %(py2)s.key\n}, %(py7)s\n{%(py7)s = %(py5)s.add_references\n})\n} is %(py12)s',), (@py_assert8, @py_assert11)) % {'py12': @pytest_ar._saferepr(@py_assert11), 'py2': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py0': @pytest_ar._saferepr(read_communication_from_redis_key) if 'read_communication_from_redis_key' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(read_communication_from_redis_key) else 'read_communication_from_redis_key', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis', 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel'}
        @py_format15 = ('' + 'assert %(py14)s') % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    redis.get.assert_called_once_with(sentinel.key)
    @py_assert1 = mock_read_communication_from_buffer.called
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_read_communication_from_buffer) if 'mock_read_communication_from_buffer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_read_communication_from_buffer) else 'mock_read_communication_from_buffer'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None


@patch('concrete.util.redis_io.write_communication_to_buffer')
def test_write_communication_to_redis_key(mock_write_communication_to_buffer):
    redis = Mock(set=Mock())
    mock_write_communication_to_buffer.side_effect = [sentinel.buf]
    write_communication_to_redis_key(redis, sentinel.key, sentinel.comm)
    redis.set.assert_called_once_with(sentinel.key, sentinel.buf)
    mock_write_communication_to_buffer.assert_called_once_with(sentinel.comm)


@mark.parametrize('right_to_left,pop,inferred,block', list(product((False, True), (False,
                                                                                   True), (False,
                                                                                           True), (False, ))) + list(product((False,
                                                                                                                              True), (True, ), (False,
                                                                                                                                                True), (True, ))))
@patch('concrete.util.redis_io.read_communication_from_buffer')
def test_redis_communication_reader_list(mock_read_communication_from_buffer, right_to_left, pop, inferred, block):
    redis = Mock(llen=Mock(return_value=2), lindex=Mock(side_effect=[sentinel.buf0, sentinel.buf1]), lpop=Mock(side_effect=[sentinel.buf0, sentinel.buf1, None]), rpop=Mock(side_effect=[sentinel.buf0, sentinel.buf1, None]), blpop=Mock(side_effect=[
     (
      sentinel.key, sentinel.buf0), (sentinel.key, sentinel.buf1), None]), brpop=Mock(side_effect=[
     (
      sentinel.key, sentinel.buf0), (sentinel.key, sentinel.buf1), None]), type=Mock(return_value='list'))
    mock_read_communication_from_buffer.side_effect = [
     sentinel.comm0, sentinel.comm1]
    reader = RedisCommunicationReader(redis, sentinel.key, key_type=None if inferred else 'list', add_references=sentinel.add_references, right_to_left=right_to_left, pop=pop, block=block, block_timeout=sentinel.block_timeout)
    it = iter(reader)
    @py_assert2 = next(it)
    @py_assert6 = sentinel.comm0
    @py_assert4 = @py_assert2 == @py_assert6
    if not @py_assert4:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.comm0\n}', ), (@py_assert2, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert2 = next(it)
    @py_assert6 = sentinel.comm1
    @py_assert4 = @py_assert2 == @py_assert6
    if not @py_assert4:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.comm1\n}', ), (@py_assert2, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    with raises(StopIteration):
        next(it)
    if inferred:
        redis.type.assert_called_once_with(sentinel.key)
    else:
        @py_assert1 = redis.type
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
    if pop:
        @py_assert1 = redis.llen
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.llen\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = redis.lindex
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.lindex\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        if block:
            @py_assert1 = redis.lpop
            @py_assert3 = @py_assert1.called
            @py_assert5 = not @py_assert3
            if not @py_assert5:
                @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.lpop\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert3 = @py_assert5 = None
            @py_assert1 = redis.rpop
            @py_assert3 = @py_assert1.called
            @py_assert5 = not @py_assert3
            if not @py_assert5:
                @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.rpop\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert3 = @py_assert5 = None
            getattr(redis, 'brpop' if right_to_left else 'blpop').assert_has_calls([
             call(sentinel.key, timeout=sentinel.block_timeout),
             call(sentinel.key, timeout=sentinel.block_timeout),
             call(sentinel.key, timeout=sentinel.block_timeout)])
            @py_assert2 = 'blpop' if right_to_left else 'brpop'
            @py_assert4 = getattr(redis, @py_assert2)
            @py_assert6 = @py_assert4.called
            @py_assert8 = not @py_assert6
            if not @py_assert8:
                @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}.called\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(getattr) if 'getattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getattr) else 'getattr', 'py7': @pytest_ar._saferepr(@py_assert6)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
        else:
            getattr(redis, 'rpop' if right_to_left else 'lpop').assert_has_calls([
             call(sentinel.key),
             call(sentinel.key),
             call(sentinel.key)])
            @py_assert2 = 'lpop' if right_to_left else 'rpop'
            @py_assert4 = getattr(redis, @py_assert2)
            @py_assert6 = @py_assert4.called
            @py_assert8 = not @py_assert6
            if not @py_assert8:
                @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}.called\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(getattr) if 'getattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getattr) else 'getattr', 'py7': @pytest_ar._saferepr(@py_assert6)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
            @py_assert1 = redis.blpop
            @py_assert3 = @py_assert1.called
            @py_assert5 = not @py_assert3
            if not @py_assert5:
                @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.blpop\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert3 = @py_assert5 = None
            @py_assert1 = redis.brpop
            @py_assert3 = @py_assert1.called
            @py_assert5 = not @py_assert3
            if not @py_assert5:
                @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.brpop\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert3 = @py_assert5 = None
    else:
        redis.llen.assert_called_with(sentinel.key)
        redis.lindex.assert_has_calls([
         call(sentinel.key, -1 if right_to_left else 0),
         call(sentinel.key, -2 if right_to_left else 1)])
        @py_assert1 = redis.lpop
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.lpop\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = redis.rpop
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.rpop\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = redis.blpop
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.blpop\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = redis.brpop
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.brpop\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
    mock_read_communication_from_buffer.assert_has_calls([
     call(sentinel.buf0, add_references=sentinel.add_references),
     call(sentinel.buf1, add_references=sentinel.add_references)])


@mark.parametrize('right_to_left,pop,block', list(product((False, True), (False, True), (False, ))) + list(product((False,
                                                                                                                    True), (True, ), (True, ))))
@patch('concrete.util.redis_io.read_communication_from_buffer')
def test_redis_communication_reader_list_empty(mock_read_communication_from_buffer, right_to_left, pop, block):
    redis = Mock(llen=Mock(return_value=0), lindex=Mock(), lpop=Mock(side_effect=[None]), rpop=Mock(side_effect=[None]), blpop=Mock(side_effect=[None]), brpop=Mock(side_effect=[None]))
    reader = RedisCommunicationReader(redis, sentinel.key, key_type='list', add_references=sentinel.add_references, right_to_left=right_to_left, pop=pop, block=block, block_timeout=sentinel.block_timeout)
    it = iter(reader)
    with raises(StopIteration):
        next(it)
    if pop:
        if block:
            @py_assert1 = redis.llen
            @py_assert3 = @py_assert1.called
            @py_assert5 = not @py_assert3
            if not @py_assert5:
                @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.llen\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert3 = @py_assert5 = None
            @py_assert1 = redis.lindex
            @py_assert3 = @py_assert1.called
            @py_assert5 = not @py_assert3
            if not @py_assert5:
                @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.lindex\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert3 = @py_assert5 = None
            @py_assert1 = redis.lpop
            @py_assert3 = @py_assert1.called
            @py_assert5 = not @py_assert3
            if not @py_assert5:
                @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.lpop\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert3 = @py_assert5 = None
            @py_assert1 = redis.rpop
            @py_assert3 = @py_assert1.called
            @py_assert5 = not @py_assert3
            if not @py_assert5:
                @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.rpop\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert3 = @py_assert5 = None
            getattr(redis, 'brpop' if right_to_left else 'blpop').assert_called_once_with(sentinel.key, timeout=sentinel.block_timeout)
            @py_assert2 = 'blpop' if right_to_left else 'brpop'
            @py_assert4 = getattr(redis, @py_assert2)
            @py_assert6 = @py_assert4.called
            @py_assert8 = not @py_assert6
            if not @py_assert8:
                @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}.called\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(getattr) if 'getattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getattr) else 'getattr', 'py7': @pytest_ar._saferepr(@py_assert6)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
        else:
            @py_assert1 = redis.llen
            @py_assert3 = @py_assert1.called
            @py_assert5 = not @py_assert3
            if not @py_assert5:
                @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.llen\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert3 = @py_assert5 = None
            @py_assert1 = redis.lindex
            @py_assert3 = @py_assert1.called
            @py_assert5 = not @py_assert3
            if not @py_assert5:
                @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.lindex\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert3 = @py_assert5 = None
            getattr(redis, 'rpop' if right_to_left else 'lpop').assert_called_once_with(sentinel.key)
            @py_assert2 = 'lpop' if right_to_left else 'rpop'
            @py_assert4 = getattr(redis, @py_assert2)
            @py_assert6 = @py_assert4.called
            @py_assert8 = not @py_assert6
            if not @py_assert8:
                @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}.called\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(getattr) if 'getattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getattr) else 'getattr', 'py7': @pytest_ar._saferepr(@py_assert6)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
            @py_assert1 = redis.blpop
            @py_assert3 = @py_assert1.called
            @py_assert5 = not @py_assert3
            if not @py_assert5:
                @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.blpop\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert3 = @py_assert5 = None
            @py_assert1 = redis.brpop
            @py_assert3 = @py_assert1.called
            @py_assert5 = not @py_assert3
            if not @py_assert5:
                @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.brpop\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert3 = @py_assert5 = None
    else:
        redis.llen.assert_called_with(sentinel.key)
        @py_assert1 = redis.lindex
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.lindex\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = redis.lpop
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.lpop\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = redis.rpop
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.rpop\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = redis.blpop
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.blpop\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = redis.brpop
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.brpop\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = mock_read_communication_from_buffer.called
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_read_communication_from_buffer) if 'mock_read_communication_from_buffer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_read_communication_from_buffer) else 'mock_read_communication_from_buffer'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None


@mark.parametrize('right_to_left,inferred', list(product((False, True), (False, True))))
@patch('concrete.util.redis_io.read_communication_from_buffer')
def test_redis_communication_reader_set(mock_read_communication_from_buffer, right_to_left, inferred):

    def _sadd(_, buf):
        return {sentinel.buf0: 1, 
         sentinel.buf1: 0, 
         sentinel.buf2: 0, 
         sentinel.buf3: 1, 
         sentinel.buf4: 0}[buf]

    redis = Mock(sscan=Mock(side_effect=[
     (
      7, [sentinel.buf0, sentinel.buf1]),
     (
      3, [sentinel.buf2]),
     (
      0, [sentinel.buf3, sentinel.buf4])]), sadd=Mock(side_effect=_sadd), scard=Mock(return_value=2), expire=Mock(), exists=Mock(side_effect=[True, False]), type=Mock(return_value='set'))
    mock_read_communication_from_buffer.side_effect = [
     sentinel.comm0, sentinel.comm3]
    reader = RedisCommunicationReader(redis, 'my-key', key_type=None if inferred else 'set', add_references=sentinel.add_references, right_to_left=right_to_left)
    it = iter(reader)
    @py_assert2 = next(it)
    @py_assert6 = sentinel.comm0
    @py_assert4 = @py_assert2 == @py_assert6
    if not @py_assert4:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.comm0\n}', ), (@py_assert2, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert2 = next(it)
    @py_assert6 = sentinel.comm3
    @py_assert4 = @py_assert2 == @py_assert6
    if not @py_assert4:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.comm3\n}', ), (@py_assert2, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    with raises(StopIteration):
        next(it)
    if inferred:
        redis.type.assert_called_once_with('my-key')
    else:
        @py_assert1 = redis.type
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
    redis.sscan.assert_has_calls([
     call('my-key', 0),
     call('my-key', 7),
     call('my-key', 3)])
    mock_read_communication_from_buffer.assert_has_calls([
     call(sentinel.buf0, add_references=sentinel.add_references),
     call(sentinel.buf3, add_references=sentinel.add_references)])


@mark.parametrize('right_to_left,inferred', list(product((False, True), (False, True))))
@patch('concrete.util.redis_io.read_communication_from_buffer')
def test_redis_communication_reader_set_batch(mock_read_communication_from_buffer, right_to_left, inferred):
    redis = Mock(srandmember=Mock(side_effect=[
     [
      sentinel.buf0, sentinel.buf1]]), type=Mock(return_value='set'))
    mock_read_communication_from_buffer.side_effect = [
     sentinel.comm0, sentinel.comm1]
    reader = RedisCommunicationReader(redis, sentinel.key, key_type=None if inferred else 'set', add_references=sentinel.add_references, right_to_left=right_to_left)
    @py_assert1 = reader.batch
    @py_assert4 = sentinel.batch_size
    @py_assert6 = @py_assert1(@py_assert4)
    @py_assert9 = [sentinel.comm0, sentinel.comm1]
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.batch\n}(%(py5)s\n{%(py5)s = %(py3)s.batch_size\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py3': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(reader) if 'reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reader) else 'reader', 'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    if inferred:
        redis.type.assert_called_once_with(sentinel.key)
    else:
        @py_assert1 = redis.type
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
    redis.srandmember.assert_called_once_with(sentinel.key, sentinel.batch_size)
    mock_read_communication_from_buffer.assert_has_calls([
     call(sentinel.buf0, add_references=sentinel.add_references),
     call(sentinel.buf1, add_references=sentinel.add_references)])


@mark.parametrize('right_to_left,inferred', list(product((False, True), (False, True))))
@patch('concrete.util.redis_io.read_communication_from_buffer')
def test_redis_communication_reader_hash(mock_read_communication_from_buffer, right_to_left, inferred):

    def _sadd(_, comm_id):
        return {sentinel.comm_id0: 1, 
         sentinel.comm_id1: 0, 
         sentinel.comm_id2: 0, 
         sentinel.comm_id3: 1, 
         sentinel.comm_id4: 0}[comm_id]

    redis = Mock(hscan=Mock(side_effect=[
     (
      7, {sentinel.comm_id0: sentinel.buf0, sentinel.comm_id1: sentinel.buf1}),
     (
      3, {sentinel.comm_id2: sentinel.buf2}),
     (
      0, {sentinel.comm_id3: sentinel.buf3, sentinel.comm_id4: sentinel.buf4})]), sadd=Mock(side_effect=_sadd), hlen=Mock(return_value=2), expire=Mock(), exists=Mock(side_effect=[True, False]), type=Mock(return_value='hash'))
    mock_read_communication_from_buffer.side_effect = [
     sentinel.comm0, sentinel.comm3]
    reader = RedisCommunicationReader(redis, 'my-key', key_type=None if inferred else 'hash', add_references=sentinel.add_references, right_to_left=right_to_left)
    it = iter(reader)
    @py_assert2 = next(it)
    @py_assert6 = sentinel.comm0
    @py_assert4 = @py_assert2 == @py_assert6
    if not @py_assert4:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.comm0\n}', ), (@py_assert2, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert2 = next(it)
    @py_assert6 = sentinel.comm3
    @py_assert4 = @py_assert2 == @py_assert6
    if not @py_assert4:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.comm3\n}', ), (@py_assert2, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    with raises(StopIteration):
        next(it)
    if inferred:
        redis.type.assert_called_once_with('my-key')
    else:
        @py_assert1 = redis.type
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
    redis.hscan.assert_has_calls([
     call('my-key', 0),
     call('my-key', 7),
     call('my-key', 3)])
    mock_read_communication_from_buffer.assert_has_calls([
     call(sentinel.buf0, add_references=sentinel.add_references),
     call(sentinel.buf3, add_references=sentinel.add_references)])


@mark.parametrize('right_to_left,inferred', list(product((False, True), (False, True))))
@patch('concrete.util.redis_io.read_communication_from_buffer')
def test_redis_communication_reader_set_pop(mock_read_communication_from_buffer, right_to_left, inferred):
    redis = Mock(spop=Mock(side_effect=[sentinel.buf0, sentinel.buf1, None]), type=Mock(return_value='set'))
    mock_read_communication_from_buffer.side_effect = [
     sentinel.comm0, sentinel.comm1]
    reader = RedisCommunicationReader(redis, sentinel.key, key_type=None if inferred else 'set', add_references=sentinel.add_references, right_to_left=right_to_left, pop=True)
    it = iter(reader)
    @py_assert2 = next(it)
    @py_assert6 = sentinel.comm0
    @py_assert4 = @py_assert2 == @py_assert6
    if not @py_assert4:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.comm0\n}', ), (@py_assert2, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert2 = next(it)
    @py_assert6 = sentinel.comm1
    @py_assert4 = @py_assert2 == @py_assert6
    if not @py_assert4:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.comm1\n}', ), (@py_assert2, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    with raises(StopIteration):
        next(it)
    if inferred:
        redis.type.assert_called_once_with(sentinel.key)
    else:
        @py_assert1 = redis.type
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
    redis.spop.assert_has_calls([
     call(sentinel.key),
     call(sentinel.key),
     call(sentinel.key)])
    mock_read_communication_from_buffer.assert_has_calls([
     call(sentinel.buf0, add_references=sentinel.add_references),
     call(sentinel.buf1, add_references=sentinel.add_references)])


@mark.parametrize('right_to_left', [
 (False, ), (True, )])
@patch('concrete.util.redis_io.read_communication_from_buffer')
def test_redis_communication_reader_set_pop_empty(mock_read_communication_from_buffer, right_to_left):
    redis = Mock(spop=Mock(side_effect=[None]), type=Mock(return_value='set'))
    reader = RedisCommunicationReader(redis, sentinel.key, key_type='set', add_references=sentinel.add_references, right_to_left=right_to_left, pop=True)
    it = iter(reader)
    with raises(StopIteration):
        next(it)
    @py_assert1 = redis.type
    @py_assert3 = @py_assert1.called
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    redis.spop.assert_called_once_with(sentinel.key)
    @py_assert1 = mock_read_communication_from_buffer.called
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_read_communication_from_buffer) if 'mock_read_communication_from_buffer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_read_communication_from_buffer) else 'mock_read_communication_from_buffer'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None


@mark.parametrize('right_to_left,inferred,key_type,pop,block', list(product((False,
                                                                             True), (False,
                                                                                     True), ('set',
                                                                                             'list',
                                                                                             'hash'), (False, ), (False, ))) + list(product((False,
                                                                                                                                             True), (False,
                                                                                                                                                     True), ('set',
                                                                                                                                                             'list'), (True, ), (False, ))) + list(product((False,
                                                                                                                                                                                                            True), (False,
                                                                                                                                                                                                                    True), ('list', ), (True, ), (True, ))))
def test_redis_communication_reader_len(right_to_left, inferred, key_type, pop, block):
    redis = Mock(llen=Mock(side_effect=[3]), hlen=Mock(side_effect=[3]), scard=Mock(side_effect=[3]), type=Mock(return_value=key_type.encode('utf-8')))
    reader = RedisCommunicationReader(redis, sentinel.key, key_type=None if inferred else key_type, right_to_left=right_to_left, pop=pop, block=block)
    if inferred:
        redis.type.assert_called_once_with(sentinel.key)
    else:
        @py_assert1 = redis.type
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
    len(reader)
    if key_type == 'set':
        @py_assert1 = redis.scard
        @py_assert3 = @py_assert1.called_once_with
        @py_assert6 = sentinel.key
        @py_assert8 = @py_assert3(@py_assert6)
        if not @py_assert8:
            @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.scard\n}.called_once_with\n}(%(py7)s\n{%(py7)s = %(py5)s.key\n})\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis', 'py7': @pytest_ar._saferepr(@py_assert6), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py9': @pytest_ar._saferepr(@py_assert8)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
        @py_assert1 = redis.llen
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.llen\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = redis.hlen
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.hlen\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
    else:
        if key_type == 'list':
            @py_assert1 = redis.scard
            @py_assert3 = @py_assert1.called
            @py_assert5 = not @py_assert3
            if not @py_assert5:
                @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.scard\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert3 = @py_assert5 = None
            @py_assert1 = redis.llen
            @py_assert3 = @py_assert1.called_once_with
            @py_assert6 = sentinel.key
            @py_assert8 = @py_assert3(@py_assert6)
            if not @py_assert8:
                @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.llen\n}.called_once_with\n}(%(py7)s\n{%(py7)s = %(py5)s.key\n})\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis', 'py7': @pytest_ar._saferepr(@py_assert6), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py9': @pytest_ar._saferepr(@py_assert8)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format10))
            @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
            @py_assert1 = redis.hlen
            @py_assert3 = @py_assert1.called
            @py_assert5 = not @py_assert3
            if not @py_assert5:
                @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.hlen\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert3 = @py_assert5 = None
        else:
            if key_type == 'hash':
                @py_assert1 = redis.scard
                @py_assert3 = @py_assert1.called
                @py_assert5 = not @py_assert3
                if not @py_assert5:
                    @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.scard\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                @py_assert1 = @py_assert3 = @py_assert5 = None
                @py_assert1 = redis.llen
                @py_assert3 = @py_assert1.called
                @py_assert5 = not @py_assert3
                if not @py_assert5:
                    @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.llen\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                @py_assert1 = @py_assert3 = @py_assert5 = None
                @py_assert1 = redis.hlen
                @py_assert3 = @py_assert1.called_once_with
                @py_assert6 = sentinel.key
                @py_assert8 = @py_assert3(@py_assert6)
                if not @py_assert8:
                    @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.hlen\n}.called_once_with\n}(%(py7)s\n{%(py7)s = %(py5)s.key\n})\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis', 'py7': @pytest_ar._saferepr(@py_assert6), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py9': @pytest_ar._saferepr(@py_assert8)}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
            else:
                raise ValueError('unexpected key type {}'.format(key_type))


def test_redis_communication_reader_failed_infer():
    redis = Mock(type=Mock(return_value='none'))
    with raises(Exception):
        RedisCommunicationReader(redis, sentinel.key, add_references=sentinel.add_references)
    redis.type.assert_called_with(sentinel.key)


@mark.parametrize('key_type', [
 ('string', ), ('zset', )])
def test_redis_communication_reader_failed_key_type(key_type):
    with raises(ValueError):
        RedisCommunicationReader(sentinel.redis, sentinel.key, key_type=key_type)


@mark.parametrize('right_to_left,inferred,key_type,pop', list(product((False, True), (False,
                                                                                      True), ('set',
                                                                                              'hash'), (True, ))) + list(product((False,
                                                                                                                                  True), (False,
                                                                                                                                          True), ('set',
                                                                                                                                                  'hash',
                                                                                                                                                  'list'), (False, ))))
def test_redis_communication_reader_failed_block(right_to_left, inferred, key_type, pop):
    redis = Mock(type=Mock(return_value=key_type.encode('utf-8')))
    with raises(ValueError):
        RedisCommunicationReader(redis, sentinel.key, key_type=None if inferred else key_type, add_references=sentinel.add_references, pop=pop, block=True)
    if not inferred:
        @py_assert1 = redis.type
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None


@mark.parametrize('right_to_left,inferred,key_type,pop,block', list(product((False,
                                                                             True), (False,
                                                                                     True), ('set', ), (False,
                                                                                                        True), (False, ))) + list(product((False,
                                                                                                                                           True), (False,
                                                                                                                                                   True), ('hash', ), (False, ), (False, ))) + list(product((False,
                                                                                                                                                                                                             True), (False,
                                                                                                                                                                                                                     True), ('list', ), (False,
                                                                                                                                                                                                                                         True), (False, ))) + list(product((False,
                                                                                                                                                                                                                                                                            True), (False,
                                                                                                                                                                                                                                                                                    True), ('list', ), (True, ), (True, ))))
def test_redis_communication_reader_failed_batch(right_to_left, inferred, key_type, pop, block):
    redis = Mock(type=Mock(return_value=key_type.encode('utf-8')))
    reader = RedisCommunicationReader(redis, sentinel.key, key_type=None if inferred else key_type, add_references=sentinel.add_references, pop=pop, block=block)
    if inferred:
        redis.type.assert_called_once_with(sentinel.key)
    else:
        @py_assert1 = redis.type
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
    with raises(Exception):
        reader.batch(sentinel.batch_size)


@mark.parametrize('right_to_left,inferred,block', list(product((False, True), (False,
                                                                               True), (False,
                                                                                       True))))
def test_redis_communication_reader_failed_pop(right_to_left, inferred, block):
    redis = Mock(type=Mock(return_value='hash'))
    with raises(ValueError):
        RedisCommunicationReader(redis, sentinel.key, key_type=None if inferred else 'hash', add_references=sentinel.add_references, block=block, pop=True)
    if not inferred:
        @py_assert1 = redis.type
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None


@mark.parametrize('right_to_left,inferred', list(product((False, True), (False, True))))
@patch('concrete.util.redis_io.write_communication_to_buffer')
def test_redis_communication_writer_list(mock_write_communication_to_buffer, right_to_left, inferred):
    redis = Mock(lpush=Mock(side_effect=[3]), rpush=Mock(side_effect=[3]), type=Mock(return_value='list'))
    mock_write_communication_to_buffer.side_effect = [
     sentinel.buf]
    writer = RedisCommunicationWriter(redis, sentinel.key, key_type=None if inferred else 'list', right_to_left=right_to_left)
    if inferred:
        redis.type.assert_called_once_with(sentinel.key)
    else:
        @py_assert1 = redis.type
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
    writer.write(sentinel.comm)
    getattr(redis, 'lpush' if right_to_left else 'rpush').assert_called_once_with(sentinel.key, sentinel.buf)
    @py_assert2 = 'rpush' if right_to_left else 'lpush'
    @py_assert4 = getattr(redis, @py_assert2)
    @py_assert6 = @py_assert4.called
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}.called\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(getattr) if 'getattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getattr) else 'getattr', 'py7': @pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    mock_write_communication_to_buffer.assert_called_once_with(sentinel.comm)


@mark.parametrize('right_to_left,inferred', list(product((False, True), (False, True))))
@patch('concrete.util.redis_io.write_communication_to_buffer')
def test_redis_communication_writer_set(mock_write_communication_to_buffer, right_to_left, inferred):
    redis = Mock(sadd=Mock(side_effect=[0]), type=Mock(return_value='set'))
    mock_write_communication_to_buffer.side_effect = [
     sentinel.buf]
    writer = RedisCommunicationWriter(redis, sentinel.key, key_type=None if inferred else 'set', right_to_left=right_to_left)
    if inferred:
        redis.type.assert_called_once_with(sentinel.key)
    else:
        @py_assert1 = redis.type
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
    writer.write(sentinel.comm)
    redis.sadd.assert_called_once_with(sentinel.key, sentinel.buf)
    @py_assert2 = 'rpush' if right_to_left else 'lpush'
    @py_assert4 = getattr(redis, @py_assert2)
    @py_assert6 = @py_assert4.called
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}.called\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(getattr) if 'getattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getattr) else 'getattr', 'py7': @pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    mock_write_communication_to_buffer.assert_called_once_with(sentinel.comm)


@mark.parametrize('right_to_left,inferred,uuid_hash_key', list(product((False, True), (False,
                                                                                       True), (False,
                                                                                               True))))
@patch('concrete.util.redis_io.write_communication_to_buffer')
def test_redis_communication_writer_hash(mock_write_communication_to_buffer, right_to_left, inferred, uuid_hash_key):
    redis = Mock(hset=Mock(side_effect=[0]), type=Mock(return_value='hash'))
    comm = Mock(id=sentinel.comm_id, uuid=Mock(uuidString=sentinel.comm_uuid))
    mock_write_communication_to_buffer.side_effect = [sentinel.buf]
    writer = RedisCommunicationWriter(redis, sentinel.key, key_type=None if inferred else 'hash', right_to_left=right_to_left, uuid_hash_key=uuid_hash_key)
    if inferred:
        redis.type.assert_called_once_with(sentinel.key)
    else:
        @py_assert1 = redis.type
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
    writer.write(comm)
    redis.hset.assert_called_once_with(sentinel.key, sentinel.comm_uuid if uuid_hash_key else sentinel.comm_id, sentinel.buf)
    @py_assert2 = 'rpush' if right_to_left else 'lpush'
    @py_assert4 = getattr(redis, @py_assert2)
    @py_assert6 = @py_assert4.called
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}.called\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(getattr) if 'getattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getattr) else 'getattr', 'py7': @pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    mock_write_communication_to_buffer.assert_called_once_with(comm)


@mark.parametrize('right_to_left,inferred,key_type', list(product((False, True), (False,
                                                                                  True), ('set',
                                                                                          'list',
                                                                                          'hash'))))
def test_redis_communication_writer_clear(right_to_left, inferred, key_type):
    redis = Mock(delete=Mock(side_effect=[0]), type=Mock(return_value=key_type.encode('utf-8')))
    writer = RedisCommunicationWriter(redis, sentinel.key, key_type=None if inferred else 'hash', right_to_left=right_to_left)
    if inferred:
        redis.type.assert_called_once_with(sentinel.key)
    else:
        @py_assert1 = redis.type
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(redis) if 'redis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(redis) else 'redis'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
    writer.clear()
    redis.delete.assert_called_once_with(sentinel.key)


def test_redis_communication_writer_failed_infer():
    redis = Mock(type=Mock(return_value='none'))
    with raises(Exception):
        RedisCommunicationWriter(redis, sentinel.key)
    redis.type.assert_called_with(sentinel.key)


@mark.parametrize('key_type', [
 ('string', ), ('zset', )])
def test_redis_communication_writer_failed_key_type(key_type):
    with raises(ValueError):
        RedisCommunicationWriter(sentinel.redis, sentinel.key, key_type=key_type)