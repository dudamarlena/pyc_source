# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/turbomail/adapters/tg1.py
# Compiled at: 2009-08-26 19:20:04
"""TurboGears automatic startup/shutdown extension."""
from turbogears import config
from turbomail.control import interface
__all__ = [
 'start_extension', 'shutdown_extension']

def start_extension():
    interface.start(config)


def shutdown_extension():
    interface.stop()