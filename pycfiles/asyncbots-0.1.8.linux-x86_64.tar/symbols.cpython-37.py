# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/asyncbots/parsing/symbols.py
# Compiled at: 2018-01-04 18:06:59
# Size of source mod 2**32: 1423 bytes
"""Definitions of a few commonly used symbols for convenience."""
from pyparsing import alphanums, nums, CaselessLiteral, CharsNotIn, delimitedList, OneOrMore, originalTextFor, printables, QuotedString, quotedString, Regex, removeQuotes, Suppress, White, Word
emoji = Regex(':[\\S]+:').setResultsName('emoji')
message = OneOrMore(Word(alphanums + '#')).setResultsName('message')

def tail(name):
    """Match any amount of characters"""
    return Suppress(White(max=1)) + CharsNotIn('').setResultsName(name)


channel_name = Word(alphanums + '-').setResultsName('channel')
user_name = Word(alphanums + '-_.')
mention = Regex('<@(U[0-9A-Z]{8})>')
link = Word(printables)
int_num = Word(nums)
single_quotes = QuotedString('‘', endQuoteChar='’', escChar='\\')
double_quotes = QuotedString('“', endQuoteChar='”', escChar='\\')
quotedString.addParseAction(removeQuotes)
comma_list = delimitedList(single_quotes | double_quotes | quotedString | originalTextFor(OneOrMore(Word(printables, excludeChars=',')))).setResultsName('comma_list')
alphanum_word = Word(alphanums)

def flag(name):
    dashes = '--' if len(name) > 1 else '-'
    return CaselessLiteral(dashes + name).setResultsName(name)


def flag_with_arg(name, argtype):
    dashes = '--' if len(name) > 1 else '-'
    return CaselessLiteral(dashes + name) + argtype.setResultsName(name)