# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Neko\Desktop\aperturec\aperture\__s_lib__.py
# Compiled at: 2020-01-09 14:38:43
# Size of source mod 2**32: 1153 bytes
import json

class modifiers:
    speed = 1
    pitch = 1
    volume = 100

    def __init__(self):
        pass


class _import:

    def __init__(self):
        self.a = None

    def csp(name: str, soundvalue: str):
        try:
            try:
                csp = open(name)
            except FileNotFoundError:
                raise FileNotFoundError

        finally:
            return

        var = json.load(csp)
        return var[soundvalue]

    def ctp(name: str):
        try:
            try:
                ctp = open(name)
            except FileNotFoundError:
                raise FileNotFoundError

        finally:
            return

        var = ctp.read()
        p1, v1, s1 = ('pitch', 'volume', 'speed')
        d = var.replace(p1, '').replace(v1, '').replace(s1, '').replace(' ', '').replace('\n', '').split('=')
        data = d
        v = data[1]
        p = data[2]
        s = data[3]
        try:
            g = data[4]
        except IndexError:
            pass

        out = {'volume':v,  'pitch':p,  'speed':s}
        return dict(out)