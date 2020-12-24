# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/timers/Dummy/Dummy.py
# Compiled at: 2015-07-18 19:40:58
import AccessControl
from Products.ZScheduler.timers.Base import BaseTimer
from Products.ZScheduler.interfaces.ITimer import ITimer

class Dummy(BaseTimer):
    """
    A timer that doesn't actually do anything

    This is also the base class for other timers ;)
    """
    __implements__ = (
     ITimer,)
    meta_type = 'Dummy'


AccessControl.class_init.InitializeClass(Dummy)