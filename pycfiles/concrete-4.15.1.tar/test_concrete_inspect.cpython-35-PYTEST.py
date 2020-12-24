# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/charman/src/concrete-python/integration-tests/test_concrete_inspect.py
# Compiled at: 2019-01-21 14:21:03
# Size of source mod 2**32: 42317 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, sys, json
from pytest import fixture, mark
from subprocess import Popen, PIPE

@fixture
def comm_path(request):
    return 'tests/testdata/serif_dog-bites-man.concrete'


@fixture
def comms_path(request):
    return 'tests/testdata/serif_les-deux_concatenated.concrete'


@fixture
def comms_tgz_path(request):
    return 'tests/testdata/serif_les-deux.tar.gz'


@fixture
def simple_comms_tgz_path(request):
    return 'tests/testdata/simple.tar.gz'


def _augment_args(args_idx, params_list):
    augmented_params_list = []
    for params in params_list:
        augmented_params_list.append(params)
        args = params[args_idx]
        augmented_args = []
        i = 0
        while i < len(args):
            if args[i].startswith('--') and args[i].endswith('-tool'):
                augmented_args.extend([
                 '--filter-annotations',
                 args[i][2:-5],
                 json.dumps(dict(filter_fields=dict(tool=args[(i + 1)])))])
                i += 2
            else:
                augmented_args.append(args[i])
                i += 1

        augmented_params = params[:args_idx] + (tuple(augmented_args),) + params[args_idx + 1:]
        if augmented_params != params:
            augmented_params_list.append(tuple(augmented_params))

    return augmented_params_list


@mark.parametrize('which,args,output_prefix', _augment_args(1, [
 ((0, 1, 2), ('--char-offsets',), ''),
 ((0, 1, 2), ('--char-offsets', '--annotation-headers'), '\nconll\n-----\n'),
 ((0, 1, 4), ('--pos', '--pos-tool', 'Serif: part-of-speech'), ''),
 ((0, 1, 4), ('--pos', '--pos-tool', 'Serif: part-of-speech', '--annotation-headers'),
 '\nconll\n-----\n'),
 ((0, 1), ('--pos', '--pos-tool', 'fake'), ''),
 ((0, 1), ('--pos', '--pos-tool', 'fake', '--annotation-headers'), '\nconll\n-----\n'),
 ((0, 1, 5), ('--ner', '--ner-tool', 'Serif: names'), ''),
 ((0, 1, 5), ('--ner', '--ner-tool', 'Serif: names', '--annotation-headers'), '\nconll\n-----\n'),
 ((0, 1), ('--ner', '--ner-tool', 'fake'), ''),
 ((0, 1), ('--ner', '--ner-tool', 'fake', '--annotation-headers'), '\nconll\n-----\n'),
 ((0, 1, 6, 7), ('--dependency', '--dependency-tool', 'Stanford'), ''),
 ((0, 1, 6, 7), ('--dependency', '--dependency-tool', 'Stanford', '--annotation-headers'),
 '\nconll\n-----\n'),
 ((0, 1), ('--dependency', '--dependency-tool', 'fake'), ''),
 ((0, 1), ('--dependency', '--dependency-tool', 'fake', '--annotation-headers'), '\nconll\n-----\n'),
 ((0, 1, 4, 6, 7), ('--pos', '--dependency'), ''),
 ((0, 1, 4, 6, 7), ('--pos', '--dependency', '--annotation-headers'), '\nconll\n-----\n'),
 ((0, 1, 4), ('--pos', '--dependency', '--pos-tool', 'Serif: part-of-speech', '--dependency-tool', 'fake'),
 ''),
 ((0, 1, 4), ('--pos', '--dependency', '--pos-tool', 'Serif: part-of-speech', '--dependency-tool', 'fake', '--annotation-headers'),
 '\nconll\n-----\n'),
 ((0, 1), ('--pos', '--dependency', '--pos-tool', 'fake', '--dependency-tool', 'fake'),
 ''),
 ((0, 1), ('--pos', '--dependency', '--pos-tool', 'fake', '--dependency-tool', 'fake', '--annotation-headers'),
 '\nconll\n-----\n'),
 ((0, 1, 2, 4, 6, 7), ('--pos', '--char-offsets', '--dependency'), ''),
 ((0, 1, 2, 4, 6, 7), ('--pos', '--char-offsets', '--dependency', '--annotation-headers'),
 '\nconll\n-----\n'),
 ((0, 1, 2, 4, 5, 6, 7), ('--pos', '--char-offsets', '--dependency', '--ner'), ''),
 ((0, 1, 2, 4, 5, 6, 7), ('--pos', '--char-offsets', '--dependency', '--ner', '--annotation-headers'),
 '\nconll\n-----\n')]))
