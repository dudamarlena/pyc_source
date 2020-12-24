# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Python\enigmapad\pyhinavrophonetic\hinavro.py
# Compiled at: 2016-09-14 06:13:39
"""Python implementation of Avro Phonetic in hindi.

-------------------------------------------------------------------------------
Copyright (C) 2016 Subrata Sarkar <subrotosarkar32@gmail.com>
modified by:- Subrata Sarkar <subrotosarkar32@gmail.com>
original by:- Kaustav Das Modak <kaustav.dasmodak@yahoo.co.in.
Copyright (C) 2013 Kaustav Das Modak <kaustav.dasmodak@yahoo.co.in.

This file is part of pyAvroPhonetic.

pyAvroPhonetic is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyAvroPhonetic is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyAvroPhonetic.  If not, see <http://www.gnu.org/licenses/>.

"""
from utils import validate
from utils import utf
import config
PATTERNS = config.AVRO_DICT['data']['patterns']
NON_RULE_PATTERNS = [ p for p in PATTERNS if 'rules' not in p ]
RULE_PATTERNS = [ p for p in PATTERNS if 'rules' in p ]

def parse(text):
    """Parses input text, matches and replaces using avrodict

    If a valid replacement is found, returns the replaced string. If
    no replacement is found, returns the input text.

    Usage:

    ::
      from pyavrophonetic import avro
      avro.parse("ami banglay gan gai")

    """
    fixed_text = validate.fix_string_case(utf(text))
    output = []
    cur_end = 0
    for cur, i in enumerate(fixed_text):
        try:
            i.encode('utf-8')
        except UnicodeDecodeError:
            uni_pass = False
        else:
            uni_pass = True

        match = {'matched': False}
        if not uni_pass:
            cur_end = cur + 1
            output.append(i)
        elif cur >= cur_end and uni_pass:
            match = match_non_rule_patterns(fixed_text, cur)
            if match['matched']:
                output.append(match['replaced'])
                cur_end = cur + len(match['found'])
            else:
                match = match_rule_patterns(fixed_text, cur)
                if match['matched']:
                    cur_end = cur + len(match['found'])
                    replaced = process_rules(rules=match['rules'], fixed_text=fixed_text, cur=cur, cur_end=cur_end)
                    if replaced is not None:
                        output.append(replaced)
                    else:
                        output.append(match['replaced'])
            if not match['matched']:
                cur_end = cur + 1
                output.append(i)

    return ('').join(output)


def match_non_rule_patterns(fixed_text, cur=0):
    """Matches given text at cursor position with non rule patterns

    Returns a dictionary of three elements:

    - "matched" - Bool: depending on if match found
    - "found" - string/None: Value of matched pattern's 'find' key or none
    - "replaced": string Replaced string if match found else input string at
    cursor

     """
    pattern = exact_find_in_pattern(fixed_text, cur, NON_RULE_PATTERNS)
    if len(pattern) > 0:
        return {'matched': True, 'found': pattern[0]['find'], 'replaced': pattern[0]['replace']}
    else:
        return {'matched': False, 'found': None, 'replaced': fixed_text[cur]}
        return


def match_rule_patterns(fixed_text, cur=0):
    """Matches given text at cursor position with rule patterns

    Returns a dictionary of four elements:

    - "matched" - Bool: depending on if match found
    - "found" - string/None: Value of matched pattern's 'find' key or none
    - "replaced": string Replaced string if match found else input string at
    cursor
    - "rules": dict/None: A dict of rules or None if no match found

    """
    pattern = exact_find_in_pattern(fixed_text, cur, RULE_PATTERNS)
    if len(pattern) > 0:
        return {'matched': True, 'found': pattern[0]['find'], 'replaced': pattern[0]['replace'], 
           'rules': pattern[0]['rules']}
    else:
        return {'matched': False, 'found': None, 'replaced': fixed_text[cur], 
           'rules': None}
        return


def exact_find_in_pattern(fixed_text, cur=0, patterns=PATTERNS):
    """Returns pattern items that match given text, cur position and pattern"""
    return [ x for x in patterns if cur + len(x['find']) <= len(fixed_text) and x['find'] == fixed_text[cur:cur + len(x['find'])]
           ]


def process_rules(rules, fixed_text, cur=0, cur_end=1):
    """Process rules matched in pattern and returns suitable replacement

    If any rule's condition is satisfied, output the rules "replace",
    else output None

    """
    replaced = ''
    for rule in rules:
        matched = False
        for match in rule['matches']:
            matched = process_match(match, fixed_text, cur, cur_end)
            if not matched:
                break

        if matched:
            replaced = rule['replace']
            break

    if matched:
        return replaced
    else:
        return
        return


def process_match(match, fixed_text, cur, cur_end):
    """Processes a single match in rules"""
    replace = True
    if match['type'] == 'prefix':
        chk = cur - 1
    else:
        chk = cur_end
    if match['scope'].startswith('!'):
        scope = match['scope'][1:]
        negative = True
    else:
        scope = match['scope']
        negative = False
    if scope == 'punctuation':
        if not (chk < 0 and match['type'] == 'prefix' or chk >= len(fixed_text) and match['type'] == 'suffix' or validate.is_punctuation(fixed_text[chk])) ^ negative:
            replace = False
    elif scope == 'vowel':
        if not ((chk >= 0 and match['type'] == 'prefix' or chk < len(fixed_text) and match['type'] == 'suffix') and validate.is_vowel(fixed_text[chk])) ^ negative:
            replace = False
    elif scope == 'consonant':
        if not ((chk >= 0 and match['type'] == 'prefix' or chk < len(fixed_text) and match['type'] == 'suffix') and validate.is_consonant(fixed_text[chk])) ^ negative:
            replace = False
    elif scope == 'exact':
        if match['type'] == 'prefix':
            exact_start = cur - len(match['value'])
            exact_end = cur
        else:
            exact_start = cur_end
            exact_end = cur_end + len(match['value'])
        if not validate.is_exact(match['value'], fixed_text, exact_start, exact_end, negative):
            replace = False
    return replace