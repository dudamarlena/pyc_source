# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/boduch/subscription/predicate/greater.py
# Compiled at: 2009-08-14 17:29:30
"""This module defines subscription instances for greater predicate events."""
from boduch.event import subscribe, EventGreater
from boduch.handle import HandleGreater
SubGreater = subscribe(EventGreater, HandleGreater)
__all__ = [
 'SubGreater']