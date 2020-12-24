# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.7/site-packages/carbonium_fb/__init__.py
# Compiled at: 2019-09-02 08:45:49
# Size of source mod 2**32: 223 bytes
__doc__ = 'Carbonium - a framework for creating Facebook Messenger bots'
__version__ = '0.2.2'
__author__ = 'szymonszl'
from .bot import Bot
from . import dataclasses, handlers, contrib