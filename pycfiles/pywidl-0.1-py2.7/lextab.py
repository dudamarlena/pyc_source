# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pywidl/lextab.py
# Compiled at: 2012-03-17 10:29:43
_tabversion = '3.4'
_lextokens = {'string': 1, 'float': 1, 'other': 1, 'integer': 1, 'identifier': 1, 'whitespace': 1}
_lexreflags = 0
_lexliterals = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere = {'INITIAL': [('(?P<t_whitespace>[\\t\\n\\r ]+|[\\t\\n\\r ]*((//.*|/\\*.*?\\*/)[\\t\\n\\r ]*)+)|(?P<t_integer>-?(0([0-7]*|[Xx][0-9A-Fa-f]+)|[1-9][0-9]*))|(?P<t_identifier>[A-Z_a-z][0-9A-Z_a-z]*)|(?P<t_string>\\"[^\\"]*\\")', [None, (None, 'whitespace'), None, None, (None, 'integer'), None, None, (None, 'identifier'), (None, 'string')])]}
_lexstateignore = {'INITIAL': ''}
_lexstateerrorf = {'INITIAL': 't_error'}