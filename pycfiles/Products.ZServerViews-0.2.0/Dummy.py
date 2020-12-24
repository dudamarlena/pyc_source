# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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