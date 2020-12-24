# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/models/observation_methods/default.py
# Compiled at: 2014-08-27 19:26:12
from datetime import datetime

def link(self):
    return False


def update(self, success_status):
    """Updates the Observation when do() is called.

    NOTE this gets overwritten by some Observation subclasses below"""
    self.touch()
    self.increment_attempts()
    return self.save()


def touch(self):
    """Set the last_attempt for the Observation to the current datetime."""
    self.last_attempted = datetime.now()
    return self.save()


def do(self):
    """By default, nothing should happen except recording that we tried."""
    self.touch()
    self.increment_attempts()
    return self.save()