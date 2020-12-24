# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/charman/src/concrete-python/integration-tests/test_file_io.py
# Compiled at: 2018-03-01 12:43:03
# Size of source mod 2**32: 30161 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, gzip, os, tarfile
from time import time, localtime
from calendar import timegm
import zipfile
from concrete.util import CommunicationReader, CommunicationWriter, CommunicationWriterTar, CommunicationWriterTGZ, CommunicationWriterZip, read_communication_from_file, FileType
from pytest import fixture, raises
from tempfile import mkstemp
TIME_MARGIN = 3600

@fixture
def login_info():
    if os.name == 'nt':
        return dict(uid=0, gid=0, username='', groupname='')
    else:
        import pwd, grp
        uid = os.getuid()
        gid = os.getgid()
        return dict(uid=uid, gid=gid, username=pwd.getpwuid(uid).pw_name, groupname=grp.getgrgid(gid).gr_name)


@fixture
def output_file(request):
    fd, path = mkstemp()
    os.close(fd)

    def _remove():
        if os.path.exists(path):
            os.remove(path)

    request.addfinalizer(_remove)
    return path


def test_output_file_finalizer_sanity(output_file):
    @py_assert0 = True
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None


def test_CommunicationReader_single_file():
    filename = 'tests/testdata/simple_1.concrete'
    reader = CommunicationReader(filename)
    comm1, comm1_filename = next(reader)
    @py_assert2 = 'sentenceForUUID'
    @py_assert4 = hasattr(comm1, @py_assert2)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert0 = 'one'
    @py_assert4 = comm1.id
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert1 = filename == comm1_filename
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (filename, comm1_filename)) % {'py2': @pytest_ar._saferepr(comm1_filename) if 'comm1_filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1_filename) else 'comm1_filename', 'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_CommunicationReader_single_gz_file():
    filename = 'tests/testdata/simple_1.concrete.gz'
    reader = CommunicationReader(filename)
    comm1, comm1_filename = next(reader)
    @py_assert2 = 'sentenceForUUID'
    @py_assert4 = hasattr(comm1, @py_assert2)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert0 = 'one'
    @py_assert4 = comm1.id
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert1 = filename == comm1_filename
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (filename, comm1_filename)) % {'py2': @pytest_ar._saferepr(comm1_filename) if 'comm1_filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1_filename) else 'comm1_filename', 'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_CommunicationReader_single_bz2_file():
    filename = 'tests/testdata/simple_1.concrete.bz2'
    reader = CommunicationReader(filename)
    comm1, comm1_filename = next(reader)
    @py_assert2 = 'sentenceForUUID'
    @py_assert4 = hasattr(comm1, @py_assert2)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert0 = 'one'
    @py_assert4 = comm1.id
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert1 = filename == comm1_filename
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (filename, comm1_filename)) % {'py2': @pytest_ar._saferepr(comm1_filename) if 'comm1_filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1_filename) else 'comm1_filename', 'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_CommunicationReader_concatenated_file():
    filename = 'tests/testdata/simple_concatenated'
    reader = CommunicationReader(filename)
    comms, filenames = zip(*[(c, f) for c, f in reader])
    for i, comm_id in enumerate(['one', 'two', 'three']):
        @py_assert1 = comms[i]
        @py_assert3 = 'sentenceForUUID'
        @py_assert5 = hasattr(@py_assert1, @py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert2 = comms[i]
        @py_assert4 = @py_assert2.id
        @py_assert1 = comm_id == @py_assert4
        if not @py_assert1:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (comm_id, @py_assert4)) % {'py0': @pytest_ar._saferepr(comm_id) if 'comm_id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm_id) else 'comm_id', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert2 = @py_assert4 = None
        @py_assert2 = filenames[i]
        @py_assert1 = filename == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (filename, @py_assert2)) % {'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_CommunicationReader_concatenated_gz_file():
    filename = 'tests/testdata/simple_concatenated.gz'
    reader = CommunicationReader(filename)
    comms, filenames = zip(*[(c, f) for c, f in reader])
    for i, comm_id in enumerate(['one', 'two', 'three']):
        @py_assert1 = comms[i]
        @py_assert3 = 'sentenceForUUID'
        @py_assert5 = hasattr(@py_assert1, @py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert2 = comms[i]
        @py_assert4 = @py_assert2.id
        @py_assert1 = comm_id == @py_assert4
        if not @py_assert1:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (comm_id, @py_assert4)) % {'py0': @pytest_ar._saferepr(comm_id) if 'comm_id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm_id) else 'comm_id', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert2 = @py_assert4 = None
        @py_assert2 = filenames[i]
        @py_assert1 = filename == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (filename, @py_assert2)) % {'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_CommunicationReader_concatenated_bz2_file():
    filename = 'tests/testdata/simple_concatenated.bz2'
    reader = CommunicationReader(filename)
    comms, filenames = zip(*[(c, f) for c, f in reader])
    for i, comm_id in enumerate(['one', 'two', 'three']):
        @py_assert1 = comms[i]
        @py_assert3 = 'sentenceForUUID'
        @py_assert5 = hasattr(@py_assert1, @py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert2 = comms[i]
        @py_assert4 = @py_assert2.id
        @py_assert1 = comm_id == @py_assert4
        if not @py_assert1:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (comm_id, @py_assert4)) % {'py0': @pytest_ar._saferepr(comm_id) if 'comm_id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm_id) else 'comm_id', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert2 = @py_assert4 = None
        @py_assert2 = filenames[i]
        @py_assert1 = filename == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (filename, @py_assert2)) % {'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_CommunicationReader_tar_file():
    filename = 'tests/testdata/simple.tar'
    reader = CommunicationReader(filename)
    comms, filenames = zip(*[(c, f) for c, f in reader])
    @py_assert1 = comms[0]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[1]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[2]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'one'
    @py_assert3 = comms[0]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'two'
    @py_assert3 = comms[1]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'three'
    @py_assert3 = comms[2]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'simple_1.concrete'
    @py_assert3 = filenames[0]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_2.concrete'
    @py_assert3 = filenames[1]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_3.concrete'
    @py_assert3 = filenames[2]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_CommunicationReader_tar_gz_file():
    reader = CommunicationReader('tests/testdata/simple.tar.gz')
    comms, filenames = zip(*[(c, f) for c, f in reader])
    @py_assert1 = comms[0]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[1]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[2]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'one'
    @py_assert3 = comms[0]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'two'
    @py_assert3 = comms[1]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'three'
    @py_assert3 = comms[2]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'simple_1.concrete'
    @py_assert3 = filenames[0]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_2.concrete'
    @py_assert3 = filenames[1]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_3.concrete'
    @py_assert3 = filenames[2]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_CommunicationReader_tar_bz2_file():
    reader = CommunicationReader('tests/testdata/simple.tar.bz2')
    comms, filenames = zip(*[(c, f) for c, f in reader])
    @py_assert1 = comms[0]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[1]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[2]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'one'
    @py_assert3 = comms[0]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'two'
    @py_assert3 = comms[1]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'three'
    @py_assert3 = comms[2]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'simple_1.concrete'
    @py_assert3 = filenames[0]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_2.concrete'
    @py_assert3 = filenames[1]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_3.concrete'
    @py_assert3 = filenames[2]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_CommunicationReader_nested_tar_file():
    reader = CommunicationReader('tests/testdata/simple_nested.tar')
    comms, filenames = zip(*[(c, f) for c, f in reader])
    @py_assert1 = comms[0]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[1]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[2]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'one'
    @py_assert3 = comms[0]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'two'
    @py_assert3 = comms[1]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'three'
    @py_assert3 = comms[2]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'a/b/simple_1.concrete'
    @py_assert3 = filenames[0]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'a/c/simple_2.concrete'
    @py_assert3 = filenames[1]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'a/c/simple_3.concrete'
    @py_assert3 = filenames[2]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_CommunicationReader_zip_file():
    reader = CommunicationReader('tests/testdata/simple.zip')
    comms, filenames = zip(*[(c, f) for c, f in reader])
    @py_assert1 = comms[0]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[1]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[2]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'one'
    @py_assert3 = comms[0]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'two'
    @py_assert3 = comms[1]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'three'
    @py_assert3 = comms[2]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'simple_1.concrete'
    @py_assert3 = filenames[0]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_2.concrete'
    @py_assert3 = filenames[1]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_3.concrete'
    @py_assert3 = filenames[2]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_CommunicationReader_explicit_single_file():
    filename = 'tests/testdata/simple_1.concrete'
    reader = CommunicationReader(filename, filetype=FileType.STREAM)
    comm1, comm1_filename = next(reader)
    @py_assert2 = 'sentenceForUUID'
    @py_assert4 = hasattr(comm1, @py_assert2)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert0 = 'one'
    @py_assert4 = comm1.id
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert1 = filename == comm1_filename
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (filename, comm1_filename)) % {'py2': @pytest_ar._saferepr(comm1_filename) if 'comm1_filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1_filename) else 'comm1_filename', 'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_CommunicationReader_explicit_single_gz_file():
    filename = 'tests/testdata/simple_1.concrete.gz'
    reader = CommunicationReader(filename, filetype=FileType.STREAM_GZ)
    comm1, comm1_filename = next(reader)
    @py_assert2 = 'sentenceForUUID'
    @py_assert4 = hasattr(comm1, @py_assert2)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert0 = 'one'
    @py_assert4 = comm1.id
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert1 = filename == comm1_filename
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (filename, comm1_filename)) % {'py2': @pytest_ar._saferepr(comm1_filename) if 'comm1_filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1_filename) else 'comm1_filename', 'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_CommunicationReader_explicit_single_bz2_file():
    filename = 'tests/testdata/simple_1.concrete.bz2'
    reader = CommunicationReader(filename, filetype=FileType.STREAM_BZ2)
    comm1, comm1_filename = next(reader)
    @py_assert2 = 'sentenceForUUID'
    @py_assert4 = hasattr(comm1, @py_assert2)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert0 = 'one'
    @py_assert4 = comm1.id
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert1 = filename == comm1_filename
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (filename, comm1_filename)) % {'py2': @pytest_ar._saferepr(comm1_filename) if 'comm1_filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1_filename) else 'comm1_filename', 'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_CommunicationReader_explicit_concatenated_file():
    filename = 'tests/testdata/simple_concatenated'
    reader = CommunicationReader(filename, filetype=FileType.STREAM)
    comms, filenames = zip(*[(c, f) for c, f in reader])
    for i, comm_id in enumerate(['one', 'two', 'three']):
        @py_assert1 = comms[i]
        @py_assert3 = 'sentenceForUUID'
        @py_assert5 = hasattr(@py_assert1, @py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert2 = comms[i]
        @py_assert4 = @py_assert2.id
        @py_assert1 = comm_id == @py_assert4
        if not @py_assert1:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (comm_id, @py_assert4)) % {'py0': @pytest_ar._saferepr(comm_id) if 'comm_id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm_id) else 'comm_id', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert2 = @py_assert4 = None
        @py_assert2 = filenames[i]
        @py_assert1 = filename == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (filename, @py_assert2)) % {'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_CommunicationReader_explicit_concatenated_gz_file():
    filename = 'tests/testdata/simple_concatenated.gz'
    reader = CommunicationReader(filename, filetype=FileType.STREAM_GZ)
    comms, filenames = zip(*[(c, f) for c, f in reader])
    for i, comm_id in enumerate(['one', 'two', 'three']):
        @py_assert1 = comms[i]
        @py_assert3 = 'sentenceForUUID'
        @py_assert5 = hasattr(@py_assert1, @py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert2 = comms[i]
        @py_assert4 = @py_assert2.id
        @py_assert1 = comm_id == @py_assert4
        if not @py_assert1:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (comm_id, @py_assert4)) % {'py0': @pytest_ar._saferepr(comm_id) if 'comm_id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm_id) else 'comm_id', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert2 = @py_assert4 = None
        @py_assert2 = filenames[i]
        @py_assert1 = filename == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (filename, @py_assert2)) % {'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_CommunicationReader_explicit_concatenated_bz2_file():
    filename = 'tests/testdata/simple_concatenated.bz2'
    reader = CommunicationReader(filename, filetype=FileType.STREAM_BZ2)
    comms, filenames = zip(*[(c, f) for c, f in reader])
    for i, comm_id in enumerate(['one', 'two', 'three']):
        @py_assert1 = comms[i]
        @py_assert3 = 'sentenceForUUID'
        @py_assert5 = hasattr(@py_assert1, @py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert2 = comms[i]
        @py_assert4 = @py_assert2.id
        @py_assert1 = comm_id == @py_assert4
        if not @py_assert1:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (comm_id, @py_assert4)) % {'py0': @pytest_ar._saferepr(comm_id) if 'comm_id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm_id) else 'comm_id', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert2 = @py_assert4 = None
        @py_assert2 = filenames[i]
        @py_assert1 = filename == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (filename, @py_assert2)) % {'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_CommunicationReader_explicit_tar_file():
    filename = 'tests/testdata/simple.tar'
    reader = CommunicationReader(filename, filetype=FileType.TAR)
    comms, filenames = zip(*[(c, f) for c, f in reader])
    @py_assert1 = comms[0]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[1]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[2]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'one'
    @py_assert3 = comms[0]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'two'
    @py_assert3 = comms[1]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'three'
    @py_assert3 = comms[2]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'simple_1.concrete'
    @py_assert3 = filenames[0]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_2.concrete'
    @py_assert3 = filenames[1]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_3.concrete'
    @py_assert3 = filenames[2]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_CommunicationReader_explicit_tar_gz_file():
    reader = CommunicationReader('tests/testdata/simple.tar.gz', filetype=FileType.TAR_GZ)
    comms, filenames = zip(*[(c, f) for c, f in reader])
    @py_assert1 = comms[0]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[1]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[2]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'one'
    @py_assert3 = comms[0]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'two'
    @py_assert3 = comms[1]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'three'
    @py_assert3 = comms[2]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'simple_1.concrete'
    @py_assert3 = filenames[0]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_2.concrete'
    @py_assert3 = filenames[1]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_3.concrete'
    @py_assert3 = filenames[2]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_CommunicationReader_explicit_tar_bz2_file():
    reader = CommunicationReader('tests/testdata/simple.tar.bz2', filetype=FileType.TAR_BZ2)
    comms, filenames = zip(*[(c, f) for c, f in reader])
    @py_assert1 = comms[0]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[1]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[2]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'one'
    @py_assert3 = comms[0]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'two'
    @py_assert3 = comms[1]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'three'
    @py_assert3 = comms[2]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'simple_1.concrete'
    @py_assert3 = filenames[0]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_2.concrete'
    @py_assert3 = filenames[1]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_3.concrete'
    @py_assert3 = filenames[2]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_CommunicationReader_explicit_nested_tar_file():
    reader = CommunicationReader('tests/testdata/simple_nested.tar', filetype=FileType.TAR)
    comms, filenames = zip(*[(c, f) for c, f in reader])
    @py_assert1 = comms[0]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[1]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[2]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'one'
    @py_assert3 = comms[0]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'two'
    @py_assert3 = comms[1]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'three'
    @py_assert3 = comms[2]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'a/b/simple_1.concrete'
    @py_assert3 = filenames[0]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'a/c/simple_2.concrete'
    @py_assert3 = filenames[1]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'a/c/simple_3.concrete'
    @py_assert3 = filenames[2]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_CommunicationReader_explicit_zip_file():
    reader = CommunicationReader('tests/testdata/simple.zip', filetype=FileType.ZIP)
    comms, filenames = zip(*[(c, f) for c, f in reader])
    @py_assert1 = comms[0]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[1]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comms[2]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'one'
    @py_assert3 = comms[0]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'two'
    @py_assert3 = comms[1]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'three'
    @py_assert3 = comms[2]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'simple_1.concrete'
    @py_assert3 = filenames[0]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_2.concrete'
    @py_assert3 = filenames[1]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_3.concrete'
    @py_assert3 = filenames[2]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_CommunicationReader_single_file_no_add_references():
    filename = 'tests/testdata/simple_1.concrete'
    reader = CommunicationReader(filename, add_references=False)
    comm1, comm1_filename = next(reader)
    @py_assert2 = 'sentenceForUUID'
    @py_assert4 = hasattr(comm1, @py_assert2)
    @py_assert6 = not @py_assert4
    if not @py_assert6:
        @py_format7 = ('' + 'assert not %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'one'
    @py_assert4 = comm1.id
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert1 = filename == comm1_filename
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (filename, comm1_filename)) % {'py2': @pytest_ar._saferepr(comm1_filename) if 'comm1_filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1_filename) else 'comm1_filename', 'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_CommunicationReader_single_gz_file_no_add_references():
    filename = 'tests/testdata/simple_1.concrete.gz'
    reader = CommunicationReader(filename, add_references=False)
    comm1, comm1_filename = next(reader)
    @py_assert2 = 'sentenceForUUID'
    @py_assert4 = hasattr(comm1, @py_assert2)
    @py_assert6 = not @py_assert4
    if not @py_assert6:
        @py_format7 = ('' + 'assert not %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'one'
    @py_assert4 = comm1.id
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert1 = filename == comm1_filename
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (filename, comm1_filename)) % {'py2': @pytest_ar._saferepr(comm1_filename) if 'comm1_filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1_filename) else 'comm1_filename', 'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_CommunicationReader_concatenated_file_no_add_references():
    filename = 'tests/testdata/simple_concatenated'
    reader = CommunicationReader(filename, add_references=False)
    comms, filenames = zip(*[(c, f) for c, f in reader])
    for i, comm_id in enumerate(['one', 'two', 'three']):
        @py_assert1 = comms[i]
        @py_assert3 = 'sentenceForUUID'
        @py_assert5 = hasattr(@py_assert1, @py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert2 = comms[i]
        @py_assert4 = @py_assert2.id
        @py_assert1 = comm_id == @py_assert4
        if not @py_assert1:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (comm_id, @py_assert4)) % {'py0': @pytest_ar._saferepr(comm_id) if 'comm_id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm_id) else 'comm_id', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert2 = @py_assert4 = None
        @py_assert2 = filenames[i]
        @py_assert1 = filename == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (filename, @py_assert2)) % {'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_CommunicationReader_concatenated_gz_file_no_add_references():
    filename = 'tests/testdata/simple_concatenated.gz'
    reader = CommunicationReader(filename, add_references=False)
    comms, filenames = zip(*[(c, f) for c, f in reader])
    for i, comm_id in enumerate(['one', 'two', 'three']):
        @py_assert1 = comms[i]
        @py_assert3 = 'sentenceForUUID'
        @py_assert5 = hasattr(@py_assert1, @py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert2 = comms[i]
        @py_assert4 = @py_assert2.id
        @py_assert1 = comm_id == @py_assert4
        if not @py_assert1:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (comm_id, @py_assert4)) % {'py0': @pytest_ar._saferepr(comm_id) if 'comm_id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm_id) else 'comm_id', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert2 = @py_assert4 = None
        @py_assert2 = filenames[i]
        @py_assert1 = filename == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (filename, @py_assert2)) % {'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_CommunicationReader_tar_file_no_add_references():
    filename = 'tests/testdata/simple.tar'
    reader = CommunicationReader(filename, add_references=False)
    comms, filenames = zip(*[(c, f) for c, f in reader])
    @py_assert1 = comms[0]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = comms[1]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = comms[2]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert0 = 'one'
    @py_assert3 = comms[0]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'two'
    @py_assert3 = comms[1]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'three'
    @py_assert3 = comms[2]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'simple_1.concrete'
    @py_assert3 = filenames[0]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_2.concrete'
    @py_assert3 = filenames[1]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_3.concrete'
    @py_assert3 = filenames[2]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_CommunicationReader_tar_gz_file_no_add_references():
    reader = CommunicationReader('tests/testdata/simple.tar.gz', add_references=False)
    comms, filenames = zip(*[(c, f) for c, f in reader])
    @py_assert1 = comms[0]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = comms[1]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = comms[2]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert0 = 'one'
    @py_assert3 = comms[0]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'two'
    @py_assert3 = comms[1]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'three'
    @py_assert3 = comms[2]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'simple_1.concrete'
    @py_assert3 = filenames[0]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_2.concrete'
    @py_assert3 = filenames[1]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_3.concrete'
    @py_assert3 = filenames[2]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_CommunicationReader_zip_file_no_add_references():
    reader = CommunicationReader('tests/testdata/simple.zip', add_references=False)
    comms, filenames = zip(*[(c, f) for c, f in reader])
    @py_assert1 = comms[0]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = comms[1]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = comms[2]
    @py_assert3 = 'sentenceForUUID'
    @py_assert5 = hasattr(@py_assert1, @py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert0 = 'one'
    @py_assert3 = comms[0]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'two'
    @py_assert3 = comms[1]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'three'
    @py_assert3 = comms[2]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'simple_1.concrete'
    @py_assert3 = filenames[0]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_2.concrete'
    @py_assert3 = filenames[1]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'simple_3.concrete'
    @py_assert3 = filenames[2]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_CommunicationReader_single_file_unicode():
    reader = CommunicationReader('tests/testdata/les-deux-chandeliers.concrete')
    comms, filenames = zip(*[(c, f) for c, f in reader])
    @py_assert2 = len(comms)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comms) if 'comms' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comms) else 'comms'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = 'tests/testdata/les-deux-chandeliers.txt'
    @py_assert3 = comms[0]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None


def test_CommunicationReader_tar_gz_file_unicode():
    reader = CommunicationReader('tests/testdata/les-deux-chandeliers.concrete.tar.gz')
    comms, filenames = zip(*[(c, f) for c, f in reader])
    @py_assert2 = len(comms)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comms) if 'comms' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comms) else 'comms'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = 'les-deux-chandeliers/l0.txt'
    @py_assert3 = comms[0]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 'les-deux-chandeliers/l1.txt'
    @py_assert3 = comms[1]
    @py_assert5 = @py_assert3.id
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None


def test_CommunicationReader_truncated_file():
    reader = CommunicationReader('tests/testdata/truncated.comm')
    with raises(EOFError):
        comms, filenames = zip(*[(c, f) for c, f in reader])


def test_CommunicationReader_truncated_gz_file():
    reader = CommunicationReader('tests/testdata/truncated.comm.gz')
    with raises(EOFError):
        comms, filenames = zip(*[(c, f) for c, f in reader])


def test_CommunicationReader_truncated_tgz_file():
    reader = CommunicationReader('tests/testdata/simple_1_and_truncated.tar.gz')
    simple_comm, _ = reader.next()
    with raises(EOFError):
        truncated_comm, _ = reader.next()


def test_CommunicationWriter_fixed_point(output_file):
    input_file = 'tests/testdata/simple_1.concrete'
    comm = read_communication_from_file(input_file)
    writer = CommunicationWriter()
    try:
        writer.open(output_file)
        writer.write(comm)
    finally:
        writer.close()

    with open(input_file, 'rb') as (expected_f):
        expected_data = expected_f.read()
        with open(output_file, 'rb') as (actual_f):
            actual_data = actual_f.read()
            @py_assert1 = expected_data == actual_data
            if not @py_assert1:
                @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected_data, actual_data)) % {'py2': @pytest_ar._saferepr(actual_data) if 'actual_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_data) else 'actual_data', 'py0': @pytest_ar._saferepr(expected_data) if 'expected_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_data) else 'expected_data'}
                @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
                raise AssertionError(@pytest_ar._format_explanation(@py_format5))
            @py_assert1 = None


def test_CommunicationWriter_fixed_point_ctx_mgr(output_file):
    input_file = 'tests/testdata/simple_1.concrete'
    comm = read_communication_from_file(input_file)
    with CommunicationWriter(output_file) as (writer):
        writer.write(comm)
    with open(input_file, 'rb') as (expected_f):
        expected_data = expected_f.read()
        with open(output_file, 'rb') as (actual_f):
            actual_data = actual_f.read()
            @py_assert1 = expected_data == actual_data
            if not @py_assert1:
                @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected_data, actual_data)) % {'py2': @pytest_ar._saferepr(actual_data) if 'actual_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_data) else 'actual_data', 'py0': @pytest_ar._saferepr(expected_data) if 'expected_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_data) else 'expected_data'}
                @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
                raise AssertionError(@pytest_ar._format_explanation(@py_format5))
            @py_assert1 = None


def test_CommunicationWriter_fixed_point_unicode(output_file):
    input_file = 'tests/testdata/les-deux-chandeliers.concrete'
    comm = read_communication_from_file(input_file)
    with CommunicationWriter(output_file) as (writer):
        writer.write(comm)
    with open(input_file, 'rb') as (expected_f):
        expected_data = expected_f.read()
        with open(output_file, 'rb') as (actual_f):
            actual_data = actual_f.read()
            @py_assert1 = expected_data == actual_data
            if not @py_assert1:
                @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected_data, actual_data)) % {'py2': @pytest_ar._saferepr(actual_data) if 'actual_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_data) else 'actual_data', 'py0': @pytest_ar._saferepr(expected_data) if 'expected_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_data) else 'expected_data'}
                @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
                raise AssertionError(@pytest_ar._format_explanation(@py_format5))
            @py_assert1 = None


