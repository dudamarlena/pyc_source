# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/charman/src/concrete-python/integration-tests/test_create_comm.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 3721 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pytest import fixture, mark
from concrete.util import CommunicationReader
from concrete.validate import validate_communication
import os, sys
from subprocess import Popen, PIPE
from tempfile import mkstemp

@fixture
def text():
    return "Madame Magloire comprit, et elle alla chercher sur la cheminée de la chambre à coucher de monseigneur les deux chandeliers d'argent qu'elle posa sur la table tout allumés.\n\n—Monsieur le curé, dit l'homme, vous êtes bon. Vous ne me méprisez pas. Vous me recevez chez vous. Vous allumez vos cierges pour moi. Je ne vous ai pourtant pas caché d'où je viens et que je suis un homme malheureux.\n"


@fixture
def output_file(request):
    fd, path = mkstemp()
    os.close(fd)

    def _remove():
        if os.path.exists(path):
            os.remove(path)

    request.addfinalizer(_remove)
    return path


def test_create_comm(output_file, text):
    p = Popen([
     sys.executable,
     'scripts/create-comm.py',
     'tests/testdata/les-deux-chandeliers.txt',
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
    @py_assert1 = comm.id
    @py_assert4 = 'tests/testdata/les-deux-chandeliers.txt'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert2 = validate_communication(comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    @py_assert1 = comm.text
    @py_assert3 = @py_assert1 == text
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text) if 'text' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text) else 'text'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = comm.sectionList
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.sectionList\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
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
def test_create_comm_stdin(output_file, text):
    p = Popen([
     sys.executable,
     'scripts/create-comm.py',
     '-',
     output_file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    with open('tests/testdata/les-deux-chandeliers.txt', 'rb') as (f):
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
    @py_assert1 = comm.id
    @py_assert4 = '/dev/fd/0'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert2 = validate_communication(comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    @py_assert1 = comm.text
    @py_assert3 = @py_assert1 == text
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text) if 'text' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text) else 'text'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = comm.sectionList
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.sectionList\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
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
def test_create_comm_stdout(output_file, text):
    p = Popen([
     sys.executable,
     'scripts/create-comm.py',
     'tests/testdata/les-deux-chandeliers.txt',
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
    @py_assert1 = comm.id
    @py_assert4 = 'tests/testdata/les-deux-chandeliers.txt'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert2 = validate_communication(comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    @py_assert1 = comm.text
    @py_assert3 = @py_assert1 == text
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text) if 'text' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text) else 'text'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = comm.sectionList
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.sectionList\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
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


def test_create_comm_annotated(output_file, text):
    p = Popen([
     sys.executable,
     'scripts/create-comm.py',
     '--annotation-level', 'section',
     'tests/testdata/les-deux-chandeliers.txt',
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
    @py_assert1 = comm.id
    @py_assert4 = 'tests/testdata/les-deux-chandeliers.txt'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert2 = validate_communication(comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    @py_assert1 = comm.text
    @py_assert3 = @py_assert1 == text
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text) if 'text' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text) else 'text'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert2 = comm.sectionList
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 2
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.sectionList\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
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