# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\engines\engine.py
# Compiled at: 2008-11-19 12:15:15
"""
    This file implements an interface to the available engines.
"""

def get_engine():
    global _engine
    if _engine:
        return _engine
    engine = get_natlink_engine()
    if engine:
        return engine
    engine = get_sapi5_engine()
    if engine:
        return engine
    raise Exception


_engine = None
NatlinkEngine = None
_natlink_engine = None

def get_natlink_engine():
    global NatlinkEngine
    global _engine
    global _natlink_engine
    if _natlink_engine:
        return _natlink_engine
    import dragonfly.engines.engine_natlink as engine_natlink
    NatlinkEngine = engine_natlink.NatlinkEngine
    if NatlinkEngine.is_available():
        _natlink_engine = NatlinkEngine()
        _engine = _natlink_engine
        return _natlink_engine
    return


Sapi5Engine = None
_sapi5_engine = None

def get_sapi5_engine():
    global Sapi5Engine
    global _engine
    global _sapi5_engine
    if _sapi5_engine:
        return _sapi5_engine
    import dragonfly.engines.engine_sapi5 as engine_sapi5
    Sapi5Engine = engine_sapi5.Sapi5Engine
    if Sapi5Engine.is_available():
        _sapi5_engine = Sapi5Engine()
        _engine = _sapi5_engine
        return _sapi5_engine
    return