def test_CommunicationWriter_gz_fixed_point(output_file):
    input_file = 'tests/testdata/simple_1.concrete'
    comm = read_communication_from_file(input_file)
    writer = CommunicationWriter(gzip=True)
    try:
        writer.open(output_file)
        writer.write(comm)
    finally:
        writer.close()

    with open(input_file, 'rb') as (expected_f):
        expected_data = expected_f.read()
        with gzip.open(output_file, 'rb') as (actual_f):
            actual_data = actual_f.read()
            @py_assert1 = expected_data == actual_data
            if not @py_assert1:
                @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected_data, actual_data)) % {'py2': @pytest_ar._saferepr(actual_data) if 'actual_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_data) else 'actual_data', 'py0': @pytest_ar._saferepr(expected_data) if 'expected_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_data) else 'expected_data'}
                @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
                raise AssertionError(@pytest_ar._format_explanation(@py_format5))
            @py_assert1 = None


def test_CommunicationWriter_gz_fixed_point_ctx_mgr(output_file):
    input_file = 'tests/testdata/simple_1.concrete'
    comm = read_communication_from_file(input_file)
    with CommunicationWriter(output_file, gzip=True) as (writer):
        writer.write(comm)
    with open(input_file, 'rb') as (expected_f):
        expected_data = expected_f.read()
        with gzip.open(output_file, 'rb') as (actual_f):
            actual_data = actual_f.read()
            @py_assert1 = expected_data == actual_data
            if not @py_assert1:
                @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected_data, actual_data)) % {'py2': @pytest_ar._saferepr(actual_data) if 'actual_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_data) else 'actual_data', 'py0': @pytest_ar._saferepr(expected_data) if 'expected_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_data) else 'expected_data'}
                @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
                raise AssertionError(@pytest_ar._format_explanation(@py_format5))
            @py_assert1 = None


