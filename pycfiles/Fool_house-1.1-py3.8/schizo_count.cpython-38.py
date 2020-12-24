# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fool_house/schizo_count.py
# Compiled at: 2020-01-14 11:08:40
# Size of source mod 2**32: 443 bytes
schizo_count = ['ноль',
 'целковый',
 'чекушка',
 'порнушка',
 'пердушка',
 'засерушка',
 'жучок',
 'мудачок',
 'хуй на воротничок',
 'дурачок']

def from_int_to_schizo_str(num):
    base = len(schizo_count)
    res = []
    for ch in str(num):
        res.append(schizo_count[int(ch, base)])
    else:
        return '-'.join(res)