def test_print_conll_style_tags_for_communication(comm_path, which, args, output_prefix):
    p = Popen([
     sys.executable, 'scripts/concrete-inspect.py'] + list(args) + [
     comm_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    expected_output = output_prefix + '\n'.join('\t'.join(w for i, w in enumerate(row) if i in which) for row in (('INDEX', 'TOKEN', 'CHAR', 'LEMMA', 'POS', 'NER', 'HEAD', 'DEPREL'), ('-----', '-----', '----', '-----', '---', '---', '----', '------'), ('1', 'John', 'John', '', 'NNP', 'PER', '2', 'compound'), ('2', 'Smith', 'Smith', '', 'NNP', 'PER', '10', 'nsubjpass'), ('3', ',', ',', '', ',', '', '', ''), ('4', 'manager', 'manager', '', 'NN', '', '2', 'appos'), ('5', 'of', 'of', '', 'IN', '', '7', 'case'), ('6', 'ACMÉ', 'ACMÉ', '', 'NNP', 'ORG', '7', 'compound'), ('7', 'INC', 'INC', '', 'NNP', 'ORG', '4', 'nmod'), ('8', ',', ',', '', ',', '', '', ''), ('9', 'was', 'was', '', 'VBD', '', '10', 'auxpass'), ('10', 'bit', 'bit', '', 'NN', '', '0', 'ROOT'), ('11', 'by', 'by', '', 'IN', '', '13', 'case'), ('12', 'a', 'a', '', 'DT', '', '13', 'det'), ('13', 'dog', 'dog', '', 'NN', '', '10', 'nmod'), ('14', 'on', 'on', '', 'IN', '', '15', 'case'), ('15', 'March', 'March', '', 'DATE-NNP', '', '13', 'nmod'), ('16', '10th', '10th', '', 'JJ', '', '15', 'amod'), ('17', ',', ',', '', ',', '', '', ''), ('18', '2013', '2013', '', 'CD', '', '13', 'amod'), ('19', '.', '.', '', '.', '', '', ''), (), ('1', 'He', 'He', '', 'PRP', '', '2', 'nsubj'), ('2', 'died', 'died', '', 'VBD', '', '0', 'ROOT'), ('3', '!', '!', '', '.', '', '', ''), (), ('1', 'John', 'John', '', 'NNP', 'PER', '3', 'nmod:poss'), ('2', "'s", "'s", '', 'POS', '', '1', 'case'), ('3', 'daughter', 'daughter', '', 'NN', '', '5', 'dep'),
     ('4', 'Mary',
      'Mary', '', 'NNP', 'PER', '5', 'nsubj'), ('5', 'expressed', 'expressed', '', 'VBD', '', '0', 'ROOT'), ('6', 'sorrow', 'sorrow', '', 'NN', '', '5', 'dobj'), ('7', '.', '.', '', '.', '', '', ''), ())) + '\n'
    @py_assert0 = []
    @py_assert3 = [line for line in stderr.decode('utf-8').split(os.linesep) if line.strip() and 'deprecated' not in line]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = stdout.decode
    @py_assert5 = 'utf-8'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7.replace
    @py_assert12 = os.linesep
    @py_assert14 = '\n'
    @py_assert16 = @py_assert9(@py_assert12, @py_assert14)
    @py_assert1 = expected_output == @py_assert16
    if not @py_assert1:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py17)s\n{%(py17)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.decode\n}(%(py6)s)\n}.replace\n}(%(py13)s\n{%(py13)s = %(py11)s.linesep\n}, %(py15)s)\n}',), (expected_output, @py_assert16)) % {'py2': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5), 'py11': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py0': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = 0
    @py_assert4 = p.returncode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.returncode\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@mark.parametrize('first,second,args,output_prefix', _augment_args(2, [
 (
  True, True, (), ''),
 (True, True, ('--annotation-headers',), '\nentities\n--------\n'),
 (False, False, ('--entities-tool', 'fake'), ''),
 (False, False, ('--entities-tool', 'fake', '--annotation-headers'), '\nentities\n--------\n'),
 (True, False, ('--entities-tool', 'Serif: doc-entities'), ''),
 (True, False, ('--entities-tool', 'Serif: doc-entities', '--annotation-headers'), '\nentities\n--------\n'),
 (False, True, ('--entities-tool', 'Serif: doc-values'), ''),
 (False, True, ('--entities-tool', 'Serif: doc-values', '--annotation-headers'), '\nentities\n--------\n')]))
def test_print_entities(comm_path, first, second, args, output_prefix):
    p = Popen([
     sys.executable, 'scripts/concrete-inspect.py', '--entities'] + list(args) + [
     comm_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    expected_output = output_prefix
    if first:
        expected_output += "Entity Set 0 (Serif: doc-entities):\n  Entity 0-0:\n      EntityMention 0-0-0:\n          tokens:     John Smith\n          text:       John Smith\n          entityType: PER\n          phraseType: PhraseType.NAME\n      EntityMention 0-0-1:\n          tokens:     John Smith , manager of ACMÉ INC ,\n          text:       John Smith, manager of ACMÉ INC,\n          entityType: PER\n          phraseType: PhraseType.APPOSITIVE\n          child EntityMention #0:\n              tokens:     John Smith\n              text:       John Smith\n              entityType: PER\n              phraseType: PhraseType.NAME\n          child EntityMention #1:\n              tokens:     manager of ACMÉ INC\n              text:       manager of ACMÉ INC\n              entityType: PER\n              phraseType: PhraseType.COMMON_NOUN\n      EntityMention 0-0-2:\n          tokens:     manager of ACMÉ INC\n          text:       manager of ACMÉ INC\n          entityType: PER\n          phraseType: PhraseType.COMMON_NOUN\n      EntityMention 0-0-3:\n          tokens:     He\n          text:       He\n          entityType: PER\n          phraseType: PhraseType.PRONOUN\n      EntityMention 0-0-4:\n          tokens:     John\n          text:       John\n          entityType: PER.Individual\n          phraseType: PhraseType.NAME\n\n  Entity 0-1:\n      EntityMention 0-1-0:\n          tokens:     ACMÉ INC\n          text:       ACMÉ INC\n          entityType: ORG\n          phraseType: PhraseType.NAME\n\n  Entity 0-2:\n      EntityMention 0-2-0:\n          tokens:     John 's daughter Mary\n          text:       John's daughter Mary\n          entityType: PER.Individual\n          phraseType: PhraseType.NAME\n          child EntityMention #0:\n              tokens:     Mary\n              text:       Mary\n              entityType: PER\n              phraseType: PhraseType.OTHER\n      EntityMention 0-2-1:\n          tokens:     daughter\n          text:       daughter\n          entityType: PER\n          phraseType: PhraseType.COMMON_NOUN\n\n\n"
    if second:
        expected_output += 'Entity Set 1 (Serif: doc-values):\n  Entity 1-0:\n      EntityMention 1-0-0:\n          tokens:     March 10th , 2013\n          text:       March 10th, 2013\n          entityType: TIMEX2.TIME\n          phraseType: PhraseType.OTHER\n\n\n'
    @py_assert0 = []
    @py_assert3 = [line for line in stderr.decode('utf-8').split(os.linesep) if line.strip() and 'deprecated' not in line]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = stdout.decode
    @py_assert5 = 'utf-8'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7.replace
    @py_assert12 = os.linesep
    @py_assert14 = '\n'
    @py_assert16 = @py_assert9(@py_assert12, @py_assert14)
    @py_assert1 = expected_output == @py_assert16
    if not @py_assert1:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py17)s\n{%(py17)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.decode\n}(%(py6)s)\n}.replace\n}(%(py13)s\n{%(py13)s = %(py11)s.linesep\n}, %(py15)s)\n}',), (expected_output, @py_assert16)) % {'py2': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5), 'py11': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py0': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = 0
    @py_assert4 = p.returncode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.returncode\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@mark.parametrize('first,second,args,output_prefix', _augment_args(2, [
 (
  True, True, (), ''),
 (True, True, ('--annotation-headers',), '\nsituation mentions\n------------------\n'),
 (False, False, ('--situation-mentions-tool', 'fake'), ''),
 (False, False, ('--situation-mentions-tool', 'fake', '--annotation-headers'), '\nsituation mentions\n------------------\n'),
 (True, False, ('--situation-mentions-tool', 'Serif: relations'), ''),
 (True, False, ('--situation-mentions-tool', 'Serif: relations', '--annotation-headers'),
 '\nsituation mentions\n------------------\n'),
 (False, True, ('--situation-mentions-tool', 'Serif: events'), ''),
 (False, True, ('--situation-mentions-tool', 'Serif: events', '--annotation-headers'),
 '\nsituation mentions\n------------------\n')]))
