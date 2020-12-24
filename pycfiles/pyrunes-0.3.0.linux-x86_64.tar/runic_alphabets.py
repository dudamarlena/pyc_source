# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yori/Envs/pyrunes/lib/python2.7/site-packages/runes/runic_alphabets.py
# Compiled at: 2016-06-29 13:58:18
from __future__ import absolute_import, unicode_literals
from bidict import bidict
elder_futhark = bidict(f=b'ᚠ', v=b'ᚡ', u=b'ᚢ', a=b'ᚨ', r=b'ᚱ', k=b'ᚲ', g=b'ᚷ', w=b'ᚹ', h=b'ᚺ', n=b'ᚾ', i=b'ᛁ', p=b'ᛈ', j=b'ᛃ', z=b'ᛉ', s=b'ᛊ', t=b'ᛏ', b=b'ᛒ', ng=b'ᛜ', e=b'ᛖ', m=b'ᛗ', l=b'ᛚ', o=b'ᛟ', d=b'ᛞ')
elder_futhark.update({b'ï': b'ᛇ', b'þ': b'ᚦ'})

def get_alphabet(runic_alphabet):
    runic_alphabets = {b'elder_futhark': elder_futhark}
    return runic_alphabets.get(runic_alphabet)