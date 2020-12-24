# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/ask/views/parse_definitions.py
# Compiled at: 2014-08-27 19:26:12
from itertools import groupby
from ask.models import ChoiceSet
from ask.models import Question
from ask.models.fields import FIELD_NAMES
from django.core.exceptions import ValidationError
from signalbox.models import ScoreSheet
from signalbox.utilities.djangobits import get_or_modify, flatten
from stats import stats
import yaml
from signalbox.utilities.gibberish import random_stata_varname
from pyparsing import *
blockstart = Suppress(Literal('~') * 3 + ZeroOrMore(Literal('~')))
attrword = Word(('').join([ i for i in set(printables) - set('<>{}~=()') ]))
classword = Literal('.').suppress() + attrword
DEFIDSTRING = '__ID__REPLACE__ME__'
iden = Optional(Literal('#').suppress() + attrword, default=DEFIDSTRING)('iden')
iden.setParseAction(lambda s, loc, toks: toks[0] != DEFIDSTRING and toks[0] or random_stata_varname())
_keyval = Group(attrword('key') + Literal('=').suppress() + (dblQuotedString.setParseAction(removeQuotes) | attrword)('val'))
header = Literal('{').suppress() + iden + ZeroOrMore(classword)('classes') + ZeroOrMore(_keyval)('keyvals').setParseAction(lambda t: {k:v for k, v in t}) + Literal('}').suppress()
hiddenLiteral = lambda x: Literal(x).suppress()
_choice = Optional(Literal('*')('isdefault'), default='') + Word(nums)('score') + Optional(hiddenLiteral('[') + Word(nums)('mapped_score') + hiddenLiteral(']')) + Literal('=').suppress() + SkipTo(LineEnd().suppress())('label').setParseAction(lambda t: t[0].strip())
code = SkipTo(Literal('>>>').suppress() | Literal('~~~').suppress())
_choice.setParseAction(lambda t: {'score': t.score, 'label': t.label, 'isdefault': bool(t.isdefault), 
   'mapped_score': t.mapped_score or t.score})
choices = Suppress(Literal('>>>')) + ZeroOrMore(_choice) + Literal('~~~').suppress()
_functions = oneOf('min max mean sum')
variable = attrword('variable_name')
function = oneOf('sum min max')
expr = function('function') + Literal('(').suppress() + Group(OneOrMore(variable))('variables') + Literal(')').suppress()
calculated_score = Suppress(Literal('>>>')) + attrword('name') + Literal('<-').suppress() + expr('expression')
page = LineStart() + Suppress(Literal('#')) + ZeroOrMore(Word(alphanums))('step_name') + LineEnd()
block = blockstart + header + code('code') + Optional(choices('choices') | calculated_score('calculated_score')) | page
_yaml_header_start = Literal('-').suppress() * 3 + Optional(ZeroOrMore(Literal('-'))).suppress()
yaml_header = _yaml_header_start + SkipTo(Literal('---') | Literal('...'))('yaml')
ispage = lambda x: bool(x.step_name)
isnotpage = lambda x: not ispage(x)

def make_question_dict(blockParseResult):
    """Make a dictionary from a pyparsing parseResult question.

    :param blockParseResult: A parseResult
    :rtype: dict

    """
    qytypeclasslist = [ i for i in blockParseResult.classes if i in FIELD_NAMES ]
    d = {'variable_name': blockParseResult.iden.strip(), 
       'text': blockParseResult.code.strip(), 
       'q_type': qytypeclasslist and qytypeclasslist[0] or 'instruction'}
    if blockParseResult.choices:
        numbereddict = {k:v for k, v in enumerate(blockParseResult.choices.asList())}
        yamlstring = yaml.safe_dump(numbereddict)
        d.update({'choiceset': get_or_modify(ChoiceSet, {'name': d['variable_name']}, {'yaml': yamlstring})[0]})
    keyvals = blockParseResult.keyvals or {}
    classlist = blockParseResult.classes and blockParseResult.classes.asList()
    d.update({'extra_attrs': {k:v for k, v in keyvals.items()}})
    d.update({'extra_attrs': {k:v for k, v in keyvals.items()}})
    d['extra_attrs'].update({'classes': {k:True for k in classlist}})
    d.update({'required': 'required' in classlist})
    return d


def add_scoresheet_to_question(question, parseResult):
    cs = parseResult.calculated_score
    if cs:
        variables = Question.objects.filter(variable_name__in=cs.variables.asList())
        if len(variables) != len(cs.variables.asList()):
            raise ValidationError(('Not all variables from scoresheet ({}) were matched.').format(cs.name))
        ss, _ = get_or_modify(ScoreSheet, {'name': cs.name}, {'function': cs.function})
        ss.save()
        [ ss.variables.add(i) for i in variables ]
        ss.save()
        question.scoresheet = ss
        question.save()


def make_page_dict(blockParseResult):
    """Make a dictionary from a pyparsing parseResult question.

    :param blockParseResult: A parseResult
    :rtype: dict

    """
    d = {'step_name': (' ').join(blockParseResult.step_name.asList())}
    return d