# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/charman/src/concrete-python/integration-tests/test_compress_uuids.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 3896 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pytest import fixture, mark
from concrete.util import CommunicationReader
from concrete.validate import validate_communication
from concrete.util import compress_uuids
import os, sys
from subprocess import Popen, PIPE
from tempfile import mkstemp

@fixture
def output_file(request):
    fd, path = mkstemp()
    os.close(fd)

    def _remove():
        if os.path.exists(path):
            os.remove(path)

    request.addfinalizer(_remove)
    return path


@mark.parametrize('args', [(),
 ('--verify', ),
 ('--verify', '--single-analytic'),
 ('--single-analytic', )])
def test_compress_uuids(output_file, args):
    input_file = 'tests/testdata/simple.tar.gz'
    p = Popen([
     sys.executable,
     'scripts/compress-uuids.py',
     input_file,
     output_file] + list(args), stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    @py_assert1 = p.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    reader = CommunicationReader(output_file)
    it = iter(reader)
    comm, comm_filename = next(it)
    @py_assert2 = 'simple_1.concrete'
    @py_assert1 = comm_filename == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py3)s',), (comm_filename, @py_assert2)) % {'py0': @pytest_ar._saferepr(comm_filename) if 'comm_filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm_filename) else 'comm_filename', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = ('' + 'assert %(py5)s') % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = comm.id
    @py_assert4 = 'one'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert2 = validate_communication(comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    comm, comm_filename = next(it)
    @py_assert2 = 'simple_2.concrete'
    @py_assert1 = comm_filename == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py3)s',), (comm_filename, @py_assert2)) % {'py0': @pytest_ar._saferepr(comm_filename) if 'comm_filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm_filename) else 'comm_filename', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = ('' + 'assert %(py5)s') % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = comm.id
    @py_assert4 = 'two'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert2 = validate_communication(comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    comm, comm_filename = next(it)
    @py_assert2 = 'simple_3.concrete'
    @py_assert1 = comm_filename == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py3)s',), (comm_filename, @py_assert2)) % {'py0': @pytest_ar._saferepr(comm_filename) if 'comm_filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm_filename) else 'comm_filename', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = ('' + 'assert %(py5)s') % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = comm.id
    @py_assert4 = 'three'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert2 = validate_communication(comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    @py_assert1 = os.stat
    @py_assert4 = @py_assert1(output_file)
    @py_assert6 = @py_assert4.st_size
    @py_assert10 = os.stat
    @py_assert13 = @py_assert10(input_file)
    @py_assert15 = @py_assert13.st_size
    @py_assert8 = @py_assert6 < @py_assert15
    if not @py_assert8:
        @py_format17 = @pytest_ar._call_reprcompare(('<',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}(%(py3)s)\n}.st_size\n} < %(py16)s\n{%(py16)s = %(py14)s\n{%(py14)s = %(py11)s\n{%(py11)s = %(py9)s.stat\n}(%(py12)s)\n}.st_size\n}',), (@py_assert6, @py_assert15)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py16': @pytest_ar._saferepr(@py_assert15), 'py14': @pytest_ar._saferepr(@py_assert13), 'py3': @pytest_ar._saferepr(output_file) if 'output_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output_file) else 'output_file', 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py12': @pytest_ar._saferepr(input_file) if 'input_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(input_file) else 'input_file', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert13 = @py_assert15 = None
    try:
        next(it)
    except StopIteration:
        pass
    else:
        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = ('' + 'assert %(py1)s') % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None


@mark.parametrize('reader_kwargs,compress_kwargs', [
 (
  dict(add_references=False), dict()),
 (
  dict(add_references=False), dict(verify=True)),
 (
  dict(add_references=False), dict(verify=False)),
 (
  dict(add_references=False), dict(verify=True, single_analytic=True)),
 (
  dict(add_references=False), dict(verify=False, single_analytic=True)),
 (
  dict(add_references=False), dict(verify=True, single_analytic=False)),
 (
  dict(add_references=False), dict(verify=False, single_analytic=False)),
 (
  dict(add_references=False), dict(single_analytic=False)),
 (
  dict(add_references=False), dict(single_analytic=True)),
 (
  dict(add_references=True), dict()),
 mark.xfail((
  dict(add_references=True), dict(verify=True)), strict=True),
 (
  dict(add_references=True), dict(verify=False)),
 mark.xfail((
  dict(add_references=True), dict(verify=True, single_analytic=True)), strict=True),
 (
  dict(add_references=True), dict(verify=False, single_analytic=True)),
 mark.xfail((
  dict(add_references=True), dict(verify=True, single_analytic=False)), strict=True),
 (
  dict(add_references=True), dict(verify=False, single_analytic=False)),
 (
  dict(add_references=True), dict(single_analytic=False)),
 (
  dict(add_references=True), dict(single_analytic=True))])
def test_compress_uuids_api(reader_kwargs, compress_kwargs):
    input_file = 'tests/testdata/simple.tar.gz'
    reader = CommunicationReader(input_file, **reader_kwargs)
    it = iter(reader)
    comm, _ = next(it)
    new_comm, uc = compress_uuids(comm, **compress_kwargs)
    @py_assert1 = new_comm.id
    @py_assert4 = 'one'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(new_comm) if 'new_comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_comm) else 'new_comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = comm.id
    @py_assert5 = new_comm.id
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(new_comm) if 'new_comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_comm) else 'new_comm'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert2 = validate_communication(new_comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(new_comm) if 'new_comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_comm) else 'new_comm'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    comm, _ = next(it)
    new_comm, uc = compress_uuids(comm, **compress_kwargs)
    @py_assert1 = new_comm.id
    @py_assert4 = 'two'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(new_comm) if 'new_comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_comm) else 'new_comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = comm.id
    @py_assert5 = new_comm.id
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(new_comm) if 'new_comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_comm) else 'new_comm'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert2 = validate_communication(new_comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(new_comm) if 'new_comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_comm) else 'new_comm'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    comm, _ = next(it)
    new_comm, uc = compress_uuids(comm, **compress_kwargs)
    @py_assert1 = new_comm.id
    @py_assert4 = 'three'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(new_comm) if 'new_comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_comm) else 'new_comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = comm.id
    @py_assert5 = new_comm.id
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py6)s\n{%(py6)s = %(py4)s.id\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(new_comm) if 'new_comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_comm) else 'new_comm'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert2 = validate_communication(new_comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(new_comm) if 'new_comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_comm) else 'new_comm'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
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