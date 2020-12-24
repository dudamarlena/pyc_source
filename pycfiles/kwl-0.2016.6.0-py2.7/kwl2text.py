# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/kwl2text/kwl2text.py
# Compiled at: 2016-06-22 18:24:58
from __future__ import print_function, division, absolute_import, unicode_literals
from grako.parsing import graken, Parser
from grako.util import re, RE_FLAGS
__version__ = (
 2016, 6, 22, 22, 24, 58, 2)
__all__ = [
 b'kwl2textParser',
 b'kwl2textSemantics',
 b'main']

class kwl2textParser(Parser):

    def __init__(self, whitespace=None, nameguard=None, comments_re=None, eol_comments_re=None, ignorecase=None, left_recursion=True, **kwargs):
        super(kwl2textParser, self).__init__(whitespace=whitespace, nameguard=nameguard, comments_re=comments_re, eol_comments_re=eol_comments_re, ignorecase=ignorecase, left_recursion=left_recursion, **kwargs)

    @graken()
    def _kwl2text_(self):
        self._token(b'<kwl')

        def block1():
            self._sentence_()
            self._token(b';')

        self._closure(block1)
        self.ast[b'@'] = self.last_node
        with self._optional():
            self._token(b'kwl>')

    @graken()
    def _sentence_(self):
        with self._choice():
            with self._option():
                self._formatted_()
            with self._option():
                self._command_()
            with self._option():
                self._question_()
            with self._option():
                self._statement_()
            with self._option():
                self._expression_()
            self._error(b'no available options')

    @graken()
    def _formatted_(self):
        self._sentence_formatting_()
        self.ast[b'@'] = self.last_node
        self._token(b'(')
        self._expression_()
        self.ast[b'@'] = self.last_node
        self._token(b')')

    @graken()
    def _sentence_formatting_(self):
        self._token(b'headline')

    @graken()
    def _statement_(self):
        self._expression_()
        self.ast[b'@'] = self.last_node
        self._token(b'.')

    @graken()
    def _command_(self):
        self._expression_()
        self.ast[b'@'] = self.last_node
        self._token(b'!')

    @graken()
    def _question_(self):
        self._expression_()
        self.ast[b'@'] = self.last_node
        self._token(b'?')

    @graken()
    def _expression_(self):
        with self._choice():
            with self._option():
                self._conjunction_()
                self._join_()
                self._conjunction_()
            with self._option():
                self._conjunction_()
            self._error(b'no available options')

    @graken()
    def _conjunction_(self):
        with self._choice():
            with self._option():
                self._clause_()
                self._join_()
                self._clause_()
            with self._option():
                self._token(b'if')
                self._clause_()
                self.ast[b'@'] = self.last_node
                self._token(b'then')
                self.ast[b'@'] = self.last_node
                self._clause_()
                self.ast[b'@'] = self.last_node
            with self._option():
                self._clause_()
            self._error(b'no available options')

    @graken()
    def _clause_(self):
        with self._choice():
            with self._option():
                self._subject_verb_object_()
            with self._option():
                self._subject_verb_()
            with self._option():
                self._verb_object_()
            with self._option():
                self._group_()
            self._error(b'no available options')

    @graken()
    def _subject_verb_object_(self):
        self._group_()
        self.ast[b'subject'] = self.last_node
        self._action_()
        self.ast[b'verb'] = self.last_node
        self._group_()
        self.ast[b'object'] = self.last_node
        self.ast._define([
         b'subject', b'verb', b'object'], [])

    @graken()
    def _subject_verb_(self):
        self._group_()
        self.ast[b'subject'] = self.last_node
        self._action_()
        self.ast[b'verb'] = self.last_node
        self.ast._define([
         b'subject', b'verb'], [])

    @graken()
    def _verb_object_(self):
        self._action_()
        self.ast[b'verb'] = self.last_node
        self._group_()
        self.ast[b'object'] = self.last_node
        self.ast._define([
         b'verb', b'object'], [])

    @graken()
    def _group_(self):
        with self._choice():
            with self._option():
                self._token(b'{')
                self._single_()
                self.ast[b'@'] = self.last_node
                self._token(b'}')
            with self._option():
                self._single_()
            with self._option():
                self._token(b'{')
                self._conjunction_()
                self.ast[b'@'] = self.last_node
                self._token(b'}')
            self._error(b'no available options')

    @graken()
    def _single_(self):
        with self._choice():
            with self._option():
                self._methods_()
            with self._option():
                self._triple_phrase_()
            with self._option():
                self._tuple_kwl_()
            with self._option():
                self._entry_()
            with self._option():
                self._raw_()
            self._error(b'no available options')

    @graken()
    def _action_(self):
        with self._choice():
            with self._option():
                self._token(b'{')
                self._action_()
                self.ast[b'@'] = self.last_node
                self._token(b'}')
            with self._option():
                self._conjugated_verb_()
            with self._option():
                self._tuple_verb_()
            with self._option():
                self._verb_()
            self._error(b'no available options')

    @graken()
    def _conjugated_verb_(self):
        with self._choice():
            with self._option():
                self._tenses_()
                self.ast[b'@'] = self.last_node
                self._token(b'(')
                self._conjugations_()
                self.ast[b'@'] = self.last_node
                self._token(b'(')
                self._verb_()
                self.ast[b'@'] = self.last_node
                self._token(b'))')
            with self._option():
                self._tenses_()
                self.ast[b'@'] = self.last_node
                self._token(b'(')
                self._conjugations_()
                self.ast[b'@'] = self.last_node
                self._token(b'(')
                self._tuple_verb_()
                self.ast[b'@'] = self.last_node
                self._token(b'))')
            self._error(b'no available options')

    @graken()
    def _tuple_verb_(self):
        self._verb_()
        self.ast[b'@'] = self.last_node
        self._token(b'_')
        self._adverb_()
        self.ast[b'@'] = self.last_node

    @graken()
    def _methods_(self):
        with self._choice():
            with self._option():
                self._modifiers_()
                self.ast[b't'] = self.last_node
                self._token(b'(')
                self._methods_()
                self.ast[b'v'] = self.last_node
                self._token(b')')
            with self._option():
                self._modifiers_()
                self.ast[b't'] = self.last_node
                self._token(b'(')
                self._triple_phrase_()
                self.ast[b'v'] = self.last_node
                self._token(b')')
            with self._option():
                self._modifiers_()
                self.ast[b't'] = self.last_node
                self._token(b'(')
                self._tuple_kwl_()
                self.ast[b'v'] = self.last_node
                self._token(b')')
            with self._option():
                self._modifiers_()
                self.ast[b't'] = self.last_node
                self._token(b'(')
                self._entry_()
                self.ast[b'v'] = self.last_node
                self._token(b')')
            with self._option():
                self._modifiers_()
                self.ast[b't'] = self.last_node
                self._token(b'(')
                self._raw_()
                self.ast[b'v'] = self.last_node
                self._token(b')')
            self._error(b'no available options')
        self.ast._define([
         b't', b'v'], [])

    @graken()
    def _triple_phrase_(self):
        self._entry_()
        self.ast[b'@'] = self.last_node
        self._token(b'(')
        self._tuple_kwl_()
        self.ast[b'@'] = self.last_node
        self._token(b')')

    @graken()
    def _tuple_kwl_(self):
        with self._choice():
            with self._option():
                self._entry_()
                self.ast[b'@'] = self.last_node
                self._token(b'_')
                self._entry_()
                self.ast[b'@'] = self.last_node
            with self._option():
                self._entry_()
                self.ast[b'@'] = self.last_node
                self._token(b'_')
                self._raw_()
                self.ast[b'@'] = self.last_node
            self._error(b'no available options')

    @graken()
    def _modifiers_(self):
        with self._choice():
            with self._option():
                self._partofspeech_()
            with self._option():
                self._conjugations_()
            with self._option():
                self._prepositions_()
            with self._option():
                self._tenses_()
            with self._option():
                self._token(b'plural')
            with self._option():
                self._formatting_()
            self._error(b'expecting one of: plural')

    @graken()
    def _formatting_(self):
        with self._choice():
            with self._option():
                self._token(b'defn')
            with self._option():
                self._token(b'quote')
            with self._option():
                self._token(b'sample')
            with self._option():
                self._token(b'title')
            self._error(b'expecting one of: defn quote sample title')

    @graken()
    def _join_(self):
        with self._choice():
            with self._option():
                self._token(b':')
            with self._option():
                self._token(b',')
            with self._option():
                self._token(b'and')
            with self._option():
                self._token(b'because')
            with self._option():
                self._token(b'but')
            with self._option():
                self._token(b'of')
            with self._option():
                self._token(b'or')
            with self._option():
                self._token(b'so')
            with self._option():
                self._token(b'then')
            with self._option():
                self._token(b'when')
            self._error(b'expecting one of: , : and because but of or so then when')

    @graken()
    def _conjugations_(self):
        with self._choice():
            with self._option():
                self._token(b'f')
            with self._option():
                self._token(b'i')
            with self._option():
                self._token(b'je')
            with self._option():
                self._token(b'm')
            with self._option():
                self._token(b'tu')
            with self._option():
                self._token(b'il')
            with self._option():
                self._token(b'elle')
            with self._option():
                self._token(b'nous')
            with self._option():
                self._token(b'vous')
            with self._option():
                self._token(b'ils')
            with self._option():
                self._token(b'elles')
            self._error(b'expecting one of: elle elles f i il ils je m nous tu vous')

    @graken()
    def _prepositions_(self):
        with self._choice():
            with self._option():
                self._token(b'at')
            with self._option():
                self._token(b'for')
            with self._option():
                self._token(b'from')
            with self._option():
                self._token(b'in')
            with self._option():
                self._token(b'of')
            with self._option():
                self._token(b'like')
            with self._option():
                self._token(b'on')
            with self._option():
                self._token(b'to')
            self._error(b'expecting one of: at for from in like of on to')

    @graken()
    def _tenses_(self):
        with self._choice():
            with self._option():
                self._token(b'cmd')
            with self._option():
                self._token(b'done_tdy')
            with self._option():
                self._token(b'done_tmw')
            with self._option():
                self._token(b'done_ydy')
            with self._option():
                self._token(b'inf')
            with self._option():
                self._token(b'may')
            with self._option():
                self._token(b'not_tdy')
            with self._option():
                self._token(b'not_tmw')
            with self._option():
                self._token(b'not_ydy')
            with self._option():
                self._token(b'now_tdy')
            with self._option():
                self._token(b'now_tmw')
            with self._option():
                self._token(b'now_ydy')
            with self._option():
                self._token(b'tdy')
            with self._option():
                self._token(b'tmw')
            with self._option():
                self._token(b'ydy')
            self._error(b'expecting one of: cmd done_tdy done_tmw done_ydy inf may not_tdy not_tmw not_ydy now_tdy now_tmw now_ydy tdy tmw ydy')

    @graken()
    def _adjective_(self):
        self._token(b'adj')
        self.ast[b't'] = self.last_node
        self._token(b':')
        self._token_()
        self.ast[b'v'] = self.last_node
        self.ast._define([
         b't', b'v'], [])

    @graken()
    def _adverb_(self):
        self._token(b'adv')
        self.ast[b't'] = self.last_node
        self._token(b':')
        self._token_()
        self.ast[b'v'] = self.last_node
        self.ast._define([
         b't', b'v'], [])

    @graken()
    def _determiner_(self):
        self._token(b'det')
        self.ast[b't'] = self.last_node
        self._token(b':')
        self._token_()
        self.ast[b'v'] = self.last_node
        self.ast._define([
         b't', b'v'], [])

    @graken()
    def _noun_(self):
        self._token(b'nom')
        self.ast[b't'] = self.last_node
        self._token(b':')
        self._token_()
        self.ast[b'v'] = self.last_node
        self.ast._define([
         b't', b'v'], [])

    @graken()
    def _possessive_(self):
        self._token(b'pos')
        self.ast[b't'] = self.last_node
        self._token(b':')
        self._token_()
        self.ast[b'v'] = self.last_node
        self.ast._define([
         b't', b'v'], [])

    @graken()
    def _preposition_(self):
        self._token(b'pre')
        self.ast[b't'] = self.last_node
        self._token(b':')
        self._token_()
        self.ast[b'v'] = self.last_node
        self.ast._define([
         b't', b'v'], [])

    @graken()
    def _pronoun_(self):
        self._token(b'pro')
        self.ast[b't'] = self.last_node
        self._token(b':')
        self._token_()
        self.ast[b'v'] = self.last_node
        self.ast._define([
         b't', b'v'], [])

    @graken()
    def _raw_(self):
        with self._choice():
            with self._option():
                self._pattern(b'raw\\((.*?)\\)')
            with self._option():
                self._pattern(b'date\\((.*?)\\)')
            self._error(b'expecting one of: date\\((.*?)\\) raw\\((.*?)\\)')

    @graken()
    def _verb_(self):
        self._token(b'act')
        self.ast[b't'] = self.last_node
        self._token(b':')
        self._token_()
        self.ast[b'v'] = self.last_node
        self.ast._define([
         b't', b'v'], [])

    @graken()
    def _entry_(self):
        self._partofspeech_()
        self.ast[b't'] = self.last_node
        self._token(b':')
        self._token_()
        self.ast[b'v'] = self.last_node
        self.ast._define([
         b't', b'v'], [])

    @graken()
    def _partofspeech_(self):
        with self._choice():
            with self._option():
                self._token(b'act')
            with self._option():
                self._token(b'adj')
            with self._option():
                self._token(b'adv')
            with self._option():
                self._token(b'det')
            with self._option():
                self._token(b'exc')
            with self._option():
                self._token(b'kg')
            with self._option():
                self._token(b'nom')
            with self._option():
                self._token(b'pos')
            with self._option():
                self._token(b'pre')
            with self._option():
                self._token(b'pro')
            with self._option():
                self._token(b'sci')
            self._error(b'expecting one of: act adj adv det exc kg nom pos pre pro sci')

    @graken()
    def _token_(self):
        self._pattern(b'[a-zA-Z0-9#\\-]*')


