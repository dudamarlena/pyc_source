# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/utilsDb.py
# Compiled at: 2014-05-29 10:16:48


def setDefaults2Obj(pObj, defaults, exclude=[]):
    """ Asignas las props q vienen en un dict a un objeto
    """
    for key in defaults:
        if key in exclude:
            continue
        try:
            setattr(pObj, key, defaults[key])
        except:
            pass