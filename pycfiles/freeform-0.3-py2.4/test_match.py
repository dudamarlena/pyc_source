# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/freeform_tests/test_match.py
# Compiled at: 2006-03-28 21:38:29
from heapq import *
from freeform.levenshtein import *
from freeform.match import *
from freeform.formtable import *
from freeform.match import _fieldtype_reprtab
from freeform.levenshtein import _levenshtein_firstcol, _levenshtein_firstrow
from profile_match import profile_match_scentence, format_results
from freeform import levenshtein
import unittest

def _xxx_match_scentence_noplurals(formtable, words):
    """Match a scentence.

    Assumes there are no forms in formtable that use plurals"""
    wordcount = len(words)
    maxfieldcount = formtable['maxfieldcount']
    tymatch = formtable['tymatch']
    tyflags = formtable['tyflags']
    tyformids = formtable['tystartformids']
    tyselects = formtable['tyselects']
    matchfieldforms = formtable['matchfieldforms']
    fieldcount = min(maxfieldcount, wordcount)
    ilastfield = fieldcount - 1
    match = []
    TYEND = -2
    for ifield in range(0, fieldcount):
        candidatenextformids = None
        for (matchfn, selects, formids) in zip(tymatch[:TYEND], tyselects[:TYEND], tyformids[:TYEND]):
            matched = matchfn(selects, words[ifield], ifield, formids)
            if matched:
                match.append(matched)
                if len(matched) > 1:
                    ffs = matchfieldforms.get(matched, [0, [], [], {}])[(-1)].get(ifield, [])
                    formids = [ formid for formid in formids if formid in ffs ]
                candidatenextformids = formids
                if ifield < ilastfield:
                    tyformids = _nextforms(formids, ifield, tyflags)
                break

        if not candidatenextformids:
            match.append(words[ifield])
            candidatenextformids = tyformids[TYEND]
            if ifield < ilastfield:
                tyformids = _nextforms(tyformids[TYEND], ifield, tyflags)
        if not candidatenextformids:
            break

    return (
     match, candidatenextformids)


def debug():
    sources = dict(TestDisambiguation.sources)
    test_inputs = dict(TestDisambiguation.source_tests)
    verbose = False
    while not verbose:
        for (verbose, numruns, profilefile, xmatch_scentence, xformtable_prepare) in [(True, 1, None and 'profile.log', match_scentence, formtable_prepare)]:
            (allsucces, allmsgs) = profile_match_scentence(compile, profilefile, [
             'menu_vs_listmenu', 'disambiguate_on_singular_param_position', 'plural_params_at_arbitrary_positions', 'pylon_session_commands'], sources, test_inputs, numruns, xmatch_scentence, xformtable_prepare)
            print ('\n').join(verbose and allmsgs or allmsgs[-2:])
            if verbose:
                break

    return


class TestCompiler(unittest.TestCase):
    __module__ = __name__

    def test_commandset_construction(self):
        for (sourcename, source) in TestDisambiguation.sources:
            ((commands, forms), brokenforms) = compile([source])
            for (cmd, formids) in commands.items():
                for formid in formids:
                    self.assertEqual(forms[formid][0], cmd)


