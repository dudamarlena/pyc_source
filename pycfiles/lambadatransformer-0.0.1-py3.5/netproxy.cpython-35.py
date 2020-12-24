# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lambadalib/netproxy.py
# Compiled at: 2017-04-24 15:46:12
# Size of source mod 2**32: 573 bytes
import json, importlib

def color(s):
    return '\x1b[92m' + s + '\x1b[0m'


def Netproxy(d, classname, name, args):
    print(color('[netproxy] {} {} {} <{}>'.format(classname, name, args, d)))
    if '.' in classname:
        modname, classname = classname.split('.')
        mod = importlib.import_module(modname)
        importlib.reload(mod)
        C = getattr(mod, classname)
    else:
        C = globals()[classname]
    _o = C()
    _o.__dict__ = json.loads(d)
    ret = getattr(_o, name)(*args)
    d = json.dumps(_o.__dict__)
    return (d, ret)