class kwl2textSemantics(object):

    def kwl2text(self, ast):
        return ast

    def sentence(self, ast):
        return ast

    def formatted(self, ast):
        return ast

    def sentence_formatting(self, ast):
        return ast

    def statement(self, ast):
        return ast

    def command(self, ast):
        return ast

    def question(self, ast):
        return ast

    def expression(self, ast):
        return ast

    def conjunction(self, ast):
        return ast

    def clause(self, ast):
        return ast

    def subject_verb_object(self, ast):
        return ast

    def subject_verb(self, ast):
        return ast

    def verb_object(self, ast):
        return ast

    def group(self, ast):
        return ast

    def single(self, ast):
        return ast

    def action(self, ast):
        return ast

    def conjugated_verb(self, ast):
        return ast

    def tuple_verb(self, ast):
        return ast

    def methods(self, ast):
        return ast

    def triple_phrase(self, ast):
        return ast

    def tuple_kwl(self, ast):
        return ast

    def modifiers(self, ast):
        return ast

    def formatting(self, ast):
        return ast

    def join(self, ast):
        return ast

    def conjugations(self, ast):
        return ast

    def prepositions(self, ast):
        return ast

    def tenses(self, ast):
        return ast

    def adjective(self, ast):
        return ast

    def adverb(self, ast):
        return ast

    def determiner(self, ast):
        return ast

    def noun(self, ast):
        return ast

    def possessive(self, ast):
        return ast

    def preposition(self, ast):
        return ast

    def pronoun(self, ast):
        return ast

    def raw(self, ast):
        return ast

    def verb(self, ast):
        return ast

    def entry(self, ast):
        return ast

    def partofspeech(self, ast):
        return ast

    def token(self, ast):
        return ast


