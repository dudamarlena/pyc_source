# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rsutton/workarea/env/eulxml/lib/python2.7/site-packages/eulxml/xpath/lextab.py
# Compiled at: 2016-04-26 10:58:33
_tabversion = '3.8'
_lextokens = set(['CLOSE_BRACKET', 'ABBREV_PATH_SEP', 'NCNAME', 'DIV_OP', 'COLON', 'REL_OP', 'MINUS_OP', 'OPEN_BRACKET', 'OR_OP', 'OPEN_PAREN', 'PATH_SEP', 'ABBREV_STEP_PARENT', 'INTEGER', 'ABBREV_STEP_SELF', 'AXISNAME', 'DOLLAR', 'AND_OP', 'LITERAL', 'EQUAL_OP', 'CLOSE_PAREN', 'STAR_OP', 'MULT_OP', 'NODETYPE', 'ABBREV_AXIS_AT', 'FLOAT', 'UNION_OP', 'FUNCNAME', 'PLUS_OP', 'AXIS_SEP', 'COMMA', 'MOD_OP'])
_lexreflags = 32
_lexliterals = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere = {'INITIAL': [('(?P<t_LITERAL>"[^"]*"|\'[^\']*\')|(?P<t_FLOAT>\\d+\\.\\d*|\\.\\d+)|(?P<t_INTEGER>\\d+)|(?P<t_NCNAME>([A-Z]|_|[a-z]|\\xc0-\\xd6]|[\\xd8-\\xf6]|[\\xf8-˿]|[Ͱ-ͽ]|[Ϳ-\u1fff]|[\u200c-\u200d]|[⁰-\u218f]|[Ⰰ-\u2fef]|[、-\ud7ff]|[豈-\ufdcf]|[ﷰ-�])([A-Z]|_|[a-z]|\\xc0-\\xd6]|[\\xd8-\\xf6]|[\\xf8-˿]|[Ͱ-ͽ]|[Ϳ-\u1fff]|[\u200c-\u200d]|[⁰-\u218f]|[Ⰰ-\u2fef]|[、-\ud7ff]|[豈-\ufdcf]|[ﷰ-�]|[-.0-9\\xb7̀-ͯ‿-⁀])*)|(?P<t_REL_OP>[<>]=?)|(?P<t_ABBREV_STEP_PARENT>\\.\\.)|(?P<t_EQUAL_OP>!?=)|(?P<t_DOLLAR>\\$)|(?P<t_OPEN_BRACKET>\\[)|(?P<t_PLUS_OP>\\+)|(?P<t_CLOSE_PAREN>\\))|(?P<t_AXIS_SEP>::)|(?P<t_STAR_OP>\\*)|(?P<t_CLOSE_BRACKET>\\])|(?P<t_ABBREV_PATH_SEP>//)|(?P<t_UNION_OP>\\|)|(?P<t_OPEN_PAREN>\\()|(?P<t_ABBREV_STEP_SELF>\\.)|(?P<t_ABBREV_AXIS_AT>@)|(?P<t_COLON>:)|(?P<t_COMMA>,)|(?P<t_MINUS_OP>-)|(?P<t_PATH_SEP>/)', [None, ('t_LITERAL', 'LITERAL'), ('t_FLOAT', 'FLOAT'), ('t_INTEGER', 'INTEGER'), (None, 'NCNAME'), None, None, (None, 'REL_OP'), (None, 'ABBREV_STEP_PARENT'), (None, 'EQUAL_OP'), (None, 'DOLLAR'), (None, 'OPEN_BRACKET'), (None, 'PLUS_OP'), (None, 'CLOSE_PAREN'), (None, 'AXIS_SEP'), (None, 'STAR_OP'), (None, 'CLOSE_BRACKET'), (None, 'ABBREV_PATH_SEP'), (None, 'UNION_OP'), (None, 'OPEN_PAREN'), (None, 'ABBREV_STEP_SELF'), (None, 'ABBREV_AXIS_AT'), (None, 'COLON'), (None, 'COMMA'), (None, 'MINUS_OP'), (None, 'PATH_SEP')])]}
_lexstateignore = {'INITIAL': ' \t\r\n'}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}