def test_CommunicationWriter_gz_fixed_point_unicode(output_file):
    input_file = 'tests/testdata/les-deux-chandeliers.concrete'
    comm = read_communication_from_file(input_file)
    with CommunicationWriter(output_file, gzip=True) as (writer):
        writer.write(comm)
    with open(input_file, 'rb') as (expected_f):
        expected_data = expected_f.read()
        with gzip.open(output_file, 'rb') as (actual_f):
            actual_data = actual_f.read()
            @py_assert1 = expected_data == actual_data
            if not @py_assert1:
                @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected_data, actual_data)) % {'py2': @pytest_ar._saferepr(actual_data) if 'actual_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_data) else 'actual_data', 'py0': @pytest_ar._saferepr(expected_data) if 'expected_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_data) else 'expected_data'}
                @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
                raise AssertionError(@pytest_ar._format_explanation(@py_format5))
            @py_assert1 = None


def test_CommunicationWriterTar_single_file(output_file, login_info):
    comm = read_communication_from_file('tests/testdata/simple_1.concrete')
    writer = CommunicationWriterTar()
    try:
        writer.open(output_file)
        writer.write(comm, 'simple_1.concrete')
    finally:
        writer.close()

    @py_assert1 = tarfile.is_tarfile
    @py_assert4 = @py_assert1(output_file)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.is_tarfile\n}(%(py3)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarfile) if 'tarfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarfile) else 'tarfile', 'py3': @pytest_ar._saferepr(output_file) if 'output_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output_file) else 'output_file', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    f = tarfile.open(output_file)
    tarinfo = f.next()
    @py_assert2 = None
    @py_assert1 = tarinfo is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (tarinfo, @py_assert2)) % {'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = 'simple_1.concrete'
    @py_assert4 = tarinfo.name
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.name\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert1 = tarinfo.isreg
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.isreg\n}()\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = tarinfo.mtime
    @py_assert5 = time()
    @py_assert8 = @py_assert5 - TIME_MARGIN
    @py_assert3 = @py_assert1 > @py_assert8
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('>', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mtime\n} > (%(py6)s\n{%(py6)s = %(py4)s()\n} - %(py7)s)', ), (@py_assert1, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(time) if 'time' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(time) else 'time', 'py7': @pytest_ar._saferepr(TIME_MARGIN) if 'TIME_MARGIN' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TIME_MARGIN) else 'TIME_MARGIN'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = None
    @py_assert1 = os.stat
    @py_assert3 = 'tests/testdata/simple_1.concrete'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5.st_size
    @py_assert11 = tarinfo.size
    @py_assert9 = @py_assert7 == @py_assert11
    if not @py_assert9:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}(%(py4)s)\n}.st_size\n} == %(py12)s\n{%(py12)s = %(py10)s.size\n}', ), (@py_assert7, @py_assert11)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert0 = 420
    @py_assert4 = tarinfo.mode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.mode\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['uid']
    @py_assert4 = tarinfo.uid
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.uid\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['username']
    @py_assert4 = tarinfo.uname
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.uname\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['gid']
    @py_assert4 = tarinfo.gid
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.gid\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['groupname']
    @py_assert4 = tarinfo.gname
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.gname\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    tarinfo = f.next()
    @py_assert2 = None
    @py_assert1 = tarinfo is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (tarinfo, @py_assert2)) % {'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    f.close()


def test_CommunicationWriterTar_single_file_ctx_mgr(output_file, login_info):
    comm = read_communication_from_file('tests/testdata/simple_1.concrete')
    with CommunicationWriterTar(output_file) as (writer):
        writer.write(comm, 'simple_1.concrete')
    @py_assert1 = tarfile.is_tarfile
    @py_assert4 = @py_assert1(output_file)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.is_tarfile\n}(%(py3)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarfile) if 'tarfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarfile) else 'tarfile', 'py3': @pytest_ar._saferepr(output_file) if 'output_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output_file) else 'output_file', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    f = tarfile.open(output_file)
    tarinfo = f.next()
    @py_assert2 = None
    @py_assert1 = tarinfo is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (tarinfo, @py_assert2)) % {'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = 'simple_1.concrete'
    @py_assert4 = tarinfo.name
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.name\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert1 = tarinfo.isreg
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.isreg\n}()\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = tarinfo.mtime
    @py_assert5 = time()
    @py_assert8 = @py_assert5 - TIME_MARGIN
    @py_assert3 = @py_assert1 > @py_assert8
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('>', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mtime\n} > (%(py6)s\n{%(py6)s = %(py4)s()\n} - %(py7)s)', ), (@py_assert1, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(time) if 'time' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(time) else 'time', 'py7': @pytest_ar._saferepr(TIME_MARGIN) if 'TIME_MARGIN' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TIME_MARGIN) else 'TIME_MARGIN'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = None
    @py_assert1 = os.stat
    @py_assert3 = 'tests/testdata/simple_1.concrete'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5.st_size
    @py_assert11 = tarinfo.size
    @py_assert9 = @py_assert7 == @py_assert11
    if not @py_assert9:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}(%(py4)s)\n}.st_size\n} == %(py12)s\n{%(py12)s = %(py10)s.size\n}', ), (@py_assert7, @py_assert11)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert0 = 420
    @py_assert4 = tarinfo.mode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.mode\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['uid']
    @py_assert4 = tarinfo.uid
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.uid\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['username']
    @py_assert4 = tarinfo.uname
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.uname\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['gid']
    @py_assert4 = tarinfo.gid
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.gid\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['groupname']
    @py_assert4 = tarinfo.gname
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.gname\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    tarinfo = f.next()
    @py_assert2 = None
    @py_assert1 = tarinfo is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (tarinfo, @py_assert2)) % {'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    f.close()


def test_CommunicationWriterTar_single_file_fixed_point(output_file, login_info):
    comm = read_communication_from_file('tests/testdata/simple_1.concrete')
    with CommunicationWriterTar(output_file) as (writer):
        writer.write(comm, 'simple_1.concrete')
    @py_assert1 = tarfile.is_tarfile
    @py_assert4 = @py_assert1(output_file)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.is_tarfile\n}(%(py3)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarfile) if 'tarfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarfile) else 'tarfile', 'py3': @pytest_ar._saferepr(output_file) if 'output_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output_file) else 'output_file', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    f = tarfile.open(output_file)
    tarinfo = f.next()
    @py_assert2 = None
    @py_assert1 = tarinfo is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (tarinfo, @py_assert2)) % {'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = 'simple_1.concrete'
    @py_assert4 = tarinfo.name
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.name\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    actual_data = f.extractfile(tarinfo).read()
    with open('tests/testdata/simple_1.concrete', 'rb') as (expected_f):
        expected_data = expected_f.read()
        @py_assert1 = expected_data == actual_data
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected_data, actual_data)) % {'py2': @pytest_ar._saferepr(actual_data) if 'actual_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_data) else 'actual_data', 'py0': @pytest_ar._saferepr(expected_data) if 'expected_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_data) else 'expected_data'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
    tarinfo = f.next()
    @py_assert2 = None
    @py_assert1 = tarinfo is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (tarinfo, @py_assert2)) % {'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    f.close()


def test_CommunicationWriterTar_single_file_fixed_point_unicode(output_file, login_info):
    comm = read_communication_from_file('tests/testdata/les-deux-chandeliers.concrete')
    with CommunicationWriterTar(output_file) as (writer):
        writer.write(comm, 'les-deux-chandeliers.concrete')
    @py_assert1 = tarfile.is_tarfile
    @py_assert4 = @py_assert1(output_file)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.is_tarfile\n}(%(py3)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarfile) if 'tarfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarfile) else 'tarfile', 'py3': @pytest_ar._saferepr(output_file) if 'output_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output_file) else 'output_file', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    f = tarfile.open(output_file)
    tarinfo = f.next()
    @py_assert2 = None
    @py_assert1 = tarinfo is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (tarinfo, @py_assert2)) % {'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = 'les-deux-chandeliers.concrete'
    @py_assert4 = tarinfo.name
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.name\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    actual_data = f.extractfile(tarinfo).read()
    with open('tests/testdata/les-deux-chandeliers.concrete', 'rb') as (expected_f):
        expected_data = expected_f.read()
        @py_assert1 = expected_data == actual_data
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected_data, actual_data)) % {'py2': @pytest_ar._saferepr(actual_data) if 'actual_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_data) else 'actual_data', 'py0': @pytest_ar._saferepr(expected_data) if 'expected_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_data) else 'expected_data'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
    tarinfo = f.next()
    @py_assert2 = None
    @py_assert1 = tarinfo is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (tarinfo, @py_assert2)) % {'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    f.close()


def test_CommunicationWriterTar_single_file_default_name(output_file, login_info):
    comm = read_communication_from_file('tests/testdata/simple_1.concrete')
    writer = CommunicationWriterTar()
    try:
        writer.open(output_file)
        writer.write(comm)
    finally:
        writer.close()

    @py_assert1 = tarfile.is_tarfile
    @py_assert4 = @py_assert1(output_file)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.is_tarfile\n}(%(py3)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarfile) if 'tarfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarfile) else 'tarfile', 'py3': @pytest_ar._saferepr(output_file) if 'output_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output_file) else 'output_file', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    f = tarfile.open(output_file)
    tarinfo = f.next()
    @py_assert2 = None
    @py_assert1 = tarinfo is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (tarinfo, @py_assert2)) % {'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = comm.id
    @py_assert3 = '.concrete'
    @py_assert5 = @py_assert1 + @py_assert3
    @py_assert8 = tarinfo.name
    @py_assert6 = @py_assert5 == @py_assert8
    if not @py_assert6:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('(%(py2)s\n{%(py2)s = %(py0)s.id\n} + %(py4)s) == %(py9)s\n{%(py9)s = %(py7)s.name\n}', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py9': @pytest_ar._saferepr(@py_assert8), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = @py_assert8 = None
    @py_assert1 = tarinfo.isreg
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.isreg\n}()\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = tarinfo.mtime
    @py_assert5 = time()
    @py_assert8 = @py_assert5 - TIME_MARGIN
    @py_assert3 = @py_assert1 > @py_assert8
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('>', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mtime\n} > (%(py6)s\n{%(py6)s = %(py4)s()\n} - %(py7)s)', ), (@py_assert1, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(time) if 'time' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(time) else 'time', 'py7': @pytest_ar._saferepr(TIME_MARGIN) if 'TIME_MARGIN' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TIME_MARGIN) else 'TIME_MARGIN'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = None
    @py_assert1 = os.stat
    @py_assert3 = 'tests/testdata/simple_1.concrete'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5.st_size
    @py_assert11 = tarinfo.size
    @py_assert9 = @py_assert7 == @py_assert11
    if not @py_assert9:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}(%(py4)s)\n}.st_size\n} == %(py12)s\n{%(py12)s = %(py10)s.size\n}', ), (@py_assert7, @py_assert11)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert0 = 420
    @py_assert4 = tarinfo.mode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.mode\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['uid']
    @py_assert4 = tarinfo.uid
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.uid\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['username']
    @py_assert4 = tarinfo.uname
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.uname\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['gid']
    @py_assert4 = tarinfo.gid
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.gid\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['groupname']
    @py_assert4 = tarinfo.gname
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.gname\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    tarinfo = f.next()
    @py_assert2 = None
    @py_assert1 = tarinfo is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (tarinfo, @py_assert2)) % {'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    f.close()


def test_CommunicationWriterTGZ_single_file(output_file, login_info):
    comm = read_communication_from_file('tests/testdata/simple_1.concrete')
    writer = CommunicationWriterTGZ()
    try:
        writer.open(output_file)
        writer.write(comm, 'simple_1.concrete')
    finally:
        writer.close()

    @py_assert1 = tarfile.is_tarfile
    @py_assert4 = @py_assert1(output_file)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.is_tarfile\n}(%(py3)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarfile) if 'tarfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarfile) else 'tarfile', 'py3': @pytest_ar._saferepr(output_file) if 'output_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output_file) else 'output_file', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    f = tarfile.open(output_file)
    tarinfo = f.next()
    @py_assert2 = None
    @py_assert1 = tarinfo is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (tarinfo, @py_assert2)) % {'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = 'simple_1.concrete'
    @py_assert4 = tarinfo.name
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.name\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert1 = tarinfo.isreg
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.isreg\n}()\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = tarinfo.mtime
    @py_assert5 = time()
    @py_assert8 = @py_assert5 - TIME_MARGIN
    @py_assert3 = @py_assert1 > @py_assert8
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('>', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mtime\n} > (%(py6)s\n{%(py6)s = %(py4)s()\n} - %(py7)s)', ), (@py_assert1, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(time) if 'time' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(time) else 'time', 'py7': @pytest_ar._saferepr(TIME_MARGIN) if 'TIME_MARGIN' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TIME_MARGIN) else 'TIME_MARGIN'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = None
    @py_assert1 = os.stat
    @py_assert3 = 'tests/testdata/simple_1.concrete'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5.st_size
    @py_assert11 = tarinfo.size
    @py_assert9 = @py_assert7 == @py_assert11
    if not @py_assert9:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}(%(py4)s)\n}.st_size\n} == %(py12)s\n{%(py12)s = %(py10)s.size\n}', ), (@py_assert7, @py_assert11)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert0 = 420
    @py_assert4 = tarinfo.mode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.mode\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['uid']
    @py_assert4 = tarinfo.uid
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.uid\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['username']
    @py_assert4 = tarinfo.uname
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.uname\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['gid']
    @py_assert4 = tarinfo.gid
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.gid\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['groupname']
    @py_assert4 = tarinfo.gname
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.gname\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    tarinfo = f.next()
    @py_assert2 = None
    @py_assert1 = tarinfo is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (tarinfo, @py_assert2)) % {'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    f.close()


def test_CommunicationWriterTGZ_single_file_ctx_mgr(output_file, login_info):
    comm = read_communication_from_file('tests/testdata/simple_1.concrete')
    with CommunicationWriterTGZ(output_file) as (writer):
        writer.write(comm, 'simple_1.concrete')
    @py_assert1 = tarfile.is_tarfile
    @py_assert4 = @py_assert1(output_file)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.is_tarfile\n}(%(py3)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarfile) if 'tarfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarfile) else 'tarfile', 'py3': @pytest_ar._saferepr(output_file) if 'output_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output_file) else 'output_file', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    f = tarfile.open(output_file)
    tarinfo = f.next()
    @py_assert2 = None
    @py_assert1 = tarinfo is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (tarinfo, @py_assert2)) % {'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = 'simple_1.concrete'
    @py_assert4 = tarinfo.name
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.name\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert1 = tarinfo.isreg
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.isreg\n}()\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = tarinfo.mtime
    @py_assert5 = time()
    @py_assert8 = @py_assert5 - TIME_MARGIN
    @py_assert3 = @py_assert1 > @py_assert8
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('>', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mtime\n} > (%(py6)s\n{%(py6)s = %(py4)s()\n} - %(py7)s)', ), (@py_assert1, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(time) if 'time' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(time) else 'time', 'py7': @pytest_ar._saferepr(TIME_MARGIN) if 'TIME_MARGIN' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TIME_MARGIN) else 'TIME_MARGIN'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = None
    @py_assert1 = os.stat
    @py_assert3 = 'tests/testdata/simple_1.concrete'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5.st_size
    @py_assert11 = tarinfo.size
    @py_assert9 = @py_assert7 == @py_assert11
    if not @py_assert9:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}(%(py4)s)\n}.st_size\n} == %(py12)s\n{%(py12)s = %(py10)s.size\n}', ), (@py_assert7, @py_assert11)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert0 = 420
    @py_assert4 = tarinfo.mode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.mode\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['uid']
    @py_assert4 = tarinfo.uid
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.uid\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['username']
    @py_assert4 = tarinfo.uname
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.uname\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['gid']
    @py_assert4 = tarinfo.gid
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.gid\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['groupname']
    @py_assert4 = tarinfo.gname
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.gname\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    tarinfo = f.next()
    @py_assert2 = None
    @py_assert1 = tarinfo is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (tarinfo, @py_assert2)) % {'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    f.close()


def test_CommunicationWriterTGZ_single_file_default_name(output_file, login_info):
    comm = read_communication_from_file('tests/testdata/simple_1.concrete')
    writer = CommunicationWriterTGZ()
    try:
        writer.open(output_file)
        writer.write(comm)
    finally:
        writer.close()

    @py_assert1 = tarfile.is_tarfile
    @py_assert4 = @py_assert1(output_file)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.is_tarfile\n}(%(py3)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarfile) if 'tarfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarfile) else 'tarfile', 'py3': @pytest_ar._saferepr(output_file) if 'output_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output_file) else 'output_file', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    f = tarfile.open(output_file)
    tarinfo = f.next()
    @py_assert2 = None
    @py_assert1 = tarinfo is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (tarinfo, @py_assert2)) % {'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = comm.id
    @py_assert3 = '.concrete'
    @py_assert5 = @py_assert1 + @py_assert3
    @py_assert8 = tarinfo.name
    @py_assert6 = @py_assert5 == @py_assert8
    if not @py_assert6:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('(%(py2)s\n{%(py2)s = %(py0)s.id\n} + %(py4)s) == %(py9)s\n{%(py9)s = %(py7)s.name\n}', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py9': @pytest_ar._saferepr(@py_assert8), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = @py_assert8 = None
    @py_assert1 = tarinfo.isreg
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.isreg\n}()\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = tarinfo.mtime
    @py_assert5 = time()
    @py_assert8 = @py_assert5 - TIME_MARGIN
    @py_assert3 = @py_assert1 > @py_assert8
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('>', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mtime\n} > (%(py6)s\n{%(py6)s = %(py4)s()\n} - %(py7)s)', ), (@py_assert1, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(time) if 'time' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(time) else 'time', 'py7': @pytest_ar._saferepr(TIME_MARGIN) if 'TIME_MARGIN' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TIME_MARGIN) else 'TIME_MARGIN'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = None
    @py_assert1 = os.stat
    @py_assert3 = 'tests/testdata/simple_1.concrete'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5.st_size
    @py_assert11 = tarinfo.size
    @py_assert9 = @py_assert7 == @py_assert11
    if not @py_assert9:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}(%(py4)s)\n}.st_size\n} == %(py12)s\n{%(py12)s = %(py10)s.size\n}', ), (@py_assert7, @py_assert11)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert0 = 420
    @py_assert4 = tarinfo.mode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.mode\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['uid']
    @py_assert4 = tarinfo.uid
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.uid\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['username']
    @py_assert4 = tarinfo.uname
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.uname\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['gid']
    @py_assert4 = tarinfo.gid
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.gid\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = login_info['groupname']
    @py_assert4 = tarinfo.gname
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.gname\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    tarinfo = f.next()
    @py_assert2 = None
    @py_assert1 = tarinfo is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (tarinfo, @py_assert2)) % {'py0': @pytest_ar._saferepr(tarinfo) if 'tarinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tarinfo) else 'tarinfo', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    f.close()


def test_CommunicationWriterZip_single_file(output_file, login_info):
    comm = read_communication_from_file('tests/testdata/simple_1.concrete')
    writer = CommunicationWriterZip()
    try:
        writer.open(output_file)
        writer.write(comm, 'simple_1.concrete')
    finally:
        writer.close()

    @py_assert1 = zipfile.is_zipfile
    @py_assert4 = @py_assert1(output_file)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.is_zipfile\n}(%(py3)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(zipfile) if 'zipfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipfile) else 'zipfile', 'py3': @pytest_ar._saferepr(output_file) if 'output_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output_file) else 'output_file', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    f = zipfile.ZipFile(output_file)
    zipinfo, = f.infolist()
    @py_assert0 = 'simple_1.concrete'
    @py_assert4 = zipinfo.filename
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.filename\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(zipinfo) if 'zipinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipinfo) else 'zipinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert2 = zipinfo.date_time
    @py_assert4 = timegm(@py_assert2)
    @py_assert9 = localtime()
    @py_assert11 = timegm(@py_assert9)
    @py_assert14 = @py_assert11 - TIME_MARGIN
    @py_assert6 = @py_assert4 > @py_assert14
    if not @py_assert6:
        @py_format15 = @pytest_ar._call_reprcompare(('>',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.date_time\n})\n} > (%(py12)s\n{%(py12)s = %(py7)s(%(py10)s\n{%(py10)s = %(py8)s()\n})\n} - %(py13)s)',), (@py_assert4, @py_assert14)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(TIME_MARGIN) if 'TIME_MARGIN' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TIME_MARGIN) else 'TIME_MARGIN', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(timegm) if 'timegm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(timegm) else 'timegm', 'py8': @pytest_ar._saferepr(localtime) if 'localtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(localtime) else 'localtime', 
         'py1': @pytest_ar._saferepr(zipinfo) if 'zipinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipinfo) else 'zipinfo', 'py7': @pytest_ar._saferepr(timegm) if 'timegm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(timegm) else 'timegm'}
        @py_format17 = ('' + 'assert %(py16)s') % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert14 = None
    @py_assert1 = os.stat
    @py_assert3 = 'tests/testdata/simple_1.concrete'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5.st_size
    @py_assert11 = zipinfo.file_size
    @py_assert9 = @py_assert7 == @py_assert11
    if not @py_assert9:
        @py_format13 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}(%(py4)s)\n}.st_size\n} == %(py12)s\n{%(py12)s = %(py10)s.file_size\n}',), (@py_assert7, @py_assert11)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(zipinfo) if 'zipinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipinfo) else 'zipinfo', 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format15 = ('' + 'assert %(py14)s') % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
    f.close()


