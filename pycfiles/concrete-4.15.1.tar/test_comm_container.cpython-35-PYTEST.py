# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/charman/src/concrete-python/tests/test_comm_container.py
# Compiled at: 2017-08-05 16:54:39
# Size of source mod 2**32: 8350 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from concrete.util import DirectoryBackedCommunicationContainer, MemoryBackedCommunicationContainer, ZipFileBackedCommunicationContainer, RedisHashBackedCommunicationContainer, S3BackedCommunicationContainer
from concrete.util import create_comm
from concrete.util import write_communication_to_buffer
from concrete.validate import validate_communication
from pytest import raises, fixture
from mock import Mock, sentinel, patch, call

@fixture
def comm_id_and_buf(request):
    comm_id = 'temp comm'
    return (comm_id, write_communication_to_buffer(create_comm(comm_id)))


def test_directory_backed_comm_container_find_files_recursively():
    directory_path = 'tests/testdata/a'
    cc = DirectoryBackedCommunicationContainer(directory_path)
    @py_assert0 = 3
    @py_assert5 = len(cc)
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(cc) if 'cc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cc) else 'cc', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert5 = None


def test_directory_backed_comm_container_retrieve():
    directory_path = 'tests/testdata/a'
    cc = DirectoryBackedCommunicationContainer(directory_path)
    @py_assert0 = 3
    @py_assert5 = len(cc)
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(cc) if 'cc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cc) else 'cc', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert5 = None
    @py_assert0 = 'simple_1'
    @py_assert2 = @py_assert0 in cc
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, cc)) % {'py3': @pytest_ar._saferepr(cc) if 'cc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cc) else 'cc', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    for comm_id in cc:
        comm = cc[comm_id]
        @py_assert2 = validate_communication(comm)
        if not @py_assert2:
            @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert2 = None


def test_memory_backed_comm_container_file_too_large():
    comm_path = 'tests/testdata/simple.tar.gz'
    with raises(Exception):
        MemoryBackedCommunicationContainer(comm_path, max_file_size=500)


def test_memory_backed_comm_container_retrieve():
    comm_path = 'tests/testdata/simple.tar.gz'
    cc = MemoryBackedCommunicationContainer(comm_path)
    @py_assert0 = 3
    @py_assert5 = len(cc)
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(cc) if 'cc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cc) else 'cc', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert5 = None
    @py_assert0 = 'one'
    @py_assert2 = @py_assert0 in cc
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, cc)) % {'py3': @pytest_ar._saferepr(cc) if 'cc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cc) else 'cc', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    for comm_id in cc:
        comm = cc[comm_id]
        @py_assert2 = validate_communication(comm)
        if not @py_assert2:
            @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert2 = None


def test_zip_file_backed_comm_container_retrieve():
    zipfile_path = 'tests/testdata/simple.zip'
    cc = ZipFileBackedCommunicationContainer(zipfile_path)
    @py_assert0 = 3
    @py_assert5 = len(cc)
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(cc) if 'cc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cc) else 'cc', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert5 = None
    @py_assert0 = 'simple_1'
    @py_assert2 = @py_assert0 in cc
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, cc)) % {'py3': @pytest_ar._saferepr(cc) if 'cc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cc) else 'cc', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    for comm_id in cc:
        comm = cc[comm_id]
        @py_assert2 = validate_communication(comm)
        if not @py_assert2:
            @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert2 = None


def test_redis_hash_backed_comm_container_iter():
    redis_db = Mock(hkeys=Mock(side_effect=[
     [
      sentinel.name0, sentinel.name1, sentinel.name2]]))
    key = sentinel.key
    cc = RedisHashBackedCommunicationContainer(redis_db, key)
    it = iter(cc)
    @py_assert2 = next(it)
    @py_assert6 = sentinel.name0
    @py_assert4 = @py_assert2 == @py_assert6
    if not @py_assert4:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.name0\n}', ), (@py_assert2, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert2 = next(it)
    @py_assert6 = sentinel.name1
    @py_assert4 = @py_assert2 == @py_assert6
    if not @py_assert4:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.name1\n}', ), (@py_assert2, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert2 = next(it)
    @py_assert6 = sentinel.name2
    @py_assert4 = @py_assert2 == @py_assert6
    if not @py_assert4:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.name2\n}', ), (@py_assert2, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    with raises(StopIteration):
        next(it)
    redis_db.hkeys.assert_called_once_with(key)


