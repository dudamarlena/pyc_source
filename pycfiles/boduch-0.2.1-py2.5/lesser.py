# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/boduch/subscription/predicate/lesser.py
# Compiled at: 2009-08-14 17:29:30
"""This module defines subscription instances for the lesser predicate
events."""
from boduch.event import subscribe, EventLesser
from boduch.handle import HandleLesser
SubLesser = subscribe(EventLesser, HandleLesser)
__all__ = [
 'SubLesser']