def test_print_situation_mentions(comm_path, first, second, args, output_prefix):
    p = Popen([
     sys.executable, 'scripts/concrete-inspect.py', '--situation-mentions'] + list(args) + [
     comm_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    expected_output = output_prefix
    if first:
        expected_output += 'Situation Set 0 (Serif: relations):\n  SituationMention 0-0:\n          situationType:      ORG-AFF.Employment\n          Argument 0:\n              role:           Role.RELATION_SOURCE_ROLE\n              entityMention:  manager of ACMÉ INC\n          Argument 1:\n              role:           Role.RELATION_TARGET_ROLE\n              entityMention:  ACMÉ INC\n\n  SituationMention 0-1:\n          situationType:      PER-SOC.Family\n          Argument 0:\n              role:           Role.RELATION_SOURCE_ROLE\n              entityMention:  John\n          Argument 1:\n              role:           Role.RELATION_TARGET_ROLE\n              entityMention:  daughter\n\n\n'
    if second:
        expected_output += 'Situation Set 1 (Serif: events):\n  SituationMention 1-0:\n          text:               died\n          situationType:      Life.Die\n          Argument 0:\n              role:           Victim\n              entityMention:  He\n\n\n'
    @py_assert0 = []
    @py_assert3 = [line for line in stderr.decode('utf-8').split(os.linesep) if line.strip() and 'deprecated' not in line]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = stdout.decode
    @py_assert5 = 'utf-8'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7.replace
    @py_assert12 = os.linesep
    @py_assert14 = '\n'
    @py_assert16 = @py_assert9(@py_assert12, @py_assert14)
    @py_assert1 = expected_output == @py_assert16
    if not @py_assert1:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py17)s\n{%(py17)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.decode\n}(%(py6)s)\n}.replace\n}(%(py13)s\n{%(py13)s = %(py11)s.linesep\n}, %(py15)s)\n}',), (expected_output, @py_assert16)) % {'py2': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5), 'py11': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py0': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = 0
    @py_assert4 = p.returncode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.returncode\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@mark.parametrize('first,second,args,output_prefix', _augment_args(2, [
 (
  True, True, (), ''),
 (True, True, ('--annotation-headers',), '\nsituations\n----------\n'),
 (False, False, ('--situations-tool', 'fake'), ''),
 (False, False, ('--situations-tool', 'fake', '--annotation-headers'), '\nsituations\n----------\n'),
 (True, False, ('--situations-tool', 'Serif: relations'), ''),
 (True, False, ('--situations-tool', 'Serif: relations', '--annotation-headers'), '\nsituations\n----------\n'),
 (False, True, ('--situations-tool', 'Serif: events'), ''),
 (False, True, ('--situations-tool', 'Serif: events', '--annotation-headers'), '\nsituations\n----------\n')]))
def test_print_situations(comm_path, first, second, args, output_prefix):
    p = Popen([
     sys.executable, 'scripts/concrete-inspect.py', '--situations'] + list(args) + [
     comm_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    expected_output = output_prefix
    if first:
        expected_output += 'Situation Set 0 (Serif: relations):\n\n'
    if second:
        expected_output += 'Situation Set 1 (Serif: events):\n  Situation 1-0:\n      situationType:    Life.Die\n\n\n'
    @py_assert0 = []
    @py_assert3 = [line for line in stderr.decode('utf-8').split(os.linesep) if line.strip() and 'deprecated' not in line]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = stdout.decode
    @py_assert5 = 'utf-8'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7.replace
    @py_assert12 = os.linesep
    @py_assert14 = '\n'
    @py_assert16 = @py_assert9(@py_assert12, @py_assert14)
    @py_assert1 = expected_output == @py_assert16
    if not @py_assert1:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py17)s\n{%(py17)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.decode\n}(%(py6)s)\n}.replace\n}(%(py13)s\n{%(py13)s = %(py11)s.linesep\n}, %(py15)s)\n}',), (expected_output, @py_assert16)) % {'py2': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5), 'py11': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py0': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = 0
    @py_assert4 = p.returncode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.returncode\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@mark.parametrize('first,args,output_prefix', _augment_args(1, [
 (
  True, (), ''),
 (True, ('--annotation-headers',), '\ntext\n----\n'),
 (False, ('--text-tool', 'fake'), ''),
 (False, ('--text-tool', 'fake', '--annotation-headers'), '\ntext\n----\n'),
 (True, ('--text-tool', 'concrete_serif v3.10.1pre'), ''),
 (True, ('--text-tool', 'concrete_serif v3.10.1pre', '--annotation-headers'), '\ntext\n----\n')]))
def test_print_text_for_communication(comm_path, first, args, output_prefix):
    p = Popen([
     sys.executable, 'scripts/concrete-inspect.py', '--text'] + list(args) + [
     comm_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    expected_output = output_prefix
    if first:
        expected_output += '<DOC id="dog-bites-man" type="other">\n<HEADLINE>\nDog Bites Man\n</HEADLINE>\n<TEXT>\n<P>\nJohn Smith, manager of ACMÉ INC, was bit by a dog on March 10th, 2013.\n</P>\n<P>\nHe died!\n</P>\n<P>\nJohn\'s daughter Mary expressed sorrow.\n</P>\n</TEXT>\n</DOC>\n\n'
    @py_assert0 = []
    @py_assert3 = [line for line in stderr.decode('utf-8').split(os.linesep) if line.strip() and 'deprecated' not in line]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = stdout.decode
    @py_assert5 = 'utf-8'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7.replace
    @py_assert12 = os.linesep
    @py_assert14 = '\n'
    @py_assert16 = @py_assert9(@py_assert12, @py_assert14)
    @py_assert1 = expected_output == @py_assert16
    if not @py_assert1:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py17)s\n{%(py17)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.decode\n}(%(py6)s)\n}.replace\n}(%(py13)s\n{%(py13)s = %(py11)s.linesep\n}, %(py15)s)\n}',), (expected_output, @py_assert16)) % {'py2': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5), 'py11': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py0': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = 0
    @py_assert4 = p.returncode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.returncode\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@mark.parametrize('first,second,third,args,output_prefix', _augment_args(3, [
 (
  True, True, True, (), ''),
 (True, True, True, ('--annotation-headers',), '\nmentions\n--------\n'),
 (False, False, False, ('--mentions-tool', 'fake'), ''),
 (False, False, False, ('--mentions-tool', 'fake', '--annotation-headers'), '\nmentions\n--------\n'),
 (True, False, False, ('--mentions-tool', 'Serif: names'), ''),
 (True, False, False, ('--mentions-tool', 'Serif: names', '--annotation-headers'), '\nmentions\n--------\n'),
 (False, True, False, ('--mentions-tool', 'Serif: values'), ''),
 (False, True, False, ('--mentions-tool', 'Serif: values', '--annotation-headers'),
 '\nmentions\n--------\n'),
 (False, False, True, ('--mentions-tool', 'Serif: mentions'), ''),
 (False, False, True, ('--mentions-tool', 'Serif: mentions', '--annotation-headers'),
 '\nmentions\n--------\n')]))
