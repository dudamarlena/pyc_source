# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/carbonium_fb/__init__.py
# Compiled at: 2019-09-02 08:45:49
# Size of source mod 2**32: 223 bytes
"""Carbonium - a framework for creating Facebook Messenger bots"""
__version__ = '0.2.2'
__author__ = 'szymonszl'
from .bot import Bot
from . import dataclasses, handlers, contrib