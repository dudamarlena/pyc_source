# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/turbomail/__init__.py
# Compiled at: 2009-08-26 19:34:09
import warnings
from turbomail.control import interface
from turbomail.exceptions import *
from turbomail.message import *
from turbomail.wrappedmessage import *
__all__ = [
 'send', 'enqueue', 'Message', 'WrappedMessage']

def send(message):
    """Send a message via TurboMail."""
    return interface.send(message)


def enqueue(message):
    """Compatability function; use send(message) instead."""
    warnings.warn('"enqueue(message)" is deprecated, please use send(message) instead.', category=DeprecationWarning)
    return send(message)