class TestLevenshtein(unittest.TestCase):
    __module__ = __name__

    def reset_levenshtein(self):
        global _levenshtein_firstcol
        global _levenshtein_firstrow
        levenshtein._levenshtein_maxwordrange = 0
        _levenshtein_firstcol[:] = []
        _levenshtein_firstrow[:] = []

    def setUp(self):
        self.reset_levenshtein()

    def test_firstinit(self):
        fcolcache = _levenshtein_firstcol
        frowcache = _levenshtein_firstrow

        def maxwordlen():
            return max(len(fcolcache), len(frowcache))

        self.assertEqual(levenshtein_distance('foobar', 'foobar'), 0, 'warmup: LD(foobar,foobar) == 0')
        self.assertEqual(maxwordlen(), len('foobar') + 1)
        self.assertNotEqual(levenshtein_distance('foobarfoobar', 'foobar'), 0)
        self.assertEqual(maxwordlen(), len('foobarfoobar') + 1)
        idoffirstelement = id(_levenshtein_firstrow[0])
        self.assertNotEqual(levenshtein_distance('foobar', 'foobarfoobar'), 0)
        self.assertEqual(maxwordlen(), len('foobarfoobar') + 1)
        self.assertEqual(idoffirstelement, id(_levenshtein_firstrow[0]), '[issue:optimization] initial row data is being rebuilt un-necessarily')

    def test_levenshtein_selectfrom(self):
        (i, d) = levenshtein_selectone(['apple', 'apple', 'apple'], 'param')
        self.assertEqual((-1, LEVENSHTEIN_DEFAULT_MAXDIST), (i, d))
        (i, d) = levenshtein_selectone(['aabaa', 'aacaa', 'aadaa'], 'aaaaa')
        self.assertEqual((i, d), (0, 1))
        (i, d) = levenshtein_selectone(['apple', 'pear', 'orange'], 'orange')
        self.assertEqual((i, d), (2, 0))
        (i, d) = levenshtein_selectone(['aaaaa', 'aabaa', 'aaaaa'], 'aaaaa')
        self.assertEqual((i, d), (0, 0))
        (i, d) = levenshtein_selectone(['apple', 'pear', 'orange'], 'apple')
        self.assertEqual(i, 0)
        self.assertEqual(d, 0)
        self.assertEqual(d, levenshtein_distance('apple', 'apple'))
        (i, d) = levenshtein_selectone(['apple', 'pear', 'orange'], 'orange')
        self.assertEqual(i, 2)
        self.assertEqual(d, 0)
        self.assertEqual(d, levenshtein_distance('orange', 'orange'))
        (i, d) = levenshtein_selectone(['apple', 'pear', 'orange'], 'pear')
        self.assertEqual(i, 1)
        self.assertEqual(d, 0)
        self.assertEqual(d, levenshtein_distance('pear', 'pear'))
        for (x, (from_, match)) in enumerate([(['aaaaa', 'baaaa', 'caaaa'], 'aaaaa'), (['aaaaa', 'baaaa', 'caaaa'], 'baaaa'), (['aaaaa', 'baaaa', 'caaaa'], 'caaaa'), (['aaaaa', 'aaaab', 'aaaac'], 'aaaaa'), (['aaaaa', 'aaaab', 'aaaac'], 'aaaab'), (['aaaaa', 'aaaab', 'aaaac'], 'aaaac')]):
            (i, d) = levenshtein_selectone(from_, match)
            self.assertEqual(i, x % 3)
            self.assertEqual(d, levenshtein_distance(from_[(x % 3)], match))

        (i, d) = levenshtein_selectone(['apple', 'pear', 'orange'], 'paple')
        self.assertEqual(i, 0)
        self.assertEqual(d, 2)
        self.assertEqual(d, levenshtein_distance('apple', 'paple'))
        (i, d) = levenshtein_selectone(['apple', 'pear', 'orange'], 'roange')
        self.assertEqual(i, 2)
        self.assertEqual(d, 2)
        self.assertEqual(d, levenshtein_distance('orange', 'roange'))
        (i, d) = levenshtein_selectone(['apple', 'pear', 'orange'], 'epar')
        self.assertEqual(i, 1)
        self.assertEqual(d, 2)
        self.assertEqual(d, levenshtein_distance('pear', 'epar'))
        (i, d) = levenshtein_selectone(['apple', 'pear', 'orange'], 'appel')
        self.assertEqual(i, 0)
        self.assertEqual(d, 2)
        self.assertEqual(d, levenshtein_distance('apple', 'appel'))
        (i, d) = levenshtein_selectone(['apple', 'pear', 'orange'], 'oraneg')
        self.assertEqual(i, 2)
        self.assertEqual(d, 2)
        self.assertEqual(d, levenshtein_distance('orange', 'oraneg'))
        (i, d) = levenshtein_selectone(['apple', 'pear', 'orange'], 'pera')
        self.assertEqual(i, 1)
        self.assertEqual(d, 2)
        self.assertEqual(d, levenshtein_distance('pear', 'pera'))

    def test_levenshtein_selectfrom_reentry(self):
        asequence = ['apple', 'apple', 'apple']
        state = _levenshtein_select(asequence, 'appel')
        htop = heappop(state[1])
        i, d = htop[(-1)], htop[0]
        self.assertEqual((0, 2), (i, d))
        state = _levenshtein_select(asequence, 'appel', None, 0, 0, state)
        htop = heappop(state[1])
        i, d = htop[(-1)], htop[0]
        self.assertEqual((1, 2), (i, d))
        self.assertRaises(IndexError, _levenshtein_select, asequence, 'appel', None, 0, 0, state)
        return