def main(filename, startrule, trace=False, whitespace=None, nameguard=None):
    import json
    with open(filename) as (f):
        text = f.read()
    parser = kwl2textParser(parseinfo=False)
    ast = parser.parse(text, startrule, filename=filename, trace=trace, whitespace=whitespace, nameguard=nameguard)
    print(b'AST:')
    print(ast)
    print()
    print(b'JSON:')
    print(json.dumps(ast, indent=2))
    print()


if __name__ == b'__main__':
    import argparse, string, sys

    class ListRules(argparse.Action):

        def __call__(self, parser, namespace, values, option_string):
            print(b'Rules:')
            for r in kwl2textParser.rule_list():
                print(r)

            print()
            sys.exit(0)


    parser = argparse.ArgumentParser(description=b'Simple parser for kwl2text.')
    parser.add_argument(b'-l', b'--list', action=ListRules, nargs=0, help=b'list all rules and exit')
    parser.add_argument(b'-n', b'--no-nameguard', action=b'store_true', dest=b'no_nameguard', help=b"disable the 'nameguard' feature")
    parser.add_argument(b'-t', b'--trace', action=b'store_true', help=b'output trace information')
    parser.add_argument(b'-w', b'--whitespace', type=str, default=string.whitespace, help=b'whitespace specification')
    parser.add_argument(b'file', metavar=b'FILE', help=b'the input file to parse')
    parser.add_argument(b'startrule', metavar=b'STARTRULE', help=b'the start rule for parsing')
    args = parser.parse_args()
    main(args.file, args.startrule, trace=args.trace, whitespace=args.whitespace, nameguard=not args.no_nameguard)