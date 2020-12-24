# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/scheduler/metaconfigure.py
# Compiled at: 2012-10-22 06:18:07
__docformat__ = 'restructuredtext'
from ztfy.scheduler.interfaces import ISchedulerHandler
from zope.component.zcml import utility
from ztfy.scheduler.manager import SchedulerHandler

def config(context, name=''):
    handler = SchedulerHandler()
    utility(context, ISchedulerHandler, component=handler, name=name)