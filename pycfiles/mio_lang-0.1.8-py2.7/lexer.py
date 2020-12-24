# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/mio/lexer.py
# Compiled at: 2013-12-09 06:38:59
import re
from collections import OrderedDict
from funcparserlib.lexer import make_tokenizer
tokval = lambda tok: tok.value
Spec = lambda name, value: (name, (value,))
operators = OrderedDict([
 ('**', 1), ('++', 1), ('--', 1), ('+=', 1), ('-=', 1), ('*=', 1), ('/=', 1),
 ('<<', 1), ('>>', 1), ('==', 0), ('!=', 0), ('<=', 0), ('>=', 0), ('..', 1),
 ('+', 1), ('-', 1), ('*', 1), ('/', 1), ('=', 1), ('<', 0), ('>', 0),
 ('!', 0), ('%', 1), ('|', 0), ('^', 0), ('&', 0), ('?', 1), (':', 1),
 ('in', 0), ('is', 0), ('or', 0), ('and', 0), ('not', 0),
 ('return', 0), ('yield', 0), ('from', 1), ('import', 1), ('raise', 0), ('assert', 0)])
strtpl = b'\n    ([bu])?\n    {start:s}\n    [^\\{quote:s}]*?\n    (\n    (   \\\\[\x00-\xff]\n        |   {quote:s}\n        (   \\\\[\x00-\xff]\n        |   [^\\{quote:s}]\n        |   {quote:s}\n        (   \\\\[\x00-\xff]\n            |   [^\\{quote:s}]\n        )\n        )\n    )\n    [^\\{quote:s}]*?\n    )*?\n    {end:s}\n'
quotes = [{'quote': "'", 'start': "'''", 'end': "'''"}, {'quote': '"', 'start': '"""', 'end': '"""'}, {'quote': "'", 'start': "'", 'end': "'"}, {'quote': '"', 'start': '"', 'end': '"'}]
strre = ('').join(strtpl.split())
strre = ('|').join([ strre.format(**quote) for quote in quotes ])
strre = re.compile(strre.format(**quotes[3]))
encoding = 'utf-8'
ops = ('|').join([ re.escape(op) for op in operators ])
specs = [
 Spec('comment', '#.*'),
 Spec('whitespace', '[ \\t]+'),
 Spec('string', strre),
 Spec('number', '(-?(0|([1-9][0-9]*))(\\.[0-9]+)?([Ee]-?[0-9]+)?)'),
 Spec('identifier', '[A-Za-z_][A-Za-z0-9_]*'),
 Spec('operator', ops),
 Spec('op', '[(){}\\[\\],:;\\n\\r]')]
useless = [
 'comment', 'whitespace']
tokenizer = make_tokenizer(specs)

def tokenize(s):
    return [ x for x in tokenizer(s) if x.type not in useless ]