def test_CommunicationWriterZip_single_file_ctx_mgr(output_file, login_info):
    comm = read_communication_from_file('tests/testdata/simple_1.concrete')
    with CommunicationWriterZip(output_file) as (writer):
        writer.write(comm, 'simple_1.concrete')
    @py_assert1 = zipfile.is_zipfile
    @py_assert4 = @py_assert1(output_file)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.is_zipfile\n}(%(py3)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(zipfile) if 'zipfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipfile) else 'zipfile', 'py3': @pytest_ar._saferepr(output_file) if 'output_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output_file) else 'output_file', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    f = zipfile.ZipFile(output_file)
    zipinfo, = f.infolist()
    @py_assert0 = 'simple_1.concrete'
    @py_assert4 = zipinfo.filename
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.filename\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(zipinfo) if 'zipinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipinfo) else 'zipinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert2 = zipinfo.date_time
    @py_assert4 = timegm(@py_assert2)
    @py_assert9 = localtime()
    @py_assert11 = timegm(@py_assert9)
    @py_assert14 = @py_assert11 - TIME_MARGIN
    @py_assert6 = @py_assert4 > @py_assert14
    if not @py_assert6:
        @py_format15 = @pytest_ar._call_reprcompare(('>',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.date_time\n})\n} > (%(py12)s\n{%(py12)s = %(py7)s(%(py10)s\n{%(py10)s = %(py8)s()\n})\n} - %(py13)s)',), (@py_assert4, @py_assert14)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(TIME_MARGIN) if 'TIME_MARGIN' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TIME_MARGIN) else 'TIME_MARGIN', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(timegm) if 'timegm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(timegm) else 'timegm', 'py8': @pytest_ar._saferepr(localtime) if 'localtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(localtime) else 'localtime', 
         'py1': @pytest_ar._saferepr(zipinfo) if 'zipinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipinfo) else 'zipinfo', 'py7': @pytest_ar._saferepr(timegm) if 'timegm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(timegm) else 'timegm'}
        @py_format17 = ('' + 'assert %(py16)s') % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert14 = None
    @py_assert1 = os.stat
    @py_assert3 = 'tests/testdata/simple_1.concrete'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5.st_size
    @py_assert11 = zipinfo.file_size
    @py_assert9 = @py_assert7 == @py_assert11
    if not @py_assert9:
        @py_format13 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}(%(py4)s)\n}.st_size\n} == %(py12)s\n{%(py12)s = %(py10)s.file_size\n}',), (@py_assert7, @py_assert11)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(zipinfo) if 'zipinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipinfo) else 'zipinfo', 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format15 = ('' + 'assert %(py14)s') % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
    f.close()


