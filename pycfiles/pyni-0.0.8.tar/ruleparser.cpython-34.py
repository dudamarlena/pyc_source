# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynhost/ruleparser.py
# Compiled at: 2015-07-18 14:40:34
# Size of source mod 2**32: 7428 bytes
import re
from pynhost import dynamic, regex_range, utilities
try:
    from pynhost.grammars import _locals
except ImportError:
    _locals = None

REP_PATTERN = re.compile('<\\d+(-\\d?)?>')
HOM_PATTERN = re.compile('<hom_.+>')
SINGLE_NUM_RANGE_PATTERN = re.compile('<num_-?\\d+>')
DOUBLE_NUM_RANGE_PATTERN = re.compile('<num_-?\\d+_-?\\d+>')

class Rule:

    def __init__(self, pattern, actions=None, grammar=None):
        if not isinstance(actions, list):
            actions = [
             actions]
        self.actions = actions
        self.groups = {}
        if isinstance(pattern, str):
            self.compiled_regex = re.compile(self.convert_to_regex_pattern(pattern, grammar))
        else:
            self.compiled_regex = pattern
        self.grammar = grammar

    def __str__(self):
        return '<Rule: {}>'.format(self.compiled_regex.pattern)

    def __repr__(self):
        return '<Rule: {}>'.format(self.compiled_regex.pattern)

    def convert_to_regex_pattern(self, rule_string, grammar):
        regex_pattern = ''
        tag = ''
        word = ''
        stack = []
        rule_string = ' '.join(rule_string.strip().split())
        group_num = 0
        for i, char in enumerate(rule_string):
            if stack and stack[(-1)] == '<':
                tag += char
                if char == '>':
                    if HOM_PATTERN.match(tag) and not (hasattr(_locals, 'HOMOPHONES') and tag[5:-1] in _locals.HOMOPHONES and _locals.HOMOPHONES[tag[5:-1]]):
                        regex_pattern += tag[5:-1] + ' '
                    else:
                        if tag == '<num>' or HOM_PATTERN.match(tag) or SINGLE_NUM_RANGE_PATTERN.match(tag) or DOUBLE_NUM_RANGE_PATTERN.match(tag):
                            group_num += 1
                        if REP_PATTERN.match(tag):
                            regex_pattern = surround_previous_word(regex_pattern)
                        regex_pattern += token_to_regex(tag, group_num, rule_string, self.groups)
                    tag = ''
                    word = ''
                    stack.pop()
                continue
            if char in '([<':
                if word:
                    regex_pattern += '{} '.format(word)
                word = ''
                stack.append(char)
                if char == '<':
                    tag = '<'
                    continue
                regex_pattern += '('
                tag = char
            elif char in ')]':
                stack.pop()
                if word:
                    word += ' '
                if char == ']':
                    char = ')?'
                regex_pattern += word + char
                word = ''
            elif char == '|':
                if word:
                    regex_pattern += '{} |'.format(word)
                    word = ''
                else:
                    regex_pattern += '|'
            elif char == ' ':
                if word and rule_string[(i + 1)] not in '|>)]' and rule_string[(i - 1)] not in '(<[|]>)':
                    regex_pattern += '{} '.format(word)
                    word = ''
            elif char in '.+?*-':
                word += '\\{}'.format(char)
            else:
                word += char

        if word:
            regex_pattern += '{} '.format(word)
        if stack:
            raise ValueError('Error balancing delimiters for string "{}" in grammar {}. Check that your rule pattern has balanced delimiters or use an already compiled regular expression pattern instead'.format(rule_string, grammar))
        return regex_pattern


def regex_string_from_list(input_list, token):
    if not input_list:
        return token
    if token:
        text_list = [
         '{} '.format(token)]
        for ele in input_list:
            text_list.append('|{} '.format(ele))

    else:
        text_list = []
        for i, ele in enumerate(input_list):
            text_list.append('{} '.format(ele))
            if i != len(input_list) - 1:
                text_list[(-1)] += '|'
                continue

    return '({})'.format(''.join(text_list))


def surround_previous_word(input_str):
    """
    Surround last word in string with parentheses. If last non-whitespace character
    is delimiter, do nothing
    """
    start = None
    end = None
    for i, char in enumerate(reversed(input_str)):
        if start is None:
            if char in '{}()[]<>?|':
                return input_str
            if char != ' ':
                start = i
        elif char in '{}()[]<>?| ':
            end = i
            break

    if start is None:
        return input_str
    if end is None:
        end = len(input_str)
    new_str = ''
    for i, char in enumerate(reversed(input_str)):
        if char == ' ' and i + 1 == start:
            continue
        if i == start:
            new_str += ') '
        elif i == end:
            new_str += '('
        new_str += char

    if end == len(input_str):
        new_str += '('
    return new_str[::-1]


def set_num_range_pattern(start, stop, group_num):
    istart, istop = int(start), int(stop)
    if not istart < istop:
        raise ValueError('start must be lower than stop in num range')
    pattern_list = [
     '?P<n{}>'.format(group_num) + ' |'.join(regex_range.regex_for_range(istart, istop).split('|'))]
    if not hasattr(_locals, 'NUMBERS_MAP'):
        return '({})'.format(pattern_list[0])
    for word in sorted(_locals.NUMBERS_MAP):
        if istart <= int(_locals.NUMBERS_MAP[word]) < istop:
            pattern_list.append(word)
            continue

    pattern_list[(-1)] += ' '
    return '({})'.format(' |'.join(pattern_list))


def token_to_regex(token, group_num, rule_string, groups):
    if token == '<start>':
        return '^'
    if token == '<end>':
        return '$'
    if token == '<any>':
        return '([^()<>|[\\] ]+ )'
    if REP_PATTERN.match(token):
        split_tag = token.replace('<', '').replace('>', '').split('-')
        if len(split_tag) == 1:
            return '{' + split_tag[0] + '}'
        return '{' + '{},{}'.format(split_tag[0], split_tag[1]) + '}'
    if HOM_PATTERN.match(token):
        token = token[5:-1]
        groups['n{}'.format(group_num)] = token
        return regex_string_from_list(sorted(_locals.HOMOPHONES[token]), '?P<n{0}>{1}'.format(group_num, token))
    groups['n{}'.format(group_num)] = ''
    if token == '<num>':
        if not hasattr(_locals, 'NUMBERS_MAP'):
            return '(?P<n{}>-?\\d+(\\.d+)? )'.format(group_num)
        return regex_string_from_list(sorted(_locals.NUMBERS_MAP), '?P<n{}>(-?\\d+(\\.\\d+)?)'.format(group_num))
    if SINGLE_NUM_RANGE_PATTERN.match(token):
        num = token.split('_')[1][:-1]
        return set_num_range_pattern('0', num, group_num)
    if DOUBLE_NUM_RANGE_PATTERN.match(token):
        low, high = token.split('_')[1], token.split('_')[2][:-1]
        return set_num_range_pattern(low, high, group_num)
    raise ValueError("invalid token '{}' for rule string '{}'".format(token, rule_string))