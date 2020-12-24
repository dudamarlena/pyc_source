# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/rus/rus2lat.py
# Compiled at: 2017-04-23 16:42:07
from __future__ import print_function
from ..lazy.dict import LazyDictInitFunc
koi2lat_d = {b'\xe1': 'A', 
   b'\xe2': 'B', 
   b'\xf7': 'V', 
   b'\xe7': 'G', 
   b'\xe4': 'D', 
   b'\xe5': 'E', 
   b'\xf6': 'Zh', 
   b'\xfa': 'Z', 
   b'\xe9': 'I', 
   b'\xea': 'Y', 
   b'\xeb': 'K', 
   b'\xec': 'L', 
   b'\xed': 'M', 
   b'\xee': 'N', 
   b'\xef': 'O', 
   b'\xf0': 'P', 
   b'\xf2': 'R', 
   b'\xf3': 'S', 
   b'\xf4': 'T', 
   b'\xf5': 'U', 
   b'\xe6': 'F', 
   b'\xe8': 'H', 
   b'\xe3': 'Ts', 
   b'\xfe': 'Ch', 
   b'\xfb': 'Sh', 
   b'\xfd': 'Sh', 
   b'\xff': "'", 
   b'\xf8': "'", 
   b'\xf9': 'Y', 
   b'\xfc': 'E', 
   b'\xe0': 'Yu', 
   b'\xf1': 'Ya', 
   b'\xc1': 'a', 
   b'\xc2': 'b', 
   b'\xd7': 'v', 
   b'\xc7': 'g', 
   b'\xc4': 'd', 
   b'\xc5': 'e', 
   b'\xd6': 'zh', 
   b'\xda': 'z', 
   b'\xc9': 'i', 
   b'\xca': 'y', 
   b'\xcb': 'k', 
   b'\xcc': 'l', 
   b'\xcd': 'm', 
   b'\xce': 'n', 
   b'\xcf': 'o', 
   b'\xd0': 'p', 
   b'\xd2': 'r', 
   b'\xd3': 's', 
   b'\xd4': 't', 
   b'\xd5': 'u', 
   b'\xc6': 'f', 
   b'\xc8': 'h', 
   b'\xc3': 'ts', 
   b'\xde': 'ch', 
   b'\xdb': 'sh', 
   b'\xdd': 'sh', 
   b'\xdf': "'", 
   b'\xd8': "'", 
   b'\xd9': 'y', 
   b'\xdc': 'e', 
   b'\xc0': 'yu', 
   b'\xd1': 'ya'}

def make_xxx2lat(encoding='cp1251'):
    d = {}
    for (k, v) in koi2lat_d.items():
        d[k] = v

    return d


win2lat_d = LazyDictInitFunc(make_xxx2lat, encoding='cp1251')

def rus2lat(instr, rus2lat_d=koi2lat_d):
    out = []
    for c in instr:
        c = rus2lat_d.get(c, c)
        if isinstance(c, int):
            c = chr(c)
        out.append(c)

    return ('').join(out)


koi2lat = rus2lat

def win2lat(instr):
    return rus2lat(instr, win2lat_d)


if __name__ == '__main__':
    Test = b'\xfd\xc5\xd2\xc2\xc1\xcb\xcf\xd7 \xe9\xc7\xcf\xd2\xd8 \xe7\xd2\xc9\xc7\xcf\xd2\xd8\xc5\xd7\xc9\xde. \xe1\xe2\xf7 xyz \xc1\xc2\xd7 \xf8\xf8\xfc\xe0\xf1 \xdf\xd8\xdc\xc0\xd1'
    print('Test:', Test)
    print(b'\xf4\xc5\xd3\xd4:', koi2lat(Test))
    print(b'\xf4\xc5\xd3\xd4:', win2lat(Test))