class TestDisambiguation(unittest.TestCase):
    __module__ = __name__

    def _generic_source_tests(self, name, compiler=None):
        compiler = compiler or self.compiler
        msgs = []
        results = []
        (commandforms, e) = compiler([self.sources[name]])
        formtable = create_formtable(*commandforms)
        self.assert_(not e, ('\n').join(e))
        formtable = formtable_prepare(formtable)
        results = []
        for (input, expect) in self.source_tests[name]:
            words = input.split()
            (match, productions) = match_scentence(formtable, words)
            results.append((words, expect, match, productions))

        (success, msg) = self._process_match_results(formtable, results)
        return (success, msg)

    def setUp(self):
        self.compiler = compile
        self.sources = dict(self.sources)
        self.source_tests = dict(self.source_tests)

    def test_token_const_assumptions(self):
        for i in range(0, max(_fieldtype_reprtab.keys()) + 1):
            self.assertEqual(_fieldtype_reprtab.has_key(i), True)

    def _process_match_results(self, formtable, results):
        return format_results(formtable, results)

    def test_menu_precedence_trumps_listmenu(self):
        (success, msg) = self._generic_source_tests('menu_vs_listmenu')
        self.assert_(success, msg)

    def test_singular_param_disambiguation(self):
        (success, msg) = self._generic_source_tests('disambiguate_on_singular_param_position')
        self.assert_(success, msg)

    def test_plural_params_at_arbitrary_positions(self):
        (success, msg) = self._generic_source_tests('plural_params_at_arbitrary_positions')
        self.assert_(success, msg)

    source_tests = [
     (
      'menu_vs_listmenu', [('apple pear a bannana e', [('cmd_m', ['apple', 'pear', 'a', 'bannana', 'e']), ('cmd_lm', ['apple', 'pear', 'a', 'bannana', 'e'])]), ('apple pear carrot bannana e', ('cmd_lm', ['apple', 'pear', 'carrot', 'bannana', 'e'])), ('apple pear carrot bannana pepper', ['cmd_lm', 'cmd_lm2']), ('apple pear a bannana pepper', 'cmd_lm'), ('apple pear y bannana pepper', 'cmd_lm2')]), ('disambiguate_on_singular_param_position', [('apple pear a bannana e', [('cmd_e', ['apple', 'pear', 'a', 'bannana', 'e']), ('cmd_g', ['apple', 'pear', 'a', 'bannana', 'e'])]), ('parsnip apple pear e bannana', 'cmd_h'), ('apple pear param_a param_b bannana param_c', ('cmd_a', ['apple', 'pear', 'param_a', 'param_b', 'bannana', 'param_c'])), ('apple param_a pear param_b bannana param_c', ''), ('apple param_a pear param_b param_c bannana', ('cmd_c', ['apple', 'param_a', 'pear', 'param_b', 'param_c', 'bannana'])), ('apple pear param_a bannana param_b param_c', ('cmd_d', ['apple', 'pear', 'param_a', 'bannana', 'param_b', 'param_c'])), ('param_a apple pear param_b param_c bannana', ('cmd_b', ['param_a', 'apple', 'pear', 'param_b', 'param_c', 'bannana'])), ('param_a apple pear carrot param_c bannana', ('cmd_i', ['param_a', 'apple', 'pear', 'carrot', 'param_c', 'bannana'])), ('parsnip apple pear x bannana', '')]), ('plural_params_at_arbitrary_positions', [('apple pear param_a param_b bannana foo bar bannana bannana', ('cmd_a', ['apple', 'pear', 'param_a', 'param_b', 'bannana', ['foo', 'bar', 'bannana', 'bannana']])), ('apple pear param_a param_b foo bar bannana', ('cmd_b', ['apple', 'pear', 'param_a', 'param_b', ['foo', 'bar'], 'bannana'])), ('param_a apple pear param_b foo bar bannana bannana', ('cmd_c', ['param_a', 'apple', 'pear', 'param_b', ['foo', 'bar', 'bannana'], 'bannana'])), ('param_a apple pear param_b foo bar bannana bannana', ('cmd_c', ['param_a', 'apple', 'pear', 'param_b', ['foo', 'bar', 'bannana'], 'bannana'])), ('param_a apple pear param_b foo bar bannana baz bannana', ('cmd_c', ['param_a', 'apple', 'pear', 'param_b', ['foo', 'bar', 'bannana', 'baz'], 'bannana'])), ('param_a bannana pear param_b foo bar apple param_d orrange', ('cmd_e', ['param_a', 'bannana', 'pear', 'param_b', ['foo', 'bar'], 'apple', 'param_d', 'orrange'])), ('param_a bannana pear param_b foo bar apple baz apple param_d orrange', ('cmd_e', ['param_a', 'bannana', 'pear', 'param_b', ['foo', 'bar', 'apple', 'baz'], 'apple', 'param_d', 'orrange']))]), ('pylon_session_commands', [('create account bakdog bakdog password', ('create_named_account', ['create', 'account', 'bakdog', 'bakdog', 'password']))])]
    sources = [
     (
      'menu_vs_listmenu', 'cmd_m: apple pear {menu_a(menu abcd)} bannana {menu_b(menu efgh)};cmd_lm: apple pear {listmenu_a(list potatoe,carrot,turnip,parsnip. menu abcd)} bannana {listmenu_b(list salt,sugar,thyme,pepper. menu efgh)};cmd_lm2: apple pear {listmenu_a(list potator,carrot,turnip,parsnip. menu xyzw)} bannana {listmenu_b(list salt,sugar,thyme,pepper. menu lmno)};'), ('disambiguate_on_singular_param_position', 'cmd_a: apple pear {param_a} {param_b} bannana {param_c};cmd_b: {param_a} apple pear {param_b} {param_c} bannana;cmd_c: apple {param_a} pear {param_b} {param_c} bannana;cmd_d: apple pear {param_a} bannana {param_b} {param_c};cmd_e: apple pear {menu_a(menu abcd)} bannana {menu_b(menu efgh)};cmd_f: {menu_a(menu abcd)} apple pear {menu_b(menu efgh)} bannana;cmd_g: apple pear {listmenu_a(list potatoe,carrot,turnip,parsnip. menu abcd)} bannana {listmenu_b(list salt,sugar,thyme,pepper. menu efgh)};cmd_h: {listmenu_a(list potatoe,carrot,turnip,parsnip. menu abcd)} apple pear {listmenu_b(list salt,sugar,thyme,pepper. menu efgh)} bannana;\ncmd_i: {param_a} apple pear {list_a(list potatoe,carrot,turnip,parsnip.)} {param_c} bannana;'), ('pylon_session_commands', 'login: login {displayname} {password};\ncreate_named_account: create account {displayname} {password} {password_confirm};\ncreate_acccount_default_name: create account {password} {password_confirm};'), ('plural_params_at_arbitrary_positions', 'cmd_a: apple pear {param_a} {param_b} bannana {param_c(s)};\ncmd_b: apple pear {param_a} {param_b} {param_c(s)} bannana;\ncmd_c: {param_a} apple pear {param_b} {param_c(s)} bannana;\ncmd_d: {param_a} pear apple {param_b(s)} {param_c} bannana;\ncmd_e: {param_a} bannana pear {param_b} {param_c(s)} apple {param_d} orrange;\ncmd_f: {param_a} bannana apple {param_b(s)} {param_c} pear {param_d} orrange;\ncmd_g: {param_a} pear bannana {param_b} {param_c(s)} apple {param_d} orrange;\ncmd_h: {param_a} pear bannana {param_b(s)} {param_c} apple {param_d} orrange;')]


if __name__ == '__main__':
    from os import environ
    if environ.get('FREEFORM_DEBUG', None):
        import wingdbstub
        debug()
    else:
        unittest.main()