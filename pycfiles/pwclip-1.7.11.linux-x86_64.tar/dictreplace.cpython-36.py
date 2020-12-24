# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/lib/system/dictreplace.py
# Compiled at: 2020-03-20 08:07:42
# Size of source mod 2**32: 551 bytes
from colortext import error

def dictreplace(srcdict, trgdict):
    if not isinstance(srcdict, dict):
        return error("type 'dict' expected, got", type(trgdict))
    else:
        newdict = {}
        for k, v in srcdict.items():
            if k in trgdict.keys() and isinstance(trgdict[k], dict):
                __dict = dictreplace(srcdict[k], trgdict[k])
                if 'delkey' in trgdict[k].keys():
                    for ik, iv in __dict.items():
                        newdict[ik] = iv

                else:
                    newdict[k] = __dict
                    continue
            else:
                if k in trgdict.keys():
                    newdict[trgdict[k]] = v
                else:
                    newdict[k] = v

        return newdict