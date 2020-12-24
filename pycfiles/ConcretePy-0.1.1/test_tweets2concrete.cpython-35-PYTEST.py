# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/charman/src/concrete-python/integration-tests/test_tweets2concrete.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 10854 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pytest import fixture, mark
from concrete.util import CommunicationReader
from concrete.validate import validate_communication
import os, sys, json
from subprocess import Popen, PIPE
from tempfile import mkstemp

def assert_first_comm(comm):
    @py_assert1 = comm.id
    @py_assert4 = '238426131689242624'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = comm.startTime
    @py_assert4 = 1345680194
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.startTime\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = comm.endTime
    @py_assert4 = 1345680194
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.endTime\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert2 = validate_communication(comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None


def assert_second_comm(comm):
    @py_assert1 = comm.id
    @py_assert4 = '238426131689242625'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = comm.startTime
    @py_assert4 = 1345680195
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.startTime\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = comm.endTime
    @py_assert4 = 1345680195
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.endTime\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert2 = validate_communication(comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None


@fixture
def log_conf(request):
    fd, log_path = mkstemp()
    os.close(fd)
    fd, conf_path = mkstemp()
    os.close(fd)
    with open(conf_path, 'w') as (f):
        json.dump(dict(version=1, root=dict(level='INFO', handlers=[
         'file']), formatters=dict(medium=dict(format='%(asctime)-15s %(levelname)s: %(message)s')), handlers=dict(file={'class': 'logging.FileHandler', 
         'formatter': 'medium', 
         'filename': log_path})), f)

    def _remove():
        if os.path.exists(conf_path):
            os.remove(conf_path)
        if os.path.exists(log_path):
            os.remove(log_path)

    request.addfinalizer(_remove)
    return (
     conf_path, log_path)


@fixture
def output_file(request):
    fd, path = mkstemp()
    os.close(fd)

    def _remove():
        if os.path.exists(path):
            os.remove(path)

    request.addfinalizer(_remove)
    return path


def test_tweets2concrete(output_file):
    p = Popen([
     sys.executable,
     'scripts/tweets2concrete.py',
     'tests/testdata/tweets.json',
     output_file], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    @py_assert1 = p.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    reader = CommunicationReader(output_file)
    it = iter(reader)
    comm, _ = next(it)
    assert_first_comm(comm)
    comm, _ = next(it)
    assert_second_comm(comm)
    try:
        next(it)
    except StopIteration:
        pass
    else:
        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None


@mark.posix
def test_tweets2concrete_stdin(output_file):
    p = Popen([
     sys.executable,
     'scripts/tweets2concrete.py',
     '-',
     output_file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    with open('tests/testdata/tweets.json', 'rb') as (f):
        stdout, stderr = p.communicate(f.read())
    @py_assert1 = p.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    reader = CommunicationReader(output_file)
    it = iter(reader)
    comm, _ = next(it)
    assert_first_comm(comm)
    comm, _ = next(it)
    assert_second_comm(comm)
    try:
        next(it)
    except StopIteration:
        pass
    else:
        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None


@mark.posix
def test_tweets2concrete_stdout(output_file):
    p = Popen([
     sys.executable,
     'scripts/tweets2concrete.py',
     'tests/testdata/tweets.json',
     '-'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    @py_assert1 = p.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    with open(output_file, 'wb') as (f):
        f.write(stdout)
    reader = CommunicationReader(output_file)
    it = iter(reader)
    comm, _ = next(it)
    assert_first_comm(comm)
    comm, _ = next(it)
    assert_second_comm(comm)
    try:
        next(it)
    except StopIteration:
        pass
    else:
        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None


def test_tweets2concrete_multiproc(output_file):
    p = Popen([
     sys.executable,
     'scripts/tweets2concrete.py',
     '--num-proc', '2',
     'tests/testdata/tweets.json',
     output_file], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    @py_assert1 = p.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    reader = CommunicationReader(output_file)
    it = iter(reader)
    comm, _ = next(it)
    assert_first_comm(comm)
    comm, _ = next(it)
    assert_second_comm(comm)
    try:
        next(it)
    except StopIteration:
        pass
    else:
        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None


def test_tweets2concrete_log_every(output_file):
    p = Popen([
     sys.executable,
     'scripts/tweets2concrete.py',
     '--log-level', 'INFO',
     '--log-interval', '1',
     'tests/testdata/tweets.json',
     output_file], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    @py_assert1 = p.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = [line for line in stderr.decode('utf-8').strip().split('\n') if 'INFO' in line]
    @py_assert3 = len(@py_assert1)
    @py_assert6 = 2
    @py_assert5 = @py_assert3 >= @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} >= %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    reader = CommunicationReader(output_file)
    it = iter(reader)
    comm, _ = next(it)
    assert_first_comm(comm)
    comm, _ = next(it)
    assert_second_comm(comm)
    try:
        next(it)
    except StopIteration:
        pass
    else:
        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None


def test_tweets2concrete_unicode(output_file):
    p = Popen([
     sys.executable,
     'scripts/tweets2concrete.py',
     'tests/testdata/tweets.unicode.json',
     output_file], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    @py_assert1 = p.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    reader = CommunicationReader(output_file)
    it = iter(reader)
    comm, _ = next(it)
    assert_first_comm(comm)
    @py_assert2 = validate_communication(comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    comm, _ = next(it)
    assert_second_comm(comm)
    try:
        next(it)
    except StopIteration:
        pass
    else:
        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None


def test_tweets2concrete_gz(output_file):
    p = Popen([
     sys.executable,
     'scripts/tweets2concrete.py',
     'tests/testdata/tweets.json.gz',
     output_file], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    @py_assert1 = p.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    reader = CommunicationReader(output_file)
    it = iter(reader)
    comm, _ = next(it)
    assert_first_comm(comm)
    comm, _ = next(it)
    assert_second_comm(comm)
    try:
        next(it)
    except StopIteration:
        pass
    else:
        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None


def test_tweets2concrete_incomplete_gz(output_file):
    p = Popen([
     sys.executable,
     'scripts/tweets2concrete.py',
     '--catch-ioerror',
     'tests/testdata/tweets.json.incomplete.gz',
     output_file], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    @py_assert1 = p.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    reader = CommunicationReader(output_file)
    it = iter(reader)
    comm, _ = next(it)
    assert_first_comm(comm)
    comm, _ = next(it)
    assert_second_comm(comm)
    try:
        next(it)
    except StopIteration:
        pass
    else:
        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None


def test_tweets2concrete_incomplete_gz_multiproc(output_file):
    p = Popen([
     sys.executable,
     'scripts/tweets2concrete.py',
     '--num-proc', '2',
     '--catch-ioerror',
     'tests/testdata/tweets.json.incomplete.gz',
     output_file], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    @py_assert1 = p.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    reader = CommunicationReader(output_file)
    it = iter(reader)
    comm, _ = next(it)
    assert_first_comm(comm)
    comm, _ = next(it)
    assert_second_comm(comm)
    try:
        next(it)
    except StopIteration:
        pass
    else:
        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None


def test_tweets2concrete_log_config(log_conf, output_file):
    log_conf_path, log_path = log_conf
    p = Popen([
     sys.executable,
     'scripts/tweets2concrete.py',
     '--log-conf-path', log_conf_path,
     '--log-interval', '1',
     'tests/testdata/tweets.json',
     output_file], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    @py_assert1 = stdout.decode
    @py_assert3 = 'utf-8'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = ''
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.decode\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = stderr.decode
    @py_assert3 = 'utf-8'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = ''
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.decode\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(stderr) if 'stderr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stderr) else 'stderr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = p.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    with open(log_path) as (f):
        data = f.read()
        @py_assert1 = [line for line in data.strip().split('\n') if 'INFO' in line]
        @py_assert3 = len(@py_assert1)
        @py_assert6 = 2
        @py_assert5 = @py_assert3 >= @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} >= %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    reader = CommunicationReader(output_file)
    it = iter(reader)
    comm, _ = next(it)
    assert_first_comm(comm)
    comm, _ = next(it)
    assert_second_comm(comm)
    try:
        next(it)
    except StopIteration:
        pass
    else:
        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None


def test_tweets2concrete_deleted(output_file):
    p = Popen([
     sys.executable,
     'scripts/tweets2concrete.py',
     'tests/testdata/tweets.deleted.json',
     output_file], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    @py_assert1 = p.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    reader = CommunicationReader(output_file)
    it = iter(reader)
    comm, _ = next(it)
    assert_first_comm(comm)
    comm, _ = next(it)
    assert_second_comm(comm)
    try:
        next(it)
    except StopIteration:
        pass
    else:
        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None


def test_tweets2concrete_bad_line(output_file):
    p = Popen([
     sys.executable,
     'scripts/tweets2concrete.py',
     '--skip-bad-lines',
     'tests/testdata/tweets.bad-line.json',
     output_file], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    @py_assert1 = p.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    reader = CommunicationReader(output_file)
    it = iter(reader)
    comm, _ = next(it)
    assert_first_comm(comm)
    comm, _ = next(it)
    assert_second_comm(comm)
    try:
        next(it)
    except StopIteration:
        pass
    else:
        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None


def test_tweets2concrete_bad_line_unicode(output_file):
    p = Popen([
     sys.executable,
     'scripts/tweets2concrete.py',
     '--skip-bad-lines',
     'tests/testdata/tweets.bad-line-unicode.json',
     output_file], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    @py_assert1 = p.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    reader = CommunicationReader(output_file)
    it = iter(reader)
    comm, _ = next(it)
    assert_first_comm(comm)
    comm, _ = next(it)
    assert_second_comm(comm)
    try:
        next(it)
    except StopIteration:
        pass
    else:
        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None


def test_tweets2concrete_invalid(output_file):
    p = Popen([
     sys.executable,
     'scripts/tweets2concrete.py',
     '--skip-invalid-comms',
     'tests/testdata/tweets.invalid.json',
     output_file], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    @py_assert1 = p.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    reader = CommunicationReader(output_file)
    it = iter(reader)
    comm, _ = next(it)
    assert_first_comm(comm)
    comm, _ = next(it)
    assert_second_comm(comm)
    try:
        next(it)
    except StopIteration:
        pass
    else:
        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None