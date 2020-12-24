# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/whistle/__init__.py
# Compiled at: 2018-03-18 07:17:27
# Size of source mod 2**32: 190 bytes
from whistle._version import __version__
from whistle.dispatcher import EventDispatcher
from whistle.event import Event
__all__ = [
 'Event',
 'EventDispatcher',
 '__version__']