def test_CommunicationWriterZip_single_file_fixed_point(output_file, login_info):
    comm = read_communication_from_file('tests/testdata/simple_1.concrete')
    with CommunicationWriterZip(output_file) as (writer):
        writer.write(comm, 'simple_1.concrete')
    @py_assert1 = zipfile.is_zipfile
    @py_assert4 = @py_assert1(output_file)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.is_zipfile\n}(%(py3)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(zipfile) if 'zipfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipfile) else 'zipfile', 'py3': @pytest_ar._saferepr(output_file) if 'output_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output_file) else 'output_file', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    f = zipfile.ZipFile(output_file)
    zipinfo, = f.infolist()
    @py_assert0 = 'simple_1.concrete'
    @py_assert4 = zipinfo.filename
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.filename\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(zipinfo) if 'zipinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipinfo) else 'zipinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    actual_data = f.open(zipinfo).read()
    with open('tests/testdata/simple_1.concrete', 'rb') as (expected_f):
        expected_data = expected_f.read()
        @py_assert1 = expected_data == actual_data
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected_data, actual_data)) % {'py2': @pytest_ar._saferepr(actual_data) if 'actual_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_data) else 'actual_data', 'py0': @pytest_ar._saferepr(expected_data) if 'expected_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_data) else 'expected_data'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
    f.close()