def test_print_tokens_with_entityMentions(comm_path, first, second, third, args, output_prefix):
    p = Popen([
     sys.executable, 'scripts/concrete-inspect.py', '--mentions'] + list(args) + [
     comm_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if third:
        expected_output = output_prefix + "\n<ENTITY ID=0><ENTITY ID=0>John Smith</ENTITY> , <ENTITY ID=0>manager of <ENTITY ID=1>ACMÉ INC</ENTITY></ENTITY> ,</ENTITY> was bit by a dog on %sMarch 10th , 2013%s .\n\n<ENTITY ID=0>He</ENTITY> died !\n\n<ENTITY ID=2><ENTITY ID=0>John</ENTITY> 's <ENTITY ID=2>daughter</ENTITY> Mary</ENTITY> expressed sorrow .\n\n"
    else:
        expected_output = output_prefix + "\nJohn Smith , manager of ACMÉ INC , was bit by a dog on %sMarch 10th , 2013%s .\n\nHe died !\n\nJohn 's daughter Mary expressed sorrow .\n\n"
    expected_output = expected_output % (
     '<ENTITY ID=3>' if second else '',
     '</ENTITY>' if second else '')
    @py_assert0 = []
    @py_assert3 = [line for line in stderr.decode('utf-8').split(os.linesep) if line.strip() and 'deprecated' not in line]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = stdout.decode
    @py_assert5 = 'utf-8'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7.replace
    @py_assert12 = os.linesep
    @py_assert14 = '\n'
    @py_assert16 = @py_assert9(@py_assert12, @py_assert14)
    @py_assert1 = expected_output == @py_assert16
    if not @py_assert1:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py17)s\n{%(py17)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.decode\n}(%(py6)s)\n}.replace\n}(%(py13)s\n{%(py13)s = %(py11)s.linesep\n}, %(py15)s)\n}',), (expected_output, @py_assert16)) % {'py2': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5), 'py11': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py0': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = 0
    @py_assert4 = p.returncode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.returncode\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@mark.parametrize('first,args,output_prefix', _augment_args(1, [
 (
  True, (), ''),
 (True, ('--annotation-headers',), '\ntokens\n------\n'),
 (False, ('--tokens-tool', 'fake'), ''),
 (False, ('--tokens-tool', 'fake', '--annotation-headers'), '\ntokens\n------\n'),
 (True, ('--tokens-tool', 'Serif: tokens'), ''),
 (True, ('--tokens-tool', 'Serif: tokens', '--annotation-headers'), '\ntokens\n------\n')]))
def test_print_tokens_for_communication(comm_path, first, args, output_prefix):
    p = Popen([
     sys.executable, 'scripts/concrete-inspect.py', '--tokens'] + list(args) + [
     comm_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    expected_output = output_prefix
    if first:
        expected_output += '\nJohn Smith , manager of ACMÉ INC , was bit by a dog on March 10th , 2013 .\n'
    expected_output += '\n'
    if first:
        expected_output += 'He died !\n'
    expected_output += '\n'
    if first:
        expected_output += "John 's daughter Mary expressed sorrow ."
    expected_output += '\n\n'
    @py_assert0 = []
    @py_assert3 = [line for line in stderr.decode('utf-8').split(os.linesep) if line.strip() and 'deprecated' not in line]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = stdout.decode
    @py_assert5 = 'utf-8'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7.replace
    @py_assert12 = os.linesep
    @py_assert14 = '\n'
    @py_assert16 = @py_assert9(@py_assert12, @py_assert14)
    @py_assert1 = expected_output == @py_assert16
    if not @py_assert1:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py17)s\n{%(py17)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.decode\n}(%(py6)s)\n}.replace\n}(%(py13)s\n{%(py13)s = %(py11)s.linesep\n}, %(py15)s)\n}',), (expected_output, @py_assert16)) % {'py2': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5), 'py11': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py0': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = 0
    @py_assert4 = p.returncode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.returncode\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@mark.parametrize('first,args,output_prefix', _augment_args(1, [
 (
  True, (), ''),
 (True, ('--annotation-headers',), '\ntreebank\n--------\n'),
 (False, ('--treebank-tool', 'fake'), ''),
 (False, ('--treebank-tool', 'fake', '--annotation-headers'), '\ntreebank\n--------\n'),
 (True, ('--treebank-tool', 'Serif: parse'), ''),
 (True, ('--treebank-tool', 'Serif: parse', '--annotation-headers'), '\ntreebank\n--------\n')]))
