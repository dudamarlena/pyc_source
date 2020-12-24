# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synapseclient/core/dozer.py
# Compiled at: 2020-03-23 17:17:03
# Size of source mod 2**32: 542 bytes
"""
Created on Sep 21, 2017

@author: bhoff

sleep while checking registered _listeners
"""
import time
_listeners = []

def add_listener(listener):
    if not callable(listener):
        raise ValueError('listener is not callable')
    _listeners.append(listener)


def clear_listeners():
    del _listeners[:]


def doze(secs, listener_check_interval_secs=0.1):
    end_time = time.time() + secs
    while time.time() < end_time:
        for listener in _listeners:
            listener()

        time.sleep(listener_check_interval_secs)