def test_CommunicationWriterZip_single_file_fixed_point_unicode(output_file, login_info):
    comm = read_communication_from_file('tests/testdata/les-deux-chandeliers.concrete')
    with CommunicationWriterZip(output_file) as (writer):
        writer.write(comm, 'les-deux-chandeliers.concrete')
    @py_assert1 = zipfile.is_zipfile
    @py_assert4 = @py_assert1(output_file)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.is_zipfile\n}(%(py3)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(zipfile) if 'zipfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipfile) else 'zipfile', 'py3': @pytest_ar._saferepr(output_file) if 'output_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output_file) else 'output_file', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    f = zipfile.ZipFile(output_file)
    zipinfo, = f.infolist()
    @py_assert0 = 'les-deux-chandeliers.concrete'
    @py_assert4 = zipinfo.filename
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.filename\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(zipinfo) if 'zipinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipinfo) else 'zipinfo', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    actual_data = f.open(zipinfo).read()
    with open('tests/testdata/les-deux-chandeliers.concrete', 'rb') as (expected_f):
        expected_data = expected_f.read()
        @py_assert1 = expected_data == actual_data
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected_data, actual_data)) % {'py2': @pytest_ar._saferepr(actual_data) if 'actual_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_data) else 'actual_data', 'py0': @pytest_ar._saferepr(expected_data) if 'expected_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_data) else 'expected_data'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
    f.close()