def test_print_penn_treebank_for_communication(comm_path, first, args, output_prefix):
    p = Popen([
     sys.executable, 'scripts/concrete-inspect.py', '--treebank'] + list(args) + [
     comm_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    expected_output = output_prefix
    if first:
        expected_output += "(S (NP (NPP (NNP john)\n            (NNP smith))\n       (, ,)\n       (NP (NPA (NN manager))\n           (PP (IN of)\n               (NPP (NNP acme)\n                    (NNP inc))))\n       (, ,))\n   (VP (VBD was)\n       (NP (NPA (NN bit))\n           (PP (IN by)\n               (NP (NPA (DT a)\n                        (NN dog))\n                   (PP (IN on)\n                       (NP (DATE (DATE-NNP march)\n                                 (JJ 10th))\n                           (, ,)\n                           (NPA (CD 2013))))))))\n   (. .))\n\n\n(S (NPA (PRP he))\n   (VP (VBD died))\n   (. !))\n\n\n(S (NPA (NPPOS (NPP (NNP john))\n               (POS 's))\n        (NN daughter)\n        (NPP (NNP mary)))\n   (VP (VBD expressed)\n       (NPA (NN sorrow)))\n   (. .))\n\n\n"
    @py_assert0 = []
    @py_assert3 = [line for line in stderr.decode('utf-8').split(os.linesep) if line.strip() and 'deprecated' not in line]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = stdout.decode
    @py_assert5 = 'utf-8'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7.replace
    @py_assert12 = os.linesep
    @py_assert14 = '\n'
    @py_assert16 = @py_assert9(@py_assert12, @py_assert14)
    @py_assert1 = expected_output == @py_assert16
    if not @py_assert1:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py17)s\n{%(py17)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.decode\n}(%(py6)s)\n}.replace\n}(%(py13)s\n{%(py13)s = %(py11)s.linesep\n}, %(py15)s)\n}',), (expected_output, @py_assert16)) % {'py2': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5), 'py11': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py0': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = 0
    @py_assert4 = p.returncode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.returncode\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@mark.parametrize('which,args,output_prefix', _augment_args(1, [
 (
  range(17), (), ''),
 (
  range(17), ('--annotation-headers', ), '\nmetadata\n--------\n'),
 ((0,), ('--metadata-tool', 'concrete_serif v3.10.1pre'), ''),
 ((0,), ('--metadata-tool', 'concrete_serif v3.10.1pre', '--annotation-headers'), '\nmetadata\n--------\n'),
 ((1,), ('--metadata-tool', 'Serif: tokens'), ''),
 ((1,), ('--metadata-tool', 'Serif: tokens', '--annotation-headers'), '\nmetadata\n--------\n'),
 ((2,), ('--metadata-tool', 'Stanford'), ''),
 ((2,), ('--metadata-tool', 'Stanford', '--annotation-headers'), '\nmetadata\n--------\n'),
 ((3,), ('--metadata-tool', 'Serif: parse'), ''),
 ((3,), ('--metadata-tool', 'Serif: parse', '--annotation-headers'), '\nmetadata\n--------\n'),
 ((4, 6), ('--metadata-tool', 'Serif: names'), ''),
 ((4, 6), ('--metadata-tool', 'Serif: names', '--annotation-headers'), '\nmetadata\n--------\n'),
 ((5,), ('--metadata-tool', 'Serif: part-of-speech'), ''),
 ((5,), ('--metadata-tool', 'Serif: part-of-speech', '--annotation-headers'), '\nmetadata\n--------\n'),
 ((7,), ('--metadata-tool', 'Serif: values'), ''),
 ((7,), ('--metadata-tool', 'Serif: values', '--annotation-headers'), '\nmetadata\n--------\n'),
 ((8,), ('--metadata-tool', 'Serif: mentions'), ''),
 ((8,), ('--metadata-tool', 'Serif: mentions', '--annotation-headers'), '\nmetadata\n--------\n'),
 ((9,), ('--metadata-tool', 'Serif: doc-entities'), ''),
 ((9,), ('--metadata-tool', 'Serif: doc-entities', '--annotation-headers'), '\nmetadata\n--------\n'),
 ((10,), ('--metadata-tool', 'Serif: doc-values'), ''),
 ((10,), ('--metadata-tool', 'Serif: doc-values', '--annotation-headers'), '\nmetadata\n--------\n'),
 ((11, 13), ('--metadata-tool', 'Serif: relations'), ''),
 ((11, 13), ('--metadata-tool', 'Serif: relations', '--annotation-headers'), '\nmetadata\n--------\n'),
 ((12, 14), ('--metadata-tool', 'Serif: events'), ''),
 ((12, 14), ('--metadata-tool', 'Serif: events', '--annotation-headers'), '\nmetadata\n--------\n'),
 ((15,), ('--metadata-tool', 'lda'), ''),
 ((15,), ('--metadata-tool', 'lda', '--annotation-headers'), '\nmetadata\n--------\n'),
 ((16,), ('--metadata-tool', 'urgency'), ''),
 ((16,), ('--metadata-tool', 'urgency', '--annotation-headers'), '\nmetadata\n--------\n')]))
def test_print_metadata_for_communication(comm_path, which, args, output_prefix):
    p = Popen([
     sys.executable, 'scripts/concrete-inspect.py', '--metadata'] + list(args) + [
     comm_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    expected_output = output_prefix
    if 0 in which:
        expected_output += 'Communication:  concrete_serif v3.10.1pre\n'
        expected_output += '\n'
    if 1 in which:
        expected_output += '  Tokenization:  Serif: tokens\n'
        expected_output += '\n'
    if 2 in which:
        expected_output += '    Dependency Parse:  Stanford\n'
        expected_output += '\n'
    if 3 in which:
        expected_output += '    Parse:  Serif: parse\n'
        expected_output += '\n'
    if 4 in which:
        expected_output += '    TokenTagging:  Serif: names\n'
    if 5 in which:
        expected_output += '    TokenTagging:  Serif: part-of-speech\n'
    if 4 in which or 5 in which:
        expected_output += '\n'
    if 6 in which:
        expected_output += '  EntityMentionSet #0:  Serif: names\n'
    if 7 in which:
        expected_output += '  EntityMentionSet #1:  Serif: values\n'
    if 8 in which:
        expected_output += '  EntityMentionSet #2:  Serif: mentions\n'
    expected_output += '\n'
    if 9 in which:
        expected_output += '  EntitySet #0:  Serif: doc-entities\n'
    if 10 in which:
        expected_output += '  EntitySet #1:  Serif: doc-values\n'
    expected_output += '\n'
    if 11 in which:
        expected_output += '  SituationMentionSet #0:  Serif: relations\n'
    if 12 in which:
        expected_output += '  SituationMentionSet #1:  Serif: events\n'
    expected_output += '\n'
    if 13 in which:
        expected_output += '  SituationSet #0:  Serif: relations\n'
    if 14 in which:
        expected_output += '  SituationSet #1:  Serif: events\n'
    expected_output += '\n'
    if 15 in which:
        expected_output += '  CommunicationTagging:  lda\n'
    if 16 in which:
        expected_output += '  CommunicationTagging:  urgency\n'
    if 15 in which or 16 in which:
        expected_output += '\n'
    @py_assert0 = []
    @py_assert3 = [line for line in stderr.decode('utf-8').split(os.linesep) if line.strip() and 'deprecated' not in line]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = stdout.decode
    @py_assert5 = 'utf-8'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7.replace
    @py_assert12 = os.linesep
    @py_assert14 = '\n'
    @py_assert16 = @py_assert9(@py_assert12, @py_assert14)
    @py_assert1 = expected_output == @py_assert16
    if not @py_assert1:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py17)s\n{%(py17)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.decode\n}(%(py6)s)\n}.replace\n}(%(py13)s\n{%(py13)s = %(py11)s.linesep\n}, %(py15)s)\n}',), (expected_output, @py_assert16)) % {'py2': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5), 'py11': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py0': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = 0
    @py_assert4 = p.returncode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.returncode\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@mark.parametrize('first,args,output_prefix', _augment_args(1, [
 (
  True, (), ''),
 (True, ('--annotation-headers',), '\nsections\n--------\n'),
 (False, ('--sections-tool', 'fake'), ''),
 (False, ('--sections-tool', 'fake', '--annotation-headers'), '\nsections\n--------\n'),
 (True, ('--sections-tool', 'concrete_serif v3.10.1pre'), ''),
 (True, ('--sections-tool', 'concrete_serif v3.10.1pre', '--annotation-headers'), '\nsections\n--------\n')]))
