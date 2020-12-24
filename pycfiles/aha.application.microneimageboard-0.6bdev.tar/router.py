# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/dispatch/router.py
# Compiled at: 2011-03-16 21:46:32
__all__ = [
 'get_router', 'get_fallback_router', 'rebuild_router']
from routes.mapper import Mapper
router = Mapper()
fallback_router = Mapper()

def get_router():
    """
    A function to obtain mapper object, which is used as a singleton.
    """
    global router
    return router


def get_fallback_router():
    """
    A function to obtain mapper object, which is used as a singleton.
    """
    global fallback_router
    return fallback_router


def rebuild_router():
    global fallback_router
    global router
    router = Mapper()
    fallback_router = Mapper()