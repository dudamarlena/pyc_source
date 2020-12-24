# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/david.jetelina/.local/share/virtualenvs/pyCardDeck/lib/python3.6/site-packages/pyCardDeck/__init__.py
# Compiled at: 2018-10-23 07:23:53
# Size of source mod 2**32: 461 bytes
__doc__ = "\npyCardDeck\n==========\n\nDeck of cards with all the logic, so you don't have to!\n\n:copyright:     (c) 2016 David Jetelina\n:license:       MIT\n"
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