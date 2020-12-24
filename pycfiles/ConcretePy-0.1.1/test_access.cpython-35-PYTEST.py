# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/charman/src/concrete-python/tests/test_access.py
# Compiled at: 2017-08-05 16:54:39
# Size of source mod 2**32: 2741 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from concrete.util import RedisHashBackedStoreHandler, S3BackedStoreHandler, prefix_s3_key, unprefix_s3_key
from concrete import ServiceInfo
from mock import Mock, sentinel, patch

def test_redis_hash_backed_store_handler_about():
    redis_db = Mock()
    key = Mock()
    handler = RedisHashBackedStoreHandler(redis_db, key)
    @py_assert2 = handler.about
    @py_assert4 = @py_assert2()
    @py_assert7 = isinstance(@py_assert4, ServiceInfo)
    if not @py_assert7:
        @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.about\n}()\n}, %(py6)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py1': @pytest_ar._saferepr(handler) if 'handler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(handler) else 'handler', 'py5': @pytest_ar._saferepr(@py_assert4), 'py6': @pytest_ar._saferepr(ServiceInfo) if 'ServiceInfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ServiceInfo) else 'ServiceInfo'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert7 = None


def test_redis_hash_backed_store_handler_alive():
    redis_db = Mock()
    key = Mock()
    handler = RedisHashBackedStoreHandler(redis_db, key)
    @py_assert1 = handler.alive
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.alive\n}()\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(handler) if 'handler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(handler) else 'handler'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


@patch('concrete.util.access.RedisCommunicationWriter')
def test_redis_hash_backed_store_handler_store(mock_redis_communication_writer_class):
    mock_redis_communication_writer = mock_redis_communication_writer_class.return_value
    redis_db = Mock()
    key = Mock()
    comm = Mock()
    comm.id = sentinel.comm_id
    handler = RedisHashBackedStoreHandler(redis_db, key)
    mock_redis_communication_writer_class.assert_called_once_with(redis_db, key, key_type='hash')
    handler.store(comm)
    mock_redis_communication_writer.write.assert_called_once_with(comm)


def test_s3_backed_store_handler_about():
    bucket = Mock()
    handler = S3BackedStoreHandler(bucket)
    @py_assert2 = handler.about
    @py_assert4 = @py_assert2()
    @py_assert7 = isinstance(@py_assert4, ServiceInfo)
    if not @py_assert7:
        @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.about\n}()\n}, %(py6)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py1': @pytest_ar._saferepr(handler) if 'handler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(handler) else 'handler', 'py5': @pytest_ar._saferepr(@py_assert4), 'py6': @pytest_ar._saferepr(ServiceInfo) if 'ServiceInfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ServiceInfo) else 'ServiceInfo'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert7 = None


def test_s3_backed_store_handler_alive():
    bucket = Mock()
    handler = S3BackedStoreHandler(bucket)
    @py_assert1 = handler.alive
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.alive\n}()\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(handler) if 'handler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(handler) else 'handler'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_prefix_s3_key():
    @py_assert1 = 'asdf'
    @py_assert3 = 0
    @py_assert5 = prefix_s3_key(@py_assert1, @py_assert3)
    @py_assert8 = 'asdf'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(prefix_s3_key) if 'prefix_s3_key' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(prefix_s3_key) else 'prefix_s3_key', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 'asdf'
    @py_assert3 = 1
    @py_assert5 = prefix_s3_key(@py_assert1, @py_assert3)
    @py_assert8 = '9asdf'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(prefix_s3_key) if 'prefix_s3_key' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(prefix_s3_key) else 'prefix_s3_key', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 'asdf'
    @py_assert3 = 2
    @py_assert5 = prefix_s3_key(@py_assert1, @py_assert3)
    @py_assert8 = '91asdf'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(prefix_s3_key) if 'prefix_s3_key' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(prefix_s3_key) else 'prefix_s3_key', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_unprefix_s3_key():
    @py_assert1 = 'xyasdf'
    @py_assert3 = 0
    @py_assert5 = unprefix_s3_key(@py_assert1, @py_assert3)
    @py_assert8 = 'xyasdf'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(unprefix_s3_key) if 'unprefix_s3_key' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(unprefix_s3_key) else 'unprefix_s3_key', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 'xyasdf'
    @py_assert3 = 1
    @py_assert5 = unprefix_s3_key(@py_assert1, @py_assert3)
    @py_assert8 = 'yasdf'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(unprefix_s3_key) if 'unprefix_s3_key' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(unprefix_s3_key) else 'unprefix_s3_key', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 'xyasdf'
    @py_assert3 = 2
    @py_assert5 = unprefix_s3_key(@py_assert1, @py_assert3)
    @py_assert8 = 'asdf'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(unprefix_s3_key) if 'unprefix_s3_key' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(unprefix_s3_key) else 'unprefix_s3_key', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


@patch('concrete.util.access.prefix_s3_key')
@patch('concrete.util.access.write_communication_to_buffer')
def test_s3_backed_store_handler_store(mock_write_communication_to_buffer, mock_prefix_s3_key):
    key = Mock()
    bucket = Mock(get_key=Mock(side_effect=[key]))
    comm = Mock()
    comm.id = sentinel.comm_id
    handler = S3BackedStoreHandler(bucket, sentinel.prefix_len)
    mock_prefix_s3_key.side_effect = [
     sentinel.prefixed_key]
    mock_write_communication_to_buffer.side_effect = [sentinel.buf]
    handler.store(comm)
    bucket.get_key.assert_called_once_with(sentinel.prefixed_key, validate=False)
    mock_prefix_s3_key.assert_called_once_with(sentinel.comm_id, sentinel.prefix_len)
    mock_write_communication_to_buffer.assert_called_once_with(comm)
    key.set_contents_from_string.assert_called_once_with(sentinel.buf)