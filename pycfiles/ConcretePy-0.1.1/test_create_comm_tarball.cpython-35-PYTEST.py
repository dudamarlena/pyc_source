# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/charman/src/concrete-python/integration-tests/test_create_comm_tarball.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 8016 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pytest import fixture, mark
from concrete.util import CommunicationReader
from concrete.validate import validate_communication
import os, sys
from subprocess import Popen, PIPE
from tempfile import mkstemp

@fixture
def text_l0():
    return "Madame Magloire comprit, et elle alla chercher sur la cheminée de la chambre à coucher de monseigneur les deux chandeliers d'argent qu'elle posa sur la table tout allumés.\n"


@fixture
def text_l1():
    return "—Monsieur le curé, dit l'homme, vous êtes bon. Vous ne me méprisez pas. Vous me recevez chez vous. Vous allumez vos cierges pour moi. Je ne vous ai pourtant pas caché d'où je viens et que je suis un homme malheureux.\n"


@fixture
def text_l1_s0():
    return "—Monsieur le curé, dit l'homme, vous êtes bon.\n"


@fixture
def text_l1_s1():
    return 'Vous ne me méprisez pas.\n'


@fixture
def text_l1_s2():
    return 'Vous me recevez chez vous.\n'


@fixture
def text_l1_s3():
    return 'Vous allumez vos cierges pour moi.\n'


@fixture
def text_l1_s4():
    return "Je ne vous ai pourtant pas caché d'où je viens et que je suis un homme malheureux.\n"


@fixture
def output_file(request):
    fd, path = mkstemp()
    os.close(fd)

    def _remove():
        if os.path.exists(path):
            os.remove(path)

    request.addfinalizer(_remove)
    return path


def test_create_comm_tarball(output_file, text_l0, text_l1):
    p = Popen([
     sys.executable,
     'scripts/create-comm-tarball.py',
     'tests/testdata/les-deux-chandeliers.tar.gz',
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
    @py_assert4 = 'les-deux-chandeliers/l0.txt'
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
    @py_assert3 = @py_assert1 == text_l0
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text_l0)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text_l0) if 'text_l0' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text_l0) else 'text_l0'}
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
    comm, _ = next(it)
    @py_assert1 = comm.id
    @py_assert4 = 'les-deux-chandeliers/l1.txt'
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
    @py_assert3 = @py_assert1 == text_l1
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text_l1)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text_l1) if 'text_l1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text_l1) else 'text_l1'}
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
def test_create_comm_tarball_stdin(output_file, text_l0, text_l1):
    p = Popen([
     sys.executable,
     'scripts/create-comm-tarball.py',
     '-',
     output_file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    with open('tests/testdata/les-deux-chandeliers.tar.gz', 'rb') as (f):
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
    @py_assert4 = 'les-deux-chandeliers/l0.txt'
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
    @py_assert3 = @py_assert1 == text_l0
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text_l0)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text_l0) if 'text_l0' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text_l0) else 'text_l0'}
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
    comm, _ = next(it)
    @py_assert1 = comm.id
    @py_assert4 = 'les-deux-chandeliers/l1.txt'
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
    @py_assert3 = @py_assert1 == text_l1
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text_l1)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text_l1) if 'text_l1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text_l1) else 'text_l1'}
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
def test_create_comm_tarball_stdout(output_file, text_l0, text_l1):
    p = Popen([
     sys.executable,
     'scripts/create-comm-tarball.py',
     'tests/testdata/les-deux-chandeliers.tar.gz',
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
    @py_assert4 = 'les-deux-chandeliers/l0.txt'
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
    @py_assert3 = @py_assert1 == text_l0
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text_l0)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text_l0) if 'text_l0' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text_l0) else 'text_l0'}
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
    comm, _ = next(it)
    @py_assert1 = comm.id
    @py_assert4 = 'les-deux-chandeliers/l1.txt'
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
    @py_assert3 = @py_assert1 == text_l1
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text_l1)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text_l1) if 'text_l1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text_l1) else 'text_l1'}
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


