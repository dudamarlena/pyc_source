# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/umeboshi/triggers.py
# Compiled at: 2016-11-01 11:12:10
from django_light_enums import enum

class TriggerBehavior(enum.Enum):
    """
    Trigger Behaviors govern when to allow an Event to be scheduled.
    """
    DEFAULT = 'default'
    SCHEDULE_ONCE = 'schedule-once'
    RUN_ONCE = 'run-once'
    RUN_AND_SCHEDULE_ONCE = 'run-and-schedule-once'
    LAST_ONLY = 'last-only'
    DELETE_AFTER_PROCESSING = 'delete-after-processing'