def test_redis_hash_backed_comm_container_len():
    redis_db = Mock(hlen=Mock(side_effect=[3]))
    key = sentinel.key
    cc = RedisHashBackedCommunicationContainer(redis_db, key)
    @py_assert0 = 3
    @py_assert5 = len(cc)
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(cc) if 'cc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cc) else 'cc', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert5 = None
    redis_db.hlen.assert_called_once_with(key)


def test_redis_hash_backed_comm_container_not_contains():
    redis_db = Mock(hexists=Mock(side_effect=[False]))
    key = sentinel.key
    cc = RedisHashBackedCommunicationContainer(redis_db, key)
    @py_assert1 = sentinel.comm_id
    @py_assert3 = @py_assert1 not in cc
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.comm_id\n} not in %(py4)s', ), (@py_assert1, cc)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(cc) if 'cc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cc) else 'cc', 'py0': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    redis_db.hexists.assert_called_once_with(key, sentinel.comm_id)


def test_redis_hash_backed_comm_container_contains():
    redis_db = Mock(hexists=Mock(side_effect=[True]))
    key = sentinel.key
    cc = RedisHashBackedCommunicationContainer(redis_db, key)
    @py_assert1 = sentinel.comm_id
    @py_assert3 = @py_assert1 in cc
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.comm_id\n} in %(py4)s', ), (@py_assert1, cc)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(cc) if 'cc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cc) else 'cc', 'py0': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    redis_db.hexists.assert_called_once_with(key, sentinel.comm_id)


@patch('concrete.util.comm_container.read_communication_from_buffer')
def test_redis_hash_backed_comm_container_not_getitem(mock_read_communication_from_buffer):
    redis_db = Mock(hget=Mock(side_effect=[None]))
    key = sentinel.key
    cc = RedisHashBackedCommunicationContainer(redis_db, key)
    with raises(KeyError):
        cc[sentinel.comm_id]
    redis_db.hget.assert_called_once_with(key, sentinel.comm_id)
    @py_assert1 = mock_read_communication_from_buffer.called
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_read_communication_from_buffer) if 'mock_read_communication_from_buffer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_read_communication_from_buffer) else 'mock_read_communication_from_buffer'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None


@patch('concrete.util.comm_container.read_communication_from_buffer')
def test_redis_hash_backed_comm_container_getitem(mock_read_communication_from_buffer):
    redis_db = Mock(hget=Mock(side_effect=[sentinel.comm_buf]))
    key = sentinel.key
    cc = RedisHashBackedCommunicationContainer(redis_db, key)
    mock_read_communication_from_buffer.side_effect = [
     sentinel.comm]
    @py_assert0 = cc[sentinel.comm_id]
    @py_assert4 = sentinel.comm
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.comm\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    redis_db.hget.assert_called_once_with(key, sentinel.comm_id)
    mock_read_communication_from_buffer.assert_called_once_with(sentinel.comm_buf)


@patch('concrete.util.comm_container.unprefix_s3_key')
def test_s3_backed_comm_container_iter(mock_unprefix_s3_key):
    keys = [Mock(), Mock(), Mock()]
    keys[0].name = sentinel.prefixed_name0
    keys[1].name = sentinel.prefixed_name1
    keys[2].name = sentinel.prefixed_name2
    bucket = Mock(list=Mock(side_effect=[keys]))
    mock_unprefix_s3_key.side_effect = [
     sentinel.name0,
     sentinel.name1,
     sentinel.name2]
    cc = S3BackedCommunicationContainer(bucket, sentinel.prefix_len)
    it = iter(cc)
    @py_assert2 = next(it)
    @py_assert6 = sentinel.name0
    @py_assert4 = @py_assert2 == @py_assert6
    if not @py_assert4:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.name0\n}', ), (@py_assert2, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert2 = next(it)
    @py_assert6 = sentinel.name1
    @py_assert4 = @py_assert2 == @py_assert6
    if not @py_assert4:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.name1\n}', ), (@py_assert2, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert2 = next(it)
    @py_assert6 = sentinel.name2
    @py_assert4 = @py_assert2 == @py_assert6
    if not @py_assert4:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.name2\n}', ), (@py_assert2, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py5': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    with raises(StopIteration):
        next(it)
    bucket.list.assert_called_once_with()
    mock_unprefix_s3_key.assert_has_calls([
     call(sentinel.prefixed_name0, sentinel.prefix_len),
     call(sentinel.prefixed_name1, sentinel.prefix_len),
     call(sentinel.prefixed_name2, sentinel.prefix_len)])