def test_print_sections_for_communication(comm_path, first, args, output_prefix):
    p = Popen([
     sys.executable, 'scripts/concrete-inspect.py', '--sections'] + list(args) + [
     comm_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    expected_output = output_prefix
    if first:
        expected_output += "Section 0 (0ab68635-c83d-4b02-b8c3-288626968e05)[kind: SectionKind.PASSAGE], from 81 to 82:\n\n\n\nSection 1 (54902d75-1841-4d8d-b4c5-390d4ef1a47a)[kind: SectionKind.PASSAGE], from 85 to 162:\n\nJohn Smith, manager of ACMÉ INC, was bit by a dog on March 10th, 2013.\n</P>\n\n\nSection 2 (7ec8b7d9-6be0-4c62-af57-3c6c48bad711)[kind: SectionKind.PASSAGE], from 165 to 180:\n\nHe died!\n</P>\n\n\nSection 3 (68da91a1-5beb-4129-943d-170c40c7d0f7)[kind: SectionKind.PASSAGE], from 183 to 228:\n\nJohn's daughter Mary expressed sorrow.\n</P>\n\n\n\n"
    @py_assert0 = []
    @py_assert3 = [line for line in stderr.decode('utf-8').split(os.linesep) if line.strip() and 'deprecated' not in line]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = stdout.decode
    @py_assert5 = 'utf-8'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7.replace
    @py_assert12 = os.linesep
    @py_assert14 = '\n'
    @py_assert16 = @py_assert9(@py_assert12, @py_assert14)
    @py_assert1 = expected_output == @py_assert16
    if not @py_assert1:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py17)s\n{%(py17)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.decode\n}(%(py6)s)\n}.replace\n}(%(py13)s\n{%(py13)s = %(py11)s.linesep\n}, %(py15)s)\n}',), (expected_output, @py_assert16)) % {'py2': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5), 'py11': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py0': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = 0
    @py_assert4 = p.returncode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.returncode\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@mark.parametrize('first,args,output_prefix', _augment_args(1, [
 (
  True, (), ''),
 (True, ('--annotation-headers',), '\nid\n--\n'),
 (False, ('--id-tool', 'fake'), ''),
 (False, ('--id-tool', 'fake', '--annotation-headers'), '\nid\n--\n'),
 (True, ('--id-tool', 'concrete_serif v3.10.1pre'), ''),
 (True, ('--id-tool', 'concrete_serif v3.10.1pre', '--annotation-headers'), '\nid\n--\n')]))
def test_print_id_for_communication(comm_path, first, args, output_prefix):
    p = Popen([
     sys.executable, 'scripts/concrete-inspect.py', '--id'] + list(args) + [
     comm_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    expected_output = output_prefix
    if first:
        expected_output += 'tests/testdata/serif_dog-bites-man.xml\n'
    @py_assert0 = []
    @py_assert3 = [line for line in stderr.decode('utf-8').split(os.linesep) if line.strip() and 'deprecated' not in line]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = stdout.decode
    @py_assert5 = 'utf-8'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7.replace
    @py_assert12 = os.linesep
    @py_assert14 = '\n'
    @py_assert16 = @py_assert9(@py_assert12, @py_assert14)
    @py_assert1 = expected_output == @py_assert16
    if not @py_assert1:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py17)s\n{%(py17)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.decode\n}(%(py6)s)\n}.replace\n}(%(py13)s\n{%(py13)s = %(py11)s.linesep\n}, %(py15)s)\n}',), (expected_output, @py_assert16)) % {'py2': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5), 'py11': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py0': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = 0
    @py_assert4 = p.returncode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.returncode\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@mark.parametrize('first,second,args,output_prefix', _augment_args(2, [
 (
  True, True, (), ''),
 (True, True, ('--annotation-headers',), '\ncommunication taggings\n----------------------\n'),
 (True, False, ('--communication-taggings-tool', 'lda'), ''),
 (True, False, ('--communication-taggings-tool', 'lda', '--annotation-headers'), '\ncommunication taggings\n----------------------\n'),
 (False, True, ('--communication-taggings-tool', 'urgency'), ''),
 (False, True, ('--communication-taggings-tool', 'urgency', '--annotation-headers'),
 '\ncommunication taggings\n----------------------\n'),
 (False, False, ('--communication-taggings-tool', 'fake'), ''),
 (False, False, ('--communication-taggings-tool', 'fake', '--annotation-headers'), '\ncommunication taggings\n----------------------\n')]))
