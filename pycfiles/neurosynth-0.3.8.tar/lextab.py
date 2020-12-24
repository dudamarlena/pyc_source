# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tal/Dropbox/Code/neurosynth/neurosynth/tests/lextab.py
# Compiled at: 2014-03-25 13:54:48
_tabversion = '3.4'
_lextokens = {'AND': 1, 'LPAR': 1, 'FLOAT': 1, 'FEATURE': 1, 'RPAR': 1, 'LT': 1, 'RT': 1, 'ANDNOT': 1, 'OR': 1, 'CONTRAST': 1}
_lexreflags = 0
_lexliterals = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere = {'INITIAL': [('(?P<t_FLOAT>[0-9\\.]+)|(?P<t_FEATURE>[a-z\\_\\-\\*]+)|(?P<t_ANDNOT>\\&\\~)|(?P<t_RPAR>\\))|(?P<t_LT>\\<)|(?P<t_LPAR>\\()|(?P<t_RT>\\>)|(?P<t_AND>\\&)|(?P<t_OR>\\|)', [None, ('t_FLOAT', 'FLOAT'), (None, 'FEATURE'), (None, 'ANDNOT'), (None, 'RPAR'), (None, 'LT'), (None, 'LPAR'), (None, 'RT'), (None, 'AND'), (None, 'OR')])]}
_lexstateignore = {'INITIAL': ' \t'}
_lexstateerrorf = {'INITIAL': 't_error'}