@patch('concrete.util.comm_container.unprefix_s3_key')
def test_s3_backed_comm_container_len(mock_unprefix_s3_key):
    keys = [Mock(), Mock(), Mock()]
    keys[0].name = sentinel.prefixed_name0
    keys[1].name = sentinel.prefixed_name1
    keys[2].name = sentinel.prefixed_name2
    bucket = Mock(list=Mock(side_effect=[keys]))
    cc = S3BackedCommunicationContainer(bucket, sentinel.prefix_len)
    @py_assert0 = 3
    @py_assert5 = len(cc)
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(cc) if 'cc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cc) else 'cc', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert5 = None
    bucket.list.assert_called_once_with()


@patch('concrete.util.comm_container.prefix_s3_key')
def test_s3_backed_comm_container_not_contains(mock_prefix_s3_key):
    bucket = Mock(get_key=Mock(side_effect=[None]))
    mock_prefix_s3_key.side_effect = [sentinel.prefixed_name]
    cc = S3BackedCommunicationContainer(bucket, sentinel.prefix_len)
    @py_assert1 = sentinel.comm_id
    @py_assert3 = @py_assert1 not in cc
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.comm_id\n} not in %(py4)s', ), (@py_assert1, cc)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(cc) if 'cc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cc) else 'cc', 'py0': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    bucket.get_key.assert_called_once_with(sentinel.prefixed_name)
    mock_prefix_s3_key.assert_called_once_with(sentinel.comm_id, sentinel.prefix_len)


@patch('concrete.util.comm_container.prefix_s3_key')
def test_s3_backed_comm_container_contains(mock_prefix_s3_key):
    bucket = Mock(get_key=Mock(side_effect=[sentinel.key]))
    mock_prefix_s3_key.side_effect = [sentinel.prefixed_name]
    cc = S3BackedCommunicationContainer(bucket, sentinel.prefix_len)
    @py_assert1 = sentinel.comm_id
    @py_assert3 = @py_assert1 in cc
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.comm_id\n} in %(py4)s', ), (@py_assert1, cc)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(cc) if 'cc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cc) else 'cc', 'py0': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    bucket.get_key.assert_called_once_with(sentinel.prefixed_name)
    mock_prefix_s3_key.assert_called_once_with(sentinel.comm_id, sentinel.prefix_len)


@patch('concrete.util.comm_container.prefix_s3_key')
@patch('concrete.util.comm_container.read_communication_from_buffer')
def test_s3_backed_comm_container_not_getitem(mock_read_communication_from_buffer, mock_prefix_s3_key):
    bucket = Mock(get_key=Mock(side_effect=[None]))
    mock_prefix_s3_key.side_effect = [sentinel.prefixed_name]
    cc = S3BackedCommunicationContainer(bucket, sentinel.prefix_len)
    with raises(KeyError):
        cc[sentinel.comm_id]
    bucket.get_key.assert_called_once_with(sentinel.prefixed_name)
    mock_prefix_s3_key.assert_called_once_with(sentinel.comm_id, sentinel.prefix_len)
    @py_assert1 = mock_read_communication_from_buffer.called
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_read_communication_from_buffer) if 'mock_read_communication_from_buffer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_read_communication_from_buffer) else 'mock_read_communication_from_buffer'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None


@patch('concrete.util.comm_container.prefix_s3_key')
@patch('concrete.util.comm_container.read_communication_from_buffer')
def test_s3_backed_comm_container_getitem(mock_read_communication_from_buffer, mock_prefix_s3_key):
    bucket = Mock(get_key=Mock(side_effect=[
     Mock(get_contents_as_string=Mock(side_effect=[sentinel.comm_buf]))]))
    mock_prefix_s3_key.side_effect = [
     sentinel.prefixed_name]
    mock_read_communication_from_buffer.side_effect = [sentinel.comm]
    cc = S3BackedCommunicationContainer(bucket, sentinel.prefix_len)
    @py_assert0 = cc[sentinel.comm_id]
    @py_assert4 = sentinel.comm
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.comm\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    bucket.get_key.assert_called_once_with(sentinel.prefixed_name)
    mock_prefix_s3_key.assert_called_once_with(sentinel.comm_id, sentinel.prefix_len)
    mock_read_communication_from_buffer.assert_called_once_with(sentinel.comm_buf)