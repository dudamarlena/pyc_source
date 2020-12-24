# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/david.jetelina/.local/share/virtualenvs/pyCardDeck/lib/python3.6/site-packages/pyCardDeck/__init__.py
# Compiled at: 2018-10-23 07:23:53
# Size of source mod 2**32: 461 bytes
"""
pyCardDeck
==========

Deck of cards with all the logic, so you don't have to!

:copyright:     (c) 2016 David Jetelina
:license:       MIT
"""
__title__ = 'pyCardDeck'
__author__ = 'David Jetelina'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 David Jetelina'
__version__ = '1.4.0'
from .deck import *
from .errors import *
from .cards import *
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())