def test_CommunicationWriterZip_single_file_default_name(output_file, login_info):
    comm = read_communication_from_file('tests/testdata/simple_1.concrete')
    writer = CommunicationWriterZip()
    try:
        writer.open(output_file)
        writer.write(comm)
    finally:
        writer.close()

    @py_assert1 = zipfile.is_zipfile
    @py_assert4 = @py_assert1(output_file)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.is_zipfile\n}(%(py3)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(zipfile) if 'zipfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipfile) else 'zipfile', 'py3': @pytest_ar._saferepr(output_file) if 'output_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output_file) else 'output_file', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    f = zipfile.ZipFile(output_file)
    zipinfo, = f.infolist()
    @py_assert1 = comm.id
    @py_assert3 = '.concrete'
    @py_assert5 = @py_assert1 + @py_assert3
    @py_assert8 = zipinfo.filename
    @py_assert6 = @py_assert5 == @py_assert8
    if not @py_assert6:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('(%(py2)s\n{%(py2)s = %(py0)s.id\n} + %(py4)s) == %(py9)s\n{%(py9)s = %(py7)s.filename\n}',), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py9': @pytest_ar._saferepr(@py_assert8), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(zipinfo) if 'zipinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipinfo) else 'zipinfo'}
        @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = @py_assert8 = None
    @py_assert2 = zipinfo.date_time
    @py_assert4 = timegm(@py_assert2)
    @py_assert9 = localtime()
    @py_assert11 = timegm(@py_assert9)
    @py_assert14 = @py_assert11 - TIME_MARGIN
    @py_assert6 = @py_assert4 > @py_assert14
    if not @py_assert6:
        @py_format15 = @pytest_ar._call_reprcompare(('>',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.date_time\n})\n} > (%(py12)s\n{%(py12)s = %(py7)s(%(py10)s\n{%(py10)s = %(py8)s()\n})\n} - %(py13)s)',), (@py_assert4, @py_assert14)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(TIME_MARGIN) if 'TIME_MARGIN' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TIME_MARGIN) else 'TIME_MARGIN', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(timegm) if 'timegm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(timegm) else 'timegm', 'py8': @pytest_ar._saferepr(localtime) if 'localtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(localtime) else 'localtime', 
         'py1': @pytest_ar._saferepr(zipinfo) if 'zipinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipinfo) else 'zipinfo', 'py7': @pytest_ar._saferepr(timegm) if 'timegm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(timegm) else 'timegm'}
        @py_format17 = ('' + 'assert %(py16)s') % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert14 = None
    @py_assert1 = os.stat
    @py_assert3 = 'tests/testdata/simple_1.concrete'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5.st_size
    @py_assert11 = zipinfo.file_size
    @py_assert9 = @py_assert7 == @py_assert11
    if not @py_assert9:
        @py_format13 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}(%(py4)s)\n}.st_size\n} == %(py12)s\n{%(py12)s = %(py10)s.file_size\n}',), (@py_assert7, @py_assert11)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(zipinfo) if 'zipinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipinfo) else 'zipinfo', 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format15 = ('' + 'assert %(py14)s') % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
    f.close()