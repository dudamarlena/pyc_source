# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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