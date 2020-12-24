# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/code/yaml.py
# Compiled at: 2019-10-21 21:28:14
# Size of source mod 2**32: 2634 bytes
"""Load the raw YAML"""
from typing import Tuple, List
from ruamel.yaml import YAML
from ruamel.yaml.parser import ParserError
from ruamel.yaml.scanner import ScannerError
from ruamel.yaml.composer import ComposerError
from ruamel.yaml.compat import StringIO
from langserver.lspobjects import Diagnostic, DiagnosticSeverity, Range, Position
import logging
logger = logging.getLogger(__name__)
_yaml_loader = YAML(typ='rt')
_yaml_loader.allow_duplicate_keys = True
fast_load = YAML(typ='safe')
fast_load.indent(mapping=2, sequence=4, offset=2)
fast_load.default_flow_style = False

def fast_yaml_load(txt):
    try:
        return fast_load.load(txt)
    except (ParserError, ScannerError) as e:
        try:
            pass
        finally:
            e = None
            del e


def yaml_to_string(v: dict):
    s = StringIO()
    fast_load.dump(v, s)
    return s.getvalue()


def parse_yaml(text, retries=3) -> Tuple[(dict, List[Diagnostic])]:
    problems = []
    try:
        cwl = _yaml_loader.load(text)
    except (ParserError, ScannerError, ComposerError) as e:
        try:
            if retries:
                if e.problem == "could not find expected ':'":
                    return parse_yaml(heal_incomplete_key(text, e), retries - 1)
                if e.problem == 'mapping values are not allowed here':
                    return parse_yaml(heal_incomplete_key_typeB(text, e), retries - 1)
            cwl = None
            problems = [
             Diagnostic(_range=Range(start=(Position(e.problem_mark.line, e.problem_mark.column)), end=(Position(e.problem_mark.line, e.problem_mark.column))),
               message=(str(e)),
               severity=(DiagnosticSeverity.Error),
               code='YAML err',
               source='Benten')]
        finally:
            e = None
            del e

    return (
     cwl, problems)


def heal_incomplete_key(original_text, e):
    logger.debug('Attempting to heal incomplete key')
    lines = original_text.splitlines(keepends=False)
    lines[e.context_mark.line] = lines[e.context_mark.line] + ':'
    return '\n'.join(lines)


def heal_incomplete_key_typeB(original_text, e):
    logger.debug('Attempting to heal incomplete key')
    lines = original_text.splitlines(keepends=False)
    ln = e.problem_mark.line - 1
    while ln > 0 and len(lines[ln].strip()) == 0:
        ln -= 1

    if len(lines[ln]):
        lines[ln] = lines[ln] + ':'
    return '\n'.join(lines)