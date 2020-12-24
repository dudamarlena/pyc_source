# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/umeboshi/exceptions.py
# Compiled at: 2015-12-31 08:37:33
"""
django-umeboshi.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains all exceptions used by the Django Umeboshi module
"""

class NoRoutineTriggerException(Exception):
    """ No trigger_name was provided when registering a Routine """
    pass


class DuplicateEvent(Exception):
    """ Event could not be triggered again because of trigger limitation """
    pass


class RoutineRunException(Exception):
    """ An error occurred during the run() method of Event processing """
    pass


class UnknownTriggerException(Exception):
    """ Event's trigger is not defined """
    pass


class RoutineRetryException(Exception):
    """ Could not complete; schedule for later """

    def __init__(self, new_datetime=None):
        self.new_datetime = new_datetime