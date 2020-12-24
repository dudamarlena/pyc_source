# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/rus/lat2rus.py
# Compiled at: 2017-04-23 16:42:07
from __future__ import print_function
from ..lazy.dict import LazyDictInitFunc
lat2koi_d = {'q': b'\xca', 
   'w': b'\xc3', 
   'e': b'\xd5', 
   'r': b'\xcb', 
   't': b'\xc5', 
   'y': b'\xce', 
   'u': b'\xc7', 
   'i': b'\xdb', 
   'o': b'\xdd', 
   'p': b'\xda', 
   '[': b'\xc8', 
   ']': b'\xdf', 
   'a': b'\xc6', 
   's': b'\xd9', 
   'd': b'\xd7', 
   'f': b'\xc1', 
   'g': b'\xd0', 
   'h': b'\xd2', 
   'j': b'\xcf', 
   'k': b'\xcc', 
   'l': b'\xc4', 
   ';': b'\xd6', 
   "'": b'\xdc', 
   'z': b'\xd1', 
   'x': b'\xde', 
   'c': b'\xd3', 
   'v': b'\xcd', 
   'b': b'\xc9', 
   'n': b'\xd4', 
   'm': b'\xd8', 
   ',': b'\xc2', 
   '.': b'\xc0', 
   'Q': b'\xea', 
   'W': b'\xe3', 
   'E': b'\xf5', 
   'R': b'\xeb', 
   'T': b'\xe5', 
   'Y': b'\xee', 
   'U': b'\xe7', 
   'I': b'\xfb', 
   'O': b'\xfd', 
   'P': b'\xfa', 
   '{': b'\xe8', 
   '}': b'\xff', 
   'A': b'\xe6', 
   'S': b'\xf9', 
   'D': b'\xf7', 
   'F': b'\xe1', 
   'G': b'\xf0', 
   'H': b'\xf2', 
   'J': b'\xef', 
   'K': b'\xec', 
   'L': b'\xe4', 
   ':': b'\xf6', 
   '"': b'\xfc', 
   'Z': b'\xf1', 
   'X': b'\xfe', 
   'C': b'\xf3', 
   'V': b'\xed', 
   'B': b'\xe9', 
   'N': b'\xf4', 
   'M': b'\xf8', 
   '<': b'\xe2', 
   '>': b'\xe0', 
   '`': b'\xa3', 
   '~': b'\xb3', 
   '!': '!', 
   '@': '"', 
   '#': '#', 
   '$': '*', 
   '%': ':', 
   '^': ',', 
   '&': '.', 
   '*': ';'}

def make_lat2xxx(encoding='cp1251'):
    d = {}
    for (k, v) in lat2koi_d.items():
        d[k] = v

    return d


lat2win_d = LazyDictInitFunc(make_lat2xxx, encoding='cp1251')

def lat2rus(instr, lat2rus_d=lat2koi_d):
    out = []
    for c in instr:
        c = lat2rus_d.get(c, c)
        out.append(c)

    return ('').join(out)


lat2koi = lat2rus

def lat2win(instr):
    return lat2rus(instr, lat2win_d)


if __name__ == '__main__':
    Test = 'Ghbdtn nt,t^ ghtrhfcysq vbh!'
    print('Test:', Test)
    print(b'\xf4\xc5\xd3\xd4:', lat2koi(Test))
    test = lat2win(Test)
    print(b'\xf4\xc5\xd3\xd4:', test)