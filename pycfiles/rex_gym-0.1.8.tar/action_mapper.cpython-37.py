# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/seven/dev/rex-gym/rex_gym/util/action_mapper.py
# Compiled at: 2019-12-07 11:19:06
# Size of source mod 2**32: 136 bytes
ACTION_MAP = {'run': ('rex_gym/policies/galloping/balanced', '20000000')}

def fromAction(action):
    return ACTION_MAP[action]