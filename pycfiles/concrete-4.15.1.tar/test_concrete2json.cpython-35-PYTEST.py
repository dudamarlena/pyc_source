# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/charman/src/concrete-python/integration-tests/test_concrete2json.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 2652 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pytest import fixture, mark
import io, os, sys, json
from subprocess import Popen, PIPE
from tempfile import mkstemp
SERIF_TEXT = '<DOC id="dog-bites-man" type="other">\n<HEADLINE>\nDog Bites Man\n</HEADLINE>\n<TEXT>\n<P>\nJohn Smith, manager of ACMÉ INC, was bit by a dog on March 10th, 2013.\n</P>\n<P>\nHe died!\n</P>\n<P>\nJohn\'s daughter Mary expressed sorrow.\n</P>\n</TEXT>\n</DOC>\n'
LES_DEUX_TEXT = "Madame Magloire comprit, et elle alla chercher sur la cheminée de la chambre à coucher de monseigneur les deux chandeliers d'argent qu'elle posa sur la table tout allumés.\n\n—Monsieur le curé, dit l'homme, vous êtes bon. Vous ne me méprisez pas. Vous me recevez chez vous. Vous allumez vos cierges pour moi. Je ne vous ai pourtant pas caché d'où je viens et que je suis un homme malheureux.\n"

def assert_json_protocol_ok(json_path, expected_text):
    with io.open(json_path, encoding='utf-8') as (f):
        json_obj = json.load(f)
        @py_assert0 = json_obj['4']['str']
        @py_assert2 = @py_assert0 == expected_text
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, expected_text)) % {'py3': @pytest_ar._saferepr(expected_text) if 'expected_text' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_text) else 'expected_text', 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None


def assert_simple_json_protocol_ok(json_path, expected_text):
    with io.open(json_path, encoding='utf-8') as (f):
        json_obj = json.load(f)
        @py_assert0 = json_obj['text']
        @py_assert2 = @py_assert0 == expected_text
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, expected_text)) % {'py3': @pytest_ar._saferepr(expected_text) if 'expected_text' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_text) else 'expected_text', 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None


@fixture
def output_file(request):
    fd, path = mkstemp()
    os.close(fd)

    def _remove():
        if os.path.exists(path):
            os.remove(path)

    request.addfinalizer(_remove)
    return path


@mark.parametrize('args,text,assertion', [
 (
  [
   'tests/testdata/les-deux-chandeliers.concrete'],
  LES_DEUX_TEXT, assert_simple_json_protocol_ok),
 (
  [
   '--protocol', 'simple', 'tests/testdata/les-deux-chandeliers.concrete'],
  LES_DEUX_TEXT, assert_simple_json_protocol_ok),
 (
  [
   '--protocol', 'TJSONProtocol', 'tests/testdata/les-deux-chandeliers.concrete'],
  LES_DEUX_TEXT, assert_json_protocol_ok),
 (
  [
   'tests/testdata/serif_dog-bites-man.concrete'],
  SERIF_TEXT, assert_simple_json_protocol_ok),
 (
  [
   '--protocol', 'simple', 'tests/testdata/serif_dog-bites-man.concrete'],
  SERIF_TEXT, assert_simple_json_protocol_ok),
 (
  [
   '--protocol', 'TJSONProtocol', 'tests/testdata/serif_dog-bites-man.concrete'],
  SERIF_TEXT, assert_json_protocol_ok)])
def test_concrete2json(output_file, args, text, assertion):
    p = Popen([
     sys.executable, 'scripts/concrete2json.py'] + args + [
     output_file], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    @py_assert2 = b''
    @py_assert1 = stdout == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (stdout, @py_assert2)) % {'py0': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = b''
    @py_assert1 = stderr == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (stderr, @py_assert2)) % {'py0': @pytest_ar._saferepr(stderr) if 'stderr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stderr) else 'stderr', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = p.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    assertion(output_file, text)