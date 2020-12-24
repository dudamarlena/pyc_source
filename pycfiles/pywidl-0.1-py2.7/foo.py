# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pywidl/foo.py
# Compiled at: 2012-03-16 14:42:58
_tabversion = '3.2'
_lr_method = 'LALR'
_lr_signature = b'\xa1\xca\xe6\xceB+Bb\xb0`\x8e\xbcF\x82\xe4\xa0'
_lr_action_items = {'integer': ([3], [4]), 'identifier': ([0], [2]), 'whitespace': ([2, 4], [3, 5]), '$end': ([1, 5], [0, -1])}
_lr_action = {}
for _k, _v in _lr_action_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if _x not in _lr_action:
            _lr_action[_x] = {}
        _lr_action[_x][_k] = _y

del _lr_action_items
_lr_goto_items = {'Definitions': ([0], [1])}
_lr_goto = {}
for _k, _v in _lr_goto_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if _x not in _lr_goto:
            _lr_goto[_x] = {}
        _lr_goto[_x][_k] = _y

del _lr_goto_items
_lr_productions = [
 ("S' -> Definitions", "S'", 1, None, None, None),
 ('Definitions -> identifier whitespace integer whitespace', 'Definitions', 4, 'p_Definitions',
 '/home/vasily/dev/pywidl/pywidl/parser.py', 10)]