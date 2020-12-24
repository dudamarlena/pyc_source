# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\until\tools.py
# Compiled at: 2020-04-20 05:54:40
# Size of source mod 2**32: 950 bytes
import os, base64

def nonce_str():
    return str((base64.b64encode(os.urandom(24))), encoding='utf-8')


def array_sort(ls: list):
    l_str = ''
    for i, l in enumerate(ls):
        if isinstance(l, dict):
            l_str = l_str + obj_sort(l)
        else:
            if isinstance(l, list):
                l_str = l_str + array_sort(l)
            else:
                l_str = l_str + str(l)

    return l_str


def map_sort(ds: dict):
    d_str = ''
    for k, v in ds.items():
        d_str = d_str + '{}{}'.format(k, v)

    return d_str


def obj_sort(oos):
    d_str = ''
    for k, v in oos.items():
        d_str = d_str + '{}'.format(v)

    return d_str


if __name__ == '__main__':
    print(array_sort([{'a':'111',  'b':'222',  'c':'333|||'},
     {'d':'444', 
      'e':'555',  'f':'666'}]))