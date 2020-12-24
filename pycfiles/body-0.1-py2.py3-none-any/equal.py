# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/boduch/subscription/predicate/equal.py
# Compiled at: 2009-08-14 17:29:30
__doc__ = 'This module defines subscription instances for equal predicate events.'
from boduch.event import subscribe, EventEqual
from boduch.handle import HandleEqual
SubEqual = subscribe(EventEqual, HandleEqual)
__all__ = [
 'SubEqual']