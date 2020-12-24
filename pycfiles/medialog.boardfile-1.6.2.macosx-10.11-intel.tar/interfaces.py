# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/medialog/boardfile/browser/interfaces.py
# Compiled at: 2011-10-07 04:21:09
"""
    Time based events

"""
__author__ = 'Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>'
__copyright__ = 'Copyright 2008 Twinapex Research'
__license__ = 'GPL'
__docformat__ = 'epytext'
from zope.interface import Interface, Attribute

class ITickEvent(Interface):
    """An event signaling a tick (vide the TickingMachine class).
    """
    date_time = Attribute('Time of the last tick')
    next_tick = Attribute('Estimated time of the next tick')