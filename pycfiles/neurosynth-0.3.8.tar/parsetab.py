# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tal/Dropbox/Code/neurosynth/neurosynth/tests/parsetab.py
# Compiled at: 2014-03-25 13:08:58
_tabversion = '3.2'
_lr_method = 'LALR'
_lr_signature = b'35!\xc7AD\x1b\xd2*\xe7F\x0f\xbfK\xad\xe9'
_lr_action_items = {'AND': ([2, 3, 4, 10, 11, 12, 13, 14, 15, 16], [5, -6, 5, -7, 5, -5, -8, -4, 5, 5]), 'LPAR': ([0, 1, 5, 8, 9], [1, 1, 1, 1, 1]), 'FLOAT': ([6, 7], [13, 13]), 'FEATURE': ([0, 1, 5, 8, 9], [3, 3, 3, 3, 3]), 'RPAR': ([3, 4, 10, 11, 12, 13, 14, 15, 16], [-6, 10, -7, -2, -5, -8, -4, -1, -3]), 'LT': ([2, 3, 4, 10, 11, 12, 13, 14, 15, 16], [7, -6, 7, -7, 7, -5, -8, -4, 7, 7]), 'RT': ([2, 3, 4, 10, 11, 12, 13, 14, 15, 16], [6, -6, 6, -7, 6, -5, -8, -4, 6, 6]), 'ANDNOT': ([2, 3, 4, 10, 11, 12, 13, 14, 15, 16], [8, -6, 8, -7, 8, -5, -8, -4, 8, 8]), 'OR': ([2, 3, 4, 10, 11, 12, 13, 14, 15, 16], [9, -6, 9, -7, 9, -5, -8, -4, 9, 9]), '$end': ([2, 3, 10, 11, 12, 13, 14, 15, 16], [0, -6, -7, -2, -5, -8, -4, -1, -3])}
_lr_action = {}
for _k, _v in _lr_action_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if not _x in _lr_action:
            _lr_action[_x] = {}
        _lr_action[_x][_k] = _y

del _lr_action_items
_lr_goto_items = {'freq': ([6, 7], [12, 14]), 'list': ([0, 1, 5, 8, 9], [2, 4, 11, 15, 16])}
_lr_goto = {}
for _k, _v in _lr_goto_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if not _x in _lr_goto:
            _lr_goto[_x] = {}
        _lr_goto[_x][_k] = _y

del _lr_goto_items
_lr_productions = [
 (
  "S' -> list", "S'", 1, None, None, None),
 (
  'list -> list ANDNOT list', 'list', 3, 'p_list_andnot', '/usr/local/Cellar/python/2.7.6/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/neurosynth/base/lexparser.py', 66),
 (
  'list -> list AND list', 'list', 3, 'p_list_and', '/usr/local/Cellar/python/2.7.6/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/neurosynth/base/lexparser.py', 70),
 (
  'list -> list OR list', 'list', 3, 'p_list_or', '/usr/local/Cellar/python/2.7.6/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/neurosynth/base/lexparser.py', 74),
 (
  'list -> list LT freq', 'list', 3, 'p_list_lt', '/usr/local/Cellar/python/2.7.6/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/neurosynth/base/lexparser.py', 79),
 (
  'list -> list RT freq', 'list', 3, 'p_list_rt', '/usr/local/Cellar/python/2.7.6/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/neurosynth/base/lexparser.py', 83),
 (
  'list -> FEATURE', 'list', 1, 'p_list_feature', '/usr/local/Cellar/python/2.7.6/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/neurosynth/base/lexparser.py', 87),
 (
  'list -> LPAR list RPAR', 'list', 3, 'p_list_expr', '/usr/local/Cellar/python/2.7.6/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/neurosynth/base/lexparser.py', 92),
 (
  'freq -> FLOAT', 'freq', 1, 'p_freq_float', '/usr/local/Cellar/python/2.7.6/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/neurosynth/base/lexparser.py', 96)]