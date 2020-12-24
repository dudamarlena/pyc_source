# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/syntax/lang.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 376 bytes


def NewLangId():
    global _idCounter
    _idCounter += 1
    return _idCounter


_idCounter = 32100
ID_LANG_TXT = NewLangId()

def RegisterNewLangId(langId):
    """Register a new language identifier
    @param langId: "ID_LANG_FOO"
    @return: int

    """
    gdict = globals()
    if langId not in gdict:
        gdict[langId] = NewLangId()
    return gdict[langId]