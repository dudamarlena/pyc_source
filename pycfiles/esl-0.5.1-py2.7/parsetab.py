# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/esl/parsetab.py
# Compiled at: 2016-03-31 01:04:47
_tabversion = '3.8'
_lr_method = 'LALR'
_lr_signature = '17A76441A771B4A3D86C362AEBE88676'
_lr_action_items = {'BODY': ([3, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], [4, -8, -9, 4, -10, -7, -5, -17, -16, -13, -12, -6, -15, -14]), 'SHELL': ([4, 6, 9], [13, 15, 18]), 'URL': ([0], [1]), 'QUERYSTRING': ([3, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], [6, -8, -9, 6, -10, -7, -5, -17, -16, -13, -12, -6, -15, -14]), 'VALUE': ([4, 6, 9], [14, 16, 19]), 'HEADER': ([3, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], [9, -8, -9, 9, -10, -7, -5, -17, -16, -13, -12, -6, -15, -14]), 'METHOD': ([1], [3]), '$end': ([1, 2, 3, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], [-1, 0, -2, -8, -9, -3, -10, -7, -5, -17, -16, -13, -12, -6, -15, -14])}
_lr_action = {}
for _k, _v in _lr_action_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if not _x in _lr_action:
            _lr_action[_x] = {}
        _lr_action[_x][_k] = _y

del _lr_action_items
_lr_goto_items = {'OPTION': ([3, 8], [12, 17]), 'request': ([0], [2]), 'QUERYSTRINGVALUE': ([3, 8], [7, 7]), 'BODYVALUE': ([3, 8], [10, 10]), 'OPTIONS': ([3], [8]), 'empty': ([3, 8], [11, 11]), 'HEADERVALUE': ([3, 8], [5, 5])}
_lr_goto = {}
for _k, _v in _lr_goto_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if not _x in _lr_goto:
            _lr_goto[_x] = {}
        _lr_goto[_x][_k] = _y

del _lr_goto_items
_lr_productions = [
 (
  "S' -> request", "S'", 1, None, None, None),
 (
  'request -> URL', 'request', 1, 'p_request', 'eslyacc.py', 27),
 (
  'request -> URL METHOD', 'request', 2, 'p_request', 'eslyacc.py', 28),
 (
  'request -> URL METHOD OPTIONS', 'request', 3, 'p_request', 'eslyacc.py', 29),
 (
  'OPTIONS -> <empty>', 'OPTIONS', 0, 'p_options', 'eslyacc.py', 38),
 (
  'OPTIONS -> OPTION', 'OPTIONS', 1, 'p_options', 'eslyacc.py', 39),
 (
  'OPTIONS -> OPTIONS OPTION', 'OPTIONS', 2, 'p_options', 'eslyacc.py', 40),
 (
  'OPTION -> empty', 'OPTION', 1, 'p_option_empty', 'eslyacc.py', 47),
 (
  'OPTION -> HEADERVALUE', 'OPTION', 1, 'p_option_header', 'eslyacc.py', 51),
 (
  'OPTION -> QUERYSTRINGVALUE', 'OPTION', 1, 'p_option_querystring', 'eslyacc.py', 55),
 (
  'OPTION -> BODYVALUE', 'OPTION', 1, 'p_option_body', 'eslyacc.py', 59),
 (
  'empty -> <empty>', 'empty', 0, 'p_empty', 'eslyacc.py', 63),
 (
  'QUERYSTRINGVALUE -> QUERYSTRING VALUE', 'QUERYSTRINGVALUE', 2, 'p_querystring_value', 'eslyacc.py', 67),
 (
  'QUERYSTRINGVALUE -> QUERYSTRING SHELL', 'QUERYSTRINGVALUE', 2, 'p_querystring_shell', 'eslyacc.py', 71),
 (
  'HEADERVALUE -> HEADER VALUE', 'HEADERVALUE', 2, 'p_header_value', 'eslyacc.py', 75),
 (
  'HEADERVALUE -> HEADER SHELL', 'HEADERVALUE', 2, 'p_header_shell', 'eslyacc.py', 79),
 (
  'BODYVALUE -> BODY VALUE', 'BODYVALUE', 2, 'p_body_value', 'eslyacc.py', 83),
 (
  'BODYVALUE -> BODY SHELL', 'BODYVALUE', 2, 'p_body_shell', 'eslyacc.py', 87)]