def test_print_communication_taggings_for_communication(comm_path, first, second, args, output_prefix):
    p = Popen([
     sys.executable, 'scripts/concrete-inspect.py', '--communication-taggings'] + list(args) + [
     comm_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    expected_output = output_prefix
    if first:
        expected_output += 'topic: animals:-1.500 crime:-3.000 humanity:-4.000\n'
    if second:
        expected_output += 'urgency: low:0.750\n'
    @py_assert0 = []
    @py_assert3 = [line for line in stderr.decode('utf-8').split(os.linesep) if line.strip() and 'deprecated' not in line]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = stdout.decode
    @py_assert5 = 'utf-8'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7.replace
    @py_assert12 = os.linesep
    @py_assert14 = '\n'
    @py_assert16 = @py_assert9(@py_assert12, @py_assert14)
    @py_assert1 = expected_output == @py_assert16
    if not @py_assert1:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py17)s\n{%(py17)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.decode\n}(%(py6)s)\n}.replace\n}(%(py13)s\n{%(py13)s = %(py11)s.linesep\n}, %(py15)s)\n}',), (expected_output, @py_assert16)) % {'py2': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5), 'py11': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py0': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = 0
    @py_assert4 = p.returncode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.returncode\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@mark.parametrize('first,second,third,args,first_output_prefix,second_output_prefix', _augment_args(3, [
 (True, True, True, ('--id', '--situation-mentions'), '', ''),
 (True, True, True, ('--id', '--situation-mentions', '--annotation-headers'), '\nid\n--\n',
 '\nsituation mentions\n------------------\n'),
 (False, True, True, ('--id', '--situation-mentions', '--id-tool', 'fake'), '', ''),
 (False, True, True, ('--id', '--situation-mentions', '--id-tool', 'fake', '--annotation-headers'),
 '\nid\n--\n', '\nsituation mentions\n------------------\n'),
 (True, True, True, ('--id', '--situation-mentions', '--id-tool', 'concrete_serif v3.10.1pre'),
 '', ''),
 (True, True, True, ('--id', '--situation-mentions', '--id-tool', 'concrete_serif v3.10.1pre', '--annotation-headers'),
 '\nid\n--\n', '\nsituation mentions\n------------------\n'),
 (True, True, False, ('--id', '--situation-mentions', '--situation-mentions-tool', 'Serif: relations'),
 '', ''),
 (True, True, False, ('--id', '--situation-mentions', '--situation-mentions-tool', 'Serif: relations', '--annotation-headers'),
 '\nid\n--\n', '\nsituation mentions\n------------------\n'),
 (False, True, False, ('--id', '--situation-mentions', '--situation-mentions-tool', 'Serif: relations', '--id-tool', 'fake'),
 '', ''),
 (False, True, False, ('--id', '--situation-mentions', '--situation-mentions-tool', 'Serif: relations', '--id-tool', 'fake', '--annotation-headers'),
 '\nid\n--\n', '\nsituation mentions\n------------------\n'),
 (True, True, False, ('--id', '--situation-mentions', '--situation-mentions-tool', 'Serif: relations', '--id-tool', 'concrete_serif v3.10.1pre'),
 '', ''),
 (True, True, False, ('--id', '--situation-mentions', '--situation-mentions-tool', 'Serif: relations', '--id-tool', 'concrete_serif v3.10.1pre', '--annotation-headers'),
 '\nid\n--\n', '\nsituation mentions\n------------------\n'),
 (True, False, False, ('--id', '--situation-mentions', '--situation-mentions-tool', 'fake'),
 '', ''),
 (True, False, False, ('--id', '--situation-mentions', '--situation-mentions-tool', 'fake', '--annotation-headers'),
 '\nid\n--\n', '\nsituation mentions\n------------------\n'),
 (False, False, False, ('--id', '--situation-mentions', '--situation-mentions-tool', 'fake', '--id-tool', 'fake'),
 '', ''),
 (False, False, False, ('--id', '--situation-mentions', '--situation-mentions-tool', 'fake', '--id-tool', 'fake', '--annotation-headers'),
 '\nid\n--\n', '\nsituation mentions\n------------------\n'),
 (True, False, False, ('--id', '--situation-mentions', '--situation-mentions-tool', 'fake', '--id-tool', 'concrete_serif v3.10.1pre'),
 '', ''),
 (True, False, False, ('--id', '--situation-mentions', '--situation-mentions-tool', 'fake', '--id-tool', 'concrete_serif v3.10.1pre', '--annotation-headers'),
 '\nid\n--\n', '\nsituation mentions\n------------------\n')]))
def test_print_multiple_for_communication(comm_path, first, second, third, args, first_output_prefix, second_output_prefix):
    p = Popen([
     sys.executable, 'scripts/concrete-inspect.py'] + list(args) + [
     comm_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    expected_output = first_output_prefix
    if first:
        expected_output += 'tests/testdata/serif_dog-bites-man.xml\n'
    expected_output += second_output_prefix
    if second:
        expected_output += 'Situation Set 0 (Serif: relations):\n  SituationMention 0-0:\n          situationType:      ORG-AFF.Employment\n          Argument 0:\n              role:           Role.RELATION_SOURCE_ROLE\n              entityMention:  manager of ACMÉ INC\n          Argument 1:\n              role:           Role.RELATION_TARGET_ROLE\n              entityMention:  ACMÉ INC\n\n  SituationMention 0-1:\n          situationType:      PER-SOC.Family\n          Argument 0:\n              role:           Role.RELATION_SOURCE_ROLE\n              entityMention:  John\n          Argument 1:\n              role:           Role.RELATION_TARGET_ROLE\n              entityMention:  daughter\n\n\n'
    if third:
        expected_output += 'Situation Set 1 (Serif: events):\n  SituationMention 1-0:\n          text:               died\n          situationType:      Life.Die\n          Argument 0:\n              role:           Victim\n              entityMention:  He\n\n\n'
    @py_assert0 = []
    @py_assert3 = [line for line in stderr.decode('utf-8').split(os.linesep) if line.strip() and 'deprecated' not in line]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = stdout.decode
    @py_assert5 = 'utf-8'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7.replace
    @py_assert12 = os.linesep
    @py_assert14 = '\n'
    @py_assert16 = @py_assert9(@py_assert12, @py_assert14)
    @py_assert1 = expected_output == @py_assert16
    if not @py_assert1:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py17)s\n{%(py17)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.decode\n}(%(py6)s)\n}.replace\n}(%(py13)s\n{%(py13)s = %(py11)s.linesep\n}, %(py15)s)\n}',), (expected_output, @py_assert16)) % {'py2': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5), 'py11': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py0': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = 0
    @py_assert4 = p.returncode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.returncode\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@mark.parametrize('first,second,args,output_prefix', _augment_args(2, [
 (
  True, True, (), ''),
 (True, True, ('--annotation-headers',), '\ntext\n----\n'),
 (False, True, ('--text-tool', 'concrete-python'), ''),
 (False, True, ('--text-tool', 'concrete-python', '--annotation-headers'), '\ntext\n----\n'),
 (True, False, ('--text-tool', 'concrete_serif v3.10.1pre'), ''),
 (True, False, ('--text-tool', 'concrete_serif v3.10.1pre', '--annotation-headers'),
 '\ntext\n----\n')]))