def test_create_comm_tarball_log_every(output_file, text_l0, text_l1):
    p = Popen([
     sys.executable,
     'scripts/create-comm-tarball.py',
     '--log-level', 'INFO',
     '--log-interval', '1',
     'tests/testdata/les-deux-chandeliers.tar.gz',
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
    @py_assert1 = comm.id
    @py_assert4 = 'les-deux-chandeliers/l0.txt'
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
    @py_assert3 = @py_assert1 == text_l0
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text_l0)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text_l0) if 'text_l0' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text_l0) else 'text_l0'}
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
    comm, _ = next(it)
    @py_assert1 = comm.id
    @py_assert4 = 'les-deux-chandeliers/l1.txt'
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
    @py_assert3 = @py_assert1 == text_l1
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text_l1)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text_l1) if 'text_l1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text_l1) else 'text_l1'}
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


def test_create_comm_tarball_annotated(output_file, text_l0, text_l1):
    p = Popen([
     sys.executable,
     'scripts/create-comm-tarball.py',
     '--annotation-level', 'section',
     'tests/testdata/les-deux-chandeliers.tar.gz',
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
    @py_assert4 = 'les-deux-chandeliers/l0.txt'
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
    @py_assert3 = @py_assert1 == text_l0
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text_l0)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text_l0) if 'text_l0' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text_l0) else 'text_l0'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert2 = comm.sectionList
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 1
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.sectionList\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    comm, _ = next(it)
    @py_assert1 = comm.id
    @py_assert4 = 'les-deux-chandeliers/l1.txt'
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
    @py_assert3 = @py_assert1 == text_l1
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text_l1)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text_l1) if 'text_l1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text_l1) else 'text_l1'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert2 = comm.sectionList
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 1
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


def test_create_comm_tarball_per_line(output_file, text_l0, text_l1_s0, text_l1_s1, text_l1_s2, text_l1_s3, text_l1_s4):
    p = Popen([
     sys.executable,
     'scripts/create-comm-tarball.py',
     '--per-line',
     'tests/testdata/les-deux-chandeliers-perline.tar.gz',
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
    @py_assert4 = 'les-deux-chandeliers-perline/l0.txt/0'
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
    @py_assert3 = @py_assert1 == text_l0
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text_l0)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text_l0) if 'text_l0' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text_l0) else 'text_l0'}
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
    comm, _ = next(it)
    @py_assert1 = comm.id
    @py_assert4 = 'les-deux-chandeliers-perline/l1.txt/0'
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
    @py_assert3 = @py_assert1 == text_l1_s0
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text_l1_s0)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text_l1_s0) if 'text_l1_s0' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text_l1_s0) else 'text_l1_s0'}
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
    comm, _ = next(it)
    @py_assert1 = comm.id
    @py_assert4 = 'les-deux-chandeliers-perline/l1.txt/1'
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
    @py_assert3 = @py_assert1 == text_l1_s1
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text_l1_s1)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text_l1_s1) if 'text_l1_s1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text_l1_s1) else 'text_l1_s1'}
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
    comm, _ = next(it)
    @py_assert1 = comm.id
    @py_assert4 = 'les-deux-chandeliers-perline/l1.txt/2'
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
    @py_assert3 = @py_assert1 == text_l1_s2
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text_l1_s2)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text_l1_s2) if 'text_l1_s2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text_l1_s2) else 'text_l1_s2'}
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
    comm, _ = next(it)
    @py_assert1 = comm.id
    @py_assert4 = 'les-deux-chandeliers-perline/l1.txt/3'
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
    @py_assert3 = @py_assert1 == text_l1_s3
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text_l1_s3)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text_l1_s3) if 'text_l1_s3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text_l1_s3) else 'text_l1_s3'}
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
    comm, _ = next(it)
    @py_assert1 = comm.id
    @py_assert4 = 'les-deux-chandeliers-perline/l1.txt/4'
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
    @py_assert3 = @py_assert1 == text_l1_s4
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, text_l1_s4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(text_l1_s4) if 'text_l1_s4' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text_l1_s4) else 'text_l1_s4'}
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