def test_print_multiple_communications(comms_path, first, second, args, output_prefix):
    p = Popen([
     sys.executable, 'scripts/concrete-inspect.py', '--text'] + list(args) + [
     comms_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    expected_output = output_prefix
    if first:
        expected_output += '<DOC id="dog-bites-man" type="other">\n<HEADLINE>\nDog Bites Man\n</HEADLINE>\n<TEXT>\n<P>\nJohn Smith, manager of ACMÉ INC, was bit by a dog on March 10th, 2013.\n</P>\n<P>\nHe died!\n</P>\n<P>\nJohn\'s daughter Mary expressed sorrow.\n</P>\n</TEXT>\n</DOC>\n\n'
    expected_output += output_prefix
    if second:
        expected_output += "Madame Magloire comprit, et elle alla chercher sur la cheminée de la chambre à coucher de monseigneur les deux chandeliers d'argent qu'elle posa sur la table tout allumés.\n\n—Monsieur le curé, dit l'homme, vous êtes bon. Vous ne me méprisez pas. Vous me recevez chez vous. Vous allumez vos cierges pour moi. Je ne vous ai pourtant pas caché d'où je viens et que je suis un homme malheureux.\n\n"
    @py_assert0 = []
    @py_assert3 = [line for line in stderr.decode('utf-8').split(os.linesep) if line.strip() and 'deprecated' not in line]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = stdout.decode
    @py_assert5 = 'utf-8'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7.replace
    @py_assert12 = os.linesep
    @py_assert14 = '\n'
    @py_assert16 = @py_assert9(@py_assert12, @py_assert14)
    @py_assert1 = expected_output == @py_assert16
    if not @py_assert1:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py17)s\n{%(py17)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.decode\n}(%(py6)s)\n}.replace\n}(%(py13)s\n{%(py13)s = %(py11)s.linesep\n}, %(py15)s)\n}',), (expected_output, @py_assert16)) % {'py2': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5), 'py11': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py0': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = 0
    @py_assert4 = p.returncode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.returncode\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@mark.parametrize('first,second,args,output_prefix', _augment_args(2, [
 (
  True, True, (), ''),
 (True, True, ('--annotation-headers',), '\ntext\n----\n'),
 (False, True, ('--text-tool', 'concrete-python'), ''),
 (False, True, ('--text-tool', 'concrete-python', '--annotation-headers'), '\ntext\n----\n'),
 (True, False, ('--text-tool', 'concrete_serif v3.10.1pre'), ''),
 (True, False, ('--text-tool', 'concrete_serif v3.10.1pre', '--annotation-headers'),
 '\ntext\n----\n')]))
def test_print_multiple_communications_tgz(comms_tgz_path, first, second, args, output_prefix):
    p = Popen([
     sys.executable, 'scripts/concrete-inspect.py', '--text'] + list(args) + [
     comms_tgz_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    expected_output = output_prefix
    if first:
        expected_output += '<DOC id="dog-bites-man" type="other">\n<HEADLINE>\nDog Bites Man\n</HEADLINE>\n<TEXT>\n<P>\nJohn Smith, manager of ACMÉ INC, was bit by a dog on March 10th, 2013.\n</P>\n<P>\nHe died!\n</P>\n<P>\nJohn\'s daughter Mary expressed sorrow.\n</P>\n</TEXT>\n</DOC>\n\n'
    expected_output += output_prefix
    if second:
        expected_output += "Madame Magloire comprit, et elle alla chercher sur la cheminée de la chambre à coucher de monseigneur les deux chandeliers d'argent qu'elle posa sur la table tout allumés.\n\n—Monsieur le curé, dit l'homme, vous êtes bon. Vous ne me méprisez pas. Vous me recevez chez vous. Vous allumez vos cierges pour moi. Je ne vous ai pourtant pas caché d'où je viens et que je suis un homme malheureux.\n\n"
    @py_assert0 = []
    @py_assert3 = [line for line in stderr.decode('utf-8').split(os.linesep) if line.strip() and 'deprecated' not in line]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = stdout.decode
    @py_assert5 = 'utf-8'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7.replace
    @py_assert12 = os.linesep
    @py_assert14 = '\n'
    @py_assert16 = @py_assert9(@py_assert12, @py_assert14)
    @py_assert1 = expected_output == @py_assert16
    if not @py_assert1:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py17)s\n{%(py17)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.decode\n}(%(py6)s)\n}.replace\n}(%(py13)s\n{%(py13)s = %(py11)s.linesep\n}, %(py15)s)\n}',), (expected_output, @py_assert16)) % {'py2': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5), 'py11': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py0': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = 0
    @py_assert4 = p.returncode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.returncode\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@mark.parametrize('first,second,third,args,output_prefix', _augment_args(3, [
 (
  True, True, True, (), ''),
 (True, True, True, ('--annotation-headers',), '\nid\n--\n'),
 (False, False, False, ('--count', '0'), ''),
 (False, False, False, ('--count', '0', '--annotation-headers'), '\nid\n--\n'),
 (True, False, False, ('--count', '1'), ''),
 (True, False, False, ('--count', '1', '--annotation-headers'), '\nid\n--\n'),
 (True, True, False, ('--count', '2'), ''),
 (True, True, False, ('--count', '2', '--annotation-headers'), '\nid\n--\n'),
 (True, True, True, ('--count', '3'), ''),
 (True, True, True, ('--count', '3', '--annotation-headers'), '\nid\n--\n')]))
def test_print_multiple_communications_count(simple_comms_tgz_path, first, second, third, args, output_prefix):
    p = Popen([
     sys.executable, 'scripts/concrete-inspect.py', '--id'] + list(args) + [
     simple_comms_tgz_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    expected_output = ''
    if first:
        expected_output += output_prefix
        expected_output += 'one\n'
    if second:
        expected_output += output_prefix
        expected_output += 'two\n'
    if third:
        expected_output += output_prefix
        expected_output += 'three\n'
    @py_assert0 = []
    @py_assert3 = [line for line in stderr.decode('utf-8').split(os.linesep) if line.strip() and 'deprecated' not in line]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = stdout.decode
    @py_assert5 = 'utf-8'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7.replace
    @py_assert12 = os.linesep
    @py_assert14 = '\n'
    @py_assert16 = @py_assert9(@py_assert12, @py_assert14)
    @py_assert1 = expected_output == @py_assert16
    if not @py_assert1:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py17)s\n{%(py17)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.decode\n}(%(py6)s)\n}.replace\n}(%(py13)s\n{%(py13)s = %(py11)s.linesep\n}, %(py15)s)\n}',), (expected_output, @py_assert16)) % {'py2': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py10': @pytest_ar._saferepr(@py_assert9), 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5), 'py11': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py0': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output', 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = 0
    @py_assert4 = p.returncode
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.returncode\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None